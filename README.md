# Simple SDSS Loader

A lightweight, robust Python tool to load **Sloan Digital Sky Survey (SDSS)** galaxy catalogs into a clean Pandas DataFrame. 

It automatically detects and parses both **FITS** (`.fits`, `.fits.gz`) and **ASCII** (`.dat`, `.txt`) formats, handling multiple files at once (e.g., North + South chunks).

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Get Data:**
    You need the SDSS galaxy catalogs (e.g., DR12 BOSS).
    *   **Direct Download Link:** [SDSS DR12 SAS](https://data.sdss.org/sas/dr12/boss/lss/)
    *   Look for files like `galaxy_DR12v5_CMASSLOWZTOT_North.fits.gz`.
    *   Place them in the same folder as the script.

## Usage

```python
from sdss_loader import load_sdss_catalog

# Automatically finds and merges all galaxy files in the folder
df = load_sdss_catalog(".")

print(df.head())
#      RA        DEC       Z
# 0  145.1    34.5      0.45
# 1  145.2    34.6      0.48
...
