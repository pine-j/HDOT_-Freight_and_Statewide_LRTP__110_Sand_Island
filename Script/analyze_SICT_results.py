"""
SICT Analysis Results Script

This script analyzes the FAF Hawaii data to produce summary statistics for SICT piers,
including share of Honolulu Harbor (scoped to SICT cargo types: Containers, RO/RO,
Break-Bulk) and top commodities by tonnage.

Author: Adithya Ajith
Date: 2026-02-04
"""

import pandas as pd

# Import shared constants and paths from the processing script
from process_FAF_Region import (
    PROCESSED_DATA_DIR,
    SICT_PIER_VALUE,
    OUTPUT_PATH as FAF_OUTPUT_PATH,
)

# Input files
FAF_INPUT_PATH = FAF_OUTPUT_PATH
PIER_OPERATIONS_PATH = PROCESSED_DATA_DIR / "Honolulu Harbor Pier Operations and Cargo Inventory.xlsx"

# Output file
OUTPUT_PATH = PROCESSED_DATA_DIR / "SICT_Analysis_Results.xlsx"

# Constants
TOP_N = 5

# Cargo types that SICT handles (used to scope the share calculation)
SICT_CARGO_TYPES = {"Containers", "RO/RO", "Break-Bulk"}


def load_pier_proportions():
    """
    Load pier capacity proportions from Honolulu Harbor Pier Operations file.
    
    Returns:
        pd.DataFrame: Pier proportions data with relevant columns
    """
    print("\nLoading pier proportions...")
    
    df = pd.read_excel(PIER_OPERATIONS_PATH, sheet_name='Current_v2')
    
    # Select relevant columns
    proportion_cols = [
        'Pier', 
        'Container Proportion', 
        'RO/RO Proportion', 
        'Break-Bulk Proportion', 
        'Liquid-Bulk Proportion', 
        'Dry-Bulk Proportion'
    ]
    
    df = df[proportion_cols].copy()
    
    print(f"  - Loaded {len(df)} piers")
    
    return df


def analyze_sict_share_total(df_honolulu_piers):
    """
    Calculate overall SICT share of Honolulu Harbor.
    
    Only considers the cargo types that SICT actually handles
    (Containers, RO/RO, Break-Bulk) so that the comparison is like-for-like.
    
    Args:
        df_honolulu_piers: DataFrame with Honolulu_Piers data
        
    Returns:
        pd.DataFrame: Single row with total share statistics
    """
    print("\nCalculating SICT share (total)...")
    print(f"  - Scoped to SICT cargo types: {sorted(SICT_CARGO_TYPES)}")
    
    # Filter to only the cargo types SICT handles
    df_scoped = df_honolulu_piers[df_honolulu_piers['cargo_type'].isin(SICT_CARGO_TYPES)]
    
    # Calculate Honolulu totals (scoped)
    honolulu_total_tons = df_scoped['tons_2024'].sum()
    honolulu_total_value = df_scoped['current_value_2024'].sum()
    
    # Calculate SICT totals (scoped)
    df_sict = df_scoped[df_scoped['Pier'] == SICT_PIER_VALUE]
    sict_total_tons = df_sict['tons_2024'].sum()
    sict_total_value = df_sict['current_value_2024'].sum()
    
    # Calculate percentages
    sict_share_tons_pct = (sict_total_tons / honolulu_total_tons * 100) if honolulu_total_tons > 0 else 0
    sict_share_value_pct = (sict_total_value / honolulu_total_value * 100) if honolulu_total_value > 0 else 0
    
    result = pd.DataFrame([{
        'Honolulu_Total_Tons': honolulu_total_tons,
        'SICT_Total_Tons': sict_total_tons,
        'SICT_Share_Tons_Pct': round(sict_share_tons_pct, 2),
        'Honolulu_Total_Value': honolulu_total_value,
        'SICT_Total_Value': sict_total_value,
        'SICT_Share_Value_Pct': round(sict_share_value_pct, 2)
    }])
    
    print(f"  - Honolulu total tons (scoped): {honolulu_total_tons:,.0f}")
    print(f"  - SICT total tons: {sict_total_tons:,.0f}")
    print(f"  - SICT share: {sict_share_tons_pct:.2f}%")
    
    return result


def analyze_sict_share_by_commodity(df_honolulu_piers):
    """
    Calculate SICT share by commodity.
    
    Args:
        df_honolulu_piers: DataFrame with Honolulu_Piers data
        
    Returns:
        pd.DataFrame: Per-commodity share statistics
    """
    print("\nCalculating SICT share by commodity...")
    
    # Group Honolulu totals by commodity
    honolulu_by_commodity = df_honolulu_piers.groupby('SCTG2_Commodity').agg({
        'tons_2024': 'sum',
        'current_value_2024': 'sum'
    }).reset_index()
    honolulu_by_commodity.columns = ['SCTG2_Commodity', 'Honolulu_Tons', 'Honolulu_Value']
    
    # Group SICT totals by commodity
    df_sict = df_honolulu_piers[df_honolulu_piers['Pier'] == SICT_PIER_VALUE]
    sict_by_commodity = df_sict.groupby('SCTG2_Commodity').agg({
        'tons_2024': 'sum',
        'current_value_2024': 'sum'
    }).reset_index()
    sict_by_commodity.columns = ['SCTG2_Commodity', 'SICT_Tons', 'SICT_Value']
    
    # Merge
    result = honolulu_by_commodity.merge(sict_by_commodity, on='SCTG2_Commodity', how='left')
    result['SICT_Tons'] = result['SICT_Tons'].fillna(0)
    result['SICT_Value'] = result['SICT_Value'].fillna(0)
    
    # Calculate percentages
    result['SICT_Share_Tons_Pct'] = (result['SICT_Tons'] / result['Honolulu_Tons'] * 100).round(2)
    result['SICT_Share_Value_Pct'] = (result['SICT_Value'] / result['Honolulu_Value'] * 100).round(2)
    
    # Reorder columns
    result = result[['SCTG2_Commodity', 'Honolulu_Tons', 'SICT_Tons', 'SICT_Share_Tons_Pct',
                     'Honolulu_Value', 'SICT_Value', 'SICT_Share_Value_Pct']]
    
    # Sort by SICT tons descending
    result = result.sort_values('SICT_Tons', ascending=False).reset_index(drop=True)
    
    print(f"  - Analyzed {len(result)} commodities")
    
    return result


def get_top_commodities_faf(df_sict_faf, top_n=TOP_N):
    """
    Get top commodities from SICT_Piers_FAF by tonnage.
    
    Args:
        df_sict_faf: DataFrame with SICT_Piers_FAF data
        top_n: Number of top commodities to return
        
    Returns:
        pd.DataFrame: Top commodities by tonnage
    """
    print("\nGetting top commodities from FAF model...")
    
    # Aggregate by commodity
    by_commodity = df_sict_faf.groupby('SCTG2_Commodity').agg({
        'tons_2024': 'sum',
    }).reset_index()
    
    total_tons = by_commodity['tons_2024'].sum()
    
    # Top by tonnage
    top_tons = by_commodity.nlargest(top_n, 'tons_2024').copy()
    top_tons['Pct_of_Total'] = (top_tons['tons_2024'] / total_tons * 100).round(2)
    top_tons = top_tons[['SCTG2_Commodity', 'tons_2024', 'Pct_of_Total']]
    top_tons.columns = ['SCTG2_Commodity', 'Tons', 'Pct_of_Total']
    
    print(f"  - Top {top_n} by tonnage: {list(top_tons['SCTG2_Commodity'])}")
    
    return top_tons.reset_index(drop=True)


def get_top_commodities_scaled(df_sict_scaled, top_n=TOP_N):
    """
    Get top commodities from scaled SICT data by tonnage.
    
    Args:
        df_sict_scaled: DataFrame with SICT_Piers_byPortTons data
        top_n: Number of top commodities to return
    
    Returns:
        pd.DataFrame: Top commodities by scaled tonnage
    """
    # Aggregate by commodity
    by_commodity = df_sict_scaled.groupby('SCTG2_Commodity').agg({
        'scaled_tons': 'sum',
    }).reset_index()
    
    total_tons = by_commodity['scaled_tons'].sum()
    
    # Top by tonnage
    top_tons = by_commodity.nlargest(top_n, 'scaled_tons').copy()
    top_tons['Pct_of_Total'] = (top_tons['scaled_tons'] / total_tons * 100).round(2)
    top_tons = top_tons[['SCTG2_Commodity', 'scaled_tons', 'Pct_of_Total']]
    top_tons.columns = ['SCTG2_Commodity', 'Scaled_Tons', 'Pct_of_Total']
    
    return top_tons.reset_index(drop=True)


def save_results(results_dict, output_path):
    """
    Save all results to Excel file with multiple sheets.
    
    Args:
        results_dict: Dictionary of sheet_name -> DataFrame
        output_path: Path for output Excel file
    """
    print(f"\nSaving results to {output_path}...")
    
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_name, df in results_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"  - Saved {sheet_name}: {len(df)} rows")
        
        print(f"  - Successfully saved to {output_path}")
        
    except Exception as e:
        print(f"Error saving results: {e}")
        raise


def main():
    """
    Main execution function.
    """
    print("=" * 70)
    print("SICT Analysis Results Script")
    print("=" * 70)
    
    try:
        # Load input data
        print("\nLoading input data...")
        df_honolulu_piers = pd.read_excel(FAF_INPUT_PATH, sheet_name='Honolulu_Piers')
        df_sict_faf = pd.read_excel(FAF_INPUT_PATH, sheet_name='SICT_Piers_FAF')
        df_sict_byporttons = pd.read_excel(FAF_INPUT_PATH, sheet_name='SICT_Piers_byPortTons')
        
        print(f"  - Honolulu_Piers: {len(df_honolulu_piers):,} rows")
        print(f"  - SICT_Piers_FAF: {len(df_sict_faf):,} rows")
        print(f"  - SICT_Piers_byPortTons: {len(df_sict_byporttons):,} rows")
        
        # Load pier proportions
        df_pier_proportions = load_pier_proportions()
        
        # Calculate SICT share
        df_share_total = analyze_sict_share_total(df_honolulu_piers)
        df_share_by_commodity = analyze_sict_share_by_commodity(df_honolulu_piers)
        
        # Get top commodities from FAF model
        print("\nAnalyzing FAF model top commodities...")
        top_faf_tons = get_top_commodities_faf(df_sict_faf)
        
        # Get top commodities from scaled model
        print("\nAnalyzing scaled model top commodities...")
        top_scaled_tons = get_top_commodities_scaled(df_sict_byporttons)
        print(f"  - Top {TOP_N} by tonnage: {list(top_scaled_tons['SCTG2_Commodity'])}")
        
        # Compile results
        results = {
            'Pier_Proportions': df_pier_proportions,
            'SICT_Share_Total': df_share_total,
            'SICT_Share_by_Commodity': df_share_by_commodity,
            'TopCommodities_FAF_Tons': top_faf_tons,
            'TopCommodities_Scaled_Tons': top_scaled_tons,
        }
        
        # Save results
        save_results(results, OUTPUT_PATH)
        
        print("\n" + "=" * 70)
        print("Analysis completed successfully!")
        print("=" * 70)
        
        # Print summary for presentation
        print("\n--- SUMMARY FOR PRESENTATION ---")
        print(f"\nSICT Share of Honolulu Harbor:")
        print(f"  - Tonnage: {df_share_total['SICT_Share_Tons_Pct'].iloc[0]:.1f}%")
        print(f"  - Value: {df_share_total['SICT_Share_Value_Pct'].iloc[0]:.1f}%")
        
        print(f"\nTop 5 Commodities by Tonnage (Scaled Model):")
        for i, row in top_scaled_tons.iterrows():
            print(f"  {i+1}. {row['SCTG2_Commodity']}: {row['Scaled_Tons']:,.0f} tons ({row['Pct_of_Total']:.1f}%)")
        
    except Exception as e:
        print(f"\n{'=' * 70}")
        print(f"ERROR: Analysis failed - {e}")
        print(f"{'=' * 70}")
        raise


if __name__ == "__main__":
    main()
