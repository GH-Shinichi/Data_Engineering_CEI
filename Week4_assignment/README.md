# Week 4 — Azure Cloud Fundamentals & Data Pipeline (ADF)

Celebal Summer Internship 2026 — Data Engineering

## What this week was about

Setting up basic Azure resources (Resource Group, Storage Account, Blob Container) and
building a data pipeline in Azure Data Factory that reads the Superstore CSV from Blob
Storage, checks its metadata, and copies it to a new location.

## What's in here

- `Week4_Assignment_Nomaan.docx` — full write-up with screenshots for Tasks 1–6 and the
  Mini Project

## Pipeline overview

`ss_pipeline`: **Get Metadata1** → **ForEach1** (containing **Copy data1**)

- Reads `Superstore_raw.csv` from `superstore-container`
- Get Metadata checks the file/child items before copying
- Copy Data writes the result to `output/Superstore_copy.csv`

## Resources used

| Resource | Name |
|---|---|
| Resource Group | `resogp-cei-w4` |
| Storage Account | `storceiw4` |
| Blob Container | `superstore-container` |
| Data Factory | `adf-cei-w4` |
| Linked Service | `ls_superstore_blob` |

## Status

All tasks (1–6) and the Mini Project completed and verified — pipeline run succeeded end to end.
