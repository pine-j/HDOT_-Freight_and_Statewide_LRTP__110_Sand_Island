# Sand Island Container Terminal Freight Analysis

Estimating Commodity Flows for Transportation Planning

## Agenda

### Agenda

| Section | Topics |
|---------|--------|
| **Introduction** | Project purpose, data sources and challenges |
| **Methodology** | Steps 1-5: Data collection, mapping, processing, calibration |
| **Estimation Models** | Two model scenarios |
| **Results & Analysis** | Pier proportions, SICT share, top commodities by tonnage |
| **Conclusion** | Key takeaways, limitations & considerations |

## Introduction

### Project Purpose

- Estimate types and volumes of freight commodities arriving at Sand Island Container Terminal (SICT) via water for 2024
- Support transportation planning and infrastructure assessment for the Sand Island corridor
- Focus on freight commodities transported off Sand Island via the Sand Island Access Road bridge

### Data Sources

| Source | Description | Use in Analysis |
|--------|-------------|-----------------|
| FAF 5.7.1 Regional | USDOT freight flow data by commodity (mid-range estimates) | Commodity volumes & distributions |
| Honolulu Harbor 2050 Master Plan | HDOT pier capacity data | Pier-specific allocations |
| SICT Wharfage Data | Actual port throughput (FY2025) | Calibration of FAF estimates |

**Key Temporal Assumptions:**
- **FAF reference year**: Calendar year 2024 estimates
- **SICT wharfage period**: July 2024 - June 2025 (FY2025)
- **Assumption**: One-year wharfage data is representative of CY2024 volumes

### Data Challenges

- **No SICT-specific data**: No publicly available dataset with detailed commodity breakdown for SICT
- **Regional FAF data**: Freight Analysis Framework (FAF) covers "Honolulu HI" region, not individual piers
- **Disaggregation needed**: Multiple sources used to estimate SICT's share of regional flows
- **Limited actual data**: SICT wharfage data provides totals but lacks commodity detail
- **Capacity as proxy for flow**: No actual commodity-by-pier data exists; pier capacity proportions from the Master Plan are used as a proxy for actual throughput distribution


## Methodology

### Methodology Overview

| Step | Input | Output |
|------|-------|--------|
| **1. Pier Operations Data** | Honolulu Harbor 2050 Master Plan | Capacity proportions per pier + 5 cargo type categories |
| **2. Cargo Type Definitions** | Master Plan categories | 5 types: Container, RO/RO, Break-Bulk, Liquid-Bulk, Dry-Bulk |
| **3. Commodity Mapping** | 42 FAF commodity categories | Map each commodity to a Master Plan cargo type + containerization share |
| **4. Data Processing & Pier Distribution** | FAF 5.7.1 + Steps 1–3 | Filter → Aggregate → Distribute to piers |
| **5. SICT Calibration** | Actual port wharfage data | Scale FAF to match actuals → 2 output scenarios |

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

- **Derived:** Pier proportions = Pier Capacity / Total Harbor Capacity

### Step 2: Cargo Type Definitions

- Five cargo type categories defined from the Master Plan:

| Cargo Type | Description |
|------------|-------------|
| Containers | Standardized shipping containers (TEUs) |
| RO/RO | Roll-on/Roll-off vehicles and wheeled cargo |
| Break-Bulk | Non-containerized general cargo |
| Liquid-Bulk | Petroleum products, chemicals, liquids |
| Dry-Bulk | Coal, aggregates, grain, dry commodities |

### Step 3: Commodity Mapping (FAF Commodities to Cargo Types)

- Mapped all 42 FAF commodity categories to the five cargo types defined in the Master Plan
- Assigned containerization proportions for each commodity

| Handling Type | Container % | Example Commodities |
|---------------|-------------|---------------------|
| Fully Containerized | 100% | Manufactured goods, perishables |
| Fully Non-Containerized | 0% | Grains, aggregates, petroleum |
| Mixed-Mode | 10-90% | Milled grains (90% container, 10% bulk) |

### Step 4: Data Processing & Pier Distribution

- FAF data is filtered for Honolulu water-based inbound freight

**Filtering Logic:**

| Flow Type | Origin | Destination | Mode Filter |
|-----------|--------|-------------|-------------|
| Domestic Water | Other U.S. (not Honolulu) | Honolulu HI | Domestic shipping mode is Water |
| Import Direct | Foreign → Honolulu | Honolulu HI | Foreign inbound mode is Water |
| Import Transshipped | Foreign → Other U.S. → Honolulu | Honolulu HI | Domestic shipping mode is Water |

**Processing Pipeline:**

1. Filter FAF for Honolulu water-based inbound freight (above logic)
2. Aggregate filtered data by FAF commodity category (sum tonnage)
3. Merge cargo type assignments from Commodity Dictionary (Step 3)
4. Distribute commodity totals to piers based on capacity proportions

### Step 4 (cont.): Distribution Logic

- Three handling scenarios based on containerization proportion:

| Scenario | Container % | Distribution Method |
|----------|-------------|---------------------|
| Fully Containerized | 100% | All tonnage distributed by Container pier proportions |
| Fully Non-Containerized | 0% | All tonnage distributed by Bulk/Break-Bulk/RO-RO pier proportions |
| Mixed-Mode | 1-99% | Split: containerized share → Container proportions; remainder → Alternative type proportions |

**Example:** Meat/seafood (10,000 tons, 95% containerized, non-containerized portion handled as Break-Bulk)

- 9,500 tons (95%) → distributed to piers by their Container proportions
- 500 tons (5%) → distributed to piers by their Break-Bulk proportions

### Step 5: SICT Calibration

- FAF model estimated ~132,000 tons for SICT piers
- Actual port data showed ~4,084,000 tons inbound
**Solution**: Scale FAF data to match actual throughput while preserving commodity proportions

| Source | Total Tons | Notes |
|--------|------------|-------|
| FAF Model | ~132,000 | SICT receives 0% allocation for Liquid-Bulk and Dry-Bulk per pier capacity proportions |
| Actual Port Data | 4,084,234 | Actual wharfage throughput |

### Step 5 (cont.): Classification Rules

- FAF commodities are mapped to SICT wharfage categories using two dimensions:

| Dimension | Rule |
|-----------|------|
| **Classified as "Vehicles"** | FAF commodities categorized as "Motorized vehicles" or "Transport equipment" |
| **Classified as "Cargo (Non-Vehicles)"** | All remaining FAF commodities |
| **Containerized** | Cargo assigned to the Containers cargo type |
| **Not Containerized** | Cargo assigned to other cargo types (Break-Bulk, RO/RO, or Dry-Bulk) |

### Step 5 (cont.): Scaling to Actual Port Data

**Actual Port Data Breakdown (Scaling Targets):**

| Freight Category | Containerized? | Actual Port Tons |
|------------------|----------------|------------------|
| Cargo (Non-Vehicles) | Yes | 3,958,177 |
| Cargo (Non-Vehicles) | No | 8,130 |
| Vehicles | Yes | 27,184 |
| Vehicles | No | 90,742 |

**Scaling Formula** — For each freight category and containerization group:

- **Scaling Factor** = Actual Port Tons ÷ FAF Model Tons
- **Scaled Tons** = FAF Tons × Scaling Factor
- Preserves relative commodity proportions within each group

## Estimation Models

### Two Model Scenarios

| Model | Description |
|-------|-------------|
| **Model 1: FAF Baseline** | Original FAF estimates for SICT |
| **Model 2: Calibrated to Actuals** | FAF estimates scaled to actual port tonnage |

- **Note:** Although SICT does receive jet fuel, Liquid-Bulk cargo is excluded from our estimation models. For modeling purposes, SICT is assumed to handle only Containers, RO/RO, and Break-Bulk cargo. Liquid-Bulk operations (petroleum products, chemicals) are primarily handled at other Sand Island facilities and Pier 30, and are typically transported via pipeline rather than by truck over the bridge.

## Results

### Pier Capacity Proportions

- Honolulu Harbor pier capacity allocation by cargo type:

| Pier | Container | RO/RO | Break-Bulk | Liquid-Bulk | Dry-Bulk |
|------|-----------|-------|------------|-------------|----------|
| 1 (1A, 1B) | 5% | 24% | 16% | 0% | 0% |
| 2 (2A, 2B, 2C) | 0% | 1% | 0% | 0% | 0% |
| 19 & 20 | 0% | 10% | 0% | 0% | 0% |
| 29 | 5% | 1% | 18% | 0% | 0% |
| 30 | 0% | 0% | 0% | 100% | 0% |
| 31, 32, 33 | 0% | 44% | 0% | 0% | 0% |
| 34 | 0% | 1% | 0% | 0% | 0% |
| 39 & 40 | 13% | 8% | 56% | 0% | 0% |
| **51, 52, 53 (SICT)** | **77%** | **13%** | **10%** | **0%** | **0%** |
| 60 | 0% | 0% | 0% | 0% | 100% |

- **Key Insight:** SICT dominates container handling (77%).

### SICT Share of Honolulu Harbor (FAF Model)

**Overall SICT Share (scoped to SICT cargo types: Containers, RO/RO, Break-Bulk):**
- SICT handles Containers, RO/RO (vehicles and wheeled cargo), and Break-Bulk cargo. The share calculation is scoped to these three cargo types for a like-for-like comparison.

| Metric | SICT | Honolulu Total | SICT Share |
|--------|------|----------------|------------|
| Tonnage | 132,035 tons | 214,437 tons | **61.6%** |

### Top Commodities: FAF Model (by Tonnage)

| Commodity | Tons | % of SICT |
|-----------|------|-----------|
| Nonmetal min. prods. | 16,887 | 12.8% |
| Mixed freight | 15,704 | 11.9% |
| Paper articles | 12,458 | 9.4% |
| Articles-base metal | 10,205 | 7.7% |
| Milled grain prods. | 9,441 | 7.2% |

### Top Commodities: Scaled Model (by Tonnage)

- **Key Insight:** After calibration to actual port throughput (~4.1M tons vs. ~132K FAF estimate), the top commodities remain consistent with the FAF baseline. Construction materials, mixed freight, and processed goods dominate SICT — these are the goods most likely transported by truck over the Sand Island Access Road bridge.

| Commodity | Scaled Tons | % of SICT |
|-----------|-------------|-----------|
| Nonmetal min. prods. | 537,225 | 13.2% |
| Mixed freight | 499,603 | 12.2% |
| Paper articles | 394,087 | 9.6% |
| Articles-base metal | 316,099 | 7.7% |
| Milled grain prods. | 300,350 | 7.4% |

### Top Commodity Descriptions

**What do these commodities represent?**

| Commodity | Description |
|-----------|-------------|
| **Nonmetal min. prods.** | Hydraulic cements, ceramic products, glass products, abrasives, stone articles, asphalt roofing, and mineral wool |
| **Mixed freight** | Consolidated shipments containing multiple commodity types that cannot be classified under a single code |
| **Paper articles** | Toilet paper, tissues, towels, sanitary products, sacks and bags, packing containers, wallpaper, envelopes, stationery |
| **Articles-base metal** | Pipes, tubes, fittings, structures, hand tools, cutlery, hardware, industrial fasteners, and fabricated metal products |
| **Milled grain prods.** | Wheat flour, malt, milled rice, corn products, starches, pasta, breakfast cereals, mixes and doughs, baked goods |

### Actual SICT Wharfage Breakdown

| Freight Category | Containerized? | Actual Port Tons | Share of Total |
|------------------|----------------|------------------|----------------|
| Cargo (Non-Vehicles) | Yes | 3,958,177 | 96.9% |
| Vehicles | No | 90,742 | 2.2% |
| Vehicles | Yes | 27,184 | 0.7% |
| Cargo (Non-Vehicles) | No | 8,130 | 0.2% |
| **Total** | | **4,084,234** | **100%** |

- **Key Insight:** The overwhelming majority of SICT freight (96.9%) consists of containerized non-vehicle cargo.

## Conclusion

### Key Takeaways

- **SICT handles approximately 61.6% of Honolulu Harbor's tonnage** (scoped to Container, RO/RO, and Break-Bulk cargo types)
- **SICT dominates container handling in Honolulu Harbor**, accounting for 77% of the harbor's total container capacity
- Based on wharfage data provided by the port authorities, **SICT processes 4,084,234 tons of inbound freight annually**
- **Top five commodities by tonnage** at SICT are: nonmetallic mineral products, mixed freight, paper articles, articles of base metal, and milled grain products
- **96.9% of SICT freight consists of containerized non-vehicle cargo** — general merchandise, consumer goods, construction materials, and processed foods transported by truck over the Sand Island Access Road bridge

### Limitations & Considerations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| FAF underestimates SICT throughput (~132K vs ~4.1M tons) | Scaling factors are large | Calibrated with actual wharfage data |
| Temporal mismatch: FAF CY2024 vs. wharfage FY2025 | Minor seasonal variation possible | One full year assumed representative |
| Pier capacity proportions used as a proxy for actual throughput distribution | Actual utilization may differ from designed capacity | Best available approach given data constraints |