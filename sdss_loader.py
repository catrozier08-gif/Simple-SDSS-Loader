import os
import glob
import numpy as np
from astropy.io import fits
import pandas as pd

def load_sdss_catalog(folder_path="."):
    """
    Scans a directory for SDSS galaxy catalog files (FITS or DAT) 
    and loads them into a unified Pandas DataFrame.
    
    Supports:
    - FITS (.fits, .fits.gz) - Standard SDSS format
    - ASCII (.dat, .txt) - Common text exports
    
    Returns:
    - DataFrame with columns ['RA', 'DEC', 'Z']
    """
    # 1. Look for FITS files (Preferred)
    fits_files = glob.glob(os.path.join(folder_path, "*galaxy*.fits*"))
    
    # 2. Look for DAT/TXT files (Fallback)
    text_files = glob.glob(os.path.join(folder_path, "*galaxy*.dat")) + \
                 glob.glob(os.path.join(folder_path, "*galaxy*.txt"))
    
    all_files = fits_files + text_files
    
    if not all_files:
        print(f"No SDSS files found in '{folder_path}'.")
        print("Please download data from: https://data.sdss.org/sas/dr12/boss/lss/")
        return None

    print(f"Found {len(all_files)} files. Loading...")
    
    ra_list, dec_list, z_list = [], [], []
    
    for f in all_files:
        print(f"  Reading {os.path.basename(f)}...")
        try:
            # TRY FITS
            if f.endswith('.fits') or f.endswith('.fits.gz'):
                with fits.open(f) as hdul:
                    data = hdul[1].data
                    ra_list.append(data['RA'])
                    dec_list.append(data['DEC'])
                    z_list.append(data['Z'])
            
            # TRY TEXT
            else:
                # Assume standard whitespace layout, comments with #
                # Try to auto-detect columns if headers exist
                df = pd.read_csv(f, sep=r'\s+', comment='#')
                # Standardize column names
                df.columns = [c.upper() for c in df.columns]
                
                if 'RA' in df.columns and 'DEC' in df.columns and 'Z' in df.columns:
                    ra_list.append(df['RA'].values)
                    dec_list.append(df['DEC'].values)
                    z_list.append(df['Z'].values)
                else:
                    # Fallback: Assume cols 0, 1, 2 are RA, DEC, Z
                    data = np.loadtxt(f)
                    ra_list.append(data[:, 0])
                    dec_list.append(data[:, 1])
                    z_list.append(data[:, 2])
                    
        except Exception as e:
            print(f"    Error reading {f}: {e}")

    if not ra_list:
        print("No valid data loaded.")
        return None

    # Concatenate
    print("Merging data...")
    full_ra = np.concatenate(ra_list)
    full_dec = np.concatenate(dec_list)
    full_z = np.concatenate(z_list)
    
    df_final = pd.DataFrame({'RA': full_ra, 'DEC': full_dec, 'Z': full_z})
    print(f"Successfully loaded {len(df_final)} galaxies.")
    
    return df_final

# Example Usage Block (runs only if script is executed directly)
if __name__ == "__main__":
    df = load_sdss_catalog(".")
    if df is not None:
        print("\nPreview:")
        print(df.head())
