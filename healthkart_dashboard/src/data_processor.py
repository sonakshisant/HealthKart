import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataProcessor:
    def __init__(self, data_dir='/home/ubuntu/healthkart_dashboard/data'):
        self.data_dir = data_dir
        self.influencers_df = None
        self.posts_df = None
        self.tracking_data_df = None
        self.payouts_df = None
        self.merged_df = None
        
    def load_data(self):
        """Load all CSV files into DataFrames"""
        try:
            self.influencers_df = pd.read_csv(f'{self.data_dir}/influencers.csv')
            self.posts_df = pd.read_csv(f'{self.data_dir}/posts.csv')
            self.tracking_data_df = pd.read_csv(f'{self.data_dir}/tracking_data.csv')
            self.payouts_df = pd.read_csv(f'{self.data_dir}/payouts.csv')
            
            # Convert date columns to datetime
            self.posts_df['date'] = pd.to_datetime(self.posts_df['date'])
            self.tracking_data_df['date'] = pd.to_datetime(self.tracking_data_df['date'])
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def merge_data(self):
        """Merge all DataFrames for comprehensive analysis"""
        # Merge tracking data with influencers
        merged = self.tracking_data_df.merge(
            self.influencers_df, 
            left_on='influencer_id', 
            right_on='id', 
            how='left'
        )
        
        # Merge with payouts
        merged = merged.merge(
            self.payouts_df, 
            on='influencer_id', 
            how='left'
        )
        
        # Add post metrics by aggregating posts per influencer
        post_metrics = self.posts_df.groupby('influencer_id').agg({
            'reach': 'sum',
            'likes': 'sum',
            'comments': 'sum'
        }).reset_index()
        
        merged = merged.merge(
            post_metrics, 
            on='influencer_id', 
            how='left'
        )
        
        self.merged_df = merged
        return merged
    
    def calculate_roas(self, baseline_revenue_pct=0.1):
        """Calculate ROAS and Incremental ROAS"""
        if self.merged_df is None:
            self.merge_data()
        
        # Group by influencer to calculate metrics
        influencer_metrics = self.merged_df.groupby('influencer_id').agg({
            'revenue': 'sum',
            'orders_x': 'sum',  # orders from tracking_data
            'total_payout': 'first',
            'name': 'first',
            'category': 'first',
            'gender': 'first',
            'follower_count': 'first',
            'platform': 'first',
            'reach': 'first',
            'likes': 'first',
            'comments': 'first'
        }).reset_index()
        
        # Rename orders_x to orders for clarity
        influencer_metrics.rename(columns={'orders_x': 'orders'}, inplace=True)
        
        # Calculate ROAS
        influencer_metrics['roas'] = influencer_metrics['revenue'] / influencer_metrics['total_payout']
        
        # Calculate Incremental ROAS (assuming baseline revenue is 10% of actual revenue)
        influencer_metrics['baseline_revenue'] = influencer_metrics['revenue'] * baseline_revenue_pct
        influencer_metrics['incremental_revenue'] = influencer_metrics['revenue'] - influencer_metrics['baseline_revenue']
        influencer_metrics['incremental_roas'] = influencer_metrics['incremental_revenue'] / influencer_metrics['total_payout']
        
        # Calculate engagement rate
        influencer_metrics['engagement_rate'] = (
            (influencer_metrics['likes'] + influencer_metrics['comments']) / 
            influencer_metrics['reach'] * 100
        ).fillna(0)
        
        return influencer_metrics
    
    def get_campaign_performance(self):
        """Get campaign-level performance metrics"""
        if self.merged_df is None:
            self.merge_data()
        
        campaign_metrics = self.merged_df.groupby('campaign').agg({
            'revenue': 'sum',
            'orders_x': 'sum',
            'total_payout': 'sum',
            'influencer_id': 'nunique'
        }).reset_index()
        
        campaign_metrics['roas'] = campaign_metrics['revenue'] / campaign_metrics['total_payout']
        campaign_metrics.rename(columns={'influencer_id': 'num_influencers', 'orders_x': 'orders'}, inplace=True)
        
        return campaign_metrics
    
    def get_product_performance(self):
        """Get product-level performance metrics"""
        if self.merged_df is None:
            self.merge_data()
        
        product_metrics = self.merged_df.groupby('product').agg({
            'revenue': 'sum',
            'orders_x': 'sum',
            'total_payout': 'sum',
            'influencer_id': 'nunique'
        }).reset_index()
        
        product_metrics['roas'] = product_metrics['revenue'] / product_metrics['total_payout']
        product_metrics.rename(columns={'influencer_id': 'num_influencers', 'orders_x': 'orders'}, inplace=True)
        
        return product_metrics
    
    def get_platform_performance(self):
        """Get platform-level performance metrics"""
        if self.merged_df is None:
            self.merge_data()
        
        platform_metrics = self.merged_df.groupby('platform').agg({
            'revenue': 'sum',
            'orders_x': 'sum',
            'total_payout': 'sum',
            'influencer_id': 'nunique'
        }).reset_index()
        
        platform_metrics['roas'] = platform_metrics['revenue'] / platform_metrics['total_payout']
        platform_metrics.rename(columns={'influencer_id': 'num_influencers', 'orders_x': 'orders'}, inplace=True)
        
        return platform_metrics
    
    def get_time_series_data(self, groupby_column='date'):
        """Get time series data for performance tracking"""
        if self.merged_df is None:
            self.merge_data()
        
        time_series = self.merged_df.groupby(groupby_column).agg({
            'revenue': 'sum',
            'orders_x': 'sum',
            'total_payout': 'sum'
        }).reset_index()
        
        time_series['roas'] = time_series['revenue'] / time_series['total_payout']
        time_series.rename(columns={'orders_x': 'orders'}, inplace=True)
        
        return time_series
    
    def filter_data(self, filters):
        """Apply filters to the merged data"""
        if self.merged_df is None:
            self.merge_data()
        
        filtered_df = self.merged_df.copy()
        
        if 'platform' in filters and filters['platform']:
            filtered_df = filtered_df[filtered_df['platform'].isin(filters['platform'])]
        
        if 'category' in filters and filters['category']:
            filtered_df = filtered_df[filtered_df['category'].isin(filters['category'])]
        
        if 'gender' in filters and filters['gender']:
            filtered_df = filtered_df[filtered_df['gender'].isin(filters['gender'])]
        
        if 'campaign' in filters and filters['campaign']:
            filtered_df = filtered_df[filtered_df['campaign'].isin(filters['campaign'])]
        
        if 'product' in filters and filters['product']:
            filtered_df = filtered_df[filtered_df['product'].isin(filters['product'])]
        
        if 'date_range' in filters and filters['date_range']:
            start_date, end_date = filters['date_range']
            # Convert date objects to datetime for comparison
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            filtered_df = filtered_df[
                (filtered_df['date'] >= start_date) & 
                (filtered_df['date'] <= end_date)
            ]
        
        return filtered_df
    
    def get_top_performers(self, metric='roas', top_n=10):
        """Get top performing influencers based on specified metric"""
        influencer_metrics = self.calculate_roas()
        return influencer_metrics.nlargest(top_n, metric)
    
    def get_underperformers(self, metric='roas', bottom_n=10):
        """Get underperforming influencers based on specified metric"""
        influencer_metrics = self.calculate_roas()
        return influencer_metrics.nsmallest(bottom_n, metric)
    
    def get_summary_stats(self):
        """Get overall summary statistics"""
        if self.merged_df is None:
            self.merge_data()
        
        total_revenue = self.merged_df['revenue'].sum()
        total_orders = self.merged_df['orders_x'].sum()
        total_spend = self.merged_df['total_payout'].sum()
        total_influencers = self.merged_df['influencer_id'].nunique()
        overall_roas = total_revenue / total_spend if total_spend > 0 else 0
        
        return {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'total_spend': total_spend,
            'total_influencers': total_influencers,
            'overall_roas': overall_roas,
            'avg_order_value': total_revenue / total_orders if total_orders > 0 else 0
        }

