import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_processor import DataProcessor
from export_utils import create_summary_report, generate_insights_text, create_downloadable_csv, create_downloadable_insights
import os
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="HealthKart Influencer ROI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with HealthKart theme
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E5A87;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #2E5A87 0%, #00BCD4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #00BCD4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2E5A87;
        margin-bottom: 1rem;
        padding: 0.5rem 0;
        border-bottom: 2px solid #00BCD4;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border: 1px solid #00BCD4;
    }
    .stMultiSelect > div > div {
        background-color: #f8f9fa;
        border: 1px solid #00BCD4;
    }
    /* HealthKart brand colors */
    .healthkart-primary { color: #2E5A87; }
    .healthkart-secondary { color: #00BCD4; }
    .healthkart-accent { color: #FF6B35; }
    
    /* Custom metric styling */
    [data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #00BCD4;
        color: white;
        border: none;
        border-radius: 0.25rem;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #00ACC1;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache data"""
    processor = DataProcessor()
    if processor.load_data():
        return processor
    return None

def main():
    # Add HealthKart logo and title
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("healthkart_logo.png", width=300)
        except:
            pass  # If logo not found, continue without it
    
    st.markdown('<h1 class="main-header">Influencer Marketing ROI Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">Track and optimize your influencer campaigns with data-driven insights</p>', unsafe_allow_html=True)
    
    # Initialize data processor
    processor = load_data()
    
    if processor is None:
        st.error("Failed to load data. Please check if the data files exist in the data directory.")
        return
    
    # Sidebar for navigation and filters
    st.sidebar.markdown('<div class="sidebar-header">Navigation</div>', unsafe_allow_html=True)
    page = st.sidebar.selectbox(
        "Select Page",
        ["Overview", "Campaign Performance", "ROI & ROAS Analysis", "Influencer Insights", "Payout Tracking"]
    )
    
    # Sidebar filters
    st.sidebar.markdown('<div class="sidebar-header">Filters</div>', unsafe_allow_html=True)
    
    # Get unique values for filters
    merged_df = processor.merge_data()
    
    platforms = st.sidebar.multiselect(
        "Platform",
        options=merged_df['platform'].unique(),
        default=merged_df['platform'].unique()
    )
    
    categories = st.sidebar.multiselect(
        "Category",
        options=merged_df['category'].unique(),
        default=merged_df['category'].unique()
    )
    
    campaigns = st.sidebar.multiselect(
        "Campaign",
        options=merged_df['campaign'].unique(),
        default=merged_df['campaign'].unique()
    )
    
    products = st.sidebar.multiselect(
        "Product",
        options=merged_df['product'].unique(),
        default=merged_df['product'].unique()
    )
    
    # Date range filter
    min_date = merged_df['date'].min().date()
    max_date = merged_df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Apply filters
    filters = {
        'platform': platforms,
        'category': categories,
        'campaign': campaigns,
        'product': products,
        'date_range': date_range if len(date_range) == 2 else None
    }
    
    # Filter data
    filtered_df = processor.filter_data(filters)
    processor.merged_df = filtered_df  # Update processor with filtered data
    
    # Export section
    st.sidebar.markdown('<div class="sidebar-header">Export Data</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("Generate Insights Report"):
        insights_text = generate_insights_text(processor)
        st.sidebar.markdown(create_downloadable_insights(insights_text), unsafe_allow_html=True)
    
    if st.sidebar.button("Export Summary Data"):
        summary_data = create_summary_report(processor)
        
        # Create downloadable links for each dataset
        st.sidebar.markdown("**Download Options:**")
        
        # Campaign performance
        campaign_csv = create_downloadable_csv(summary_data['campaign_performance'], "campaign_performance.csv")
        st.sidebar.markdown(campaign_csv, unsafe_allow_html=True)
        
        # Product performance
        product_csv = create_downloadable_csv(summary_data['product_performance'], "product_performance.csv")
        st.sidebar.markdown(product_csv, unsafe_allow_html=True)
        
        # Influencer metrics
        influencer_csv = create_downloadable_csv(summary_data['all_influencers'], "influencer_metrics.csv")
        st.sidebar.markdown(influencer_csv, unsafe_allow_html=True)
    
    # Display selected page
    if page == "Overview":
        show_overview(processor)
    elif page == "Campaign Performance":
        show_campaign_performance(processor)
    elif page == "ROI & ROAS Analysis":
        show_roi_analysis(processor)
    elif page == "Influencer Insights":
        show_influencer_insights(processor)
    elif page == "Payout Tracking":
        show_payout_tracking(processor)

def show_overview(processor):
    """Display overview page with summary metrics"""
    st.header("📊 Overview")
    
    # Get summary statistics
    summary = processor.get_summary_stats()
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Revenue",
            value=f"₹{summary['total_revenue']:,.0f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Total Orders",
            value=f"{summary['total_orders']:,.0f}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Overall ROAS",
            value=f"{summary['overall_roas']:.2f}x",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Total Influencers",
            value=f"{summary['total_influencers']:,.0f}",
            delta=None
        )
    
    # Revenue and ROAS trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue Trend")
        time_series = processor.get_time_series_data()
        fig = px.line(time_series, x='date', y='revenue', title="Daily Revenue")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("ROAS Trend")
        fig = px.line(time_series, x='date', y='roas', title="Daily ROAS")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Platform and campaign performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue by Platform")
        platform_perf = processor.get_platform_performance()
        fig = px.pie(platform_perf, values='revenue', names='platform', title="Revenue Distribution by Platform")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Revenue by Campaign")
        campaign_perf = processor.get_campaign_performance()
        fig = px.bar(campaign_perf, x='campaign', y='revenue', title="Revenue by Campaign")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def show_campaign_performance(processor):
    """Display campaign performance page"""
    st.header("🎯 Campaign Performance")
    
    # Campaign metrics table
    campaign_perf = processor.get_campaign_performance()
    st.subheader("Campaign Metrics")
    st.dataframe(campaign_perf, use_container_width=True)
    
    # Campaign comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue vs Spend by Campaign")
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Revenue', x=campaign_perf['campaign'], y=campaign_perf['revenue']))
        fig.add_trace(go.Bar(name='Spend', x=campaign_perf['campaign'], y=campaign_perf['total_payout']))
        fig.update_layout(barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("ROAS by Campaign")
        fig = px.bar(campaign_perf, x='campaign', y='roas', title="ROAS by Campaign")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Product performance
    st.subheader("Product Performance")
    product_perf = processor.get_product_performance()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(product_perf, x='product', y='revenue', title="Revenue by Product")
        fig.update_xaxes(tickangle=45)
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(product_perf, x='orders', y='revenue', size='roas', 
                        hover_name='product', title="Orders vs Revenue (Size = ROAS)")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def show_roi_analysis(processor):
    """Display ROI and ROAS analysis page"""
    st.header("💰 ROI & ROAS Analysis")
    
    # Get influencer metrics
    influencer_metrics = processor.calculate_roas()
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_roas = influencer_metrics['roas'].mean()
        st.metric("Average ROAS", f"{avg_roas:.2f}x")
    
    with col2:
        avg_incremental_roas = influencer_metrics['incremental_roas'].mean()
        st.metric("Average Incremental ROAS", f"{avg_incremental_roas:.2f}x")
    
    with col3:
        profitable_influencers = (influencer_metrics['roas'] > 1).sum()
        st.metric("Profitable Influencers", f"{profitable_influencers}/{len(influencer_metrics)}")
    
    # ROAS distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("ROAS Distribution")
        fig = px.histogram(influencer_metrics, x='roas', nbins=20, title="ROAS Distribution")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("ROAS vs Revenue")
        fig = px.scatter(influencer_metrics, x='revenue', y='roas', 
                        size='follower_count', color='platform',
                        hover_name='name', title="ROAS vs Revenue")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Platform and category analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("ROAS by Platform")
        platform_roas = influencer_metrics.groupby('platform')['roas'].mean().reset_index()
        fig = px.bar(platform_roas, x='platform', y='roas', title="Average ROAS by Platform")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("ROAS by Category")
        category_roas = influencer_metrics.groupby('category')['roas'].mean().reset_index()
        fig = px.bar(category_roas, x='category', y='roas', title="Average ROAS by Category")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def show_influencer_insights(processor):
    """Display influencer insights page"""
    st.header("👥 Influencer Insights")
    
    # Top and bottom performers
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top Performers (ROAS)")
        top_performers = processor.get_top_performers(metric='roas', top_n=10)
        display_cols = ['name', 'platform', 'category', 'roas', 'revenue', 'total_payout']
        st.dataframe(top_performers[display_cols], use_container_width=True)
    
    with col2:
        st.subheader("⚠️ Underperformers (ROAS)")
        underperformers = processor.get_underperformers(metric='roas', bottom_n=10)
        st.dataframe(underperformers[display_cols], use_container_width=True)
    
    # Influencer analysis
    influencer_metrics = processor.calculate_roas()
    
    # Follower count vs performance
    st.subheader("Follower Count vs Performance")
    fig = px.scatter(influencer_metrics, x='follower_count', y='roas', 
                    color='platform', size='revenue',
                    hover_name='name', title="Follower Count vs ROAS")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Engagement analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Engagement Rate vs ROAS")
        fig = px.scatter(influencer_metrics, x='engagement_rate', y='roas', 
                        color='category', hover_name='name',
                        title="Engagement Rate vs ROAS")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Gender Distribution")
        gender_perf = influencer_metrics.groupby('gender').agg({
            'roas': 'mean',
            'revenue': 'sum',
            'name': 'count'
        }).reset_index()
        gender_perf.rename(columns={'name': 'count'}, inplace=True)
        
        fig = px.bar(gender_perf, x='gender', y='count', title="Influencer Count by Gender")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def show_payout_tracking(processor):
    """Display payout tracking page"""
    st.header("💳 Payout Tracking")
    
    # Payout summary
    summary = processor.get_summary_stats()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Spend", f"₹{summary['total_spend']:,.0f}")
    
    with col2:
        avg_payout = summary['total_spend'] / summary['total_influencers']
        st.metric("Average Payout per Influencer", f"₹{avg_payout:,.0f}")
    
    with col3:
        st.metric("ROI", f"{summary['overall_roas']:.2f}x")
    
    # Payout basis analysis
    influencer_metrics = processor.calculate_roas()
    merged_df = processor.merged_df
    
    # Get payout basis distribution
    payout_basis = merged_df.groupby('basis').agg({
        'total_payout': 'sum',
        'influencer_id': 'nunique',
        'revenue': 'sum'
    }).reset_index()
    payout_basis['avg_payout'] = payout_basis['total_payout'] / payout_basis['influencer_id']
    payout_basis['roas'] = payout_basis['revenue'] / payout_basis['total_payout']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Payout by Basis")
        fig = px.pie(payout_basis, values='total_payout', names='basis', 
                    title="Total Payout Distribution by Basis")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("ROAS by Payout Basis")
        fig = px.bar(payout_basis, x='basis', y='roas', title="ROAS by Payout Basis")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed payout table
    st.subheader("Detailed Payout Information")
    payout_details = influencer_metrics[['name', 'platform', 'category', 'revenue', 'total_payout', 'roas']].copy()
    payout_details = payout_details.sort_values('total_payout', ascending=False)
    
    st.dataframe(payout_details, use_container_width=True)
    
    # Payout efficiency
    st.subheader("Payout Efficiency Analysis")
    fig = px.scatter(influencer_metrics, x='total_payout', y='revenue', 
                    color='platform', size='roas',
                    hover_name='name', title="Payout vs Revenue (Size = ROAS)")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()

