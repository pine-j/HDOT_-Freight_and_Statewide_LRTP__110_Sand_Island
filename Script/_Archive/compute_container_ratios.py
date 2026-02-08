"""
Compute Container Ratios for HS and SCTG2 Commodities

This script reads commodity dictionaries and port-level import data to calculate
containerization ratios (by value and tonnage) for both HS and SCTG2 commodity classifications.

Author: Generated Script
Date: 2026-01-15
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path


def clean_numeric_column(series):
    """
    Clean numeric columns by removing commas and converting to float.
    Handle missing values appropriately.
    
    Args:
        series: pandas Series with numeric data (possibly as strings with commas)
    
    Returns:
        pandas Series with cleaned numeric values
    """
    if series.dtype == 'object':
        # Remove commas and convert to numeric
        return pd.to_numeric(series.str.replace(',', ''), errors='coerce')
    return pd.to_numeric(series, errors='coerce')


def load_data(base_path):
    """
    Load all required data files.
    
    Args:
        base_path: Base directory path containing the data files
    
    Returns:
        tuple: (commodity_hs_df, commodity_sctg2_df, port_imports_df)
    """
    print("Loading data files...")
    
    # Construct file paths
    commodity_dict_path = os.path.join(base_path, 'Processed_Data', 'Commodity_Dict.xlsx')
    port_imports_path = os.path.join(base_path, 'Raw_Data', 'US_Trade', 'Port-level Imports.csv')
    
    # Load Commodity_Dict.xlsx sheets
    print(f"  Reading {commodity_dict_path}")
    commodity_hs_df = pd.read_excel(commodity_dict_path, sheet_name='Commodity_HS')
    commodity_sctg2_df = pd.read_excel(commodity_dict_path, sheet_name='Commodity_SCTG2')
    
    # Load Port-level Imports.csv
    print(f"  Reading {port_imports_path}")
    port_imports_df = pd.read_csv(port_imports_path)
    
    # Clean numeric columns in port_imports_df
    print("  Cleaning numeric columns...")
    numeric_columns = [
        'Vessel Customs Value (Gen) ($US)',
        'Customs Containerized Vessel Value (Gen) ($US)',
        'Vessel SWT (Gen) (kg)',
        'Containerized Vessel SWT (Gen) (kg)'
    ]
    
    for col in numeric_columns:
        if col in port_imports_df.columns:
            port_imports_df[col] = clean_numeric_column(port_imports_df[col])
    
    print(f"  Loaded Commodity_HS: {commodity_hs_df.shape[0]} rows")
    print(f"  Loaded Commodity_SCTG2: {commodity_sctg2_df.shape[0]} rows")
    print(f"  Loaded Port Imports: {port_imports_df.shape[0]} rows")
    
    return commodity_hs_df, commodity_sctg2_df, port_imports_df


def extract_hs_code(commodity_str):
    """
    Extract 2-digit HS code from commodity string.
    
    Args:
        commodity_str: String like "02 Meat And Edible Meat Offal"
    
    Returns:
        int: 2-digit HS code (e.g., 2)
    """
    if pd.isna(commodity_str):
        return None
    
    # Extract first 2 characters and convert to int
    try:
        hs_code = int(str(commodity_str).split()[0])
        return hs_code
    except (ValueError, IndexError):
        return None


def process_commodity_hs(commodity_hs_df, port_imports_df):
    """
    Process Commodity_HS sheet: match HS codes and calculate container ratios.
    
    Args:
        commodity_hs_df: DataFrame with HS commodity information
        port_imports_df: DataFrame with port-level import data
    
    Returns:
        DataFrame: Updated commodity_hs_df with new ratio columns
    """
    print("\nProcessing Commodity_HS sheet...")
    
    # Extract HS code from port imports commodity column
    port_imports_df['HS_Code_Extracted'] = port_imports_df['Commodity'].apply(extract_hs_code)
    
    # Group by HS code and sum the values
    hs_aggregated = port_imports_df.groupby('HS_Code_Extracted').agg({
        'Vessel Customs Value (Gen) ($US)': 'sum',
        'Customs Containerized Vessel Value (Gen) ($US)': 'sum',
        'Vessel SWT (Gen) (kg)': 'sum',
        'Containerized Vessel SWT (Gen) (kg)': 'sum'
    }).reset_index()
    
    # Rename for clarity
    hs_aggregated.columns = [
        'HS_Code',
        'Total_Vessel_Value',
        'Total_Containerized_Value',
        'Total_Vessel_Weight',
        'Total_Containerized_Weight'
    ]
    
    # Merge with commodity_hs_df
    commodity_hs_df = commodity_hs_df.merge(
        hs_aggregated,
        on='HS_Code',
        how='left'
    )
    
    # Calculate ratios
    # Container_Ratio_Value
    commodity_hs_df['Container_Ratio_Value'] = np.where(
        commodity_hs_df['Total_Vessel_Value'] > 0,
        commodity_hs_df['Total_Containerized_Value'] / commodity_hs_df['Total_Vessel_Value'],
        np.nan
    )
    
    # Container_Ratio_Tons
    commodity_hs_df['Container_Ratio_Tons'] = np.where(
        commodity_hs_df['Total_Vessel_Weight'] > 0,
        commodity_hs_df['Total_Containerized_Weight'] / commodity_hs_df['Total_Vessel_Weight'],
        np.nan
    )
    
    # Drop intermediate columns
    commodity_hs_df = commodity_hs_df.drop(columns=[
        'Total_Vessel_Value',
        'Total_Containerized_Value',
        'Total_Vessel_Weight',
        'Total_Containerized_Weight'
    ])
    
    # Count matches
    matched_count = commodity_hs_df['Container_Ratio_Value'].notna().sum()
    print(f"  Matched {matched_count} out of {len(commodity_hs_df)} HS codes")
    
    return commodity_hs_df


def process_commodity_sctg2(commodity_hs_df, commodity_sctg2_df, port_imports_df):
    """
    Process Commodity_SCTG2 sheet: map HS to SCTG2, aggregate, and calculate ratios.
    
    Args:
        commodity_hs_df: DataFrame with HS commodity information (includes HS to SCTG2 mapping)
        commodity_sctg2_df: DataFrame with SCTG2 commodity information
        port_imports_df: DataFrame with port-level import data
    
    Returns:
        DataFrame: Updated commodity_sctg2_df with new ratio columns
    """
    print("\nProcessing Commodity_SCTG2 sheet...")
    
    # Extract HS code from port imports
    port_imports_df['HS_Code_Extracted'] = port_imports_df['Commodity'].apply(extract_hs_code)
    
    # Merge port imports with HS to SCTG2 mapping
    port_with_sctg = port_imports_df.merge(
        commodity_hs_df[['HS_Code', 'SCTG_Code']],
        left_on='HS_Code_Extracted',
        right_on='HS_Code',
        how='left'
    )
    
    # Group by SCTG_Code and sum
    sctg_aggregated = port_with_sctg.groupby('SCTG_Code').agg({
        'Vessel Customs Value (Gen) ($US)': 'sum',
        'Customs Containerized Vessel Value (Gen) ($US)': 'sum',
        'Vessel SWT (Gen) (kg)': 'sum',
        'Containerized Vessel SWT (Gen) (kg)': 'sum'
    }).reset_index()
    
    # Rename for clarity
    sctg_aggregated.columns = [
        'SCTG_Code',
        'Total_Vessel_Value',
        'Total_Containerized_Value',
        'Total_Vessel_Weight',
        'Total_Containerized_Weight'
    ]
    
    # Merge with commodity_sctg2_df
    commodity_sctg2_df = commodity_sctg2_df.merge(
        sctg_aggregated,
        on='SCTG_Code',
        how='left'
    )
    
    # Calculate ratios
    # Container_Ratio_Value
    commodity_sctg2_df['Container_Ratio_Value'] = np.where(
        commodity_sctg2_df['Total_Vessel_Value'] > 0,
        commodity_sctg2_df['Total_Containerized_Value'] / commodity_sctg2_df['Total_Vessel_Value'],
        np.nan
    )
    
    # Container_Ratio_Tons
    commodity_sctg2_df['Container_Ratio_Tons'] = np.where(
        commodity_sctg2_df['Total_Vessel_Weight'] > 0,
        commodity_sctg2_df['Total_Containerized_Weight'] / commodity_sctg2_df['Total_Vessel_Weight'],
        np.nan
    )
    
    # Drop intermediate columns
    commodity_sctg2_df = commodity_sctg2_df.drop(columns=[
        'Total_Vessel_Value',
        'Total_Containerized_Value',
        'Total_Vessel_Weight',
        'Total_Containerized_Weight'
    ])
    
    # Count matches
    matched_count = commodity_sctg2_df['Container_Ratio_Value'].notna().sum()
    print(f"  Matched {matched_count} out of {len(commodity_sctg2_df)} SCTG2 codes")
    
    return commodity_sctg2_df


def save_results(commodity_hs_df, commodity_sctg2_df, base_path, output_filename='Commodity_Dict_with_Ratios.xlsx'):
    """
    Save updated dataframes to Excel file.
    
    Args:
        commodity_hs_df: Updated Commodity_HS dataframe
        commodity_sctg2_df: Updated Commodity_SCTG2 dataframe
        base_path: Base directory path
        output_filename: Name of output file
    """
    print(f"\nSaving results to {output_filename}...")
    
    output_path = os.path.join(base_path, 'Processed_Data', output_filename)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write to Excel with multiple sheets
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        commodity_sctg2_df.to_excel(writer, sheet_name='Commodity_SCTG2', index=False)
        commodity_hs_df.to_excel(writer, sheet_name='Commodity_HS', index=False)
    
    print(f"  Results saved to: {output_path}")
    print(f"  Commodity_HS: {len(commodity_hs_df)} rows with {len(commodity_hs_df.columns)} columns")
    print(f"  Commodity_SCTG2: {len(commodity_sctg2_df)} rows with {len(commodity_sctg2_df.columns)} columns")


def main():
    """
    Main execution function.
    """
    print("=" * 80)
    print("Container Ratio Computation Script")
    print("=" * 80)
    
    # Get base path (script directory's parent)
    script_dir = Path(__file__).parent
    base_path = script_dir.parent
    
    print(f"\nWorking directory: {base_path}")
    
    # Load data
    commodity_hs_df, commodity_sctg2_df, port_imports_df = load_data(base_path)
    
    # Process Commodity_HS
    commodity_hs_df = process_commodity_hs(commodity_hs_df, port_imports_df)
    
    # Process Commodity_SCTG2
    commodity_sctg2_df = process_commodity_sctg2(commodity_hs_df, commodity_sctg2_df, port_imports_df)
    
    # Save results
    save_results(commodity_hs_df, commodity_sctg2_df, base_path)
    
    print("\n" + "=" * 80)
    print("Processing complete!")
    print("=" * 80)
    
    # Display sample results
    print("\nSample results from Commodity_HS:")
    print(commodity_hs_df[['HS_Code', 'HS_Commodity', 'Container_Ratio_Value', 'Container_Ratio_Tons']].head(10))
    
    print("\nSample results from Commodity_SCTG2:")
    print(commodity_sctg2_df[['SCTG_Code', 'SCTG_Commodity', 'Container_Ratio_Value', 'Container_Ratio_Tons']].head(10))


if __name__ == "__main__":
    main()
