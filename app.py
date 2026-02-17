import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import warnings
from pathlib import Path
warnings.filterwarnings('ignore')

# ============================================================================
# ORIGINAL PROFESSIONAL COLOR PALETTE (from your screenshots)
# ============================================================================
COLOR_PALETTE = {
    'primary': '#1E3A8A',        # Navy Blue - Professional & Trustworthy
    'secondary': '#0EA5E9',      # Sky Blue - Modern & Energetic
    'accent': '#10B981',         # Emerald Green - Growth & Success
    'warning': '#F59E0B',        # Amber - Attention/Caution
    'danger': '#EF4444',         # Red - Decline/Alert
    'dark': '#111827',           # Dark Gray - Text (Light mode)
    'light': '#F8FAFC',          # Light Gray - Background
    'success': '#059669',        # Success Green
    'info': '#3B82F6',           # Info Blue
    'purple': '#8B5CF6',         # Royal Purple - Premium
    'pink': '#EC4899',           # Pink - Highlight
    'text_light': '#111827',     # Text for light mode
    'text_dark': '#FFFFFF',      # Text for dark mode
    'card_bg_light': '#FFFFFF',  # Card background light
    'card_bg_dark': '#1F2937',   # Card background dark
    'sidebar_bg': '#1E3A8A'      # Sidebar background
}

# Chart Color Sequences
CHART_COLORS = [
    '#1E3A8A',  # Navy
    '#0EA5E9',  # Sky Blue
    '#10B981',  # Emerald
    '#8B5CF6',  # Purple
    '#F59E0B',  # Amber
    '#EF4444',  # Red
    '#EC4899',  # Pink
    '#059669',  # Green
    '#3B82F6',  # Blue
    '#6366F1'   # Indigo
]

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Multi-Region Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# ============================================================================
# CUSTOM CSS (ORIGINAL PROFESSIONAL STYLE)
# ============================================================================
def load_original_css():
    # Determine dynamic colors based on mode
    if st.session_state.dark_mode:
        text_color = COLOR_PALETTE['text_dark']
        bg_color = '#0F172A'  # dark background
        card_bg = COLOR_PALETTE['card_bg_dark']
        border_color = '#374151'
    else:
        text_color = COLOR_PALETTE['text_light']
        bg_color = COLOR_PALETTE['light']
        card_bg = COLOR_PALETTE['card_bg_light']
        border_color = '#E5E7EB'

    sidebar_bg = COLOR_PALETTE['sidebar_bg']  # always navy

    st.markdown(f"""
    <style>
    /* Main styling */
    .main {{
        background-color: {bg_color};
    }}
    
    /* Dark/light mode text */
    .stApp {{
        color: {text_color};
    }}
    
    /* Custom metric cards */
    .metric-card {{
        background: {card_bg};
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-left: 4px solid {COLOR_PALETTE['primary']};
        color: {text_color};
        margin-bottom: 1rem;
    }}
    
    .metric-card h3 {{
        color: {'#9CA3AF' if st.session_state.dark_mode else '#6B7280'};
        font-size: 14px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .metric-card .value {{
        color: {text_color};
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 4px;
    }}
    
    .metric-card .change {{
        font-size: 14px;
        font-weight: 500;
    }}
    
    .change.positive {{
        color: {COLOR_PALETTE['success']};
    }}
    
    .change.negative {{
        color: {COLOR_PALETTE['danger']};
    }}
    
    .change.warning {{
        color: {COLOR_PALETTE['warning']};
    }}
    
    /* Header styling */
    .dashboard-title {{
        color: {COLOR_PALETTE['primary']};
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 10px;
    }}
    
    .dashboard-subtitle {{
        color: {'#D1D5DB' if st.session_state.dark_mode else '#6B7280'};
        font-size: 16px;
        margin-bottom: 30px;
    }}
    
    /* Chart containers */
    .chart-container {{
        background: {card_bg};
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        color: {text_color};
    }}
    
    .chart-container h3 {{
        color: {text_color};
    }}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: {'#374151' if st.session_state.dark_mode else '#E5E7EB'};
        color: {text_color};
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {COLOR_PALETTE['primary']} !important;
        color: white !important;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
    }}
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label {{
        color: white !important;
    }}
    
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stMultiselect,
    [data-testid="stSidebar"] .stDateInput {{
        background-color: white;
        border-radius: 6px;
    }}
    
    /* Button styling */
    .stButton button {{
        background-color: {COLOR_PALETTE['primary']};
        color: white;
        border-radius: 6px;
        font-weight: 600;
        border: none;
        padding: 8px 16px;
    }}
    
    .stButton button:hover {{
        background-color: #1D4ED8;
        color: white;
    }}
    
    /* Dataframe styling */
    .dataframe {{
        background-color: {card_bg};
        color: {text_color};
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    /* Footer styling */
    .footer-text {{
        color: {'#9CA3AF' if st.session_state.dark_mode else '#6B7280'};
        font-size: 14px;
    }}
    
    /* Plotly chart background */
    .js-plotly-plot .plotly .modebar {{
        background: transparent !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def format_currency(value):
    if value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value/1_000:.1f}K"
    else:
        return f"${value:,.0f}"

def get_chart_colors(n_colors):
    return CHART_COLORS[:min(n_colors, len(CHART_COLORS))]

def get_plotly_layout():
    """Return common layout settings for Plotly figures based on current mode"""
    if st.session_state.dark_mode:
        return dict(
            paper_bgcolor=COLOR_PALETTE['card_bg_dark'],
            plot_bgcolor=COLOR_PALETTE['card_bg_dark'],
            font=dict(color=COLOR_PALETTE['text_dark']),
            xaxis=dict(gridcolor='#374151'),
            yaxis=dict(gridcolor='#374151')
        )
    else:
        return dict(
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(color=COLOR_PALETTE['text_light']),
            xaxis=dict(gridcolor='#E5E7EB'),
            yaxis=dict(gridcolor='#E5E7EB')
        )

# ============================================================================
# SAMPLE DATA GENERATOR
# ============================================================================
def generate_sample_data():
    np.random.seed(42)
    n_rows = 5000
    
    dates = pd.date_range('2022-01-01', '2024-12-31', freq='D')
    regions = ['North America', 'Europe', 'Asia Pacific']
    countries = ['USA', 'Canada', 'UK', 'Germany', 'Japan', 'Australia']
    products = ['Laptop Pro', 'Smartphone X', 'Tablet Air', 'Monitor 4K', 'Wireless Headphones']
    categories = ['Electronics', 'Accessories', 'Furniture']
    channels = ['Online', 'Retail Store', 'Corporate']
    tiers = ['Platinum', 'Gold', 'Silver', 'Bronze']
    segments = ['Enterprise', 'Retail', 'SMB', 'Government']
    
    sales_data = {
        'OrderDate': np.random.choice(dates, n_rows),
        'Region': np.random.choice(regions, n_rows, p=[0.5, 0.3, 0.2]),
        'Country': np.random.choice(countries, n_rows),
        'ProductName': np.random.choice(products, n_rows),
        'Category': np.random.choice(categories, n_rows),
        'SalesChannel': np.random.choice(channels, n_rows, p=[0.5, 0.3, 0.2]),
        'Quantity': np.random.randint(1, 5, n_rows),
        'UnitPrice': np.random.uniform(50, 1000, n_rows),
        'ProfitMargin': np.random.uniform(0.2, 0.5, n_rows),
        'CustomerID': np.random.choice([f'C{str(i).zfill(4)}' for i in range(1, 101)], n_rows)
    }
    
    sales = pd.DataFrame(sales_data)
    sales['TotalSales'] = sales['Quantity'] * sales['UnitPrice']
    sales['Profit'] = sales['TotalSales'] * sales['ProfitMargin']
    sales['OrderDate'] = pd.to_datetime(sales['OrderDate'])
    sales['MonthYear'] = sales['OrderDate'].dt.to_period('M').astype(str)
    sales['Year'] = sales['OrderDate'].dt.year
    
    products_data = {
        'ProductID': [f'P{str(i).zfill(3)}' for i in range(1, 11)],
        'ProductName': products * 2,
        'Category': np.random.choice(categories, 10),
        'BasePrice': np.random.uniform(100, 1000, 10)
    }
    products = pd.DataFrame(products_data)
    
    customers_data = {
        'CustomerID': [f'C{str(i).zfill(4)}' for i in range(1, 101)],
        'Tier': np.random.choice(tiers, 100, p=[0.1, 0.2, 0.3, 0.4]),
        'Segment': np.random.choice(segments, 100, p=[0.2, 0.5, 0.25, 0.05]),
        'TotalPurchaseValue': np.random.uniform(1000, 50000, 100),
        'Region': np.random.choice(regions, 100, p=[0.5, 0.3, 0.2])
    }
    customers = pd.DataFrame(customers_data)
    
    regions_data = {
        'Region': regions,
        'ActualSales_2024': np.random.uniform(1000000, 5000000, 3),
        'Target_2024': np.random.uniform(1000000, 5000000, 3)
    }
    regions = pd.DataFrame(regions_data)
    
    return sales, products, customers, regions

# ============================================================================
# LOAD DATA (with corrected paths)
# ============================================================================
@st.cache_data
def load_data():
    try:
        possible_paths = [
            Path('/mount/src/Sales-Performance-Dashboard/sales_dashboard_data'),
            Path('sales_dashboard_data'),
            Path('./sales_dashboard_data'),
            Path('../sales_dashboard_data'),
            Path.cwd() / 'sales_dashboard_data',
        ]
        
        data_dir = None
        for path in possible_paths:
            if path.exists() and (path / 'sales_transactions.csv').exists():
                data_dir = path
                st.sidebar.success(f"✅ Data found at: {path}")
                break
        
        if data_dir is None:
            st.info("✨ Using sample data for demonstration")
            return generate_sample_data()
        
        sales = pd.read_csv(data_dir / 'sales_transactions.csv')
        products = pd.read_csv(data_dir / 'products.csv')
        customers = pd.read_csv(data_dir / 'customers.csv')
        regions = pd.read_csv(data_dir / 'regions.csv')
        
        sales['OrderDate'] = pd.to_datetime(sales['OrderDate'])
        sales['MonthYear'] = sales['OrderDate'].dt.to_period('M').astype(str)
        
        return sales, products, customers, regions
        
    except Exception as e:
        st.warning(f"Using sample data: {str(e)}")
        return generate_sample_data()

# ============================================================================
# TOGGLE DARK MODE
# ============================================================================
def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

# ============================================================================
# MAIN DASHBOARD
# ============================================================================
load_original_css()

# Header
st.markdown("<div class='dashboard-title'>🌐 Multi-Region Sales Performance Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='dashboard-subtitle'>Real-time insights across North America, Europe, and Asia Pacific markets</div>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h1 style='color: white; font-size: 24px;'>📊 Dashboard Controls</h1>", unsafe_allow_html=True)
    
    # Dark mode toggle
    col1, col2 = st.columns([3, 1])
    with col2:
        mode_label = "🌙 Dark" if not st.session_state.dark_mode else "☀️ Light"
        if st.button(mode_label, key="mode_toggle"):
            toggle_dark_mode()
            st.rerun()
    
    st.markdown("---")
    
    # Date Range
    st.markdown("### 📅 Date Range")
    min_date = pd.Timestamp('2022-01-01')
    max_date = pd.Timestamp('2024-12-31')
    date_range = st.date_input(
        "Select Date Range",
        value=(min_date.date(), max_date.date()),
        min_value=min_date.date(),
        max_value=max_date.date(),
        key="date_range"
    )
    
    # Region Filter
    st.markdown("### 🌍 Regions")
    region_options = ['All Regions', 'North America', 'Europe', 'Asia Pacific']
    selected_region = st.multiselect("Select Region(s)", region_options[1:], default=region_options[1:], key="region_filter")
    if not selected_region:
        selected_region = region_options[1:]
    
    # Category Filter
    st.markdown("### 📦 Categories")
    category_options = ['All Categories', 'Electronics', 'Furniture', 'Home Appliances', 'Accessories']
    selected_category = st.multiselect("Select Category(s)", category_options[1:], default=category_options[1:], key="category_filter")
    if not selected_category:
        selected_category = category_options[1:]
    
    # Customer Tier Filter
    st.markdown("### 👥 Customer Tier")
    tier_options = ['All Tiers', 'Platinum', 'Gold', 'Silver', 'Bronze']
    selected_tier = st.multiselect("Select Tier(s)", tier_options[1:], default=tier_options[1:], key="tier_filter")
    if not selected_tier:
        selected_tier = tier_options[1:]
    
    st.markdown("---")
    
    # Settings
    st.markdown("### ⚙️ Settings")
    margin_threshold = st.slider("Profit Margin Alert (%)", 0, 50, 20, key="margin_threshold")
    sales_target = st.number_input("Sales Target ($M)", min_value=1.0, max_value=100.0, value=10.0, step=0.5, key="sales_target")
    
    st.markdown("---")
    
    # Refresh & Reset
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    with col2:
        if st.button("📊 Reset", use_container_width=True):
            for key in ["region_filter", "category_filter", "tier_filter", "date_range"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# Load Data
sales, products, customers, regions = load_data()

if sales is not None:
    # Filter data
    sales_filtered = sales.copy()
    if len(date_range) == 2:
        mask = (sales_filtered['OrderDate'] >= pd.Timestamp(date_range[0])) & (sales_filtered['OrderDate'] <= pd.Timestamp(date_range[1]))
        sales_filtered = sales_filtered[mask]
    
    if 'All Regions' not in selected_region and len(selected_region) > 0:
        sales_filtered = sales_filtered[sales_filtered['Region'].isin(selected_region)]
    
    if 'All Categories' not in selected_category and len(selected_category) > 0:
        sales_filtered = sales_filtered[sales_filtered['Category'].isin(selected_category)]
    
    if 'All Tiers' not in selected_tier and len(selected_tier) > 0:
        if customers is not None and 'Tier' in customers.columns:
            customers_tier = customers[customers['Tier'].isin(selected_tier)]
            sales_filtered = sales_filtered[sales_filtered['CustomerID'].isin(customers_tier['CustomerID'])]
    
    # Calculate KPIs
    total_sales = sales_filtered['TotalSales'].sum()
    total_profit = sales_filtered['Profit'].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    avg_order_value = sales_filtered['TotalSales'].mean()
    customer_count = sales_filtered['CustomerID'].nunique()
    
    # Calculate growth
    if len(date_range) == 2:
        days_diff = (pd.Timestamp(date_range[1]) - pd.Timestamp(date_range[0])).days
        prev_start = pd.Timestamp(date_range[0]) - pd.Timedelta(days=days_diff)
        prev_end = pd.Timestamp(date_range[0]) - pd.Timedelta(days=1)
        prev_sales = sales[(sales['OrderDate'] >= prev_start) & (sales['OrderDate'] <= prev_end)]['TotalSales'].sum()
        sales_growth = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0
    else:
        sales_growth = 0
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        growth_icon = "📈" if sales_growth > 0 else "📉" if sales_growth < 0 else "➡️"
        growth_class = "positive" if sales_growth > 0 else "negative" if sales_growth < 0 else ""
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Sales</h3>
            <div class="value">{format_currency(total_sales)}</div>
            <div class="change {growth_class}">
                {growth_icon} {abs(sales_growth):.1f}% vs previous
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        margin_status = "positive" if profit_margin >= margin_threshold else "warning"
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Profit</h3>
            <div class="value">{format_currency(total_profit)}</div>
            <div class="change {margin_status}">
                {profit_margin:.1f}% Margin
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Avg Order Value</h3>
            <div class="value">{format_currency(avg_order_value)}</div>
            <div class="change">
                👥 {customer_count:,} Customers
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if regions is not None and 'ActualSales_2024' in regions.columns and 'Target_2024' in regions.columns:
            total_actual = regions['ActualSales_2024'].sum()
            total_target = regions['Target_2024'].sum()
            target_achievement = (total_actual / total_target * 100) if total_target > 0 else 0
        else:
            target_achievement = (total_sales / (sales_target * 1_000_000)) * 100
        
        achievement_class = "positive" if target_achievement >= 100 else "warning"
        achievement_icon = "🎯" if target_achievement >= 100 else "📉"
        st.markdown(f"""
        <div class="metric-card">
            <h3>Target Achievement</h3>
            <div class="value">{target_achievement:.1f}%</div>
            <div class="change {achievement_class}">
                {achievement_icon} {'Target Met' if target_achievement >= 100 else 'Below Target'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Sales Overview",
        "🌍 Regional Analysis",
        "📦 Product Performance",
        "👥 Customer Insights",
        "📊 Detailed Reports"
    ])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.subheader("Monthly Sales Trend")
            monthly = sales_filtered.set_index('OrderDate').resample('M').agg({
                'TotalSales': 'sum',
                'Profit': 'sum'
            }).reset_index()
            monthly['ProfitMargin'] = (monthly['Profit'] / monthly['TotalSales'] * 100)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=monthly['OrderDate'], y=monthly['TotalSales'],
                name='Sales', line=dict(color=COLOR_PALETTE['primary'], width=3),
                mode='lines+markers'
            ))
            fig.add_trace(go.Scatter(
                x=monthly['OrderDate'], y=monthly['ProfitMargin'],
                name='Profit Margin %', line=dict(color=COLOR_PALETTE['accent'], width=2, dash='dash'),
                yaxis='y2'
            ))
            layout = get_plotly_layout()
            fig.update_layout(
                xaxis_title="Month",
                yaxis_title="Sales ($)",
                yaxis2=dict(title="Profit Margin (%)", overlaying='y', side='right'),
                hovermode="x unified",
                height=400,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                **layout
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.subheader("Sales by Channel")
            channel_data = sales_filtered.groupby('SalesChannel')['TotalSales'].sum().reset_index()
            fig = px.bar(channel_data, x='SalesChannel', y='TotalSales',
                        color='SalesChannel', text=channel_data['TotalSales'].apply(lambda x: f"${x/1000:.0f}K"),
                        color_discrete_sequence=get_chart_colors(len(channel_data)))
            fig.update_traces(textposition='outside')
            layout = get_plotly_layout()
            fig.update_layout(showlegend=False, height=400, **layout)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.subheader("Regional Performance")
            region_summary = sales_filtered.groupby('Region').agg({
                'TotalSales': 'sum', 'Profit': 'sum', 'Quantity': 'sum'
            }).reset_index()
            fig = px.scatter(region_summary, x='TotalSales', y='Profit',
                            size='Quantity', color='Region',
                            hover_name='Region',
                            color_discrete_sequence=get_chart_colors(3),
                            height=400)
            layout = get_plotly_layout()
            fig.update_layout(**layout)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.subheader("Top Countries")
            country_data = sales_filtered.groupby('Country')['TotalSales'].sum().nlargest(10).reset_index()
            fig = px.bar(country_data, x='TotalSales', y='Country',
                        orientation='h', color='TotalSales',
                        color_continuous_scale='Viridis',
                        text=country_data['TotalSales'].apply(lambda x: f"${x/1000:.0f}K"))
            fig.update_traces(textposition='outside')
            layout = get_plotly_layout()
            fig.update_layout(height=400, **layout)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.subheader("Top 10 Products")
            product_data = sales_filtered.groupby('ProductName')['TotalSales'].sum().nlargest(10).reset_index()
            fig = px.bar(product_data, x='TotalSales', y='ProductName',
                        orientation='h', color='TotalSales',
                        color_continuous_scale='Viridis',
                        text=product_data['TotalSales'].apply(lambda x: f"${x/1000:.0f}K"))
            fig.update_traces(textposition='outside')
            layout = get_plotly_layout()
            fig.update_layout(height=400, **layout)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.subheader("Category Performance")
            category_data = sales_filtered.groupby('Category')['TotalSales'].sum().reset_index()
            fig = px.pie(category_data, values='TotalSales', names='Category',
                        hole=0.4, color_discrete_sequence=get_chart_colors(len(category_data)))
            fig.update_traces(textposition='inside', textinfo='percent+label')
            layout = get_plotly_layout()
            fig.update_layout(height=400, **layout)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4:
        if customers is not None and not customers.empty:
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.subheader("Customer Analysis")
            customer_analysis = sales_filtered.merge(
                customers[['CustomerID', 'Tier', 'Segment']], on='CustomerID', how='left'
            )
            col1, col2 = st.columns(2)
            with col1:
                segment_data = customer_analysis.groupby('Segment').agg({
                    'CustomerID': 'nunique'
                }).reset_index().rename(columns={'CustomerID': 'Count'})
                fig = px.pie(segment_data, values='Count', names='Segment',
                            title='Customer Distribution by Segment',
                            color_discrete_sequence=get_chart_colors(len(segment_data)))
                layout = get_plotly_layout()
                fig.update_layout(height=400, **layout)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                tier_data = customer_analysis.groupby('Tier').agg({
                    'TotalSales': 'sum'
                }).reset_index()
                fig = px.bar(tier_data, x='Tier', y='TotalSales',
                            color='Tier', text=tier_data['TotalSales'].apply(lambda x: f"${x/1e6:.1f}M"),
                            color_discrete_sequence=get_chart_colors(len(tier_data)))
                fig.update_traces(textposition='outside')
                layout = get_plotly_layout()
                fig.update_layout(height=400, showlegend=False, **layout)
                st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Customer data not available.")
    
    with tab5:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Detailed Sales Data")
        col1, col2, col3 = st.columns([2,1,1])
        with col2:
            if st.button("📥 Export CSV"):
                csv = sales_filtered.to_csv(index=False)
                st.download_button("Download CSV", csv, file_name=f"sales_{datetime.now():%Y%m%d_%H%M%S}.csv", mime="text/csv")
        with col3:
            if st.button("📊 Summary Stats"):
                with st.expander("Summary Statistics"):
                    st.dataframe(sales_filtered[['TotalSales','Profit','Quantity','ProfitMargin']].describe())
        st.markdown(f"**{len(sales_filtered):,} records**")
        search = st.text_input("🔍 Search")
        display = sales_filtered.copy()
        if search:
            mask = display.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)
            display = display[mask]
        st.dataframe(
            display.sort_values('OrderDate', ascending=False).head(100),
            use_container_width=True,
            column_config={
                "OrderDate": st.column_config.DateColumn("Date"),
                "TotalSales": st.column_config.NumberColumn("Sales", format="$%.2f"),
                "Profit": st.column_config.NumberColumn("Profit", format="$%.2f"),
                "ProfitMargin": st.column_config.NumberColumn("Margin %", format="%.1f%%")
            }
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**📈 Last Updated:** {datetime.now():%Y-%m-%d %H:%M}")
    with col2:
        unique_regions = sales_filtered['Region'].nunique()
        unique_countries = sales_filtered['Country'].nunique()
        st.markdown(f"**🌐 Data Coverage:** {unique_regions} Regions, {unique_countries} Countries, {len(sales_filtered):,} Transactions")
    with col3:
        mode_text = "🌙 Dark" if st.session_state.dark_mode else "☀️ Light"
        st.markdown(f"**📊 Dashboard Version:** 3.0 | Mode: {mode_text}")

else:
    st.error("❌ Failed to load data.")
