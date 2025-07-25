import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
import base64
from datetime import datetime
import streamlit as st

def export_to_csv(data, filename):
    """Export DataFrame to CSV"""
    csv = data.to_csv(index=False)
    return csv

def create_summary_report(processor):
    """Create a comprehensive summary report"""
    summary = processor.get_summary_stats()
    influencer_metrics = processor.calculate_roas()
    campaign_perf = processor.get_campaign_performance()
    product_perf = processor.get_product_performance()
    platform_perf = processor.get_platform_performance()
    
    # Top performers
    top_performers = processor.get_top_performers(metric='roas', top_n=10)
    underperformers = processor.get_underperformers(metric='roas', bottom_n=10)
    
    report_data = {
        'summary_stats': summary,
        'campaign_performance': campaign_perf,
        'product_performance': product_perf,
        'platform_performance': platform_perf,
        'top_performers': top_performers,
        'underperformers': underperformers,
        'all_influencers': influencer_metrics
    }
    
    return report_data

def generate_insights_text(processor):
    """Generate text-based insights from the data"""
    summary = processor.get_summary_stats()
    influencer_metrics = processor.calculate_roas()
    campaign_perf = processor.get_campaign_performance()
    product_perf = processor.get_product_performance()
    platform_perf = processor.get_platform_performance()
    
    insights = []
    
    # Overall performance insights
    insights.append("# HealthKart Influencer Marketing ROI Analysis")
    insights.append(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    insights.append("")
    
    insights.append("## Executive Summary")
    insights.append(f"- **Total Revenue Generated:** ₹{summary['total_revenue']:,.0f}")
    insights.append(f"- **Total Orders:** {summary['total_orders']:,.0f}")
    insights.append(f"- **Overall ROAS:** {summary['overall_roas']:.2f}x")
    insights.append(f"- **Total Influencers:** {summary['total_influencers']:,.0f}")
    insights.append(f"- **Average Order Value:** ₹{summary['avg_order_value']:,.0f}")
    insights.append("")
    
    # Campaign insights
    best_campaign = campaign_perf.loc[campaign_perf['roas'].idxmax()]
    worst_campaign = campaign_perf.loc[campaign_perf['roas'].idxmin()]
    
    insights.append("## Campaign Performance Insights")
    insights.append(f"- **Best Performing Campaign:** {best_campaign['campaign']} (ROAS: {best_campaign['roas']:.2f}x)")
    insights.append(f"- **Worst Performing Campaign:** {worst_campaign['campaign']} (ROAS: {worst_campaign['roas']:.2f}x)")
    insights.append(f"- **Total Campaigns:** {len(campaign_perf)}")
    insights.append("")
    
    # Platform insights
    best_platform = platform_perf.loc[platform_perf['roas'].idxmax()]
    insights.append("## Platform Performance Insights")
    insights.append(f"- **Best Performing Platform:** {best_platform['platform']} (ROAS: {best_platform['roas']:.2f}x)")
    insights.append(f"- **Platform Revenue Distribution:**")
    for _, row in platform_perf.iterrows():
        pct = (row['revenue'] / summary['total_revenue']) * 100
        insights.append(f"  - {row['platform']}: ₹{row['revenue']:,.0f} ({pct:.1f}%)")
    insights.append("")
    
    # Product insights
    best_product = product_perf.loc[product_perf['roas'].idxmax()]
    insights.append("## Product Performance Insights")
    insights.append(f"- **Best Performing Product:** {best_product['product']} (ROAS: {best_product['roas']:.2f}x)")
    insights.append(f"- **Product Revenue Distribution:**")
    for _, row in product_perf.iterrows():
        pct = (row['revenue'] / summary['total_revenue']) * 100
        insights.append(f"  - {row['product']}: ₹{row['revenue']:,.0f} ({pct:.1f}%)")
    insights.append("")
    
    # Influencer insights
    profitable_count = (influencer_metrics['roas'] > 1).sum()
    avg_roas = influencer_metrics['roas'].mean()
    
    insights.append("## Influencer Performance Insights")
    insights.append(f"- **Profitable Influencers:** {profitable_count}/{len(influencer_metrics)} ({(profitable_count/len(influencer_metrics)*100):.1f}%)")
    insights.append(f"- **Average ROAS:** {avg_roas:.2f}x")
    insights.append(f"- **Top 5 Performers by ROAS:**")
    
    top_5 = influencer_metrics.nlargest(5, 'roas')
    for i, (_, row) in enumerate(top_5.iterrows(), 1):
        insights.append(f"  {i}. {row['name']} ({row['platform']}) - ROAS: {row['roas']:.2f}x, Revenue: ₹{row['revenue']:,.0f}")
    
    insights.append("")
    insights.append("## Recommendations")
    
    # Generate recommendations based on data
    if best_platform['roas'] > 2:
        insights.append(f"- **Focus on {best_platform['platform']}:** This platform shows exceptional ROAS of {best_platform['roas']:.2f}x. Consider increasing budget allocation.")
    
    if profitable_count / len(influencer_metrics) < 0.7:
        insights.append("- **Influencer Optimization:** Less than 70% of influencers are profitable. Review underperforming influencers and optimize selection criteria.")
    
    if best_campaign['roas'] > worst_campaign['roas'] * 2:
        insights.append(f"- **Campaign Strategy:** {best_campaign['campaign']} significantly outperforms {worst_campaign['campaign']}. Analyze successful elements for replication.")
    
    # Category analysis
    category_performance = influencer_metrics.groupby('category')['roas'].mean().sort_values(ascending=False)
    best_category = category_performance.index[0]
    insights.append(f"- **Category Focus:** {best_category} category shows the best average ROAS ({category_performance.iloc[0]:.2f}x). Consider expanding partnerships in this category.")
    
    return "\n".join(insights)

def create_downloadable_csv(data, filename):
    """Create a downloadable CSV file"""
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

def create_downloadable_insights(insights_text, filename="insights_report.md"):
    """Create a downloadable insights report"""
    b64 = base64.b64encode(insights_text.encode()).decode()
    href = f'<a href="data:file/markdown;base64,{b64}" download="{filename}">Download Insights Report</a>'
    return href

