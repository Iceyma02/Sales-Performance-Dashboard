import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
from pathlib import Path
warnings.filterwarnings('ignore')

# ============================================================================
# PREMIUM COLOR PALETTE - Financial/Banking Grade
# ============================================================================
COLOR_PALETTE = {
    # Primary Colors
    'primary': '#0A1E3C',        # Deep Navy - Trust, Stability
    'primary_light': '#1E3A5F',   # Medium Navy
    'primary_dark': '#051024',    # Dark Navy
    
    # Accent Colors
    'accent_1': '#00A67E',        # Emerald - Growth, Success
    'accent_2': '#3182CE',        # Royal Blue - Trust, Technology
    'accent_3': '#805AD5',        # Purple - Premium, Luxury
    'accent_4': '#DD6B20',        # Orange - Warning, Attention
    'accent_5': '#E53E3E',        # Red - Alert, Decline
    
    # Neutral Colors
    'gray_50': '#F7FAFC',         # Lightest Gray - Background Light
    'gray_100': '#EDF2F7',        # Light Gray
    'gray_200': '#E2E8F0',        # Medium Light Gray
    'gray_300': '#CBD5E0',        # Medium Gray
    'gray_400': '#A0AEC0',        # Medium Dark Gray
    'gray_500': '#718096',        # Dark Gray
    'gray_600': '#4A5568',        # Darker Gray
    'gray_700': '#2D3748',        # Almost Black
    'gray_800': '#1A202C',        # Very Dark Gray
    'gray_900': '#171923',        # Black Gray
    
    # Semantic Colors
    'success': '#00A67E',
    'success_light': '#C6F6D5',
    'warning': '#DD6B20',
    'warning_light': '#FEEBC8',
    'danger': '#E53E3E',
    'danger_light': '#FED7D7',
    'info': '#3182CE',
    'info_light': '#BEE3F8',
    
    # Text Colors
    'text_primary': '#1A202C',     # Primary text - Light mode
    'text_secondary': '#4A5568',   # Secondary text - Light mode
    'text_tertiary': '#718096',    # Tertiary text - Light mode
    'text_inverse': '#FFFFFF',      # Inverse text - Dark mode
    'text_inverse_secondary': '#CBD5E0',  # Secondary inverse - Dark mode
    
    # Background Colors
    'bg_primary': '#FFFFFF',        # Primary background - Light
    'bg_secondary': '#F7FAFC',      # Secondary background - Light
    'bg_tertiary': '#EDF2F7',       # Tertiary background - Light
    'bg_inverse': '#0A1E3C',        # Inverse background - Dark
    'bg_inverse_secondary': '#1E3A5F',  # Secondary inverse - Dark
    'bg_card': '#FFFFFF',           # Card background - Light
    'bg_card_inverse': '#1A202C',   # Card background - Dark
    
    # Border Colors
    'border_light': '#E2E8F0',
    'border_dark': '#2D3748',
    
    # Chart Colors - Professional Sequence
    'chart_1': '#0A1E3C',  # Navy
    'chart_2': '#00A67E',  # Emerald
    'chart_3': '#3182CE',  # Blue
    'chart_4': '#805AD5',  # Purple
    'chart_5': '#DD6B20',  # Orange
    'chart_6': '#E53E3E',  # Red
    'chart_7': '#38B2AC',  # Teal
    'chart_8': '#D53F8C',  # Pink
}

# Chart Colors List
CHART_COLORS = [
    COLOR_PALETTE['chart_1'],
    COLOR_PALETTE['chart_2'],
    COLOR_PALETTE['chart_3'],
    COLOR_PALETTE['chart_4'],
    COLOR_PALETTE['chart_5'],
    COLOR_PALETTE['chart_6'],
    COLOR_PALETTE['chart_7'],
    COLOR_PALETTE['chart_8'],
]

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Multi-Region Sales Intelligence",
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
# PREMIUM CSS STYLING
# ============================================================================
def load_premium_css():
    """Load premium CSS with perfect dark/light mode support"""
    
    # Dynamic colors based on mode
    if st.session_state.dark_mode:
        bg_main = COLOR_PALETTE['bg_inverse']
        bg_card = COLOR_PALETTE['bg_card_inverse']
        text_primary = COLOR_PALETTE['text_inverse']
        text_secondary = COLOR_PALETTE['text_inverse_secondary']
        border_color = COLOR_PALETTE['border_dark']
        hover_bg = COLOR_PALETTE['primary_light']
    else:
        bg_main = COLOR_PALETTE['bg_secondary']
        bg_card = COLOR_PALETTE['bg_card']
        text_primary = COLOR_PALETTE['text_primary']
        text_secondary = COLOR_PALETTE['text_secondary']
        border_color = COLOR_PALETTE['border_light']
        hover_bg = COLOR_PALETTE['gray_100']
    
    st.markdown(f"""
    <style>
        /* ===== GLOBAL STYLES ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        * {{
            font-family: 'Inter', sans-serif;
        }}
        
        .stApp {{
            background-color: {bg_main};
        }}
        
        /* ===== TYPOGRAPHY ===== */
        h1, h2, h3, h4, h5, h6, p, span, div, label {{
            color: {text_primary} !important;
        }}
        
        .text-secondary {{
            color: {text_secondary} !important;
            font-size: 0.875rem;
            font-weight: 400;
        }}
        
        /* ===== HEADER SECTION ===== */
        .premium-header {{
            background: linear-gradient(135deg, {COLOR_PALETTE['primary']} 0%, {COLOR_PALETTE['primary_light']} 100%);
            padding: 2rem 2rem;
            border-radius: 0 0 20px 20px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px -10px rgba(0,0,0,0.2);
        }}
        
        .premium-title {{
            font-size: 2.5rem;
            font-weight: 800;
            color: white !important;
            margin: 0;
            line-height: 1.2;
        }}
        
        .premium-subtitle {{
            font-size: 1rem;
            color: rgba(255,255,255,0.8) !important;
            margin-top: 0.5rem;
        }}
        
        /* ===== KPI CARDS ===== */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .kpi-card {{
            background: {bg_card};
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            border: 1px solid {border_color};
            transition: all 0.3s ease;
        }}
        
        .kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
            border-color: {COLOR_PALETTE['accent_2']};
        }}
        
        .kpi-label {{
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: {text_secondary} !important;
            margin-bottom: 0.5rem;
        }}
        
        .kpi-value {{
            font-size: 2rem;
            font-weight: 700;
            color: {text_primary} !important;
            line-height: 1.2;
            margin-bottom: 0.25rem;
        }}
        
        .kpi-change {{
            font-size: 0.875rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }}
        
        .kpi-change.positive {{
            color: {COLOR_PALETTE['success']} !important;
        }}
        
        .kpi-change.negative {{
            color: {COLOR_PALETTE['danger']} !important;
        }}
        
        .kpi-change.warning {{
            color: {COLOR_PALETTE['warning']} !important;
        }}
        
        /* ===== CHART CONTAINERS ===== */
        .chart-card {{
            background: {bg_card};
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            border: 1px solid {border_color};
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        }}
        
        .chart-card:hover {{
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        }}
        
        .chart-title {{
            font-size: 1.125rem;
            font-weight: 600;
            color: {text_primary} !important;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid {border_color};
        }}
        
        /* ===== SIDEBAR STYLING ===== */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {COLOR_PALETTE['primary']} 0%, {COLOR_PALETTE['primary_dark']} 100%);
            padding: 2rem 1rem;
        }}
        
        [data-testid="stSidebar"] .sidebar-header {{
            color: white !important;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }}
        
        [data-testid="stSidebar"] .stMarkdown h3 {{
            color: rgba(255,255,255,0.7) !important;
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }}
        
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stMultiselect label,
        [data-testid="stSidebar"] .stDateInput label {{
            color: white !important;
            font-weight: 500;
        }}
        
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"],
        [data-testid="stSidebar"] .stMultiselect div[data-baseweb="select"],
        [data-testid="stSidebar"] .stDateInput input {{
            background-color: rgba(255,255,255,0.1) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            color: white !important;
            border-radius: 8px;
        }}
        
        [data-testid="stSidebar"] .stSelectbox:hover div[data-baseweb="select"],
        [data-testid="stSidebar"] .stMultiselect:hover div[data-baseweb="select"],
        [data-testid="stSidebar"] .stDateInput:hover input {{
            border-color: {COLOR_PALETTE['accent_2']} !important;
            background-color: rgba(255,255,255,0.15) !important;
        }}
        
        /* ===== BUTTON STYLING ===== */
        .stButton button {{
            background: linear-gradient(135deg, {COLOR_PALETTE['accent_2']} 0%, {COLOR_PALETTE['primary_light']} 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
            border: 1px solid transparent;
        }}
        
        .stButton button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(49,130,206,0.3);
            border-color: white;
        }}
        
        /* ===== TAB STYLING ===== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.5rem;
            background-color: transparent;
            border-bottom: 2px solid {border_color};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: transparent;
            border-radius: 8px 8px 0 0;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            color: {text_secondary} !important;
            transition: all 0.3s ease;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            background-color: {hover_bg};
            color: {COLOR_PALETTE['accent_2']} !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {COLOR_PALETTE['accent_2']} 0%, {COLOR_PALETTE['primary_light']} 100%) !important;
            color: white !important;
            font-weight: 600;
        }}
        
        /* ===== DATAFRAME STYLING ===== */
        .dataframe {{
            background-color: {bg_card};
            border-radius: 12px;
            border: 1px solid {border_color};
            overflow: hidden;
        }}
        
        /* ===== FOOTER STYLING ===== */
        .premium-footer {{
            margin-top: 3rem;
            padding: 1.5rem 0;
            border-top: 1px solid {border_color};
            color: {text_secondary} !important;
            font-size: 0.875rem;
        }}
        
        /* ===== TOOLTIPS ===== */
        .tooltip {{
            position: relative;
            display: inline-block;
        }}
        
        .tooltip .tooltiptext {{
            visibility: hidden;
            background-color: {bg_card};
            color: {text_primary};
            text-align: center;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            position: absolute;
            z-index: 1000;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            opacity: 0;
            transition: opacity 0.3s;
            border: 1px solid {border_color};
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            font-size: 0.875rem;
            white-space: nowrap;
        }}
        
        .tooltip:hover .tooltiptext {{
            visibility: visible;
            opacity: 1;
        }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def format_currency(value):
    """Professional currency formatting"""
    if value >= 1_000_000_000:
        return f"${value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value/1_000:.1f}K"
    else:
        return f"${value:,.0f}"

def format_percentage(value):
    """Format percentage with 1 decimal"""
    return f"{value:.1f}%"

def get_chart_colors(n_colors):
    """Get professional chart colors"""
    return CHART_COLORS[:min(n_colors, len(CHART_COLORS))]

# ============================================================================
# SAMPLE DATA GENERATOR
# ============================================================================
def generate_sample_data():
    """Generate premium sample data"""
    np.random.seed(42)
    n_rows = 10000
    
    dates = pd.date_range('2022-01-01', '2024-12-31', freq='D')
    regions = ['North America', 'Europe', 'Asia Pacific']
    countries = {
        'North America': ['USA', 'Canada', 'Mexico'],
        'Europe': ['UK', 'Germany', 'France', 'Italy', 'Spain'],
        'Asia Pacific': ['Japan', 'Australia', 'Singapore', 'China', 'South Korea']
    }
    products = {
        'Electronics': ['MacBook Pro', 'iPhone 15', 'iPad Air', 'AirPods Max', 'Apple Watch'],
        'Accessories': ['Magic Keyboard', 'Magic Mouse', 'USB-C Cable', 'Adapter', 'Case'],
        'Furniture': ['Standing Desk', 'Ergo Chair', 'Monitor Stand', 'Desk Lamp', 'Bookshelf']
    }
    channels = ['Online Store', 'Retail Store', 'Corporate Sales', 'Partner Network']
    
    # Flatten products
    all_products = []
    for cat, prods in products.items():
        all_products.extend(prods)
    
    data = []
    for _ in range(n_rows):
        region = np.random.choice(regions, p=[0.45, 0.30, 0.25])
        country = np.random.choice(countries[region])
        category = np.random.choice(list(products.keys()), p=[0.5, 0.3, 0.2])
        product = np.random.choice(products[category])
        channel = np.random.choice(channels, p=[0.4, 0.3, 0.2, 0.1])
        date = np.random.choice(dates)
        
        # Realistic pricing
        if category == 'Electronics':
            unit_price = np.random.uniform(299, 1999)
            margin = np.random.uniform(0.25, 0.45)
        elif category == 'Accessories':
            unit_price = np.random.uniform(29, 199)
            margin = np.random.uniform(0.35, 0.55)
        else:  # Furniture
            unit_price = np.random.uniform(199, 899)
            margin = np.random.uniform(0.30, 0.50)
        
        quantity = np.random.poisson(2) + 1
        quantity = min(quantity, 10)
        
        total_sales = quantity * unit_price
        profit = total_sales * margin
        
        data.append({
            'OrderDate': date,
            'Region': region,
            'Country': country,
            'ProductName': product,
            'Category': category,
            'SalesChannel': channel,
            'Quantity': quantity,
            'UnitPrice': round(unit_price, 2),
            'TotalSales': round(total_sales, 2),
            'Profit': round(profit, 2),
            'ProfitMargin': round(margin * 100, 1),
            'CustomerID': f'C{np.random.randint(1000, 9999)}'
        })
    
    sales = pd.DataFrame(data)
    sales['MonthYear'] = sales['OrderDate'].dt.to_period('M').astype(str)
    sales['Year'] = sales['OrderDate'].dt.year
    sales['Quarter'] = 'Q' + sales['OrderDate'].dt.quarter.astype(str)
    
    # Create customers dataframe
    unique_customers = sales['CustomerID'].unique()
    customers = pd.DataFrame({
        'CustomerID': unique_customers,
        'Tier': np.random.choice(['Platinum', 'Gold', 'Silver', 'Bronze'], len(unique_customers), p=[0.1, 0.2, 0.3, 0.4]),
        'Segment': np.random.choice(['Enterprise', 'Mid-Market', 'SMB', 'Consumer'], len(unique_customers), p=[0.15, 0.25, 0.35, 0.25]),
        'AcquisitionDate': np.random.choice(dates, len(unique_customers))
    })
    
    # Create products dataframe
    products_df = pd.DataFrame({
        'ProductName': all_products,
        'Category': [cat for cat, prods in products.items() for _ in prods],
        'BasePrice': [np.random.uniform(29, 1999) for _ in all_products]
    })
    
    return sales, products_df, customers, None

# ============================================================================
# LOAD DATA
# ============================================================================
@st.cache_data
def load_data():
    """Load or generate data"""
    try:
        # Try to find real data
        possible_paths = [
            Path('sales_dashboard_data'),
            Path('./sales_dashboard_data'),
            Path('/mount/src/sales-performance-dashboard/sales_dashboard_data'),
        ]
        
        for path in possible_paths:
            if path.exists() and (path / 'sales_transactions.csv').exists():
                sales = pd.read_csv(path / 'sales_transactions.csv')
                products = pd.read_csv(path / 'products.csv')
                customers = pd.read_csv(path / 'customers.csv')
                regions = pd.read_csv(path / 'regions.csv')
                
                sales['OrderDate'] = pd.to_datetime(sales['OrderDate'])
                sales['MonthYear'] = sales['OrderDate'].dt.to_period('M').astype(str)
                
                return sales, products, customers, regions
        
        # Generate sample data
        st.info("✨ Using premium sample data for demonstration")
        return generate_sample_data()
        
    except Exception as e:
        st.warning(f"Using sample data: {str(e)}")
        return generate_sample_data()

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

# Load CSS
load_premium_css()

# Premium Header
st.markdown("""
<div class='premium-header'>
    <div class='premium-title'>🌐 Multi-Region Sales Intelligence</div>
    <div class='premium-subtitle'>Enterprise Analytics Dashboard | Real-time Performance Metrics</div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<div class='sidebar-header'>⚙️ CONTROL PANEL</div>", unsafe_allow_html=True)
    
    # Dark Mode Toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h3>DISPLAY</h3>", unsafe_allow_html=True)
    with col2:
        mode_icon = "🌙" if not st.session_state.dark_mode else "☀️"
        if st.button(mode_icon, key="mode_toggle", help="Toggle dark/light mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    st.markdown("<h3>📅 TIME PERIOD</h3>", unsafe_allow_html=True)
    date_range = st.date_input(
        "",
        value=(pd.Timestamp('2022-01-01').date(), pd.Timestamp('2024-12-31').date()),
        key="date_range"
    )
    
    st.markdown("<h3>🌍 REGIONS</h3>", unsafe_allow_html=True)
    selected_region = st.multiselect(
        "",
        ['North America', 'Europe', 'Asia Pacific'],
        default=['North America', 'Europe', 'Asia Pacific'],
        key="region_filter"
    )
    
    st.markdown("<h3>📦 CATEGORIES</h3>", unsafe_allow_html=True)
    selected_category = st.multiselect(
        "",
        ['Electronics', 'Accessories', 'Furniture'],
        default=['Electronics', 'Accessories', 'Furniture'],
        key="category_filter"
    )
    
    st.markdown("<h3>⚡ QUICK ACTIONS</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            for key in ['region_filter', 'category_filter', 'date_range']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    st.markdown("---")
    st.markdown("<p class='text-secondary'>© 2024 Sales Intelligence v3.0</p>", unsafe_allow_html=True)

# Load Data
sales, products, customers, regions = load_data()

if sales is not None:
    # Filter data
    sales_filtered = sales.copy()
    
    if len(date_range) == 2:
        mask = (sales_filtered['OrderDate'] >= pd.Timestamp(date_range[0])) & \
               (sales_filtered['OrderDate'] <= pd.Timestamp(date_range[1]))
        sales_filtered = sales_filtered[mask]
    
    if selected_region:
        sales_filtered = sales_filtered[sales_filtered['Region'].isin(selected_region)]
    
    if selected_category:
        sales_filtered = sales_filtered[sales_filtered['Category'].isin(selected_category)]
    
    # Calculate KPIs
    total_sales = sales_filtered['TotalSales'].sum()
    total_profit = sales_filtered['Profit'].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    avg_order = sales_filtered['TotalSales'].mean()
    total_customers = sales_filtered['CustomerID'].nunique()
    total_orders = len(sales_filtered)
    
    # Calculate growth
    if len(date_range) == 2:
        days_diff = (pd.Timestamp(date_range[1]) - pd.Timestamp(date_range[0])).days
        prev_start = pd.Timestamp(date_range[0]) - pd.Timedelta(days=days_diff)
        prev_end = pd.Timestamp(date_range[0]) - pd.Timedelta(days=1)
        
        prev_sales = sales[
            (sales['OrderDate'] >= prev_start) & 
            (sales['OrderDate'] <= prev_end)
        ]['TotalSales'].sum()
        
        growth = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0
    else:
        growth = 0
    
    # KPI Grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Total Revenue</div>
            <div class='kpi-value'>{format_currency(total_sales)}</div>
            <div class='kpi-change {'positive' if growth > 0 else 'negative' if growth < 0 else ''}'>
                {'▲' if growth > 0 else '▼' if growth < 0 else '◆'} {abs(growth):.1f}% vs previous period
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Gross Profit</div>
            <div class='kpi-value'>{format_currency(total_profit)}</div>
            <div class='kpi-change positive'>
                {format_percentage(profit_margin)} Margin
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Average Order</div>
            <div class='kpi-value'>{format_currency(avg_order)}</div>
            <div class='kpi-change'>
                {total_orders:,} Orders
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        achievement = (total_sales / 10_000_000) * 100  # Example target
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Target Achievement</div>
            <div class='kpi-value'>{achievement:.1f}%</div>
            <div class='kpi-change {'positive' if achievement >= 100 else 'warning'}'>
                {'✓ On Track' if achievement >= 100 else '⚠ Below Target'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Premium Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Revenue Analytics",
        "🌍 Regional Performance",
        "📦 Product Analysis",
        "👥 Customer Insights",
        "📊 Data Explorer"
    ])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.markdown("<div class='chart-title'>📈 Revenue & Profit Trends</div>", unsafe_allow_html=True)
            
            monthly = sales_filtered.set_index('OrderDate').resample('M').agg({
                'TotalSales': 'sum',
                'Profit': 'sum'
            }).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=monthly['OrderDate'], y=monthly['TotalSales'],
                name='Revenue', line=dict(color=COLOR_PALETTE['chart_1'], width=3),
                fill='tozeroy', fillcolor=f'rgba{tuple(int(COLOR_PALETTE["chart_1"][i:i+2], 16) for i in (1, 3, 5)) + (0.1,)}'
            ))
            fig.add_trace(go.Scatter(
                x=monthly['OrderDate'], y=monthly['Profit'],
                name='Profit', line=dict(color=COLOR_PALETTE['chart_2'], width=3)
            ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='rgba(0,0,0,0.05)'),
                yaxis=dict(gridcolor='rgba(0,0,0,0.05)', title='Amount ($)'),
                hovermode='x unified',
                height=400,
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.markdown("<div class='chart-title'>📊 Channel Distribution</div>", unsafe_allow_html=True)
            
            channel_data = sales_filtered.groupby('SalesChannel')['TotalSales'].sum().reset_index()
            
            fig = px.pie(channel_data, values='TotalSales', names='SalesChannel',
                        color_discrete_sequence=get_chart_colors(len(channel_data)),
                        hole=0.6)
            
            fig.update_traces(textposition='inside', textinfo='percent+label',
                            marker=dict(line=dict(color='white', width=2)))
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.markdown("<div class='chart-title'>🌍 Regional Performance</div>", unsafe_allow_html=True)
            
            region_data = sales_filtered.groupby('Region').agg({
                'TotalSales': 'sum',
                'Profit': 'sum'
            }).reset_index()
            
            fig = px.bar(region_data, x='Region', y='TotalSales',
                        color='Region', text=region_data['TotalSales'].apply(lambda x: f'${x/1e6:.1f}M'),
                        color_discrete_sequence=get_chart_colors(len(region_data)))
            
            fig.update_traces(textposition='outside')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                showlegend=False,
                yaxis_title="Revenue ($)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.markdown("<div class='chart-title'>🏆 Top Countries</div>", unsafe_allow_html=True)
            
            country_data = sales_filtered.groupby('Country')['TotalSales'].sum().nlargest(10).reset_index()
            
            fig = px.bar(country_data, x='TotalSales', y='Country',
                        orientation='h', color='TotalSales',
                        color_continuous_scale=['#0A1E3C', '#00A67E', '#3182CE'],
                        text=country_data['TotalSales'].apply(lambda x: f'${x/1e6:.1f}M'))
            
            fig.update_traces(textposition='outside')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                xaxis_title="Revenue ($)",
                yaxis_title=""
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.markdown("<div class='chart-title'>🏅 Top Products</div>", unsafe_allow_html=True)
            
            product_data = sales_filtered.groupby('ProductName').agg({
                'TotalSales': 'sum',
                'ProfitMargin': 'mean'
            }).nlargest(10, 'TotalSales').reset_index()
            
            fig = px.bar(product_data, x='TotalSales', y='ProductName',
                        orientation='h', color='ProfitMargin',
                        color_continuous_scale='Viridis',
                        text=product_data['TotalSales'].apply(lambda x: f'${x/1e3:.0f}K'))
            
            fig.update_traces(textposition='outside')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                xaxis_title="Revenue ($)",
                yaxis_title=""
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.markdown("<div class='chart-title'>📦 Category Mix</div>", unsafe_allow_html=True)
            
            category_data = sales_filtered.groupby('Category')['TotalSales'].sum().reset_index()
            
            fig = px.pie(category_data, values='TotalSales', names='Category',
                        color_discrete_sequence=get_chart_colors(len(category_data)),
                        hole=0.4)
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                showlegend=True,
                legend=dict(orientation='h', yanchor='bottom', y=-0.2)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4:
        if customers is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.markdown("<div class='chart-title'>👥 Customer Segments</div>", unsafe_allow_html=True)
                
                if 'Segment' in customers.columns:
                    segment_counts = customers['Segment'].value_counts().reset_index()
                    segment_counts.columns = ['Segment', 'Count']
                    
                    fig = px.pie(segment_counts, values='Count', names='Segment',
                                color_discrete_sequence=get_chart_colors(len(segment_counts)))
                    
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
                st.markdown("<div class='chart-title'>🏆 Customer Tiers</div>", unsafe_allow_html=True)
                
                if 'Tier' in customers.columns:
                    tier_order = ['Platinum', 'Gold', 'Silver', 'Bronze']
                    tier_counts = customers['Tier'].value_counts().reindex(tier_order).reset_index()
                    tier_counts.columns = ['Tier', 'Count']
                    
                    fig = px.bar(tier_counts, x='Tier', y='Count',
                                color='Tier', text='Count',
                                color_discrete_sequence=get_chart_colors(4))
                    
                    fig.update_traces(textposition='outside')
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=400,
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
    
    with tab5:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        st.markdown("<div class='chart-title'>🔍 Transaction Explorer</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col2:
            search_term = st.text_input("🔍 Search", placeholder="Product, customer...")
        
        with col3:
            if st.button("📥 Export Data", use_container_width=True):
                csv = sales_filtered.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"sales_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        # Filter data
        display_data = sales_filtered.copy()
        if search_term:
            mask = display_data.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
            display_data = display_data[mask]
        
        st.markdown(f"**{len(display_data):,} transactions**")
        
        st.dataframe(
            display_data[['OrderDate', 'Region', 'Country', 'ProductName', 'Category', 
                         'SalesChannel', 'Quantity', 'UnitPrice', 'TotalSales', 'Profit']].head(100),
            use_container_width=True,
            column_config={
                "OrderDate": "Date",
                "UnitPrice": st.column_config.NumberColumn("Unit Price", format="$%.2f"),
                "TotalSales": st.column_config.NumberColumn("Revenue", format="$%.2f"),
                "Profit": st.column_config.NumberColumn("Profit", format="$%.2f"),
            }
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Premium Footer
    st.markdown(f"""
    <div class='premium-footer'>
        <div style='display: flex; justify-content: space-between;'>
            <span>📊 Sales Intelligence Platform v3.0</span>
            <span>🌍 {len(sales_filtered['Region'].unique())} Regions | {sales_filtered['Country'].nunique()} Countries | {len(sales_filtered):,} Transactions</span>
            <span>⚡ Updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("Failed to load data. Please check your data files.")
