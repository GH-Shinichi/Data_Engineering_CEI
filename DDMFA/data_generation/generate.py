"""
generate_data.py
────────────────────────────────────────────────────────────────────
Phase 0 — Drone Delivery Monitoring & Failure Analytics Pipeline
Simulates 3 raw source CSVs + 1 SCD1 update file

Outputs (written to data/raw/)
──────────────────────────────
drones.csv          100 rows   — drone fleet dimension
drones_update.csv     5 rows   — 5 recalibrated drones (SCD Type 1 demo)
deliveries.csv      5,000 rows — delivery fact records
flight_logs.csv    ~30,150 rows — telemetry logs (inc. 150 injected duplicates)

Design decisions
────────────────
- Failure rate  : 18% of deliveries fail (industry-realistic ~15-20%)
- Failure causes: Battery 40%, Signal 30%, Weather 20%, Unknown 10%
- Nulls injected: distance_km ~1%, battery_level ~3%, gps_signal ~2%,
                  weather_condition ~2%  (tests Silver DQ layer)
- Duplicates    : 150 rows injected into flight_logs (tests Bronze dedup)
- Date range    : Oct 2025 - Mar 2026 (6 months, seasonal weather patterns)
- Thresholds used in Silver classification (documented here for traceability):
    battery_level  < 20   → FAILED_BATTERY
    gps_signal     < 0.30 → FAILED_SIGNAL
    weather_condition in ['heavy_rain', 'storm'] → FAILED_WEATHER
"""

import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ─────────────────────────────────────────────────────────────
# SEED — reproducibility
# ─────────────────────────────────────────────────────────────
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

# ─────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────
NUM_DRONES        = 100
NUM_DELIVERIES    = 5_000
LOGS_PER_DELIVERY = 6          # 5,000 × 6 = 30,000 base log rows
FAILURE_RATE      = 0.18

START_DATE    = datetime(2025, 10, 1)
END_DATE      = datetime(2026, 3, 31)
TOTAL_SECONDS = int((END_DATE - START_DATE).total_seconds())

# Failure cause split among failed deliveries only
FAILURE_CAUSES  = ['BATTERY', 'SIGNAL', 'WEATHER', 'UNKNOWN']
FAILURE_WEIGHTS = [0.40,       0.30,     0.20,      0.10]

# Drone model → (min_range_km, max_range_km)
DRONE_MODELS = {
    'DJI-X300':   (40,  70),
    'DJI-X500':   (60,  90),
    'Zipline-R1': (80, 120),
    'Wing-G2':    (30,  60),
    'Skydio-D2':  (50,  80),
}

SOURCES      = ['Warehouse-North', 'Warehouse-South', 'Warehouse-East',
                'Hub-Central', 'Hub-West']
DESTINATIONS = [f'Zone-{i:02d}' for i in range(1, 31)]

WEATHER_OPTIONS = ['clear', 'cloudy', 'windy', 'heavy_rain', 'storm']

def get_weather_weights(month):
    """Seasonal weather probabilities for [clear, cloudy, windy, heavy_rain, storm]"""
    if month in [12, 1, 2]:        # Winter — more rain/storms
        return [0.25, 0.28, 0.22, 0.15, 0.10]
    elif month in [6, 7, 8]:       # Summer — mostly clear
        return [0.50, 0.25, 0.15, 0.07, 0.03]
    else:                           # Spring / Autumn
        return [0.38, 0.28, 0.19, 0.10, 0.05]


# ─────────────────────────────────────────────────────────────
# 1. drones.csv
# ─────────────────────────────────────────────────────────────
def generate_drones():
    models     = list(DRONE_MODELS.keys())
    model_list = np.random.choice(models, NUM_DRONES, replace=True)

    records = []
    for idx, model in enumerate(model_list):
        lo, hi    = DRONE_MODELS[model]
        max_range = round(float(np.random.uniform(lo, hi)), 1)
        records.append({
            'drone_id':     f'D{idx + 1:03d}',
            'model':        model,
            'max_range_km': max_range,
        })

    return pd.DataFrame(records)


# ─────────────────────────────────────────────────────────────
# 2. deliveries.csv + flight_logs.csv
# ─────────────────────────────────────────────────────────────
def generate_deliveries_and_logs(drones_df):
    drone_ids       = drones_df['drone_id'].tolist()
    drone_range_map = dict(zip(drones_df['drone_id'], drones_df['max_range_km']))

    deliveries  = []
    flight_logs = []
    log_counter = 1

    for i in range(NUM_DELIVERIES):
        delivery_id = f'DEL{i + 1:05d}'
        drone_id    = random.choice(drone_ids)
        max_range   = drone_range_map[drone_id]

        # Distance always within drone capability
        distance_km = round(float(np.random.uniform(5, max_range * 0.85)), 2)

        # Random start time across 6-month window
        offset     = random.randint(0, TOTAL_SECONDS)
        start_time = START_DATE + timedelta(seconds=offset)
        month      = start_time.month
        w_weights  = get_weather_weights(month)

        # Duration in minutes — speed varies by model/conditions
        speed_kmh        = float(np.random.uniform(40, 90))
        duration_minutes = max(5.0, (distance_km / speed_kmh) * 60)

        # ── Failure logic ─────────────────────────────────
        is_failure    = np.random.random() < FAILURE_RATE
        failure_cause = None

        if is_failure:
            failure_cause = np.random.choice(FAILURE_CAUSES, p=FAILURE_WEIGHTS)
            # Fails partway through the planned route
            ratio      = float(np.random.uniform(0.35, 0.80))
            end_time   = start_time + timedelta(minutes=duration_minutes * ratio)
            del_status = 'FAILED'
        else:
            ratio      = float(np.random.uniform(0.95, 1.10))
            end_time   = start_time + timedelta(minutes=duration_minutes * ratio)
            del_status = 'SUCCESS'

        # Deliberate null on distance_km ~1%
        deliveries.append({
            'delivery_id': delivery_id,
            'drone_id':    drone_id,
            'source':      random.choice(SOURCES),
            'destination': random.choice(DESTINATIONS),
            'distance_km': None if np.random.random() < 0.01 else distance_km,
            'start_time':  start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time':    end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status':      del_status,
        })

        # ── Flight logs ───────────────────────────────────
        delivery_seconds = max(60.0, (end_time - start_time).total_seconds())

        # Evenly spaced timestamps within delivery window
        log_times = [
            start_time + timedelta(
                seconds=(j / (LOGS_PER_DELIVERY - 1)) * delivery_seconds
            )
            for j in range(LOGS_PER_DELIVERY)
        ]

        # Battery: realistic drain proportional to distance
        init_battery = float(np.random.uniform(75, 100))
        total_drain  = min(
            init_battery - 5,
            distance_km * float(np.random.uniform(0.35, 0.65))
        )

        # Base weather for entire delivery
        base_weather = np.random.choice(WEATHER_OPTIONS, p=w_weights)
        if is_failure and failure_cause == 'WEATHER':
            base_weather = np.random.choice(['heavy_rain', 'storm'])

        for j in range(LOGS_PER_DELIVERY):
            log_id   = f'LOG{log_counter:06d}'
            log_counter += 1
            progress = j / (LOGS_PER_DELIVERY - 1)

            # ── Battery level ──────────────────────────────
            battery_level = round(init_battery - (total_drain * progress), 2)
            # Force below 20% threshold on last 2 logs for battery failures
            if is_failure and failure_cause == 'BATTERY' and j >= LOGS_PER_DELIVERY - 2:
                battery_level = round(float(np.random.uniform(5, 18)), 2)

            # ── GPS signal (0.0 – 1.0) ────────────────────
            gps_signal = round(float(np.random.uniform(0.55, 1.0)), 3)
            # Force below 0.30 threshold on last 2 logs for signal failures
            if is_failure and failure_cause == 'SIGNAL' and j >= LOGS_PER_DELIVERY - 2:
                gps_signal = round(float(np.random.uniform(0.05, 0.28)), 3)

            # ── Weather ────────────────────────────────────
            # 10% chance of shift mid-flight
            if j > 0 and np.random.random() < 0.10:
                weather = np.random.choice(WEATHER_OPTIONS, p=w_weights)
            else:
                weather = base_weather
            # Force storm/heavy_rain on last 2 logs for weather failures
            if is_failure and failure_cause == 'WEATHER' and j >= LOGS_PER_DELIVERY - 2:
                weather = np.random.choice(['heavy_rain', 'storm'])

            # ── Log status ─────────────────────────────────
            if j == LOGS_PER_DELIVERY - 1:
                log_status = 'FAILED' if is_failure else 'COMPLETED'
            else:
                log_status = 'ACTIVE'

            # ── Deliberate nulls ───────────────────────────
            flight_logs.append({
                'log_id':            log_id,
                'drone_id':          drone_id,
                'delivery_id':       delivery_id,
                'timestamp':         log_times[j].strftime('%Y-%m-%d %H:%M:%S'),
                'battery_level':     None if np.random.random() < 0.03 else battery_level,
                'gps_signal':        None if np.random.random() < 0.02 else gps_signal,
                'weather_condition': None if np.random.random() < 0.02 else weather,
                'status':            log_status,
            })

    return pd.DataFrame(deliveries), pd.DataFrame(flight_logs)


# ─────────────────────────────────────────────────────────────
# 3. Inject duplicates into flight_logs
#    Simulates real-world duplicate ingestion
#    Bronze layer must deduplicate on log_id
# ─────────────────────────────────────────────────────────────
def inject_duplicates(df, n=150):
    dupes = df.sample(n=n, random_state=SEED)
    return pd.concat([df, dupes], ignore_index=True)


# ─────────────────────────────────────────────────────────────
# 4. drones_update.csv  (SCD Type 1 demo)
#    5 drones have max_range_km recalibrated
#    Silver MERGE will overwrite old values (no history kept)
# ─────────────────────────────────────────────────────────────
def generate_drone_updates(drones_df):
    sample = drones_df.sample(n=5, random_state=7).copy()
    sample['max_range_km'] = sample['max_range_km'].apply(
        lambda x: round(x * float(np.random.uniform(0.88, 1.12)), 1)
    )
    return sample


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    os.makedirs('data/raw', exist_ok=True)

    print('── Phase 0: Dataset Generation ─────────────────')

    print('[1/4] Generating drones.csv ...')
    drones_df = generate_drones()

    print('[2/4] Generating drones_update.csv ...')
    updates_df = generate_drone_updates(drones_df)

    print('[3/4] Generating deliveries.csv + flight_logs.csv ...')
    deliveries_df, logs_df = generate_deliveries_and_logs(drones_df)

    print('[4/4] Injecting duplicates into flight_logs ...')
    logs_df = inject_duplicates(logs_df, n=150)

    # ── Save ──────────────────────────────────────────────
    drones_df.to_csv('data/raw/drones.csv',         index=False)
    updates_df.to_csv('data/raw/drones_update.csv', index=False)
    deliveries_df.to_csv('data/raw/deliveries.csv', index=False)
    logs_df.to_csv('data/raw/flight_logs.csv',      index=False)

    # ── Summary ───────────────────────────────────────────
    total      = len(deliveries_df)
    failures   = (deliveries_df['status'] == 'FAILED').sum()
    null_dist  = logs_df[['battery_level', 'gps_signal', 'weather_condition']].isnull().sum()
    dupes_check = len(logs_df) - logs_df['log_id'].nunique()

    print('\n✅ Generation complete')
    print(f'   drones.csv          {len(drones_df):>6,} rows')
    print(f'   drones_update.csv   {len(updates_df):>6,} rows')
    print(f'   deliveries.csv      {len(deliveries_df):>6,} rows')
    print(f'   flight_logs.csv     {len(logs_df):>6,} rows')
    print(f'\n── Delivery stats ──────────────────────────────')
    print(f'   SUCCESS : {total - failures:,}  ({(total-failures)/total*100:.1f}%)')
    print(f'   FAILED  : {failures:,}  ({failures/total*100:.1f}%)')
    print(f'\n── Injected nulls (flight_logs) ─────────────────')
    for col, count in null_dist.items():
        print(f'   {col:<20} {count:>4} nulls  ({count/len(logs_df)*100:.1f}%)')
    print(f'\n── Duplicate check ──────────────────────────────')
    print(f'   Duplicate log rows  : {dupes_check}')
    print(f'   (Bronze dedup target: 150)')