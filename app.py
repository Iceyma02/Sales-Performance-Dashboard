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
# PREMIUM COLOR PALETTE - Financial/Banking Grade
# ============================================================================
COLOR_PALETTE = {
    'primary': '#0A1E3C',
    'primary_light': '#1E3A5F',
    'primary_dark': '#051024',
    'accent_1': '#00A67E',
    'accent_2': '#3182CE',
    'accent_3': '#805AD5',
    'accent_4': '#DD6B20',
    'accent_5': '#E53E3E',
    'gray_50': '#F7FAFC',
    'gray_100': '#EDF2F7',
    'gray_200': '#E2E8F0',
    'gray_300': '#CBD5E0',
    'gray_400': '#A0AEC0',
    'gray_500': '#718096',
    'gray_600': '#4A5568',
    'gray_700': '#2D3748',
    'gray_800': '#1A202C',
    'gray_900': '#171923',
    'success': '#00A67E',
    'warning': '#DD6B20',
    'danger': '#E53E3E',
    'info': '#3182CE',
    'text_primary': '#1A202C',
    'text_secondary': '#4A5568',
    'text_tertiary': '#718096',
    'text_inverse': '#FFFFFF',
    'bg_primary': '#FFFFFF',
    'bg_secondary': '#F7FAFC',
    'bg_tertiary': '#EDF2F7',
    'bg_inverse': '#0A1E3C',
    'bg_inverse_secondary': '#1E3A5F',
    'bg_card': '#FFFFFF',
    'bg_card_inverse': '#1A202C',
    'border_light': '#E2E8F0',
    'border_dark': '#2D3748',
    'chart_1': '#0A1E3C',
    'chart_2': '#00A67E',
    'chart_3': '#3182CE',
    'chart_4': '#805AD5',
    'chart_5': '#DD6B20',
    'chart_6': '#E53E3E',
    'chart_7': '#38B2AC',
    'chart_8': '#D53F8C',
}

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
# PREMIUM CSS (CLEAN & ENTERPRISE)
# ============================================================================
def load_premium_css():
    if st.session_state.dark_mode:
        bg_main = "#0E1117"
        bg_card = "#161B22"
        text_primary = "#FFFFFF"
        text_secondary = "#B0B3B8"
        border = "#30363D"
    else:
        bg_main = "#F5F7FA"
        bg_card = "#FFFFFF"
        text_primary = "#111827"
        text_secondary = "#6B7280"
        border = "#E5E7EB"

    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {bg_main};
        }}
        h1, h2, h3, h4, h5, h6, p, span, div, label {{
            color: {text_primary} !important;
        }}
        .kpi-card {{
            background: {bg_card};
            padding: 1.5rem;
            border-radius: 14px;
            border: 1px solid {border};
            box-shadow: 0 6px 20px rgba(0,0,0,0.05);
            transition: 0.3s ease;
        }}
        .kpi-card:hover {{
            transform: translateY(-3px);
        }}
        .kpi-label {{
            font-size: 0.8rem;
            color: {text_secondary};
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .kpi-value {{
            font-size: 1.8rem;
            font-weight: 700;
            margin-top: 6px;
        }}
        .chart-card {{
            background: {bg_card};
            padding: 1.5rem;
            border-radius: 14px;
            border: 1px solid {border};
            margin-bottom: 1.5rem;
        }}
        .chart-title {{
            font-weight: 600;
            margin-bottom: 1rem;
        }}
        [data-testid="stSidebar"] {{
            background-color: {bg_card};
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.5rem;
            border-bottom: 1px solid {border};
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px 8px 0 0;
            padding: 0.5rem 1rem;
            color: {text_secondary};
        }}
        .stTabs [aria-selected="true"] {{
            background: {bg_card};
            border-bottom: 2px solid #00A67E;
            color: {text_primary};
        }}
        .stButton button {{
            background: {bg_card};
            color: {text_primary};
            border: 1px solid {border};
            border-radius: 8px;
        }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# PLOTLY THEME HELPER
# ============================================================================
def get_plotly_theme():
    if st.session_state.dark_mode:
        return {
            "template": "plotly_dark",
            "paper_bgcolor": "#161B22",
            "plot_bgcolor": "#161B22",
            "font_color": "#FFFFFF",
            "gridcolor": "#30363D"
        }
    else:
        return {
            "template": "plotly_white",
            "paper_bgcolor": "#FFFFFF",
            "plot_bgcolor": "#FFFFFF",
            "font_color": "#111827",
            "gridcolor": "#E5E7EB"
        }

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def format_currency(value):
    if value >= 1_000_000_000:
        return f"${value/1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value/1_000:.1f}K"
    else:
        return f"${value:,.0f}"

def get_chart_colors(n_colors):
    return CHART_COLORS[:min(n_colors, len(CHART_COLORS))]

# ============================================================================
# SAMPLE DATA GENERATOR
# ============================================================================
def generate_sample_data():
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
        
        if category == 'Electronics':
            unit_price = np.random.uniform(299, 1999)
            margin = np.random.uniform(0.25, 0.45)
        elif category == 'Accessories':
            unit_price = np.random.uniform(29, 199)
            margin = np.random.uniform(0.35, 0.55)
        else:
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
    
    unique_customers = sales['CustomerID'].unique()
    customers = pd.DataFrame({
        'CustomerID': unique_customers,
        'Tier': np.random.choice(['Platinum', 'Gold', 'Silver', 'Bronze'], len(unique_customers), p=[0.1, 0.2, 0.3, 0.4]),
        'Segment': np.random.choice(['Enterprise', 'Mid-Market', 'SMB', 'Consumer'], len(unique_customers), p=[0.15, 0.25, 0.35, 0.25]),
        'AcquisitionDate': np.random.choice(dates, len(unique_customers))
    })
    
    products_df = pd.DataFrame({
        'ProductName': all_products,
        'Category': [cat for cat, prods in products.items() for _ in prods],
        'BasePrice': [np.random.uniform(29, 1999) for _ in all_products]
    })
    
    return sales, products_df, customers, None

# ============================================================================
# LOAD DATA (FIXED PATHS)
# ============================================================================
@st.cache_data
def load_data():
    try:
        possible_paths = [
            Path('/mount/src/Sales-Performance-Dashboard/sales_dashboard_data'),  # exact repo name
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
            st.info("✨ Using premium sample data for demonstration")
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
# MAIN DASHBOARD
# ============================================================================
load_premium_css()

# Premium Header
st.markdown("""
<div style='margin-bottom: 2rem;'>
    <h1 style='font-size: 2.5rem; font-weight: 800;'>🌐 Multi-Region Sales Intelligence</h1>
    <p style='font-size: 1rem; opacity: 0.8;'>Enterprise Analytics Dashboard | Real-time Performance Metrics</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ CONTROL PANEL")
    
    # Dark mode toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("#### Display")
    with col2:
        mode_icon = "🌙" if not st.session_state.dark_mode else "☀️"
        if st.button(mode_icon, key="mode_toggle", help="Toggle dark/light mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    st.markdown("---")
    st.markdown("#### 📅 Time Period")
    date_range = st.date_input(
        "",
        value=(pd.Timestamp('2022-01-01').date(), pd.Timestamp('2024-12-31').date()),
        key="date_range"
    )
    
    st.markdown("#### 🌍 Regions")
    selected_region = st.multiselect(
        "",
        ['North America', 'Europe', 'Asia Pacific'],
        default=['North America', 'Europe', 'Asia Pacific'],
        key="region_filter"
    )
    
    st.markdown("#### 📦 Categories")
    selected_category = st.multiselect(
        "",
        ['Electronics', 'Accessories', 'Furniture'],
        default=['Electronics', 'Accessories', 'Furniture'],
        key="category_filter"
    )
    
    st.markdown("#### ⚡ Quick Actions")
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
    st.caption("© 2025 Sales Intelligence v3.0")

# Load Data
sales, products, customers, regions = load_data()

if sales is not None:
    # Filter data
    sales_filtered = sales.copy()
    if len(date_range) == 2:
        mask = (sales_filtered['OrderDate'] >= pd.Timestamp(date_range[0])) & (sales_filtered['OrderDate'] <= pd.Timestamp(date_range[1]))
        sales_filtered = sales_filtered[mask]
    if selected_region:
        sales_filtered = sales_filtered[sales_filtered['Region'].isin(selected_region)]
    if selected_category:
        sales_filtered = sales_filtered[sales_filtered['Category'].isin(selected_category)]
    
    # KPIs
    total_sales = sales_filtered['TotalSales'].sum()
    total_profit = sales_filtered['Profit'].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    avg_order = sales_filtered['TotalSales'].mean()
    total_customers = sales_filtered['CustomerID'].nunique()
    total_orders = len(sales_filtered)
    
    # Growth calculation
    if len(date_range) == 2:
        days_diff = (pd.Timestamp(date_range[1]) - pd.Timestamp(date_range[0])).days
        prev_start = pd.Timestamp(date_range[0]) - pd.Timedelta(days=days_diff)
        prev_end = pd.Timestamp(date_range[0]) - pd.Timedelta(days=1)
        prev_sales = sales[(sales['OrderDate'] >= prev_start) & (sales['OrderDate'] <= prev_end)]['TotalSales'].sum()
        growth = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0
    else:
        growth = 0
    
    # KPI Cards (simplified)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Total Revenue</div>
            <div class='kpi-value'>{format_currency(total_sales)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Gross Profit</div>
            <div class='kpi-value'>{format_currency(total_profit)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Average Order</div>
            <div class='kpi-value'>{format_currency(avg_order)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        achievement = (total_sales / 10_000_000) * 100  # example target
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-label'>Target Achievement</div>
            <div class='kpi-value'>{achievement:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs
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
                fill='tozeroy', fillcolor=f'rgba{tuple(int(COLOR_PALETTE["chart_1"][i:i+2], 16) for i in (1,3,5)) + (0.1,)}'
            ))
            fig.add_trace(go.Scatter(
                x=monthly['OrderDate'], y=monthly['Profit'],
                name='Profit', line=dict(color=COLOR_PALETTE['chart_2'], width=3)
            ))
            
            theme = get_plotly_theme()
            fig.update_layout(
                template=theme["template"],
                paper_bgcolor=theme["paper_bgcolor"],
                plot_bgcolor=theme["plot_bgcolor"],
                font=dict(color=theme["font_color"]),
                xaxis=dict(gridcolor=theme["gridcolor"]),
                yaxis=dict(gridcolor=theme["gridcolor"], title="Amount ($)"),
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
            
            theme = get_plotly_theme()
            fig.update_layout(
                template=theme["template"],
                paper_bgcolor=theme["paper_bgcolor"],
                plot_bgcolor=theme["plot_bgcolor"],
                font=dict(color=theme["font_color"]),
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
            
            theme = get_plotly_theme()
            fig.update_layout(
                template=theme["template"],
                paper_bgcolor=theme["paper_bgcolor"],
                plot_bgcolor=theme["plot_bgcolor"],
                font=dict(color=theme["font_color"]),
                yaxis=dict(gridcolor=theme["gridcolor"], title="Revenue ($)"),
                height=400,
                showlegend=False
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
            
            theme = get_plotly_theme()
            fig.update_layout(
                template=theme["template"],
                paper_bgcolor=theme["paper_bgcolor"],
                plot_bgcolor=theme["plot_bgcolor"],
                font=dict(color=theme["font_color"]),
                xaxis=dict(gridcolor=theme["gridcolor"], title="Revenue ($)"),
                yaxis=dict(gridcolor=theme["gridcolor"]),
                height=400
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
            
            theme = get_plotly_theme()
            fig.update_layout(
                template=theme["template"],
                paper_bgcolor=theme["paper_bgcolor"],
                plot_bgcolor=theme["plot_bgcolor"],
                font=dict(color=theme["font_color"]),
                xaxis=dict(gridcolor=theme["gridcolor"], title="Revenue ($)"),
                yaxis=dict(gridcolor=theme["gridcolor"]),
                height=400
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
            
            theme = get_plotly_theme()
            fig.update_layout(
                template=theme["template"],
                paper_bgcolor=theme["paper_bgcolor"],
                plot_bgcolor=theme["plot_bgcolor"],
                font=dict(color=theme["font_color"]),
                height=400,
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
                    
                    theme = get_plotly_theme()
                    fig.update_layout(
                        template=theme["template"],
                        paper_bgcolor=theme["paper_bgcolor"],
                        plot_bgcolor=theme["plot_bgcolor"],
                        font=dict(color=theme["font_color"]),
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
                    
                    theme = get_plotly_theme()
                    fig.update_layout(
                        template=theme["template"],
                        paper_bgcolor=theme["paper_bgcolor"],
                        plot_bgcolor=theme["plot_bgcolor"],
                        font=dict(color=theme["font_color"]),
                        yaxis=dict(gridcolor=theme["gridcolor"]),
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
    
    # Footer
    st.markdown(f"""
    <div style='margin-top: 2rem; padding: 1rem 0; border-top: 1px solid #E5E7EB; display: flex; justify-content: space-between; font-size: 0.85rem; opacity: 0.7;'>
        <span>📊 Sales Intelligence Platform v3.0</span>
        <span>🌍 {len(sales_filtered['Region'].unique())} Regions | {sales_filtered['Country'].nunique()} Countries | {len(sales_filtered):,} Transactions</span>
        <span>⚡ Updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</span>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("❌ Failed to load data. Please check your data files.")
