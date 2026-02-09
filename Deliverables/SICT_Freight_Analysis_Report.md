# Sand Island Container Terminal (SICT) Freight Commodity Flow Analysis

## Methodology and Results Report

**Prepared for:** Hawaii Department of Transportation (HDOT)
**Project:** Freight and Statewide LRTP — Sand Island Corridor (Task 110)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Introduction](#2-introduction)
3. [Data Sources](#3-data-sources)
4. [Methodology](#4-methodology)
5. [Results](#5-results)
6. [Key Findings](#6-key-findings)
7. [Limitations and Considerations](#7-limitations-and-considerations)

---

## 1. Executive Summary

This report documents the methodology and results of a freight commodity flow analysis for the Sand Island Container Terminal (SICT) within Honolulu Harbor. The analysis estimates the types and volumes of freight commodities arriving at SICT (Piers 51, 52, and 53) via water for calendar year 2024 — freight that is subsequently transported off Sand Island via the Sand Island Access Road bridge.

Because no publicly available dataset provides commodity-level detail for SICT specifically, this study combines three data sources — the Freight Analysis Framework (FAF) version 5.7.1, the Honolulu Harbor 2050 Master Plan, and actual SICT wharfage records — to produce pier-level commodity flow estimates. Two estimation models are provided: a raw FAF-based model and a calibrated model scaled to actual port throughput.

**Key Findings:**

- **SICT handles approximately 61.6% of Honolulu Harbor's tonnage** (scoped to Container, RO/RO, and Break-Bulk cargo types).
- Based on wharfage data provided by the port authorities, SICT processes **4,084,234 tons** of inbound freight annually.
- The top five commodities by tonnage at SICT are: nonmetallic mineral products, mixed freight, paper articles, articles of base metal, and milled grain products.
- Construction materials, mixed freight, and processed goods dominate SICT cargo — these are the goods most likely transported by truck over the Sand Island Access Road bridge.

---

## 2. Introduction

### 2.1 Purpose

The primary goal of this analysis is to estimate the types and volumes of freight commodities that arrive at the Sand Island Container Terminal (SICT) via water for the year 2024, and are subsequently transported off the island via the Sand Island Access Road bridge. This information supports transportation planning and infrastructure assessment for the Sand Island corridor.

All inbound cargo at SICT piers must exit Sand Island via the bridge, making these estimates directly applicable to bridge traffic analysis.

### 2.2 Data Challenges

Estimating commodity-level freight flows at SICT presents several challenges:

1. **No publicly available SICT commodity data.** There is no publicly available dataset that provides a detailed breakdown of commodities flowing into the Sand Island Container Terminal specifically.

2. **FAF data covers broader geography.** The Freight Analysis Framework (FAF) provides commodity-level freight flow data, but only at the regional level for "Honolulu HI." SICT (Piers 51, 52, 53) is part of Honolulu Harbor, but FAF does not distinguish between individual piers or terminals within the region.

3. **Need to disaggregate regional data.** This study uses multiple data sources to estimate what portion of the FAF regional freight flows can be attributed specifically to SICT operations.

4. **Limited actual SICT data.** Wharfage data obtained directly from SICT officials provides a high-level overview of shipment inflows for FY2025 (July 2024 through June 2025). However, this data lacks the detailed commodity breakdown available in FAF and does not cover the full calendar year 2024.

5. **Capacity-based pier distribution.** No data source provides actual commodity flows by individual pier. This study uses pier-specific annual capacity data from the Honolulu Harbor 2050 Master Plan as a proxy for actual throughput. Each pier's share of total harbor capacity for a given cargo type is assumed to reflect its share of actual freight flows.

### 2.3 Temporal Assumptions

| Item | Period | Notes |
|------|--------|-------|
| FAF reference year | Calendar year 2024 | FAF 5.7.1 dataset |
| SICT wharfage data | July 1, 2024 – June 30, 2025 (FY2025) | One full year of actual data |
| Working assumption | FY2025 wharfage data is representative of CY2024 volumes | Enables direct comparison |

### 2.4 Analytical Approach

The study employs a multi-step approach:

1. Extract pier operational characteristics and capacity proportions from the Honolulu Harbor 2050 Master Plan.
2. Define five cargo type categories and map all 42 FAF commodity codes (SCTG2) to these categories.
3. Filter FAF data for water-based inbound freight to Honolulu Harbor and distribute to individual piers using capacity proportions.
4. Calibrate (scale) the FAF-based SICT estimates using actual wharfage data to match observed port throughput.
5. Produce summary statistics and commodity rankings.

---

## 3. Data Sources

| Source | Description | Use in Analysis |
|--------|-------------|-----------------|
| **FAF 5.7.1 Regional Data** (USDOT/BTS) | National freight flow database providing commodity-level tonnage and value estimates by origin, destination, and mode for 2024 | Source of commodity volumes and distributions for the Hawaii region |
| **Honolulu Harbor 2050 Master Plan** (HDOT Harbors Division) | Long-range harbor planning document with pier-level operational characteristics and annual throughput capacities by cargo type | Source of pier capacity proportions used to distribute regional freight to individual piers |
| **SICT Wharfage Data, FY2025** (HDOT Harbors Division) | Actual inbound/outbound cargo tonnage by category and shipping operator at SICT (July 2024 – June 2025) | Source of actual SICT throughput totals used to calibrate FAF model estimates |

---

## 4. Methodology

### Step 1: Pier Operations Data Collection

**Objective:** Extract per-pier capacity data from the Honolulu Harbor 2050 Master Plan and compute capacity proportions for distributing regional freight flows.

Pier operational data was manually extracted from the Honolulu Harbor 2050 Master Plan. The following information was collected for each pier in Honolulu Harbor:

| Data Collected | Description |
|----------------|-------------|
| Pier identification | All piers in Honolulu Harbor |
| Container capacity (TEUs) | Annual container handling capacity |
| RO/RO capacity | Annual vehicle handling capacity |
| Break-Bulk capacity (Tons) | Annual break-bulk capacity |
| Liquid-Bulk capacity (Bbls) | Annual liquid-bulk capacity |
| Dry-Bulk capacity (Tons) | Annual dry-bulk capacity |

For each cargo type, a pier proportion was calculated:

> **Pier Proportion = Pier Annual Capacity / Total Harbor Annual Capacity**

These proportions represent each pier's share of total harbor capacity and are the basis for distributing commodity-level tonnage to individual piers.

**Note:** The pier proportions were refined to reflect that SICT piers (51, 52, 53) do not handle Liquid-Bulk cargo in this model. Although SICT does receive some jet fuel, Liquid-Bulk is excluded from the estimation models; SICT is assumed to handle only Containers, RO/RO, and Break-Bulk cargo.

---

### Step 2: Cargo Type Definitions

**Objective:** Establish a standardized framework of five cargo type categories, derived from the Honolulu Harbor 2050 Master Plan.

| Cargo Type | Description |
|------------|-------------|
| **Containers** | Standardized shipping containers (TEUs) |
| **RO/RO** | Roll-on/Roll-off — vehicles and wheeled cargo |
| **Break-Bulk** | Non-containerized general cargo |
| **Liquid-Bulk** | Petroleum products, chemicals, and other liquids |
| **Dry-Bulk** | Coal, aggregates, grain, and other dry commodities |

These five categories define the cargo handling framework for the entire analysis. Each pier in Honolulu Harbor handles a subset of these cargo types, and each FAF commodity is mapped to one or more of these types.

---

### Step 3: Commodity-to-Cargo-Type Mapping

**Objective:** Map each of the 42 FAF commodity codes (SCTG2 — Standard Classification of Transported Goods) to the five cargo type categories, including provisions for mixed-mode handling.

Each SCTG2 commodity was assigned a primary cargo type, a containerization proportion (0% to 100%), and an alternative cargo type where applicable. This mapping enables the translation of FAF commodity data into the cargo type categories that correspond to pier operational characteristics.

#### Examples of Commodity Mapping

| Commodity | Primary Cargo Type | Container % | Alternative Type |
|-----------|--------------------|-------------|------------------|
| Meat/seafood | Containers | 95% | Break-Bulk |
| Cereal grains | Dry-Bulk | 5% | Containers |
| Motorized vehicles | RO/RO | 0% | — |
| Electronics | Containers | 100% | — |
| Gasoline | Liquid-Bulk | 0% | — |
| Milled grain products | Containers | 90% | Dry-Bulk |

#### Three Handling Categories

| Category | Container % | Logic |
|----------|-------------|-------|
| Fully Containerized | 100% | All tonnage distributed using Container pier proportions |
| Fully Non-Containerized | 0% | All tonnage distributed using Bulk/Break-Bulk/RO-RO pier proportions |
| Mixed-Mode | 1–99% | Tonnage split: containerized share via Container proportions; remainder via alternative type proportions |

---

### Step 4: Data Processing and Pier Distribution

**Objective:** Combine FAF regional freight data with pier operational characteristics to produce a pier-level distribution of commodity flows for Honolulu Harbor.

The processing workflow performs four major sub-steps:

#### 4.1 Load and Filter FAF Data

The FAF 5.7.1 regional dataset was loaded and filtered for Hawaii-related flows (Honolulu HI and Rest of HI FAF zones). FAF reports tonnage in thousands of tons and value in millions of dollars; these were converted to base units (tons and dollars) for analysis. Records with zero tonnage and zero value were removed.

#### 4.2 Filter for Honolulu Water-Based Inbound Freight

A critical filtering step isolates only water-based freight arriving at Honolulu Harbor. The filtering logic requires both conditions to be true:

1. **Destination must be Honolulu HI**
2. **Must be either a Domestic Water flow OR an Import Water flow**

| Flow Type | Criteria | Example |
|-----------|----------|---------|
| **Domestic Water** | Domestic trade, origin is not Honolulu, mode is Water | Freight shipped by water from Los Angeles to Honolulu |
| **Import (Direct)** | Import trade, arrives directly at Honolulu by water | Container ship from Japan directly to Honolulu Harbor |
| **Import (Transshipped)** | Import trade, enters U.S. elsewhere, then shipped to Honolulu by water | Goods imported through Los Angeles, then shipped by water to Honolulu |

This ensures the dataset captures all waterborne domestic freight, all international imports arriving directly by ship, and all international imports entering the U.S. elsewhere but subsequently shipped to Honolulu by water.

#### 4.3 Aggregate and Merge Commodity Data

The filtered data was aggregated by SCTG2 commodity, summing tonnage and value. The result was merged with the commodity-to-cargo-type mapping (Step 3) to assign each commodity its primary cargo type, containerization proportion, and alternative cargo type.

#### 4.4 Distribute to Piers

The commodity-level totals were distributed to individual piers using the capacity proportions from Step 1. The distribution handles three scenarios:

**Scenario 1 — Fully Containerized** (Container % = 100%):
All tonnage and value allocated using each pier's Container proportion.

**Scenario 2 — Fully Non-Containerized** (Container % = 0%):
All tonnage and value allocated using each pier's proportion for the applicable non-container cargo type (e.g., RO/RO, Break-Bulk, Dry-Bulk, or Liquid-Bulk).

**Scenario 3 — Mixed-Mode** (Container % between 1% and 99%):
- The containerized share is distributed using Container pier proportions.
- The remaining share is distributed using the alternative cargo type pier proportions.

**Example:** Meat/seafood (10,000 tons, 95% containerized, Alternative = Break-Bulk):
- 9,500 tons (95%) distributed by Container proportions
- 500 tons (5%) distributed by Break-Bulk proportions

---

### Step 5: SICT Calibration with Actual Port Data

**Objective:** Reconcile FAF model estimates with actual SICT wharfage data to produce calibrated commodity flow estimates for Piers 51, 52, and 53.

#### 5.1 The Calibration Challenge

Comparing FAF estimates for the SICT piers to actual port data revealed a significant discrepancy:

| Source | Total Inbound Tons |
|--------|-------------------|
| FAF Model (SICT piers) | ~132,000 |
| Actual SICT Wharfage Data | ~4,084,000 |

The actual port data provides reliable throughput totals but lacks detailed commodity breakdowns. The FAF model provides commodity-level proportions but significantly underestimates total throughput at the SICT level. The calibration approach preserves FAF's commodity distributions while scaling totals to match observed port data.

#### 5.2 Processing Actual SICT Wharfage Data

The raw wharfage data was classified along two dimensions — cargo type (Vehicles vs. Cargo Non Vehicles) and containerization status (Yes vs. No) — based on the cargo description codes in the wharfage reports:

| Description | SICT-Type | Containerized |
|-------------|-----------|---------------|
| Automobile in container or frame | Vehicles | Yes |
| Vehicles (ton) | Vehicles | No |
| Shipping Device Loaded (20ft, 40ft, 45ft) | Cargo Non Vehicles | Yes |
| General Merchandise (NOS) | Cargo Non Vehicles | No |
| Explosives (ton) | Cargo Non Vehicles | No |

**Resulting Summary (Inbound Tonnage — Scaling Targets):**

| SICT-Type | Containerized | Tons |
|-----------|---------------|------|
| Cargo Non Vehicles | Yes | 3,958,177 |
| Cargo Non Vehicles | No | 8,130 |
| Vehicles | No | 90,742 |
| Vehicles | Yes | 27,184 |
| **Total** | | **4,084,234** |

#### 5.3 Classification Rules for FAF-to-SICT Mapping

Each FAF commodity record was mapped to the SICT wharfage categories using the following rules:

| Dimension | Rule |
|-----------|------|
| **Vehicles** | SCTG2 commodities "Motorized vehicles" and "Transport equip." |
| **Cargo Non Vehicles** | All other SCTG2 commodities |
| **Containerized = Yes** | When the assigned cargo type is "Containers" |
| **Containerized = No** | When the assigned cargo type is not "Containers" (i.e., Break-Bulk, RO/RO, or Dry-Bulk) |

#### 5.4 Scaling Process

For each (SICT-Type, Containerized) group, a scaling factor was calculated:

> **Scaling Factor = Actual Port Tons / FAF Model Tons**

The same scaling factor was applied to both tonnage and dollar values. This approach:

1. **Preserves** the relative distribution of specific commodities from FAF
2. **Calibrates** total tonnage to match observed port throughput
3. **Maintains** consistency with the categorical breakdowns in the SICT wharfage data

---

### Step 6: Results Analysis and Summary Statistics

**Objective:** Produce summary statistics and key findings to support reporting and presentation.

The following analyses were performed using the calibrated output from Step 5:

- **Pier capacity proportions** — reference table showing how harbor capacity is distributed across piers
- **SICT share of Honolulu Harbor** — overall tonnage share, scoped to SICT cargo types (Containers, RO/RO, Break-Bulk)
- **SICT share by commodity** — per-commodity share showing which goods are concentrated at SICT
- **Top commodities** — ranked commodity lists by tonnage for both the FAF baseline and calibrated models

---

## 5. Results

### 5.1 Pier Capacity Proportions

The following table shows how Honolulu Harbor's operational capacity is distributed across piers by cargo type. These proportions are the basis for distributing FAF commodity flows to individual piers.

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

**Key Insight:** SICT dominates container handling at 77% of total harbor container capacity. It also handles 13% of RO/RO and 10% of Break-Bulk capacity. SICT receives no Liquid-Bulk or Dry-Bulk allocations in this model.

### 5.2 SICT Share of Honolulu Harbor

The share calculation is scoped to only the cargo types that SICT handles — Containers, RO/RO, and Break-Bulk — ensuring a like-for-like comparison.

| Metric | SICT (Piers 51, 52, 53) | Honolulu Harbor Total | SICT Share |
|--------|--------------------------|----------------------|------------|
| Tonnage (FAF Model) | 132,035 tons | 214,437 tons | **61.6%** |

SICT handles approximately 61.6% of Honolulu Harbor's total Container, RO/RO, and Break-Bulk tonnage.

### 5.3 Two Estimation Models

The analysis produces two model scenarios:

| Model | Description | Total SICT Tons |
|-------|-------------|-----------------|
| **Model 1: FAF Baseline** | Original FAF estimates for SICT piers | ~132,000 |
| **Model 2: Calibrated** | FAF estimates scaled to actual port tonnage | ~4,084,000 |

**Note:** Although SICT does receive jet fuel, Liquid-Bulk cargo is excluded from these models. For modeling purposes, SICT is assumed to handle only Containers, RO/RO, and Break-Bulk cargo. Liquid-Bulk operations (petroleum products, chemicals) are primarily handled at other Sand Island facilities and Pier 30, and are typically transported via pipeline rather than by truck over the bridge.

### 5.4 Top Commodities by Tonnage

#### FAF Baseline Model (Uncalibrated)

| Rank | Commodity | Tons | % of SICT Total |
|------|-----------|------|-----------------|
| 1 | Nonmetal min. prods. | 16,887 | 12.8% |
| 2 | Mixed freight | 15,704 | 11.9% |
| 3 | Paper articles | 12,458 | 9.4% |
| 4 | Articles-base metal | 10,205 | 7.7% |
| 5 | Milled grain prods. | 9,441 | 7.2% |

#### Calibrated Model (Scaled to Actual Port Data)

| Rank | Commodity | Scaled Tons | % of SICT Total |
|------|-----------|-------------|-----------------|
| 1 | Nonmetal min. prods. | 537,225 | 13.2% |
| 2 | Mixed freight | 499,603 | 12.2% |
| 3 | Paper articles | 394,087 | 9.6% |
| 4 | Articles-base metal | 316,099 | 7.7% |
| 5 | Milled grain prods. | 300,350 | 7.4% |

After calibration to actual port throughput (~4.1M tons vs. ~132K FAF estimate), the top commodities remain consistent with the FAF baseline. The relative proportions are preserved. Construction materials, mixed freight, and processed goods dominate SICT.

### 5.5 Actual SICT Wharfage Breakdown

| SICT-Type | Containerized | Actual Port Tons | Share of Total |
|-----------|---------------|------------------|----------------|
| Cargo Non Vehicles | Yes | 3,958,177 | 96.9% |
| Vehicles | No | 90,742 | 2.2% |
| Vehicles | Yes | 27,184 | 0.7% |
| Cargo Non Vehicles | No | 8,130 | 0.2% |
| **Total** | | **4,084,234** | **100%** |

The overwhelming majority of SICT freight (96.9%) consists of containerized non-vehicle cargo — general merchandise, consumer goods, construction materials, and processed foods shipped in standard containers.

---

## 6. Key Findings

1. **SICT is the dominant freight facility in Honolulu Harbor**, handling 61.6% of tonnage across the cargo types it serves (Containers, RO/RO, Break-Bulk).

2. **Container freight is the primary cargo mode at SICT**, accounting for 77% of the terminal's total handling capacity.

3. **Construction materials and mixed freight are the top commodities**, with nonmetallic mineral products (13.2%) and mixed freight (12.2%) together representing over a quarter of SICT tonnage.

4. **The FAF model significantly underestimates SICT throughput** (~132K vs. ~4.1M tons). The calibration step using actual wharfage data is essential for producing realistic volume estimates.

5. **Commodity proportions are stable across models** — the relative distribution of commodities is consistent between the uncalibrated FAF model and the calibrated model, providing confidence in the commodity mix even after scaling.

6. **All SICT inbound freight exits via the Sand Island Access Road bridge**, making these estimates directly applicable to bridge traffic and capacity analysis. Construction materials, mixed freight, and processed goods are the primary contributors to truck traffic on the bridge.

---

## 7. Limitations and Considerations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| FAF underestimates SICT throughput (~132K vs. ~4.1M tons) | Scaling factors are large | Calibrated with actual wharfage data; commodity proportions preserved |
| Temporal mismatch: FAF CY2024 vs. wharfage FY2025 | Minor seasonal variation possible | One full year of data assumed representative of calendar year |
| Pier capacity proportions used as a proxy for actual throughput | Actual utilization may differ from designed capacity | Best available approach given data constraints |
| SCTG2 commodity codes are broad categories | Some loss of specificity within categories | Provides useful aggregate-level analysis for planning |
| Explosives category in wharfage data has no direct FAF mapping | Minor misclassification | Included as general non-containerized cargo (~0.2% of total) |
| Liquid-Bulk excluded from SICT model | Jet fuel flows not captured | Jet fuel primarily moves via pipeline, not truck over the bridge |

---
