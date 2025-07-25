import unittest
import pandas as pd
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_processor import DataProcessor
from export_utils import create_summary_report, generate_insights_text

class TestDataProcessor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = DataProcessor()
        self.assertTrue(self.processor.load_data(), "Failed to load test data")
        
    def test_data_loading(self):
        """Test data loading functionality"""
        self.assertIsNotNone(self.processor.influencers_df)
        self.assertIsNotNone(self.processor.posts_df)
        self.assertIsNotNone(self.processor.tracking_data_df)
        self.assertIsNotNone(self.processor.payouts_df)
        
        # Check data shapes
        self.assertEqual(len(self.processor.influencers_df), 100)
        self.assertEqual(len(self.processor.posts_df), 500)
        self.assertEqual(len(self.processor.tracking_data_df), 1000)
        self.assertEqual(len(self.processor.payouts_df), 100)
        
    def test_data_merging(self):
        """Test data merging functionality"""
        merged_df = self.processor.merge_data()
        self.assertIsNotNone(merged_df)
        self.assertEqual(len(merged_df), 1000)  # Should match tracking_data length
        
        # Check that all required columns are present
        required_columns = ['influencer_id', 'revenue', 'orders_x', 'total_payout', 'name', 'platform']
        for col in required_columns:
            self.assertIn(col, merged_df.columns)
            
    def test_roas_calculation(self):
        """Test ROAS calculation"""
        influencer_metrics = self.processor.calculate_roas()
        self.assertIsNotNone(influencer_metrics)
        self.assertEqual(len(influencer_metrics), 100)  # Should have metrics for all influencers
        
        # Check that ROAS values are calculated
        self.assertIn('roas', influencer_metrics.columns)
        self.assertIn('incremental_roas', influencer_metrics.columns)
        self.assertTrue(all(influencer_metrics['roas'] >= 0))  # ROAS should be non-negative
        
    def test_campaign_performance(self):
        """Test campaign performance metrics"""
        campaign_perf = self.processor.get_campaign_performance()
        self.assertIsNotNone(campaign_perf)
        self.assertEqual(len(campaign_perf), 3)  # Should have 3 campaigns
        
        # Check required columns
        required_columns = ['campaign', 'revenue', 'orders', 'total_payout', 'roas']
        for col in required_columns:
            self.assertIn(col, campaign_perf.columns)
            
    def test_product_performance(self):
        """Test product performance metrics"""
        product_perf = self.processor.get_product_performance()
        self.assertIsNotNone(product_perf)
        self.assertEqual(len(product_perf), 5)  # Should have 5 products
        
        # Check required columns
        required_columns = ['product', 'revenue', 'orders', 'total_payout', 'roas']
        for col in required_columns:
            self.assertIn(col, product_perf.columns)
            
    def test_platform_performance(self):
        """Test platform performance metrics"""
        platform_perf = self.processor.get_platform_performance()
        self.assertIsNotNone(platform_perf)
        self.assertEqual(len(platform_perf), 3)  # Should have 3 platforms
        
        # Check required columns
        required_columns = ['platform', 'revenue', 'orders', 'total_payout', 'roas']
        for col in required_columns:
            self.assertIn(col, platform_perf.columns)
            
    def test_filtering(self):
        """Test data filtering functionality"""
        # Test platform filter
        filters = {'platform': ['Instagram']}
        filtered_df = self.processor.filter_data(filters)
        self.assertTrue(all(filtered_df['platform'] == 'Instagram'))
        
        # Test category filter
        filters = {'category': ['Fitness']}
        filtered_df = self.processor.filter_data(filters)
        self.assertTrue(all(filtered_df['category'] == 'Fitness'))
        
    def test_summary_stats(self):
        """Test summary statistics calculation"""
        summary = self.processor.get_summary_stats()
        self.assertIsNotNone(summary)
        
        # Check required keys
        required_keys = ['total_revenue', 'total_orders', 'total_spend', 'total_influencers', 'overall_roas']
        for key in required_keys:
            self.assertIn(key, summary)
            self.assertGreater(summary[key], 0)  # All values should be positive
            
    def test_top_performers(self):
        """Test top performers functionality"""
        top_performers = self.processor.get_top_performers(metric='roas', top_n=5)
        self.assertIsNotNone(top_performers)
        self.assertEqual(len(top_performers), 5)
        
        # Check that results are sorted in descending order
        roas_values = top_performers['roas'].tolist()
        self.assertEqual(roas_values, sorted(roas_values, reverse=True))
        
    def test_underperformers(self):
        """Test underperformers functionality"""
        underperformers = self.processor.get_underperformers(metric='roas', bottom_n=5)
        self.assertIsNotNone(underperformers)
        self.assertEqual(len(underperformers), 5)
        
        # Check that results are sorted in ascending order
        roas_values = underperformers['roas'].tolist()
        self.assertEqual(roas_values, sorted(roas_values))

class TestExportUtils(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = DataProcessor()
        self.assertTrue(self.processor.load_data(), "Failed to load test data")
        
    def test_summary_report_generation(self):
        """Test summary report generation"""
        report_data = create_summary_report(self.processor)
        self.assertIsNotNone(report_data)
        
        # Check that all required sections are present
        required_sections = ['summary_stats', 'campaign_performance', 'product_performance', 
                           'platform_performance', 'top_performers', 'underperformers', 'all_influencers']
        for section in required_sections:
            self.assertIn(section, report_data)
            
    def test_insights_generation(self):
        """Test insights text generation"""
        insights_text = generate_insights_text(self.processor)
        self.assertIsNotNone(insights_text)
        self.assertIsInstance(insights_text, str)
        self.assertGreater(len(insights_text), 100)  # Should be a substantial report
        
        # Check that key sections are present
        self.assertIn("Executive Summary", insights_text)
        self.assertIn("Campaign Performance Insights", insights_text)
        self.assertIn("Platform Performance Insights", insights_text)
        self.assertIn("Recommendations", insights_text)

class TestDataIntegrity(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = DataProcessor()
        self.assertTrue(self.processor.load_data(), "Failed to load test data")
        
    def test_data_consistency(self):
        """Test data consistency across different aggregations"""
        # Test that total revenue is consistent across different views
        summary = self.processor.get_summary_stats()
        campaign_perf = self.processor.get_campaign_performance()
        product_perf = self.processor.get_product_performance()
        
        # Revenue should be consistent
        campaign_total = campaign_perf['revenue'].sum()
        product_total = product_perf['revenue'].sum()
        
        # Allow for small floating point differences
        self.assertAlmostEqual(campaign_total, product_total, places=2)
        self.assertAlmostEqual(campaign_total, summary['total_revenue'], places=2)
        
    def test_roas_calculation_accuracy(self):
        """Test ROAS calculation accuracy"""
        influencer_metrics = self.processor.calculate_roas()
        
        # Manually calculate ROAS for first influencer and compare
        first_influencer = influencer_metrics.iloc[0]
        manual_roas = first_influencer['revenue'] / first_influencer['total_payout']
        calculated_roas = first_influencer['roas']
        
        self.assertAlmostEqual(manual_roas, calculated_roas, places=6)
        
    def test_no_missing_data(self):
        """Test that there's no unexpected missing data"""
        merged_df = self.processor.merge_data()
        
        # Check for missing values in critical columns
        critical_columns = ['revenue', 'total_payout', 'influencer_id']
        for col in critical_columns:
            missing_count = merged_df[col].isnull().sum()
            self.assertEqual(missing_count, 0, f"Found {missing_count} missing values in {col}")

if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)

