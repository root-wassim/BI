# 🚀 Northwind Business Intelligence Solution

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Latest-green.svg)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-orange.svg)
![SQL Server](https://img.shields.io/badge/SQL%20Server-Compatible-red.svg)

A comprehensive end-to-end Business Intelligence solution for analyzing Northwind Traders' commercial performance through advanced ETL processing, dimensional modeling, and interactive visualizations.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Business Objectives](#-business-objectives)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Data Model](#-data-model)
- [Key Features](#-key-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Visualizations](#-visualizations)
- [Technical Stack](#-technical-stack)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

This project implements a complete Business Intelligence pipeline for **Northwind Traders**, a fictional company specializing in food product import/export. The solution addresses the challenge of analyzing business performance across heterogeneous data sources through:

- **Automated ETL Pipeline** built entirely in Python
- **Star Schema Data Warehouse** for optimized analytical queries
- **Interactive Dashboards** with 3D OLAP analysis
- **Real-time KPI tracking** for executive decision-making

### Problem Statement

Northwind operates with data spread across two incompatible systems:
- **SQL Server** (13 relational tables)
- **MS Access** (20 tables + 27 macros + 43 forms)

This fragmentation creates challenges in:
- Unified reporting across platforms
- Real-time performance monitoring
- Historical trend analysis
- Territory and employee performance tracking

---

## 🎯 Business Objectives

### Primary KPIs

The solution tracks and visualizes critical business metrics:

1. **Order Fulfillment Metrics**
   - Total orders delivered vs. pending
   - Delivery rate percentage by period
   - Trend analysis over time

2. **Revenue Analytics**
   - Total revenue by year, month, client, and employee
   - Revenue evolution trends
   - Comparative performance analysis

3. **Operational Efficiency**
   - Employee performance by delivery status
   - Client engagement patterns
   - Territory coverage analysis

### Analytical Dimensions

All metrics are segmented across three key axes:
- **📅 Temporal**: Year, Quarter, Month
- **👥 Customer**: ID, Company Name, City, Country
- **👤 Employee**: ID, Name, Title, Territory

---

## 🏗️ Architecture

### Four-Phase ETL Pipeline

```
┌─────────────────────────────────────────────────────────┐
│                    PHASE 1: EXTRACTION                  │
│  ┌──────────────┐              ┌──────────────┐        │
│  │ SQL Server   │              │ MS Access    │        │
│  │ (13 tables)  │              │ (20 tables)  │        │
│  └──────┬───────┘              └──────┬───────┘        │
│         │                             │                 │
│         └──────────┬──────────────────┘                 │
│                    ▼                                     │
│            data/raw/*.csv                                │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                PHASE 2: TRANSFORMATION                  │
│  • Schema harmonization                                 │
│  • Data quality checks                                  │
│  • Duplicate removal                                    │
│  • Business logic application                           │
│                    ▼                                     │
│            data/staging/*.csv                            │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  PHASE 3: LOADING                       │
│  • Dimension table creation                             │
│  • Fact table construction                              │
│  • Referential integrity validation                     │
│                    ▼                                     │
│       data/warehouse/*.parquet                           │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│               PHASE 4: VISUALIZATION                    │
│  • Interactive Jupyter Dashboards                       │
│  • 3D OLAP Analysis                                     │
│  • Real-time KPI Monitoring                             │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Northwind/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/              # Source data (CSV extracts)
│   ├── staging/          # Cleaned data
│   ├── warehouse/        # Final data warehouse (Parquet files)
│   ├── Northwind 2012.accdb
│   └── sqlserver.sql
│
├── scripts/              # ETL Pipeline
│   ├── config.py
│   ├── db_connector.py
│   ├── extract_data.py
│   ├── transform_data.py
│   ├── load_dwh.py
│   └── Main.py
│
├── notebooks/
│   └── dashboard_analysis.ipynb
│
├── reports/
│   └── rapport_BI.pdf
│
└── figures/              # Dashboard visualizations
    ├── 3D_OLAP_Analysis.png
    ├── Client_Delivery_Analysis.png
    ├── Delivery_Trend_Analysis.png
    ├── Employee_Logistics_Performance.png
    ├── Executive_Summary.png
    ├── Revenue_Evolution.png
    └── Territory_Distribution_by_Employee.png
```

---

## 🗃️ Data Model

### Star Schema Design

```
                    ┌─────────────────┐
                    │    DimDate      │
                    ├─────────────────┤
                    │ sk_date (PK)    │
                    │ full_date       │
                    │ year            │
                    │ month           │
                    │ month_name      │
                    │ quarter         │
                    └────────┬────────┘
                             │
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐   ┌───────▼────────┐   ┌──────▼──────────┐
│   DimClient    │   │   FactSales    │   │  DimEmployee    │
├────────────────┤   ├────────────────┤   ├─────────────────┤
│ sk_client (PK) │◄──┤ fact_id (PK)   │──►│sk_employee (PK) │
│ bk_customer_id │   ├────────────────┤   │ bk_employee_id  │
│ company_name   │   │ sk_date (FK)   │   │ Employee_name   │
│ city           │   │ sk_client (FK) │   │ title           │
│ country        │   │ sk_employee(FK)│   │ city            │
│ region         │   ├────────────────┤   │ country         │
└────────────────┘   │ bk_order_id    │   │ sales_region    │
                     │ quantity       │   │ territories     │
                     │ unit_price     │   └─────────────────┘
                     │ discount       │
                     │ total_amount   │
                     │ delivery_status│
                     └────────────────┘
```

### Dimension Details

#### DimDate
- **Purpose**: Temporal analysis backbone
- **Granularity**: Daily
- **Range**: 1996-2006 (actual data span)

#### DimClient
- **Purpose**: Customer segmentation
- **Attributes**: Geography, company profile
- **Enrichment**: Normalized city/country names

#### DimEmployee
- **Purpose**: Performance tracking
- **Enrichment**: Territory assignments, sales regions
- **Source Integration**: Combines employee + territory + region tables

#### FactSales
- **Purpose**: Transactional analysis
- **Grain**: Order line item
- **Measures**: Quantity, unit_price, discount, total_amount
- **Derived Metrics**: Revenue, delivery_status

---

## ✨ Key Features

### 1. Automated ETL Pipeline

- **Dual Source Extraction**: Seamlessly reads from SQL Server and MS Access
- **Smart Deduplication**: Merges data using composite primary keys
- **Error Handling**: Robust exception management with detailed logging
- **Format Flexibility**: Exports to CSV and Parquet for performance

### 2. Data Quality Management

- **Schema Validation**: Automatic column name normalization
- **Missing Value Handling**: Strategic imputation and flagging
- **Referential Integrity**: FK validation across dimensions
- **Duplicate Detection**: Multi-key deduplication logic

### 3. Advanced Analytics

#### 3D OLAP Cube Visualization
Interactive 3D scatter plot exploring:
- **X-axis**: Time (Year/Month)
- **Y-axis**: Clients
- **Z-axis**: Employees
- **Color/Size**: Revenue magnitude

#### Dynamic KPI Dashboard
- Real-time executive summary
- Year/month filtering
- Delivery status tracking
- Revenue trend analysis

#### Geospatial Analysis
- Territory coverage by employee
- Regional performance heatmaps
- Customer distribution mapping

---

## 🔧 Installation

### Prerequisites

- **Python**: 3.8 or higher
- **SQL Server**: 2012+ with Northwind database
- **MS Access Database Engine**: 2016 Redistributable
- **ODBC Driver**: 17 for SQL Server

### Step 1: Clone Repository

```bash
git clone https://github.com/root-wassim/BI
cd BI
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Database Connections

Edit `scripts/config.py`:

```python
# SQL Server Settings
SERVER_NAME = r'.\SQLEXPRESS'  # Your server instance
DATABASE_NAME = 'Northwind'
DRIVER = 'ODBC Driver 17 for SQL Server'

# Access Database
ACCESS_FILE_NAME = 'Northwind 2012.accdb'
```

### Step 5: Verify Data Files

Ensure the following files exist in `data/`:
- `Northwind 2012.accdb` (MS Access database)

---

## 🚀 Usage

### Complete ETL Execution

Run the full pipeline from extraction to warehouse loading:

```bash
cd scripts
python Main.py
```

**Expected Output:**
```
🚀 STARTING NORTHWIND ETL PIPELINE
✓ SQL Server: Orders -> sql_orders.csv (830 rows)
✓ Access: Orders -> access_orders.csv (830 rows)
✓ Creating DimDate... (2223 rows)
✓ Creating DimClient... (91 rows)
✓ Creating DimEmployee... (9 rows)
✓ Creating FactSales... (2155 rows)
✓ Load Complete! Data Warehouse is ready.
✅ ETL PIPELINE FINISHED in 12.34 seconds
```

### Individual Module Execution

#### Extract Only
```bash
python extract_data.py
```

#### Transform Only
```bash
python transform_data.py
```

#### Load Only
```bash
python load_dwh.py
```

### Interactive Dashboard

Launch Jupyter Notebook:

```bash
jupyter notebook notebooks/dashboard_analysis.ipynb
```

**Dashboard Features:**
- Year/Month filtering dropdowns
- Executive KPI summary cards
- Employee logistics performance bars
- Delivery trend area charts
- Client treemap analysis
- 3D OLAP scatter plot
- Territory sunburst diagram
- Revenue evolution line chart

---

## 📊 Visualizations

### 1. Executive Summary Dashboard

**Metrics Displayed:**
- 💰 Total Revenue: Real-time aggregation
- 📦 Total Orders: Count with delivery breakdown
- ✅ Delivered Orders: Count + percentage gauge
- ⏳ Pending Orders: Count + percentage gauge

### 2. Employee Performance Matrix

Horizontal stacked bar chart showing:
- Orders delivered (blue)
- Orders pending (red)
- Per-employee breakdown

### 3. Delivery Trend Analysis

Time-series area chart with:
- Complete timeline coverage (no gaps)
- Dual status tracking
- Smooth spline interpolation
- Interactive hover details

### 4. Client Delivery Treemap

Hierarchical visualization:
- Level 1: Company name
- Level 2: Delivery status
- Size: Order count
- Color: Status indicator

### 5. 3D OLAP Cube

Interactive scatter plot:
- **Sales markers**: Sized by revenue, colored by intensity
- **Gap markers**: Light grey dots showing zero-revenue combinations
- **Rotation/Zoom**: Full 3D interaction
- **Hover details**: Complete dimensional context

### 6. Territory Distribution

Sunburst diagram showing:
- Inner ring: Employee names
- Outer ring: Assigned territories
- Color-coded by employee
- Click-to-zoom interaction

### 7. Revenue Evolution

Dual-layer chart combining:
- Bar chart: Period-by-period values
- Line overlay: Trend visualization
- Average baseline: Dotted reference line
- Adaptive time axis (yearly/monthly)

---

## 🛠️ Technical Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.8+ | Primary development language |
| **Data Processing** | Pandas, NumPy | ETL transformations |
| **Database** | SQL Server, MS Access | Source systems |
| **Connectivity** | SQLAlchemy, PyODBC | Database adapters |
| **Storage** | Parquet, CSV | Warehouse formats |
| **Visualization** | Plotly, Matplotlib | Interactive charts |
| **Notebooks** | Jupyter | Analysis environment |
| **Geospatial** | GeoPandas | Geographic analysis |

### Libraries

```
pandas==2.0.0
numpy==1.24.0
sqlalchemy==2.0.0
pyodbc==4.0.39
matplotlib==3.7.0
plotly==5.14.0
geopandas==0.13.0
jupyter==1.0.0
seaborn==0.12.0
openpyxl==3.1.0
access-parser==0.0.2
```

---

## 📈 Performance Considerations

### Data Volume Handling

- **Parquet Format**: 60% size reduction vs. CSV
- **Chunked Processing**: Large table support
- **Indexed Dimensions**: Fast FK lookups
- **Incremental Loads**: Delta processing capability

### Query Optimization

- **Star Schema**: Optimized for analytical queries
- **Denormalized Facts**: Reduced join complexity
- **Pre-aggregated Metrics**: Calculated during ETL
- **Date Dimension**: Eliminates date calculations

---


