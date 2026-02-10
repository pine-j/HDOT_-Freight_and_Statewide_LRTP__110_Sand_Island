# Estimating Freight Commodity Flows at Sand Island Container Terminal

## Overview

### Purpose

The primary goal of this analysis is to estimate the types and volumes of freight commodities that arrive at the Sand Island Container Terminal (SICT) via water for the year 2024, and are subsequently transported off the island via the Sand Island Access Road bridge. This information supports transportation planning and infrastructure assessment for the Sand Island corridor.

### Data Challenges

Estimating commodity-level freight flows at SICT presents several challenges:

1. **No publicly available SICT commodity data**: There is no publicly available dataset that provides a detailed breakdown of commodities flowing into the Sand Island Container Terminal specifically.

2. **FAF data covers broader geography**: The Freight Analysis Framework (FAF) provides commodity-level freight flow data, but only at the regional level for "Honolulu HI." SICT (piers 51, 52, 53) is part of Honolulu Harbor, but FAF does not distinguish between individual piers or terminals within the region.

3. **Need to disaggregate regional data**: This study uses multiple data sources to estimate what portion of the FAF regional freight flows can be attributed specifically to SICT operations.

4. **Limited actual SICT data**: We obtained wharfage data directly from SICT officials, which provides a high-level overview of shipment inflows for the period July 2024 through June 2025 (FY2025). However, this data lacks the detailed commodity breakdown available in FAF, and does not cover the full calendar year 2024.

5. **Capacity-based pier distribution**: No data source provides actual commodity flows by individual pier. To distribute regional commodity totals to specific piers, this study uses pier-specific annual capacity data from the Honolulu Harbor 2050 Master Plan as a proxy for actual throughput. Each pier's share of total harbor capacity for a given cargo type is assumed to reflect its share of actual freight flows. While this is a reasonable approximation, actual utilization rates may vary from designed capacities.

### Temporal Assumptions

- **FAF reference year**: The FAF 5.7.1 dataset provides freight flow estimates for calendar year 2024.
- **SICT wharfage data period**: The actual port data covers July 1, 2024 through June 30, 2025 (fiscal year 2025).
- **Assumption**: Since the wharfage data represents a complete one-year period, we assume it is representative of calendar year 2024 freight volumes for calibration purposes. This assumption enables direct comparison between FAF model estimates and actual port throughput.

### Approach

This document explains the methodology used to create the **deliverable output sheets used for final reporting**—`Honolulu_Piers`, `SICT_Piers_FAF`, and `SICT_Piers_byPortTons`—in the `FAF_Hawaii_Region_2024.xlsx` file (located at `Processed_Data/FAF_Hawaii_Region_2024.xlsx`). `Honolulu_Piers` provides a pier-level distribution of water-based inbound freight into Honolulu Harbor; `SICT_Piers_FAF` is simply the raw FAF-based SICT subset filtered from `Honolulu_Piers` (piers 51, 52, 53); and `SICT_Piers_byPortTons` provides calibrated (scaled) estimates using actual SICT wharfage data. Other workbook tabs are intermediate/QC outputs for internal review and are not required for final reporting.

**Important Note:** The final dataset includes only water-based freight flows into Honolulu Harbor. All inbound cargo at SICT piers must exit Sand Island via the bridge, making these estimates directly applicable to bridge traffic analysis.

**Project Location:**
```
<project root>
```

All file paths referenced in this document are relative to the project root directory.

---

## Data Sources

The analysis relies on three primary data sources:

### 1. FAF 5.7.1 Regional Data
- **File:** `Raw_Data\FAF_5.7.1_Regional\FAF5.7.1.csv`
- **Description:** FAF version 5.7.1 regional database for 2017-2024 with forecasts up to 2050 (mid-range estimates only)
- **Provider:** U.S. Department of Transportation, Bureau of Transportation Statistics
- **Content:** Domestic and international freight flows between FAF regions, including:
  - Origin and destination regions
  - Commodity types (SCTG2 classification)
  - Transportation modes
  - Tonnage and value projections for 2024
- **Use in Analysis:** Source of freight flow volumes and commodity distributions for Hawaii region

### 2. Honolulu Harbor 2050 Master Plan
- **File:** `Ref_Documents\Honolulu_Harbor_2050_Master_Plan.pdf`
- **Description:** Long-range planning document for Honolulu Harbor infrastructure and operations
- **Provider:** Hawaii Department of Transportation, Harbors Division
- **Content:** 
  - Individual pier operational characteristics
  - Cargo type handling capabilities by pier
  - Annual throughput capacities by cargo type
- **Use in Analysis:** Source of pier-specific capacity data and cargo type definitions used to distribute regional freight flows to individual piers

### 3. SICT Wharfage Data (July 2024 to June 2025)
- **File:** `Ref_Documents\SICT-wharfage-data--Jul24-to-Jun25.pdf`
- **Description:** Schedule of cargo shipped through the Sand Island Container Terminal (SICT) by cargo operator, excluding transshipments
- **Provider:** Hawaii Department of Transportation, Harbors Division (DOT-H)
- **Data Basis:** Cash basis data obtained from wharfage self-reports submitted during July 1, 2024 through June 30, 2025 (FY2025)
- **Content:** 
  - Inbound and outbound cargo tonnage by cargo category
  - Categories include: Vehicles, Automobiles (containerized), General Merchandise, Explosives, and Shipping Devices (containers)
  - Tonnage by shipping operator (Matson, Pasha Hawaii, Waldron Norton Lilly)
- **Use in Analysis:** Source of actual SICT throughput totals used to calibrate FAF model estimates in Step 5
- **Processed Data:** `Processed_Data\SICT-wharfage-data--Jul24-to-Jun25.xlsx` contains the summarized tonnage data

---

## Step 1: Pier Operations Data Collection (Manual)

### Source Document
The pier operations data was manually extracted from the **Honolulu Harbor 2050 Master Plan** PDF document, located at [`Ref_Documents/Honolulu_Harbor_2050_Master_Plan.pdf`](Ref_Documents/Honolulu_Harbor_2050_Master_Plan.pdf).

### Output File
The extracted data was compiled into the **Current_v2** sheet in [`Processed_Data/Honolulu Harbor Pier Operations and Cargo Inventory.xlsx`](Processed_Data/Honolulu Harbor Pier Operations and Cargo Inventory.xlsx).

**Note:** The workbook also contains **Current** (original extraction) and **Future** (future scenario assumptions) sheets. The automated script uses the **Current_v2** sheet, which refines the original pier proportions to reflect that SICT piers (51, 52, 53) do not handle Liquid-Bulk cargo in this model. Although SICT does receive jet fuel, Liquid-Bulk is excluded from the estimation models; SICT is assumed to handle only Containers, RO/RO, and Break-Bulk cargo. Additionally, the **Current** and **Current_v2** sheets assume that KCT Piers are not operational right now and they will be operational in the future.

### Columns Extracted from Master Plan

The following columns were directly extracted from the Honolulu Harbor 2050 Master Plan:

| Column Name | Description |
|-------------|-------------|
| **Pier** | Pier identification (e.g., Pier 1, Pier 2, Sand Island) |
| **Cargo Types** | Types of cargo handled at each pier |
| **Container Annual Capacity (TEUs)** | Annual capacity for containers in Twenty-foot Equivalent Units |
| **Automobiles (RO/RO) Annual Capacity** | Annual capacity for automobiles/vehicles |
| **Break-Bulk Annual Capacity (Ton)** | Annual capacity for break-bulk cargo in tons |
| **Liquid-Bulk Annual Capacity (Bbls)** | Annual capacity for liquid-bulk cargo in barrels |
| **Dry-Bulk Annual Capacity (Tons)** | Annual capacity for dry-bulk cargo in tons |

### Columns Derived from Annual Capacities

Using the annual capacity values extracted from the Master Plan, the following proportion columns were calculated to represent each pier's share of total harbor capacity for each cargo type:

| Column Name | Description |
|-------------|-------------|
| **Container Proportion** | Pier's share of total container capacity |
| **RO/RO Proportion** | Pier's share of total RO/RO capacity |
| **Break-Bulk Proportion** | Pier's share of total break-bulk capacity |
| **Liquid-Bulk Proportion** | Pier's share of total liquid-bulk capacity |
| **Dry-Bulk Proportion** | Pier's share of total dry-bulk capacity |

**Calculation Method:**
```
Pier Proportion = Pier Annual Capacity / Total Harbor Annual Capacity (for each cargo type)
```

These proportions are used to distribute regional freight flows to individual piers based on their operational capacity.

---

## Step 2: Cargo Type Definitions

### Source File
[`Processed_Data/Commodity_Dict.xlsx`](Processed_Data/Commodity_Dict.xlsx)

### Cargo_Type Sheet

The **Cargo_Type** sheet in the Commodity Dictionary provides definitions for the five major cargo type categories used in the analysis. These definitions were also derived from the **Honolulu Harbor 2050 Master Plan**.

The five cargo types are:

1. **Containers** - Standardized shipping containers (TEUs)
2. **RO/RO (Roll-on/Roll-off)** - Vehicles and wheeled cargo
3. **Break-Bulk** - Non-containerized general cargo
4. **Liquid-Bulk** - Petroleum products, chemicals, and other liquids
5. **Dry-Bulk** - Coal, aggregates, grain, and other dry commodities

These cargo type definitions establish the framework for mapping specific SCTG2 commodities to pier operational categories.

---

## Step 3: Commodity Mapping (SCTG2 to Cargo Types)

### Source File
[`Processed_Data/Commodity_Dict.xlsx`](Processed_Data/Commodity_Dict.xlsx)

### Commodity_SCTG2 Sheet

The **Commodity_SCTG2** sheet maps Standard Classification of Transported Goods (SCTG2) commodity codes to the five cargo type categories defined in Step 2. This sheet includes both primary cargo type assignments and provisions for mixed-mode handling.

**Mapping Structure:**

| SCTG_Commodity | Primary_Cargo_Type | Containers_Proportion | Containers_Rational | Alternative_Cargo_Type |
|----------------|--------------------|-----------------------|---------------------|------------------------|
| Live animals/fish | Containers | 0.7 | High share in reefer/ventilated containers and specialized crates; remainder by air or specialized vessels. | Break-Bulk |
| Cereal grains | Dry-Bulk | 0.05 | Elevator-to-bulk-carrier flows dominate; small identity-preserved/specialty volumes ship in containers. | Containers |
| Meat/seafood | Containers | 0.95 | Cold-chain and hygiene requirements make reefer containers the norm; specialized reefer vessels are rare niche. | Break-Bulk |
| Milled grain prods. | Containers | 0.9 | Flour/DDGs and processed grains typically bagged or tote-packed in boxes; some bulk flows remain. | Dry-Bulk |
| ... | ... | ... | ... | ... |

**Column Definitions:**

- **SCTG2_Commodity**: Standard Classification of Transported Goods (SCTG2) commodity description
- **Primary_Cargo_Type**: The primary cargo handling method for this commodity (Containers, Break-Bulk, Dry-Bulk, Liquid-Bulk, or RO/RO)
- **Containers_Proportion**: A value between 0.0 and 1.0 indicating what proportion of this commodity's tonnage is handled as containers
  - `1.0` = 100% containerized (all tonnage uses container handling)
  - `0.0` = 0% containerized (all tonnage uses the primary cargo type handling)
  - Values between 0 and 1 = Mixed handling (e.g., `0.7` means 70% in containers, 30% via alternative method)
- **Containers_Rational (Rationale)**: Detailed explanation and justification for the containers proportion assignment. This column documents the specific reasoning, industry practices, physical characteristics, and expert judgment used to determine how each commodity is handled. The rationale provides critical context for understanding the proportion values and supports the analytical decisions made in the commodity mapping process. Refer to the actual spreadsheet (`Commodity_Dict.xlsx`, sheet `Commodity_SCTG2`) for the complete rationale text for each commodity.
- **Alternative_Cargo_Type**: The cargo handling method used for the non-containerized portion when Containers_Proportion is between 0 and 1 (e.g., if 70% is containerized, this specifies how the remaining 30% is handled)

This mapping enables the translation of FAF commodity data (which uses SCTG2 codes) into the cargo type categories that correspond to pier operational characteristics, while accounting for commodities that may be handled through multiple methods.

**Key Mapping Logic:**
- Bulk commodities (grains, coal, aggregates) → Dry-Bulk or Liquid-Bulk (Containers_Proportion = 0.0)
- Fully manufactured goods and perishables → Containers (Containers_Proportion = 1.0)
- Vehicles and machinery → RO/RO (Containers_Proportion = 0.0)
- Oversized or non-containerized goods → Break-Bulk (Containers_Proportion = 0.0)
- Mixed-mode commodities → Primary_Cargo_Type with partial containerization (0 < Containers_Proportion < 1.0, with Alternative_Cargo_Type specified)

---

## Step 4: Data Processing & Pier Distribution

### Script File
[`Script/process_FAF_Region.py`](Script/process_FAF_Region.py)

### Purpose
The Python script automates the process of combining FAF regional freight data with pier operational characteristics to generate the `Honolulu_Piers` deliverable and the **two SICT deliverable output sheets**.

### Processing Workflow

The script performs the following operations to create the `Honolulu_Piers` sheet (deliverable and also used to derive the SICT outputs):

#### 4.1 Load and Filter FAF Data
- Loads FAF 5.7.1 regional data from [`Raw_Data/FAF_5.7.1_Regional/FAF5.7.1.csv`](Raw_Data/FAF_5.7.1_Regional/FAF5.7.1.csv)
- Filters for Hawaii-related flows (Honolulu HI and Rest of HI)
- Replaces numeric codes with human-readable descriptions using metadata
- Converts FAF units to “base” units used in the project outputs:
  - `tons_2024`: FAF is in *thousand tons* → multiplied by 1,000 to get *tons*
  - `current_value_2024`: FAF is in *million dollars* → multiplied by 1,000,000 to get *dollars*
- Removes records where both `tons_2024` and `current_value_2024` are zero (cleanup step to reduce noise before Honolulu filtering)

#### 4.2 Filter Honolulu Water Flows

The script applies specific filters to isolate water-based freight arriving at Honolulu Harbor. This critical step ensures that only freight physically arriving by water at Honolulu Harbor piers is included in the analysis, excluding air freight, truck freight, and intra-Honolulu movements.

**Filtering Logic:**

The filter combines two conditions that must both be true:
1. **Destination must be Honolulu HI** - Only freight destined for Honolulu
2. **Must be either a Domestic Water flow OR an Import Water flow** (as defined below)

**Domestic Flows (within the United States):**

Criteria for domestic freight:
- `trade_type` = "Domestic flows"
- `dms_dest` = "Honolulu HI" (destination is Honolulu)
- `dms_orig` ≠ "Honolulu HI" (origin is NOT Honolulu - excludes local movements)
- `dms_mode` = "Water" (transported by water/ship)

*Example:* Freight shipped by water from Los Angeles to Honolulu

**Import Flows (from foreign countries):**

Criteria for imported freight varies based on the origin location:

*Case 1: Import arrives directly at Honolulu from foreign origin*
- `trade_type` = "Import flows"
- `dms_orig` = "Honolulu HI" (Honolulu is the first domestic location)
- `dms_dest` = "Honolulu HI" (destination is Honolulu)
- `fr_inmode` = "Water" (mode of entry into the U.S. is by water)

*Example:* Container ship from Japan directly to Honolulu Harbor

*Case 2: Import arrives at another U.S. location first, then transported to Honolulu*
- `trade_type` = "Import flows"
- `dms_orig` ≠ "Honolulu HI" (entered U.S. at a different location, e.g., Los Angeles)
- `dms_dest` = "Honolulu HI" (final destination is Honolulu)
- `dms_mode` = "Water" (domestic transport mode to Honolulu is by water)

*Example:* Goods imported through Los Angeles port, then shipped by water to Honolulu

**Rationale:**

This filtering approach ensures the dataset captures:
- ✅ All waterborne domestic freight arriving at Honolulu from other U.S. locations
- ✅ All international imports arriving directly at Honolulu by ship
- ✅ All international imports that enter the U.S. elsewhere but are subsequently shipped to Honolulu by water

#### 4.3 Create Honolulu Summary
The script aggregates the filtered data by:
- Destination (`dms_dest`)
- SCTG2 Commodity (`sctg2`)

For each commodity, it sums:
- `tons_2024` - Total tonnage
- `current_value_2024` - Total freight value

The script then merges cargo type information from the **Commodity_SCTG2** mapping (Step 3) to assign each SCTG2 commodity to its corresponding cargo type category, including:
- `Primary_Cargo_Type` - The primary handling method
- `Containers_Proportion` - The proportion handled as containers
- `Alternative_Cargo_Type` - The alternative handling method for mixed-mode commodities

#### 4.4 Distribute to Piers
The final step distributes the commodity-level totals to individual piers using the proportions calculated in Step 1. The distribution logic accounts for commodities that may be handled through multiple cargo types.

**Distribution Logic:**

The script handles three scenarios based on the `Containers_Proportion` value, where `Containers_Proportion` is always interpreted as the **containerized share** of the commodity’s tonnage/value:

**Scenario 1: Fully Containerized** (`Containers_Proportion` = 1.0)
```python
For each commodity with Containers_Proportion = 1.0:
    cargo_type = "Containers"

    For each pier:
        proportion = pier's Container Proportion

        If proportion > 0:
            pier_tons = commodity_tons × proportion
            pier_value = commodity_value × proportion
```

**Scenario 2: Fully Non-Containerized** (`Containers_Proportion` = 0.0)
```python
For each commodity with Containers_Proportion = 0.0:
    non_container_cargo_type =
        Primary_Cargo_Type, if Primary_Cargo_Type != "Containers"
        otherwise Alternative_Cargo_Type

    For each pier:
        proportion = pier's Proportion for non_container_cargo_type

        If proportion > 0:
            pier_tons = commodity_tons × proportion
            pier_value = commodity_value × proportion
```

**Scenario 3: Mixed-Mode Handling** (0 < `Containers_Proportion` < 1.0)
```python
For each commodity with 0 < Containers_Proportion < 1.0:
    # Part 1: Containerized share
    For each pier:
        proportion = pier's Container Proportion
        If proportion > 0:
            pier_tons = commodity_tons × Containers_Proportion × proportion
            pier_value = commodity_value × Containers_Proportion × proportion

    # Part 2: Non-containerized share
    non_container_cargo_type =
        Primary_Cargo_Type, if Primary_Cargo_Type != "Containers"
        otherwise Alternative_Cargo_Type

    For each pier:
        proportion = pier's Proportion for non_container_cargo_type
        If proportion > 0:
            pier_tons = commodity_tons × (1 - Containers_Proportion) × proportion
            pier_value = commodity_value × (1 - Containers_Proportion) × proportion
```

**Example:**

If "Meat/seafood" has:
- Total tonnage: 10,000 tons
- `Primary_Cargo_Type`: Containers
- `Containers_Proportion`: 0.95
- `Alternative_Cargo_Type`: Break-Bulk

The distribution would be:
- 9,500 tons (95%) distributed to piers based on their Container handling proportions
- 500 tons (5%) distributed to piers based on their Break-Bulk handling proportions

**Output Columns:**
- `Pier` - Pier name
- `SCTG2_Commodity` - SCTG2 commodity description
- `cargo_type` - Cargo type category used for this distribution record (may be Primary_Cargo_Type or Alternative_Cargo_Type)
- `tons_2024` - Distributed tonnage for 2024
- `current_value_2024` - Distributed freight value for 2024

**Note:** For mixed-mode commodities, each commodity will generate multiple records in the output—one set of pier distributions for the primary cargo type and another set for the alternative cargo type.

---

## Step 5: SICT Pier Analysis

### 5.1 Purpose

The SICT (Sand Island Container Terminal) analysis reconciles FAF model estimates with actual port shipment data for piers 51, 52, and 53. This step produces two output sheets that provide different perspectives on commodity flows through the SICT piers.

### 5.2 Additional Data Source

**SICT Wharfage Data (July 2024 to June 2025)**

- **File:** [`Ref_Documents/SICT-wharfage-data--Jul24-to-Jun25.pdf`](Ref_Documents/SICT-wharfage-data--Jul24-to-Jun25.pdf)
- **Description:** Schedule of cargo shipped through the Sand Island Container Terminal (SICT) by cargo operator, excluding transshipments
- **Provider:** Hawaii Department of Transportation, Harbors Division (DOT-H)
- **Data Basis:** Cash basis data obtained from wharfage self-reports submitted during July 1, 2024 through June 30, 2025 (FY2025)
- **Content:** 
  - Inbound and outbound cargo tonnage by cargo category
  - Categories include: Vehicles, Automobiles (containerized), General Merchandise, Explosives, and Shipping Devices (containers)
  - Tonnage by shipping operator (Matson, Pasha Hawaii, Waldron Norton Lilly)
- **Use in Analysis:** Source of actual SICT throughput totals used to calibrate FAF model estimates
- **Processed Data:** [`Processed_Data/SICT-wharfage-data--Jul24-to-Jun25.xlsx`](Processed_Data/SICT-wharfage-data--Jul24-to-Jun25.xlsx) contains two sheets:
  - **shipment_data**: Raw inbound cargo data with manually assigned Type classifications
  - **shipment_summary**: Aggregated inbound tonnage by SICT-Type (Vehicles / Cargo Non Vehicles) and Containerized status (Yes / No)

#### Processing SICT Wharfage Data: From shipment_data to shipment_summary

The **shipment_data** sheet contains the raw inbound cargo records extracted from the PDF, filtered for `Direction = "IN"` only. A **Type** column was manually added to classify each cargo description into one of four categories based on two dimensions:

1. **SICT-Type**: Whether the cargo is "Vehicles" or "Cargo Non Vehicles"
2. **Containerized**: Whether the cargo is shipped in containers ("Yes") or not ("No")

**Type Classification Rules:**

The following mapping was applied to assign the Type column based on the cargo description codes:

| Description Code | Description | Assigned Type | Rationale |
|-----------------|-------------|---------------|-----------|
| 60-01 | Automobile in container or frame each | Vehicles Containerized | Automobiles shipped in containers or frames |
| 60-44 | Vehicles ton | Vehicles Non Containerized | Vehicles shipped via RO/RO (roll-on/roll-off) |
| 60-73 | Shipping Device Loaded 45ft. each | Cargo Containerized | 45-foot loaded containers |
| 60-74 | Shipping Device Loaded 40ft. each | Cargo Containerized | 40-foot loaded containers |
| 60-77 | Shipping Device Loaded 20ft. each | Cargo Containerized | 20-foot loaded containers |
| 60-22 | General Merchandise (NOS) ton | Cargo Non Containerized | Non-containerized general merchandise |
| 60-19 | Explosives ton | Cargo Non Containerized | See note below |

**Note on Explosives Classification:**

The "60-19 Explosives ton" category cannot be directly mapped to any of the SCTG2 commodities in the FAF dataset. Since explosives represent a specialized cargo type that does not fit neatly into the standard commodity classifications, they were included as part of general cargo under "Cargo Non Containerized." This ensures all reported tonnage is accounted for in the analysis.

**Identifying Non-Containerized Shipments:**

The "TEU Calculated" column in the source data provides a key indicator for containerization status:
- **Empty/NaN values** indicate that the cargo is **not containerized** (applies to: Explosives, General Merchandise NOS, and Vehicles ton)
- **Numeric values** indicate the cargo is **containerized** and shows the calculated TEU count

**Aggregation to shipment_summary:**

The **shipment_summary** sheet was created by aggregating the shipment_data records by the two classification dimensions:

```
shipment_summary = shipment_data.groupby(['SICT-Type', 'Containerized'])['Ton'].sum()
```

**Resulting Summary (Inbound Tonnage):**

| SICT-Type | Containerized | Ton |
|-----------|---------------|------|
| Cargo Non Vehicles | Yes | 3,958,177 |
| Cargo Non Vehicles | No | 8,130 |
| Vehicles | No | 90,742 |
| Vehicles | Yes | 27,184 |
| **Total** | | **4,084,234** |

This summary provides the target tonnage values used to calibrate the FAF model estimates in the subsequent analysis steps.

### 5.3 Rationale for SICT Calibration

The FAF (Freight Analysis Framework) model provides valuable commodity-level detail for freight flows, including the distribution across SCTG2 commodity categories. However, when comparing FAF estimates for the SICT piers to actual port data, we observed significant discrepancies:

- **FAF Model Estimate:** ~132,000 tons total for SICT piers (51, 52, 53)
- **Actual Port Data (PDF):** ~4,084,000 tons total inbound cargo

The PDF data from SICT authorities provides actual wharfage records but lacks detailed commodity breakdowns. The cargo categories in the PDF are limited to broad groupings (Vehicles, General Merchandise, Shipping Devices) rather than the 42 SCTG2 commodity categories available in FAF.

To leverage the strengths of both data sources, we use the FAF model for commodity-level proportions while scaling the totals to match actual port throughput data. This approach:

1. Preserves the relative distribution of specific commodities from FAF (which SICT data cannot provide)
2. Calibrates total tonnage to match observed port throughput (which FAF underestimates)
3. Maintains consistency with the categorical breakdowns available in the SICT data

### 5.4 Classification Rules

The SICT analysis uses the following classification rules to map FAF commodity data to the categories available in the SICT wharfage reports:

**SICT-Type Classification:**
- **Vehicles**: SCTG2 commodities "Motorized vehicles" and "Transport equip."
- **Cargo Non Vehicles**: All other SCTG2 commodities

**Containerized Classification:**
- **Yes**: When `cargo_type` = "Containers"
- **No**: When `cargo_type` ≠ "Containers" (i.e., Break-Bulk, RO/RO, or Dry-Bulk)

### 5.5 Deliverable Output Sheets (3 sheets)

For final reporting, the script produces the `Honolulu_Piers` sheet plus two SICT output sheets in `FAF_Hawaii_Region_2024.xlsx` (other tabs are intermediate/QC outputs for internal review):

#### Honolulu_Piers

Pier-level distribution of water-based inbound freight into Honolulu Harbor, allocated from commodity totals using each pier’s cargo-type capacity proportions (Step 1). This sheet is also the source dataset used to filter and calibrate the SICT outputs.

**Columns:**
- `Pier`
- `SCTG2_Commodity`
- `cargo_type`
- `tons_2024`
- `current_value_2024`

#### SICT_Piers_FAF

Raw FAF model data filtered for SICT piers (Pier = "51, 52, 53"). Provides baseline for comparison and shows the original commodity distribution before calibration.

**Columns:**
- `Pier` - Always "51, 52, 53"
- `SCTG2_Commodity` - SCTG2 commodity description
- `cargo_type` - Cargo type category
- `tons_2024` - Original FAF tonnage
- `current_value_2024` - Original FAF value

#### SICT_Piers_byPortTons

FAF data scaled to match actual port shipment tonnage from the SICT wharfage data.

**Scaling Approach:**
1. Commodities are categorized as "Vehicles" or "Cargo Non Vehicles" based on SCTG2 commodity
2. Commodities are categorized as "Containerized" (Yes/No) based on cargo type
3. For each (SICT_Type, Containerized) group:
   - Calculate `tonnage_scale = target_tons / current_tons`
   - Apply the same scaling factor to both tonnage and dollar values
4. Preserves relative commodity proportions within each category

**Columns:**
- `Pier`, `SCTG2_Commodity`, `cargo_type`, `tons_2024`, `current_value_2024` (original values)
- `SICT_Type` - "Vehicles" or "Cargo Non Vehicles"
- `Containerized` - "Yes" or "No"
- `tonnage_scale` - Scaling factor applied
- `scaled_tons` - Tonnage after scaling
- `scaled_value` - Value after scaling (using same tonnage scale factor)

---

## Step 6: Results Analysis and Summary Statistics

### 6.1 Purpose

After generating the deliverable output sheets, a separate analysis script produces summary statistics and key findings to support reporting and presentation. This step quantifies SICT's role within Honolulu Harbor and identifies the most significant commodity flows.

### 6.2 Analysis Script

**Script File:** [`Script/analyze_SICT_results.py`](Script/analyze_SICT_results.py)

**Output File:** [`Processed_Data/SICT_Analysis_Results.xlsx`](Processed_Data/SICT_Analysis_Results.xlsx)

### 6.3 Analysis Components

The script performs three main analyses:

#### 6.3.1 Pier Capacity Proportions

**Output Sheet:** `Pier_Proportions`

Extracts and displays the pier capacity proportions from the Honolulu Harbor Pier Operations file (Step 1). This provides a reference for understanding how freight is distributed across piers based on their operational capacity.

**Columns:**
- `Pier` - Pier identification
- `Container Proportion` - Share of total container capacity
- `RO/RO Proportion` - Share of total RO/RO capacity
- `Break-Bulk Proportion` - Share of total break-bulk capacity
- `Liquid-Bulk Proportion` - Share of total liquid-bulk capacity
- `Dry-Bulk Proportion` - Share of total dry-bulk capacity

#### 6.3.2 SICT Share of Honolulu Harbor (Total)

**Output Sheet:** `SICT_Share_Total`

Calculates SICT's overall share of Honolulu Harbor freight flows by comparing total tonnage for SICT piers (51, 52, 53) against all Honolulu Harbor piers. The calculation is **scoped to only the cargo types that SICT actually handles** — Containers, RO/RO, and Break-Bulk — so that the comparison is like-for-like.

**Calculation:**
```python
# Filter Honolulu_Piers to only SICT cargo types (Containers, RO/RO, Break-Bulk)
df_scoped = df_honolulu_piers[cargo_type in {"Containers", "RO/RO", "Break-Bulk"}]

SICT_Share_Tons_Pct = (SICT_Total_Tons / Honolulu_Total_Tons) × 100   # both scoped
```

**Columns:**
- `Honolulu_Total_Tons` - Total tonnage for all Honolulu Harbor piers (scoped to SICT cargo types)
- `SICT_Total_Tons` - Total tonnage for SICT piers (51, 52, 53)
- `SICT_Share_Tons_Pct` - SICT's percentage share of total tonnage

**Use:** Provides a like-for-like summary of SICT's importance to Honolulu Harbor for the cargo types it serves.

#### 6.3.3 SICT Share by Commodity

**Output Sheet:** `SICT_Share_by_Commodity`

Breaks down SICT's share of Honolulu Harbor by individual SCTG2 commodity, showing which commodities are concentrated at SICT versus distributed across other piers.

**Calculation:**
```python
For each SCTG2_Commodity:
    SICT_Share_Tons_Pct = (SICT_Tons / Honolulu_Tons) × 100
```

**Columns:**
- `SCTG2_Commodity` - SCTG2 commodity description
- `Honolulu_Tons` - Total tonnage for this commodity across all Honolulu Harbor piers
- `SICT_Tons` - Tonnage for this commodity at SICT piers
- `SICT_Share_Tons_Pct` - SICT's percentage share of this commodity's tonnage

**Sorting:** Results are sorted by `SICT_Tons` in descending order to highlight the most significant commodities at SICT.

**Use:** Identifies which commodities are primarily handled at SICT (high share %) versus those distributed across multiple piers (low share %).

#### 6.3.4 Top Commodities Analysis (by Tonnage)

The script identifies the top 5 commodities by tonnage for two different data perspectives:

**A. FAF Model Estimates (Uncalibrated)**

**Output Sheet:** `TopCommodities_FAF_Tons` - Top 5 commodities by tonnage from `SICT_Piers_FAF` sheet

**Source:** `SICT_Piers_FAF` sheet (raw FAF model data before calibration)

**Columns:**
- `SCTG2_Commodity` - Commodity description
- `Tons` - Total tonnage for this commodity
- `Pct_of_Total` - Percentage of SICT total tonnage

**Use:** Shows the FAF model's original commodity distribution before scaling to actual port data.

**B. Scaled Model (Including All Cargo Types)**

**Output Sheet:** `TopCommodities_Scaled_Tons` - Top 5 commodities by tonnage from `SICT_Piers_byPortTons` sheet

**Source:** `SICT_Piers_byPortTons` sheet (calibrated to actual SICT wharfage data)

**Columns:**
- `SCTG2_Commodity` - Commodity description
- `Scaled_Tons` - Calibrated tonnage for this commodity
- `Pct_of_Total` - Percentage of SICT total tonnage

**Use:** Provides the primary commodity ranking after calibration to actual port throughput. This is the recommended dataset for reporting and analysis.

---