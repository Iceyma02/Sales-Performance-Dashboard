# 📊 Multi-Region Sales Performance Dashboard

## 🌟 Overview

A professional, enterprise-grade sales performance dashboard built with **Streamlit** for multi-region retail organizations. This interactive dashboard provides real-time insights across **North America, Europe, and Asia Pacific** markets with **150,000+ simulated transactions** spanning 2022-2024.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sales-performance-dashboard-6tncpbij7armwaqhzdbzdr.streamlit.app/)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red)
![License](https://img.shields.io/badge/License-Apache%202.0-green)

## ✨ Features

### 📊 **Dashboard Highlights**
- **Real-time Analytics**: Live insights across 3 continents
- **Multi-Region Coverage**: North America, Europe, Asia Pacific
- **150K+ Transactions**: Realistic synthetic data with business patterns
- **Interactive Visualizations**: Plotly charts with drill-down capabilities
- **Professional UI**: Business-grade color scheme and layout
- **Dark/Light Mode**: Toggle between themes for optimal viewing

### 📈 **Key Metrics Tracked**
- ✅ **Total Sales & Profit Margins** - Real-time financial performance
- ✅ **Regional Performance Comparison** - Cross-continent analysis
- ✅ **Product Category Analysis** - Identify top-performing products
- ✅ **Customer Segmentation & Lifetime Value** - Customer behavior insights
- ✅ **Target Achievement vs Actuals** - Performance against goals
- ✅ **Sales Channel Effectiveness** - Online vs Retail vs Corporate

### 🎨 **Design Features**
- **Professional Color Palette**: Navy blue & emerald green theme
- **Responsive Layout**: Works on desktop & mobile
- **Custom CSS Styling**: Professional business aesthetics
- **Interactive Filters**: Date range, region, category, customer tier
- **Export Capabilities**: CSV export for further analysis

## 📸 Dashboard Preview

| Sales Overview | Regional Analysis | Product Performance |
|----------------|-------------------|---------------------|
| ![Sales Overview](assets/01%20Sales%20Overview.png) | ![Regional Analysis](assets/02%20Regional%20Analysis.png) | ![Product Performance](assets/03%20Product%20Performance.png) |

| Customer Insights | Detailed Reports |
|-------------------|------------------|
| ![Customer Insights](assets/04%20Customer%20Insights.png) | ![Detailed Reports](assets/05%20Detailed%20Reports.png) |

## 🏗️ **Project Structure**

```
sales-performance-dashboard/
│
├── 📁 assets/                          # Dashboard screenshots
│   ├── 01 Sales Overview.png
│   ├── 02 Regional Analysis.png
│   ├── 03 Product Performance.png
│   ├── 04 Customer Insights.png
│   └── 05 Detailed Reports.png
│
├── 📁 sales_dashboard_data/            # Generated data files
│   ├── sales_transactions.csv          # 150K+ transactions
│   ├── products.csv                    # Product catalog
│   ├── customers.csv                   # Customer database
│   ├── regions.csv                     # Regional targets
│   ├── dates.csv                       # Date dimension
│   └── DATASET_SUMMARY.md             # Data documentation
│
├── app.py                             # Main Streamlit application
├── data_generation.py                 # Synthetic data generator
├── requirements.txt                   # Python dependencies
├── README.md                         # Project documentation
├── .gitignore                        # Git ignore file
└── LICENSE                           # Apache 2.0 License
```

## 🛠️ **Technology Stack**

| Technology | Purpose | Version |
|------------|---------|---------|
| **Streamlit** | Dashboard framework | 1.32.0 |
| **Pandas** | Data manipulation | 2.2.0 |
| **Plotly** | Interactive visualizations | 5.18.0 |
| **NumPy** | Numerical computations | 1.26.0 |
| **Plotly Express** | Quick chart generation | 0.4.1 |

## 🚀 **Quick Start**

### **1. Clone & Setup**
```bash
# Clone the repository
git clone https://github.com/Iceyma02/Sales-Performance-Dashboard.git
cd Sales-Performance-Dashboard

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Generate Data**
```bash
python data_generation.py
```

### **3. Run Dashboard**
```bash
streamlit run app.py
```

## 📊 **Data Model**

### **Core Tables:**
1. **Sales Transactions** (150,000+ records)
   - Transaction details with regional variations
   - Profit margins by product & region
   - Customer segmentation data
   - Sales channels: Online, Retail, Corporate, Distributor

2. **Products** (15 products)
   - Categories: Electronics, Furniture, Home Appliances, Accessories
   - Price ranges: Budget to Luxury ($39.99 - $1,299.99)
   - Trend indicators: Growing, Stable, Declining

3. **Customers** (1,000+ customers)
   - Segments: Enterprise, Retail, SMB, Government
   - Tiers: Bronze, Silver, Gold, Platinum
   - Purchase history and lifetime value

4. **Regions** (Multiple cities across 12 countries)
   - Sales targets 2022-2024
   - Actual vs Target comparisons
   - Economic indicators (GDP, Population)

## 🔧 **Features in Detail**

### **🎯 Interactive Filters**
- **Date Range**: 2022-01-01 to 2024-12-31
- **Region Filter**: North America, Europe, Asia Pacific
- **Category Filter**: Electronics, Furniture, Home Appliances, Accessories
- **Customer Tier**: Platinum, Gold, Silver, Bronze
- **Performance Settings**: Adjust margin thresholds and sales targets

### **📈 Visualizations**
1. **Sales Overview Tab**
   - Monthly sales trend with profit margin overlay
   - Sales channel performance analysis

2. **Regional Analysis Tab**
   - Bubble chart showing sales vs profit margin by country
   - Top 10 countries by sales

3. **Product Performance Tab**
   - Top 10 products by sales with profit margins
   - Category performance donut chart

4. **Customer Insights Tab**
   - Customer segment distribution
   - Sales by customer tier

5. **Detailed Reports Tab**
   - Interactive data table with search
   - Export to CSV functionality
   - Summary statistics

### **⚙️ Technical Features**
- **Data Caching**: `@st.cache_data` for performance optimization
- **Session State Management**: Persists user preferences
- **Error Handling**: Graceful degradation with user-friendly messages
- **Responsive Design**: Works on desktop and mobile
- **Dark/Light Mode**: Toggle between themes

## 🎯 **Business Insights Built-In**

### **1. Regional Trends**
- **North America**: Largest market (50% of sales), stable growth
- **Europe**: Competitive margins (avg 25%), slower growth
- **Asia Pacific**: High growth potential (15% YoY), expanding market

### **2. Product Performance**
- **Electronics**: Highest margin category (30-55%)
- **Accessories**: High volume, good margins
- **Furniture**: Declining trend, needs attention

### **3. Channel Analysis**
- **Online**: Fastest growing channel (45% of sales)
- **Retail**: Traditional, stable (30%)
- **Corporate**: Large orders, lower margins (15%)
- **Distributor**: Bulk sales (10%)

### **4. Customer Segmentation**
- **Enterprise**: High value, low frequency
- **Retail**: High volume, lower average order value
- **SMB**: Growing segment with good margins
- **Government**: Lowest volume, stable contracts

## 📱 **Deployment Options**

### **1. Local Development**
```bash
streamlit run app.py
```

### **2. Streamlit Cloud (Recommended)**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy with one click

### **3. Docker Deployment**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 📖 **Usage Guide**

### **For Business Users:**
1. **Start with Overview**: Check KPI metrics at the top
2. **Filter Data**: Use sidebar filters to drill down
3. **Explore Tabs**: Navigate through different analysis views
4. **Export Insights**: Download filtered data for reports
5. **Toggle Theme**: Switch between light/dark mode

### **For Developers:**
1. **Extend Features**: Add new tabs in the tab structure
2. **Customize Colors**: Modify `COLOR_PALETTE` in app.py
3. **Add Data Sources**: Modify `load_data()` function
4. **Deploy**: Follow deployment instructions above

## 🧪 **Testing**

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Generate coverage report
pytest --cov=app tests/
```

## 🤝 **Contributing**

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### **Areas for Contribution:**
- Add new visualizations
- Improve performance
- Add unit tests
- Enhance documentation
- Add more data sources

## 📄 **License**

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

```
Copyright 2026 Anesu Manjengwa

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## 👤 **Author**

**Anesu Manjengwa**

- 📧 Email: manjengwap10@gmail.com
- 🔗 LinkedIn: [linkedin.com/in/anesu-manjengwa-684766247](https://www.linkedin.com/in/anesu-manjengwa-684766247/)
- 🐙 GitHub: [github.com/Iceyma02](https://github.com/Iceyma02)

## 🙏 **Acknowledgments**

- Built with [Streamlit](https://streamlit.io/) - The fastest way to build data apps
- Charts by [Plotly](https://plotly.com/) - Interactive graphing library
- Icons from [Emoji](https://emojipedia.org/) - For visual indicators
- Color scheme inspired by modern business dashboards

## ⭐ **Support**

If you found this project helpful, please give it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=Iceyma02/Sales-Performance-Dashboard&type=Date)](https://star-history.com/#Iceyma02/Sales-Performance-Dashboard&Date)

## 🔗 **Related Projects**

- [Customer Churn Prediction Dashboard](https://github.com/yourusername/customer-churn-dashboard)
- [Inventory Management System](https://github.com/yourusername/inventory-dashboard)
- [Marketing Campaign Analytics](https://github.com/yourusername/marketing-analytics)

---

**⭐ Star this repo if you found it useful! Your support helps me create more open-source projects.**

---

*Last updated: January 2026 | Version: 3.0 | Built with ❤️ for the data community*
