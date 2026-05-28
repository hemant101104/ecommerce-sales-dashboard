import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv("data/sales.csv")

df['Order Date'] = pd.to_datetime(
    df['Order Date'],
    dayfirst=True,
    errors='coerce'
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.markdown("## 📊 Analytics Hub")

    selected = option_menu(
        menu_title=None,
        options=[
            "Overview",
            "Sales",
            "Customers",
            "Products"
        ],
        icons=[
            "house",
            "graph-up",
            "people",
            "box"
        ],
        default_index=0,
    )

    st.markdown("---")

    st.markdown("### Filters")

    # State Filter

    selected_states = st.multiselect(
        "State",
        options=df['State'].unique(),
        default=df['State'].unique()
    )

    # Category Filter

    selected_categories = st.multiselect(
        "Category",
        options=df['Category'].unique(),
        default=df['Category'].unique()
    )

    # Segment Filter

    selected_segments = st.multiselect(
        "Segment",
        options=df['Segment'].unique(),
        default=df['Segment'].unique()
    )

    # Region Filter

    selected_regions = st.multiselect(
        "Region",
        options=df['Region'].unique(),
        default=df['Region'].unique()
    )

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_df = df[
    (df['State'].isin(selected_states)) &
    (df['Category'].isin(selected_categories)) &
    (df['Segment'].isin(selected_segments)) &
    (df['Region'].isin(selected_regions))
]

# ---------------------------------------------------
# KPI VALUES
# ---------------------------------------------------

total_sales = filtered_df['Sales'].sum()

total_orders = filtered_df['Order ID'].nunique()

total_customers = filtered_df['Customer ID'].nunique()

avg_order_value = total_sales / total_orders

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #F7F8FC;
}

div[data-testid="metric-container"] {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 12px rgba(0,0,0,0.08);
    border: 1px solid #f0f0f0;
}

section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
}

h1, h2, h3 {
    color: #2E3A59;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown("""
# Hello Admin! 👋

### Measure your business performance in real time.
""")

st.markdown("---")

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Sales",
        f"${total_sales:,.0f}"
    )

with col2:
    st.metric(
        "🛒 Orders",
        total_orders
    )

with col3:
    st.metric(
        "👥 Customers",
        total_customers
    )

with col4:
    st.metric(
        "📦 Avg Order Value",
        f"${avg_order_value:,.2f}"
    )

st.markdown("---")

# ---------------------------------------------------
# OVERVIEW SECTION
# ---------------------------------------------------

st.markdown("## 📌 Overview")

left_col, right_col = st.columns((2,1))

# ---------------------------------------------------
# MONTHLY SALES TREND
# ---------------------------------------------------

with left_col:

    st.subheader("📈 Monthly Sales Trend")

    monthly_sales = filtered_df.groupby(
        filtered_df['Order Date'].dt.month_name()
    )['Sales'].sum().reset_index()

    month_order = [
        'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]

    monthly_sales['Order Date'] = pd.Categorical(
        monthly_sales['Order Date'],
        categories=month_order,
        ordered=True
    )

    monthly_sales = monthly_sales.sort_values('Order Date')

    fig1 = px.line(
        monthly_sales,
        x='Order Date',
        y='Sales',
        markers=True,
        template='plotly_white'
    )

    fig1.update_layout(
        height=400,
        xaxis_title="Month",
        yaxis_title="Sales",
        hovermode='x unified'
    )

    st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# CATEGORY DISTRIBUTION
# ---------------------------------------------------

with right_col:

    st.subheader("📊 Category Distribution")

    category_sales = filtered_df.groupby(
        'Category'
    )['Sales'].sum().reset_index()

    fig2 = px.pie(
        category_sales,
        names='Category',
        values='Sales',
        hole=0.5,
        template='plotly_white'
    )

    fig2.update_layout(height=400)

    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# SECOND ROW
# ---------------------------------------------------

col5, col6 = st.columns(2)

# ---------------------------------------------------
# TOP STATES
# ---------------------------------------------------

with col5:

    st.subheader("🏆 Top 10 States")

    top_states = filtered_df.groupby(
        'State'
    )['Sales'].sum().sort_values(
        ascending=False
    ).head(10).reset_index()

    fig3 = px.bar(
        top_states,
        x='Sales',
        y='State',
        orientation='h',
        template='plotly_white',
        color='Sales'
    )

    fig3.update_layout(
        height=450,
        yaxis={'categoryorder':'total ascending'}
    )

    st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# TOP PRODUCTS
# ---------------------------------------------------

with col6:

    st.subheader("🔥 Top 10 Products")

    top_products = filtered_df.groupby(
        'Product Name'
    )['Sales'].sum().sort_values(
        ascending=False
    ).head(10).reset_index()

    fig4 = px.bar(
        top_products,
        x='Sales',
        y='Product Name',
        orientation='h',
        template='plotly_white',
        color='Sales'
    )

    fig4.update_layout(
        height=450,
        yaxis={'categoryorder':'total ascending'}
    )

    st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------
# DATA PREVIEW
# ---------------------------------------------------

st.markdown("---")

st.subheader("🗂 Dataset Preview")

st.dataframe(filtered_df.head(20), use_container_width=True)