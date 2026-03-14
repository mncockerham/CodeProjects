# DuckDB Integration Notes

This directory contains resources, configurations, and considerations for using **DuckDB** locally and within our data pipelines (especially in coordination with Dagster, dbt, or Airflow).

## Overview
DuckDB is an in-process, high-performance analytical database. It requires no external dependencies or separate server processes, making it ideal for local development, fast testing, and lightweight embedded analytics.

## Files Here
*   `INSTALL_OPTIONS.md`: Documentation on how to install DuckDB (CLI and Python clients) across various operating systems, in case we need to migrate environments or onboard new team members.

## Next Steps
*   [ ] Document local database file paths used by Dagster/dbt.
*   [ ] Write sample queries or python scripts for quickly querying the DuckDB files.
*   [ ] Add notes on reading/writing Parquet or CSV files using DuckDB.

*Feel free to store any specific DuckDB connection logic, snippets, or configurations here!*
