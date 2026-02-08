"""
FAF Hawaii Data Processing Script

This script processes FAF (Freight Analysis Framework) data to extract Hawaii-specific
transportation information with human-readable labels.

Author: Adithya Ajith
Date: 2026-01-07
"""

import pandas as pd
import re
from pathlib import Path

# Define file paths
BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / "Raw_Data" / "FAF_5.7.1_Regional"
STATE_DATA_DIR = BASE_DIR / "Raw_Data" / "FAF_5.7.1_State"
PROCESSED_DATA_DIR = BASE_DIR / "Processed_Data"

FAF_CSV_PATH = RAW_DATA_DIR / "FAF5.7.1.csv"
STATE_CSV_PATH = STATE_DATA_DIR / "FAF5.7.1_State.csv"
METADATA_PATH = RAW_DATA_DIR / "FAF5_metadata.xlsx"
OUTPUT_PATH = PROCESSED_DATA_DIR / "FAF_Hawaii_Region_2024.xlsx"

# Hawaii state code
HAWAII_STATE_CODE = 15

# Hawaii location codes
HAWAII_CODES = {
    151: "Honolulu HI",
    159: "Rest of HI"
}

# Canonical cargo type labels used throughout the project
CANONICAL_CARGO_TYPES = {"Containers", "Break-Bulk", "Dry-Bulk", "Liquid-Bulk", "RO/RO"}

# SICT (Sand Island Container Terminal) analysis constants
SICT_WHARFAGE_PATH = PROCESSED_DATA_DIR / "SICT-wharfage-data--Jul24-to-Jun25.xlsx"
VEHICLE_COMMODITIES = {"Motorized vehicles", "Transport equip."}
SICT_PIER_VALUE = "51, 52, 53"

def normalize_cargo_type(value):
    """
    Normalize cargo type strings for comparison/validation.

    Note: We intentionally keep normalization minimal (whitespace trimming only) so
    non-canonical labels are caught by validation instead of being silently corrected.
    """
    if pd.isna(value):
        return value
    return str(value).strip()


def load_metadata_lookups(metadata_path):
    """
    Load lookup dictionaries from the metadata Excel file.
    
    Args:
        metadata_path: Path to the FAF5_metadata.xlsx file
        
    Returns:
        dict: Dictionary containing lookup tables for each field
    """
    print("Loading metadata lookups...")
    
    lookups = {}
    
    # Define sheet names and their corresponding lookup keys
    sheet_configs = [
        ('Trade Type', 'trade_type'),
        ('Commodity (SCTG2)', 'sctg2'),
        ('FAF Zone (Domestic)', 'domestic_zone'),
        ('FAF Zone (Foreign)', 'foreign_zone'),
        ('Mode', 'mode'),
        ('State', 'state'),
    ]
    
    try:
        for sheet_name, lookup_key in sheet_configs:
            sheet_df = pd.read_excel(metadata_path, sheet_name=sheet_name)
            lookups[lookup_key] = dict(zip(
                sheet_df.iloc[:, 0],
                sheet_df.iloc[:, 1]
            ))
            print(f"  - Loaded {len(lookups[lookup_key])} {lookup_key} codes")
            
    except Exception as e:
        print(f"Error loading metadata: {e}")
        raise
    
    return lookups


def remove_parenthetical_text(text):
    """
    Remove text in parentheses from a string.
    
    Args:
        text: String that may contain parenthetical text
        
    Returns:
        str: String with parenthetical text removed and trimmed
    """
    if pd.isna(text):
        return text
    
    # Remove text in parentheses and trim whitespace
    result = re.sub(r'\s*\([^)]*\)', '', str(text))
    return result.strip()


def load_and_filter_faf_data(csv_path, hawaii_codes):
    """
    Load FAF data and filter for Hawaii origins/destinations.
    
    Args:
        csv_path: Path to the FAF5.7.1.csv file
        hawaii_codes: Dictionary of Hawaii location codes
        
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    print(f"\nLoading FAF data from {csv_path}...")
    
    try:
        # Load the CSV file
        df = pd.read_csv(csv_path)
        print(f"  - Loaded {len(df):,} total records")
        
        # Filter for Hawaii origins or destinations
        hawaii_filter = (
            df['dms_orig'].isin(hawaii_codes.keys()) | 
            df['dms_dest'].isin(hawaii_codes.keys())
        )
        
        df_filtered = df[hawaii_filter].copy()
        print(f"  - Filtered to {len(df_filtered):,} Hawaii-related records")
        
        return df_filtered
        
    except Exception as e:
        print(f"Error loading FAF data: {e}")
        raise


def load_and_filter_state_data(csv_path, hawaii_state_code):
    """
    Load state-level FAF data and filter for Hawaii origins/destinations.
    
    Args:
        csv_path: Path to the FAF5.7.1_State.csv file
        hawaii_state_code: Hawaii state code (15)
        
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    print(f"\nLoading state-level FAF data from {csv_path}...")
    
    try:
        # Load the CSV file
        df = pd.read_csv(csv_path)
        print(f"  - Loaded {len(df):,} total records")
        
        # Filter for Hawaii origins or destinations
        hawaii_filter = (
            (df['dms_origst'] == hawaii_state_code) | 
            (df['dms_destst'] == hawaii_state_code)
        )
        
        df_filtered = df[hawaii_filter].copy()
        print(f"  - Filtered to {len(df_filtered):,} Hawaii state records")
        
        return df_filtered
        
    except Exception as e:
        print(f"Error loading state FAF data: {e}")
        raise


def replace_codes_with_descriptions(df, lookups):
    """
    Replace numeric codes with human-readable descriptions.
    
    Args:
        df: DataFrame with numeric codes
        lookups: Dictionary of lookup tables
        
    Returns:
        pd.DataFrame: DataFrame with replaced codes
    """
    print("\nReplacing codes with descriptions...")
    
    # Define column-to-lookup mapping
    column_lookup_map = {
        'trade_type': 'trade_type',
        'dms_orig': 'domestic_zone',
        'dms_dest': 'domestic_zone',
        'dms_mode': 'mode',
        'sctg2': 'sctg2',
        'fr_orig': 'foreign_zone',
        'fr_dest': 'foreign_zone',
        'fr_inmode': 'mode',
        'fr_outmode': 'mode',
    }
    
    for column, lookup_key in column_lookup_map.items():
        if column in df.columns:
            df[column] = df[column].map(lookups[lookup_key])
            print(f"  - Replaced {column} codes")
    
    # Apply special transformation for trade_type (remove parenthetical text)
    if 'trade_type' in df.columns:
        df['trade_type'] = df['trade_type'].apply(remove_parenthetical_text)
    
    return df


def replace_state_codes_with_descriptions(df, lookups):
    """
    Replace numeric codes with human-readable descriptions for state-level data.
    
    Args:
        df: DataFrame with numeric codes
        lookups: Dictionary of lookup tables
        
    Returns:
        pd.DataFrame: DataFrame with replaced codes
    """
    print("\nReplacing state codes with descriptions...")
    
    # Define column-to-lookup mapping for state data
    column_lookup_map = {
        'trade_type': 'trade_type',
        'dms_origst': 'state',
        'dms_destst': 'state',
        'dms_mode': 'mode',
        'sctg2': 'sctg2',
        'fr_orig': 'foreign_zone',
        'fr_dest': 'foreign_zone',
        'fr_inmode': 'mode',
        'fr_outmode': 'mode',
    }
    
    for column, lookup_key in column_lookup_map.items():
        if column in df.columns:
            df[column] = df[column].map(lookups[lookup_key])
            print(f"  - Replaced {column} codes")
    
    # Apply special transformation for trade_type (remove parenthetical text)
    if 'trade_type' in df.columns:
        df['trade_type'] = df['trade_type'].apply(remove_parenthetical_text)
    
    return df


def select_output_columns(df):
    """
    Select only the required columns for output.
    
    Args:
        df: DataFrame with all columns
        
    Returns:
        pd.DataFrame: DataFrame with only selected columns
    """
    print("\nSelecting output columns...")
    
    required_columns = [
        'trade_type',
        'dms_orig',
        'dms_dest',
        'dms_mode',
        'sctg2',
        'fr_orig',
        'fr_dest',
        'fr_inmode',
        'fr_outmode',
        'tons_2024',
        'current_value_2024'
    ]
    
    # Check which columns exist in the dataframe
    available_columns = [col for col in required_columns if col in df.columns]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"  - Warning: Missing columns: {missing_columns}")
    
    print(f"  - Selected {len(available_columns)} columns")
    
    return df[available_columns]


def select_state_output_columns(df):
    """
    Select only the required columns for state-level output.
    
    Args:
        df: DataFrame with all columns
        
    Returns:
        pd.DataFrame: DataFrame with only selected columns
    """
    print("\nSelecting state output columns...")
    
    required_columns = [
        'trade_type',
        'dms_origst',
        'dms_destst',
        'dms_mode',
        'sctg2',
        'fr_orig',
        'fr_dest',
        'fr_inmode',
        'fr_outmode',
        'tons_2024',
        'current_value_2024'
    ]
    
    # Check which columns exist in the dataframe
    available_columns = [col for col in required_columns if col in df.columns]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"  - Warning: Missing columns: {missing_columns}")
    
    print(f"  - Selected {len(available_columns)} columns")
    
    return df[available_columns]


def apply_multipliers(df):
    """
    Apply multipliers to tons_2024 and current_value_2024 columns.

    Args:
        df: DataFrame with the selected columns

    Returns:
        pd.DataFrame: DataFrame with multiplied values
    """
    print("\nApplying multipliers to numeric columns...")

    multipliers = {
        'tons_2024': 1000,
        'current_value_2024': 1000000,
    }

    for column, multiplier in multipliers.items():
        if column in df.columns:
            df[column] = df[column] * multiplier
            print(f"  - Multiplied {column} by {multiplier:,}")

    return df


def filter_honolulu_water_flows(df):
    """
    Filter data for Honolulu water-based domestic and import flows.

    Args:
        df: DataFrame with processed Hawaii data

    Returns:
        pd.DataFrame: Filtered dataframe containing only Honolulu water flows
    """
    print("\nFiltering Honolulu water flows...")

    # Filter for Honolulu destination
    honolulu_filter = df['dms_dest'] == "Honolulu HI"

    # Filter for Domestic flows with Water mode (excluding Honolulu origins)
    domestic_filter = (
        (df['trade_type'] == "Domestic flows") &
        (df['dms_orig'] != "Honolulu HI") &
        (df['dms_mode'] == "Water")
    )

    # Filter for Import flows with Water modes (different logic based on origin)
    import_filter = (
        (df['trade_type'] == "Import flows") &
        (
            ((df['dms_orig'] == "Honolulu HI") & (df['fr_inmode'] == "Water")) |
            ((df['dms_orig'] != "Honolulu HI") & (df['dms_mode'] == "Water"))
        )
    )

    # Combine filters: Honolulu destination AND (Domestic water OR Import water)
    combined_filter = honolulu_filter & (domestic_filter | import_filter)

    df_filtered = df[combined_filter].copy()
    print(f"  - Filtered to {len(df_filtered):,} Honolulu water flow records")

    return df_filtered


def create_honolulu_summary(df_honolulu):
    """
    Create a summary dataframe from Honolulu_region data with cargo type information.

    Args:
        df_honolulu: DataFrame with filtered Honolulu data

    Returns:
        pd.DataFrame: Summarized dataframe grouped by dms_dest and sctg2 with primary_cargo_type,
                      containers_proportion, and alternative_cargo_type
    """
    print("\nCreating Honolulu region summary...")

    # Keep only required columns
    required_columns = ['dms_dest', 'sctg2', 'tons_2024', 'current_value_2024']
    df_summary = df_honolulu[required_columns].copy()

    # Group by dms_dest and sctg2, summing numeric columns
    df_summary = df_summary.groupby(['dms_dest', 'sctg2'], as_index=False).agg({
        'tons_2024': 'sum',
        'current_value_2024': 'sum'
    })

    # Load cargo type lookup from Commodity_Dict.xlsx
    print("  - Loading cargo type lookup...")
    commodity_dict_path = PROCESSED_DATA_DIR / "Commodity_Dict.xlsx"
    df_cargo_types = pd.read_excel(commodity_dict_path, sheet_name='Commodity_SCTG2')

    # Merge cargo_type information using commodity descriptions
    # Include Containers_Proportion and Alternative_Cargo_Type for pier distribution logic
    df_summary = df_summary.merge(
        df_cargo_types[['SCTG2_Commodity', 'Primary_Cargo_Type', 'Containers_Proportion', 'Alternative_Cargo_Type']],
        left_on='sctg2',
        right_on='SCTG2_Commodity',
        how='left'
    )

    # Rename columns and drop the redundant SCTG2_Commodity column
    df_summary = df_summary.rename(columns={
        'Primary_Cargo_Type': 'primary_cargo_type',
        'Containers_Proportion': 'containers_proportion',
        'Alternative_Cargo_Type': 'alternative_cargo_type'
    })
    df_summary = df_summary.drop('SCTG2_Commodity', axis=1)

    # Reorder columns
    df_summary = df_summary[['dms_dest', 'sctg2', 'primary_cargo_type', 'containers_proportion', 
                             'alternative_cargo_type', 'tons_2024', 'current_value_2024']]

    print(f"  - Created summary with {len(df_summary):,} grouped records")
    print(f"  - Added primary_cargo_type column with {df_summary['primary_cargo_type'].nunique()} unique cargo types")
    print(f"  - Added containers_proportion and alternative_cargo_type columns")

    return df_summary


def create_honolulu_piers_distribution(df_honolulu_summary):
    """
    Create a pier-level distribution of commodities based on cargo type proportions.
    
    Handles three scenarios based on Containers_Proportion:
    1. 100% containerized (1.0): Allocate all tonnage/value to cargo type "Containers"
    2. 0% containerized (0.0): Allocate all tonnage/value to the non-container cargo type
    3. Mixed (0 < proportion < 1): Split between "Containers" and the non-container cargo type
    
    Important: `Containers_Proportion` is interpreted as the **containerized share** of
    tonnage/value regardless of `Primary_Cargo_Type`.

    Args:
        df_honolulu_summary: DataFrame with Honolulu summary data including:
            sctg2, primary_cargo_type, containers_proportion, alternative_cargo_type, tons, value

    Returns:
        pd.DataFrame: Pier-level distribution with columns: Pier, SCTG2_Commodity, 
                      cargo_type, tons_2024, current_value_2024
    """
    print("\nCreating Honolulu piers distribution...")

    # Load pier data from Current sheet
    pier_data_path = PROCESSED_DATA_DIR / "Honolulu Harbor Pier Operations and Cargo Inventory.xlsx"
    df_piers = pd.read_excel(pier_data_path, sheet_name='Current_v2')
    print(f"  - Loaded {len(df_piers)} piers from Current_v2 sheet")

    # Cargo type to proportion column mapping (must match `Current` sheet headers)
    cargo_type_mapping = {
        'Containers': 'Container Proportion',
        'Break-Bulk': 'Break-Bulk Proportion',
        'Dry-Bulk': 'Dry-Bulk Proportion',
        'Liquid-Bulk': 'Liquid-Bulk Proportion',
        'RO/RO': 'RO/RO Proportion'
    }

    # Create result list
    results = []

    # For each commodity in summary
    for _, commodity_row in df_honolulu_summary.iterrows():
        primary_cargo_type = normalize_cargo_type(commodity_row['primary_cargo_type'])
        alternative_cargo_type = normalize_cargo_type(commodity_row['alternative_cargo_type'])
        containers_proportion = commodity_row['containers_proportion']
        sctg2_code = commodity_row['sctg2']
        total_tons = commodity_row['tons_2024']
        total_value = commodity_row['current_value_2024']

        if pd.isna(primary_cargo_type):
            raise ValueError(f"Missing primary_cargo_type for SCTG2 '{sctg2_code}'.")

        if primary_cargo_type not in CANONICAL_CARGO_TYPES:
            raise ValueError(
                f"Invalid primary_cargo_type '{primary_cargo_type}' for SCTG2 '{sctg2_code}'. "
                f"Expected one of: {sorted(CANONICAL_CARGO_TYPES)}."
            )

        # Default handling for missing container share:
        # - If primary cargo type is Containers, assume fully containerized.
        # - Otherwise assume fully non-containerized.
        if pd.isna(containers_proportion):
            containers_proportion = 1.0 if primary_cargo_type == "Containers" else 0.0

        # Determine allocations using `containers_proportion` as containerized share.
        try:
            container_share = float(containers_proportion)
        except Exception as e:
            raise ValueError(
                f"Invalid Containers_Proportion '{containers_proportion}' for SCTG2 '{sctg2_code}'."
            ) from e

        if not (0.0 <= container_share <= 1.0):
            raise ValueError(
                f"Containers_Proportion out of bounds ({container_share}) for SCTG2 '{sctg2_code}'. "
                "Expected value in [0, 1]."
            )

        non_container_share = 1.0 - container_share

        cargo_allocations = []

        # Containerized portion (if any) always maps to cargo type "Containers"
        if container_share > 0:
            cargo_allocations.append({
                'cargo_type': 'Containers',
                'tonnage_fraction': container_share
            })

        # Non-container portion (if any) maps to a non-container cargo type.
        if non_container_share > 0:
            if primary_cargo_type == "Containers":
                if 0.0 < container_share < 1.0 and pd.isna(alternative_cargo_type):
                    raise ValueError(
                        f"Mixed container share (0<Containers_Proportion<1) but missing "
                        f"alternative_cargo_type for SCTG2 '{sctg2_code}'."
                    )

                non_container_cargo_type = alternative_cargo_type
            else:
                non_container_cargo_type = primary_cargo_type

            non_container_cargo_type = normalize_cargo_type(non_container_cargo_type)
            if pd.isna(non_container_cargo_type):
                raise ValueError(
                    f"Non-container cargo type is missing for SCTG2 '{sctg2_code}' "
                    f"(primary_cargo_type='{primary_cargo_type}', Containers_Proportion={container_share})."
                )

            if non_container_cargo_type not in CANONICAL_CARGO_TYPES:
                raise ValueError(
                    f"Invalid non-container cargo type '{non_container_cargo_type}' for SCTG2 '{sctg2_code}'. "
                    f"Expected one of: {sorted(CANONICAL_CARGO_TYPES)}."
                )

            if non_container_cargo_type == "Containers" and non_container_share > 0:
                raise ValueError(
                    f"Non-container share is positive but resolves to cargo type 'Containers' for SCTG2 '{sctg2_code}'. "
                    "Check primary/alternative cargo type mapping."
                )

            cargo_allocations.append({
                'cargo_type': non_container_cargo_type,
                'tonnage_fraction': non_container_share
            })

        # Distribute to piers for each cargo allocation
        for allocation in cargo_allocations:
            cargo_type = allocation['cargo_type']
            proportion_col = cargo_type_mapping.get(cargo_type)
            tonnage_fraction = allocation['tonnage_fraction']

            if proportion_col is None:
                raise ValueError(
                    f"Unknown cargo type '{cargo_type}' for SCTG2 '{sctg2_code}'. "
                    f"Expected one of: {sorted(CANONICAL_CARGO_TYPES)}."
                )

            if proportion_col not in df_piers.columns:
                raise ValueError(
                    f"Missing pier proportion column '{proportion_col}' in Current sheet. "
                    "Check the input workbook headers."
                )

            # For each pier
            for _, pier_row in df_piers.iterrows():
                pier_proportion = pier_row[proportion_col]

                if pd.isna(pier_proportion):
                    raise ValueError(
                        f"Missing pier proportion for pier '{pier_row.get('Pier')}' in column '{proportion_col}'."
                    )

                # Only include if proportion > 0
                if pier_proportion > 0:
                    results.append({
                        'Pier': pier_row['Pier'],
                        'SCTG2_Commodity': sctg2_code,
                        'cargo_type': cargo_type,
                        'tons_2024': total_tons * tonnage_fraction * pier_proportion,
                        'current_value_2024': total_value * tonnage_fraction * pier_proportion
                    })

    df_piers_distribution = pd.DataFrame(results)
    
    # Reorder columns for clarity
    df_piers_distribution = df_piers_distribution[['Pier', 'SCTG2_Commodity', 'cargo_type', 
                                                    'tons_2024', 'current_value_2024']]
    
    print(f"  - Created pier distribution with {len(df_piers_distribution):,} records")
    print(f"  - Distribution covers {df_piers_distribution['Pier'].nunique()} unique piers")
    print(f"  - Distribution covers {df_piers_distribution['SCTG2_Commodity'].nunique()} unique commodities")

    return df_piers_distribution


def load_sict_shipment_summary():
    """
    Load shipment summary from SICT wharfage data Excel file.
    
    Returns:
        pd.DataFrame: Shipment summary data excluding the Total row
    """
    print("\nLoading SICT shipment summary...")
    
    df = pd.read_excel(SICT_WHARFAGE_PATH, sheet_name='shipment_summary')
    
    # Exclude the Total row
    df = df[df['SICT-Type'] != 'Total'].copy()
    
    print(f"  - Loaded {len(df)} shipment summary records")
    print(f"  - Total tonnage target: {df['Ton'].sum():,.1f}")
    
    return df


def create_sict_piers_faf(df_honolulu_piers):
    """
    Filter Honolulu_Piers for SICT piers (51, 52, 53).
    
    Args:
        df_honolulu_piers: DataFrame with Honolulu pier distribution data
        
    Returns:
        pd.DataFrame: Filtered dataframe containing only SICT pier data
    """
    print("\nCreating SICT_Piers_FAF (raw FAF data)...")
    
    df_sict = df_honolulu_piers[df_honolulu_piers['Pier'] == SICT_PIER_VALUE].copy()
    
    print(f"  - Filtered to {len(df_sict):,} SICT pier records")
    print(f"  - Total tons: {df_sict['tons_2024'].sum():,.1f}")
    print(f"  - Total value: ${df_sict['current_value_2024'].sum():,.0f}")
    
    return df_sict


def create_sict_piers_byporttons(df_sict_faf, df_shipment_summary):
    """
    Scale SICT piers data to match shipment_summary tonnage totals.
    
    Uses tonnage scaling factor for both tons and dollar values.
    Preserves original commodity proportions within each (SICT_Type, Containerized) group.
    
    Args:
        df_sict_faf: DataFrame with raw SICT FAF data
        df_shipment_summary: DataFrame with target tonnage by category
        
    Returns:
        pd.DataFrame: Scaled SICT piers data with additional categorization columns
    """
    print("\nCreating SICT_Piers_byPortTons (tonnage-scaled)...")
    
    df = df_sict_faf.copy()
    
    # Add SICT_Type column based on commodity
    df['SICT_Type'] = df['SCTG2_Commodity'].apply(
        lambda x: 'Vehicles' if x in VEHICLE_COMMODITIES else 'Cargo Non Vehicles'
    )
    
    # Add Containerized column based on cargo_type
    df['Containerized'] = df['cargo_type'].apply(
        lambda x: 'Yes' if x == 'Containers' else 'No'
    )
    
    # Create a lookup dictionary from shipment_summary for target tonnage
    target_tonnage = {}
    for _, row in df_shipment_summary.iterrows():
        key = (row['SICT-Type'], row['Containerized'])
        target_tonnage[key] = row['Ton']
    
    # Calculate current tonnage by group
    current_tonnage = df.groupby(['SICT_Type', 'Containerized'])['tons_2024'].sum()
    
    # Calculate scaling factors
    scaling_factors = {}
    for (sict_type, containerized), current_tons in current_tonnage.items():
        key = (sict_type, containerized)
        target_tons = target_tonnage.get(key, 0)
        if current_tons > 0:
            scaling_factors[key] = target_tons / current_tons
        else:
            scaling_factors[key] = 1.0
        print(f"  - {sict_type}, Containerized={containerized}: "
              f"current={current_tons:,.1f}, target={target_tons:,.1f}, scale={scaling_factors[key]:.4f}")
    
    # Apply scaling factors
    def get_scale(row):
        key = (row['SICT_Type'], row['Containerized'])
        return scaling_factors.get(key, 1.0)
    
    df['tonnage_scale'] = df.apply(get_scale, axis=1)
    df['scaled_tons'] = df['tons_2024'] * df['tonnage_scale']
    df['scaled_value'] = df['current_value_2024'] * df['tonnage_scale']
    
    # Reorder columns
    df = df[['Pier', 'SCTG2_Commodity', 'cargo_type', 'tons_2024', 'current_value_2024',
             'SICT_Type', 'Containerized', 'tonnage_scale', 'scaled_tons', 'scaled_value']]
    
    print(f"  - Created {len(df):,} scaled records")
    print(f"  - Total scaled tons: {df['scaled_tons'].sum():,.1f}")
    print(f"  - Total scaled value: ${df['scaled_value'].sum():,.0f}")
    
    return df


def save_to_excel(df_hawaii, df_honolulu, df_honolulu_summary, df_honolulu_piers,
                  df_sict_faf, df_sict_byporttons,
                  df_state, output_path):
    """
    Save the processed dataframes to an Excel file with multiple sheets.

    Args:
        df_hawaii: DataFrame with all Hawaii regional data
        df_honolulu: DataFrame with filtered Honolulu data
        df_honolulu_summary: DataFrame with summarized Honolulu data
        df_honolulu_piers: DataFrame with pier-level distribution
        df_sict_faf: DataFrame with raw FAF data filtered for SICT piers
        df_sict_byporttons: DataFrame with tonnage-scaled SICT data
        df_state: DataFrame with Hawaii state-level data
        output_path: Path for the output Excel file
    """
    print(f"\nSaving output to {output_path}...")

    try:
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save to Excel with multiple sheets
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_hawaii.to_excel(writer, sheet_name='Hawaii_region', index=False)
            df_honolulu.to_excel(writer, sheet_name='Honolulu_region', index=False)
            df_honolulu_summary.to_excel(writer, sheet_name='Honolulu_region_Summary', index=False)
            df_honolulu_piers.to_excel(writer, sheet_name='Honolulu_Piers', index=False)
            df_sict_faf.to_excel(writer, sheet_name='SICT_Piers_FAF', index=False)
            df_sict_byporttons.to_excel(writer, sheet_name='SICT_Piers_byPortTons', index=False)
            df_state.to_excel(writer, sheet_name='Hawaii_state', index=False)

        print(f"  - Successfully saved Hawaii_region sheet: {len(df_hawaii):,} records")
        print(f"  - Successfully saved Honolulu_region sheet: {len(df_honolulu):,} records")
        print(f"  - Successfully saved Honolulu_region_Summary sheet: {len(df_honolulu_summary):,} records")
        print(f"  - Successfully saved Honolulu_Piers sheet: {len(df_honolulu_piers):,} records")
        print(f"  - Successfully saved SICT_Piers_FAF sheet: {len(df_sict_faf):,} records")
        print(f"  - Successfully saved SICT_Piers_byPortTons sheet: {len(df_sict_byporttons):,} records")
        print(f"  - Successfully saved Hawaii_state sheet: {len(df_state):,} records")

    except Exception as e:
        print(f"Error saving output: {e}")
        raise


def main():
    """
    Main execution function.
    """
    print("="*70)
    print("FAF Hawaii Data Processing Script")
    print("="*70)
    
    try:
        # Step 1: Load metadata lookups
        lookups = load_metadata_lookups(METADATA_PATH)
        
        # =====================================================================
        # Process Regional Data
        # =====================================================================
        # Step 2: Load and filter FAF regional data
        df = load_and_filter_faf_data(FAF_CSV_PATH, HAWAII_CODES)
        
        # Step 3: Replace codes with descriptions
        df = replace_codes_with_descriptions(df, lookups)
        
        # Step 4: Select output columns
        df = select_output_columns(df)

        # Step 5: Apply multipliers
        df_hawaii = apply_multipliers(df)

        # Step 5.5: Remove rows where both tons and value are zero
        print("\nRemoving rows where both tons_2024 and current_value_2024 are zero...")
        initial_count = len(df_hawaii)
        df_hawaii = df_hawaii[~((df_hawaii['tons_2024'] == 0) & (df_hawaii['current_value_2024'] == 0))].copy()
        removed_count = initial_count - len(df_hawaii)
        print(f"  - Removed {removed_count:,} rows with zero tons and value")
        print(f"  - Remaining records: {len(df_hawaii):,}")

        # Step 6: Filter Honolulu water flows
        df_honolulu = filter_honolulu_water_flows(df_hawaii)

        # Step 7: Create Honolulu summary
        df_honolulu_summary = create_honolulu_summary(df_honolulu)

        # Step 8: Create Honolulu piers distribution
        df_honolulu_piers = create_honolulu_piers_distribution(df_honolulu_summary)

        # =====================================================================
        # Process SICT Pier Data
        # =====================================================================
        # Step 8.5: Load SICT shipment summary
        df_shipment_summary = load_sict_shipment_summary()

        # Step 8.6: Create SICT piers - raw FAF filter
        df_sict_faf = create_sict_piers_faf(df_honolulu_piers)

        # Step 8.7: Create SICT piers - tonnage scaled
        df_sict_byporttons = create_sict_piers_byporttons(df_sict_faf, df_shipment_summary)

        # =====================================================================
        # Process State Data
        # =====================================================================
        # Step 9: Load and filter FAF state data
        df_state = load_and_filter_state_data(STATE_CSV_PATH, HAWAII_STATE_CODE)

        # Step 10: Replace state codes with descriptions
        df_state = replace_state_codes_with_descriptions(df_state, lookups)

        # Step 11: Select state output columns
        df_state = select_state_output_columns(df_state)

        # Step 12: Apply multipliers to state data
        df_state = apply_multipliers(df_state)

        # =====================================================================
        # Save Output
        # =====================================================================
        # Step 13: Save to Excel with multiple sheets
        save_to_excel(df_hawaii, df_honolulu, df_honolulu_summary, df_honolulu_piers,
                      df_sict_faf, df_sict_byporttons,
                      df_state, OUTPUT_PATH)
        
        print("\n" + "="*70)
        print("Processing completed successfully!")
        print("="*70)
        
        # Display summary statistics
        print("\nSummary Statistics:")
        print(f"  - Hawaii_region total records: {len(df_hawaii):,}")
        print(f"  - Hawaii_region total tons (2024): {df_hawaii['tons_2024'].sum():,.0f}")
        print(f"  - Hawaii_region total value (2024): ${df_hawaii['current_value_2024'].sum():,.0f}")
        print(f"\n  - Honolulu_region total records: {len(df_honolulu):,}")
        print(f"  - Honolulu_region total tons (2024): {df_honolulu['tons_2024'].sum():,.0f}")
        print(f"  - Honolulu_region total value (2024): ${df_honolulu['current_value_2024'].sum():,.0f}")
        print(f"\n  - Honolulu_Piers total records: {len(df_honolulu_piers):,}")
        print(f"  - Honolulu_Piers total tons (2024): {df_honolulu_piers['tons_2024'].sum():,.0f}")
        print(f"  - Honolulu_Piers total value (2024): ${df_honolulu_piers['current_value_2024'].sum():,.0f}")
        print(f"\n  - SICT_Piers_FAF total records: {len(df_sict_faf):,}")
        print(f"  - SICT_Piers_FAF total tons (2024): {df_sict_faf['tons_2024'].sum():,.0f}")
        print(f"  - SICT_Piers_byPortTons scaled tons: {df_sict_byporttons['scaled_tons'].sum():,.0f}")
        print(f"\n  - Hawaii_state total records: {len(df_state):,}")
        print(f"  - Hawaii_state total tons (2024): {df_state['tons_2024'].sum():,.0f}")
        print(f"  - Hawaii_state total value (2024): ${df_state['current_value_2024'].sum():,.0f}")
        
    except Exception as e:
        print(f"\n{'='*70}")
        print(f"ERROR: Processing failed - {e}")
        print(f"{'='*70}")
        raise


if __name__ == "__main__":
    main()
