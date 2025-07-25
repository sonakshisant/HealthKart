from data_processor import DataProcessor

def test_data_processor():
    # Initialize processor
    processor = DataProcessor()
    
    # Load data
    print("Loading data...")
    if processor.load_data():
        print("✓ Data loaded successfully")
    else:
        print("✗ Failed to load data")
        return
    
    # Test data merging
    print("\nMerging data...")
    merged_df = processor.merge_data()
    print(f"✓ Merged data shape: {merged_df.shape}")
    
    # Test ROAS calculation
    print("\nCalculating ROAS...")
    influencer_metrics = processor.calculate_roas()
    print(f"✓ Influencer metrics shape: {influencer_metrics.shape}")
    print(f"✓ Average ROAS: {influencer_metrics['roas'].mean():.2f}")
    
    # Test campaign performance
    print("\nGetting campaign performance...")
    campaign_perf = processor.get_campaign_performance()
    print(f"✓ Campaign performance shape: {campaign_perf.shape}")
    print(campaign_perf.head())
    
    # Test product performance
    print("\nGetting product performance...")
    product_perf = processor.get_product_performance()
    print(f"✓ Product performance shape: {product_perf.shape}")
    print(product_perf.head())
    
    # Test summary stats
    print("\nGetting summary statistics...")
    summary = processor.get_summary_stats()
    print("✓ Summary statistics:")
    for key, value in summary.items():
        print(f"  {key}: {value:.2f}")
    
    # Test top performers
    print("\nGetting top performers...")
    top_performers = processor.get_top_performers(top_n=5)
    print(f"✓ Top 5 performers by ROAS:")
    print(top_performers[['name', 'roas', 'revenue', 'total_payout']].head())
    
    print("\n✓ All tests passed!")

if __name__ == '__main__':
    test_data_processor()

