# Multi-Region Sales Dataset Summary

## Dataset Overview
- **Total Transactions**: 150,000
- **Time Period**: January 2022 - December 2024
- **Total Sales Value**: $114,108,129.57
- **Total Profit**: $54,262,016.35

## Business Insights Built-in

### 1. Regional Trends
- **North America**: Largest market, stable growth
- **Europe**: Competitive margins, slower growth
- **Asia Pacific**: High growth potential, expanding market

### 2. Product Performance
- **Electronics**: Highest margin category (30-55%)
- **Accessories**: High volume, good margins
- **Furniture**: Declining trend, needs attention

### 3. Channel Analysis
- **Online**: Fastest growing channel
- **Retail**: Traditional, stable
- **Corporate**: Large orders, lower margins

### 4. Customer Segmentation
- **Enterprise**: High value, low frequency
- **Retail**: High volume, lower average order value
- **SMB**: Growing segment

## Data Model for Power BI

### Table Relationships:
sales[ProductID] -> products[ProductID]
sales[CustomerID] -> customers[CustomerID]
sales[City] -> regions[City]
sales[OrderDate] -> dates[Date]

### Key Metrics to Build:
1. YTD Sales vs Target
2. Regional Profitability
3. Product Category Performance
4. Customer Lifetime Value
5. Sales Channel Growth
