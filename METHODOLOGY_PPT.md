# Sand Island Container Terminal Freight Analysis

Estimating Commodity Flows for Transportation Planning

## Agenda

| Section | Topics |
|---------|--------|
| **Introduction** | Project purpose, data challenges |
| **Data Sources** | FAF 5.7.1, Harbor Master Plan, SICT Wharfage Data |
| **Methodology** | Steps 1-5: Data collection, mapping, processing, calibration |
| **Estimation Models** | Two model scenarios |
| **Results & Analysis** | Pier proportions, SICT share, top commodities by tonnage |
| **Conclusion** | Key takeaways, limitations & considerations |

## Introduction

### Project Purpose

- Estimate types and volumes of freight commodities arriving at Sand Island Container Terminal (SICT) via water for 2024
- Support transportation planning and infrastructure assessment for the Sand Island corridor
- All inbound cargo at SICT piers must exit via the Sand Island Access Road bridge
- Directly applicable to bridge traffic analysis

### Data Challenges

- **No SICT-specific data**: No publicly available dataset with detailed commodity breakdown for SICT
- **Regional FAF data**: Freight Analysis Framework(FAF) covers "Honolulu HI" region, not individual piers
- **Disaggregation needed**: Multiple sources used to estimate SICT's share of regional flows
- **Limited actual data**: SICT wharfage data provides totals but lacks commodity detail
- **Capacity as proxy for flow**: No actual commodity-by-pier data exists; pier capacity proportions from the Master Plan are used as a proxy for actual throughput distribution

## Data Sources

### Primary Data Inputs

| Source | Description | Use in Analysis |
|--------|-------------|-----------------|
| FAF 5.7.1 Regional | USDOT freight flow data by commodity | Commodity volumes & distributions |
| Honolulu Harbor 2050 Master Plan | HDOT pier capacity data | Pier-specific allocations |
| SICT Wharfage Data | Actual port throughput (FY2025) | Calibration of FAF estimates |

### Key Temporal Assumptions

- **FAF reference year**: Calendar year 2024 estimates
- **SICT wharfage period**: July 2024 - June 2025 (FY2025)
- **Assumption**: One-year wharfage data is representative of CY2024 volumes

## Methodology

### Methodology Overview

```
Step 1: Pier Operations Data    → Capacity proportions per pier
         ↓
Step 2: Cargo Type Definitions  → 5 categories (Container, RO/RO, Break-Bulk, Liquid-Bulk, Dry-Bulk)
         ↓
Step 3: Commodity Mapping       → 42 SCTG2 codes → Cargo types + containerization %
         ↓
Step 4: Automated Processing    → Filter FAF → Aggregate → Distribute to piers
         ↓
Step 5: SICT Calibration        → Scale FAF to actual port data → 2 output scenarios
```

### Step 1: Pier Operations Data Collection

- **Source:** Honolulu Harbor 2050 Master Plan (manual extraction)
- **Output:** Pier Operations and Cargo Inventory spreadsheet

| Data Extracted | Description |
|----------------|-------------|
| Pier identification | All piers in Honolulu Harbor |
| Container capacity (TEUs) | Annual container handling capacity |
| RO/RO capacity | Annual vehicle handling capacity |
| Break-Bulk capacity (Tons) | Annual break-bulk capacity |
| Liquid-Bulk capacity (Bbls) | Annual liquid-bulk capacity |
| Dry-Bulk capacity (Tons) | Annual dry-bulk capacity |

**Derived:** Pier proportions = Pier Capacity / Total Harbor Capacity

### Step 2: Cargo Type Definitions

Five cargo type categories defined from the Master Plan:

| Cargo Type | Description |
|------------|-------------|
| Containers | Standardized shipping containers (TEUs) |
| RO/RO | Roll-on/Roll-off vehicles and wheeled cargo |
| Break-Bulk | Non-containerized general cargo |
| Liquid-Bulk | Petroleum products, chemicals, liquids |
| Dry-Bulk | Coal, aggregates, grain, dry commodities |

### Step 3: Commodity Mapping (SCTG2 to Cargo Types)

- **Source:** Commodity Dictionary spreadsheet
- Mapped 42 SCTG2 commodity codes to cargo types
- Assigned containerization proportions for each commodity

| Handling Type | Container % | Example Commodities |
|---------------|-------------|---------------------|
| Fully Containerized | 100% | Manufactured goods, perishables |
| Fully Non-Containerized | 0% | Grains, aggregates, petroleum |
| Mixed-Mode | 10-90% | Milled grains (90% container, 10% bulk) |

### Step 4: Automated Processing

- Python script filters FAF data for Honolulu water-based inbound freight

**Filtering Logic:**

| Flow Type | Origin | Destination | Mode Filter |
|-----------|--------|-------------|-------------|
| Domestic Water | Other U.S. (not Honolulu) | Honolulu HI | dms_mode = Water |
| Import Direct | Foreign → Honolulu | Honolulu HI | fr_inmode = Water |
| Import Transshipped | Foreign → Other U.S. → Honolulu | Honolulu HI | dms_mode = Water |

**Processing Pipeline:**

1. Filter FAF for Honolulu water-based inbound freight (above logic)
2. Aggregate filtered data by SCTG2 commodity (sum tonnage and value)
3. Merge cargo type assignments from Commodity Dictionary (Step 3)
4. Distribute commodity totals to piers based on capacity proportions

### Step 4 (cont.): Distribution Logic

Three handling scenarios based on containerization proportion:

| Scenario | Container % | Distribution Method |
|----------|-------------|---------------------|
| Fully Containerized | 100% | All tonnage distributed by Container pier proportions |
| Fully Non-Containerized | 0% | All tonnage distributed by Bulk/Break-Bulk/RO-RO pier proportions |
| Mixed-Mode | 1-99% | Split: containerized share → Container proportions; remainder → Alternative type proportions |

**Example:** Milled grain prods. (10,000 tons, 70% containerized, Alternative = Dry-Bulk)

- 7,000 tons (70%) → distributed to piers by their Container proportions
- 3,000 tons (30%) → distributed to piers by their Dry-Bulk proportions

### Step 5: SICT Calibration

- FAF model estimated ~941,000 tons for SICT piers
- Actual port data showed ~4,084,000 tons inbound
- SICT piers do not handle Liquid-Bulk cargo (handled at other Sand Island facilities and Pier 30)
- **Solution**: Scale FAF data to match actual throughput while preserving commodity proportions

| Source | Total Tons | Notes |
|--------|------------|-------|
| FAF Model | ~941,000 | Excludes Liquid-Bulk (not handled at SICT) |
| Actual Port Data | 4,084,234 | Actual wharfage throughput |

### Step 5 (cont.): Classification Rules

FAF commodities are mapped to SICT wharfage categories using two dimensions:

| Dimension | Rule |
|-----------|------|
| **SICT-Type = "Vehicles"** | SCTG2 commodities: "Motorized vehicles" and "Transport equip." |
| **SICT-Type = "Cargo Non Vehicles"** | All other SCTG2 commodities |
| **Containerized = Yes** | When cargo_type = "Containers" |
| **Containerized = No** | When cargo_type ≠ "Containers" (Break-Bulk, RO/RO, Dry-Bulk) |

**Actual Port Data Breakdown (Scaling Targets):**

| SICT-Type | Containerized | Actual Port Tons |
|-----------|---------------|------------------|
| Cargo | Yes | 3,958,177 |
| Cargo | No | 8,130 |
| Vehicles | Yes | 27,184 |
| Vehicles | No | 90,742 |

### Step 5 (cont.): Scaling Formula

For each (SICT-Type, Containerized) group:

```
tonnage_scale = Actual Port Tons / FAF Model Tons
scaled_tons   = FAF_tons  × tonnage_scale
scaled_value  = FAF_value × tonnage_scale
```

- Same scale factor applied to both tonnage and value
- Preserves relative commodity proportions within each group

## Estimation Models

### Output Sheets in FAF_Hawaii_Region_2024.xlsx

| Sheet Name | Description |
|------------|-------------|
| Estimation Model 1: SICT_Piers_FAF | Original FAF estimates for SICT (baseline) |
| Estimation Model 2: SICT_Piers_byPortTons | Scaled to actual port tonnage |

**Note:** SICT piers do not handle Liquid-Bulk cargo. Liquid-Bulk operations (petroleum products, chemicals) are handled at other Sand Island facilities and Pier 30, and are typically transported via pipeline rather than by truck over the bridge.

## Results

### Pier Capacity Proportions

Honolulu Harbor pier capacity allocation by cargo type:

| Pier | Container | RO/RO | Break-Bulk | Liquid-Bulk | Dry-Bulk |
|------|-----------|-------|------------|-------------|----------|
| 1 (1A, 1B) | 5% | 24% | 16% | 0% | 0% |
| 2 (2A, 2B, 2C) | 0% | 0.5% | 0% | 0% | 0% |
| 19 & 20 | 0% | 9.5% | 0% | 0% | 0% |
| 29 | 5% | 0.5% | 18% | 0% | 0% |
| 30 | 0% | 0% | 0% | 58% | 0% |
| 31, 32, 33 | 0% | 44% | 0% | 0% | 0% |
| 34 | 0% | 0.5% | 0% | 0% | 0% |
| 39 & 40 | 13% | 8% | 56% | 0% | 0% |
| **51, 52, 53 (SICT)** | **77%** | **13%** | **10%** | **0%** | **0%** |
| 60 | 0% | 0% | 0% | 0% | 100% |
| **Other Piers Total** | **23%** | **87%** | **90%** | **100%** | **100%** |

**Key Insight:** SICT dominates container handling (77%). SICT piers do not handle Liquid-Bulk cargo; Liquid-Bulk operations are handled at other Sand Island facilities and Pier 30.

### SICT Share of Honolulu Harbor (FAF Model)

**Overall SICT Share (scoped to SICT cargo types: Containers, RO/RO, Break-Bulk):**

SICT only handles Containers, RO/RO (automobiles), and Break-Bulk cargo. The share calculation is scoped to these three cargo types for a like-for-like comparison, excluding Liquid-Bulk and Dry-Bulk which SICT does not handle.

| Metric | SICT | Honolulu Total | SICT Share |
|--------|------|----------------|------------|
| Tonnage | TBD | TBD | **TBD%** |
| Value | TBD | TBD | **TBD%** |

### Top Commodities: FAF Model (by Tonnage)

| Commodity | Tons | % of SICT |
|-----------|------|-----------|
| Gasoline | 340,379 | 36.2% |
| Crude petroleum | 252,024 | 26.8% |
| Fuel oils | 217,038 | 23.1% |
| Natural gas/fossil | 23,054 | 2.4% |
| Nonmetal min. prods. | 22,110 | 2.3% |

### Top Commodities: Scaled Model (by Tonnage)

**Key Insight:** After calibration, petroleum products (86% of FAF tonnage) are no longer dominant. Manufactured goods, mixed freight, and food products emerge as the top commodities — these are the goods most likely transported by truck over the Sand Island Access Road bridge.

| Commodity | Scaled Tons | % of SICT |
|-----------|-------------|-----------|
| Nonmetal min. prods. | 537,225 | 13.2% |
| Mixed freight | 499,603 | 12.2% |
| Paper articles | 393,651 | 9.6% |
| Articles-base metal | 314,447 | 7.7% |
| Milled grain prods. | 300,350 | 7.3% |

## Conclusion

### Key Takeaways

- Combined FAF regional data with actual port data for robust estimates
- Preserved FAF commodity detail while matching observed throughput
- Produced pier-level allocations based on operational capacity
- SICT piers do not handle Liquid-Bulk; petroleum transported via pipeline, not bridge
- **SICT handles a significant share of Honolulu Harbor's container, RO/RO, and break-bulk tonnage**
- After calibration, non-petroleum goods (mixed freight, food products, construction materials) dominate — directly relevant to bridge truck traffic

### Limitations & Considerations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| FAF underestimates SICT throughput (~941K vs ~4.1M tons) | Scaling factors are large | Calibrated with actual wharfage data |
| Temporal mismatch: FAF CY2024 vs. wharfage FY2025 | Minor seasonal variation possible | One full year assumed representative |
| Scaling assumes FAF commodity proportions hold at actual volumes | Commodity mix may differ | Best available approach given data constraints |

### Output Files

| File | Contents |
|------|----------|
| `FAF_Hawaii_Region_2024.xlsx` | 2 estimation model sheets (SICT_Piers_FAF, SICT_Piers_byPortTons) |
| `SICT_Analysis_Results.xlsx` | Summary statistics: pier proportions, SICT share, top commodities by tonnage |