import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_realistic_influencers(num_influencers=100):
    """Generate realistic influencer data with actual fitness/health categories"""
    categories = ['Fitness', 'Nutrition', 'Bodybuilding', 'Weight Loss', 'Wellness', 'Sports Nutrition']
    genders = ['Male', 'Female', 'Other']
    platforms = ['Instagram', 'YouTube', 'Twitter', 'Facebook']
    
    # Realistic influencer names
    first_names = ['Rohit', 'Priya', 'Arjun', 'Sneha', 'Vikram', 'Ananya', 'Karan', 'Pooja', 
                   'Rahul', 'Kavya', 'Amit', 'Riya', 'Siddharth', 'Meera', 'Aditya', 'Shreya',
                   'Fitness', 'Health', 'Strong', 'Fit', 'Power', 'Muscle', 'Lean', 'Active']
    last_names = ['Sharma', 'Patel', 'Singh', 'Kumar', 'Gupta', 'Agarwal', 'Jain', 'Verma',
                  'Fitness', 'Trainer', 'Coach', 'Guru', 'Expert', 'Pro', 'Champion', 'Beast']
    
    data = []
    for i in range(1, num_influencers + 1):
        first = random.choice(first_names)
        last = random.choice(last_names)
        name = f"{first}_{last}_{i}"
        
        # Realistic follower distribution
        category = np.random.choice(categories)
        platform = np.random.choice(platforms, p=[0.5, 0.3, 0.15, 0.05])  # Instagram dominant
        
        # Follower count based on platform
        if platform == 'Instagram':
            follower_count = np.random.choice([
                np.random.randint(10000, 50000),    # Micro influencers (60%)
                np.random.randint(50000, 200000),   # Mid-tier (25%)
                np.random.randint(200000, 1000000), # Macro influencers (15%)
            ], p=[0.6, 0.25, 0.15])
        elif platform == 'YouTube':
            follower_count = np.random.choice([
                np.random.randint(5000, 25000),
                np.random.randint(25000, 100000),
                np.random.randint(100000, 500000),
            ], p=[0.7, 0.2, 0.1])
        else:
            follower_count = np.random.randint(5000, 100000)
        
        data.append({
            'id': i,
            'name': name,
            'category': category,
            'gender': np.random.choice(genders, p=[0.45, 0.45, 0.1]),
            'follower_count': follower_count,
            'platform': platform
        })
    
    return pd.DataFrame(data)

def generate_realistic_posts(influencers_df, num_posts=500):
    """Generate realistic post data"""
    posts = []
    start_date = datetime(2024, 1, 1)
    
    # Realistic post captions
    captions = [
        "Transform your fitness journey with @healthkart supplements! 💪 #FitnessGoals #HealthKart",
        "Fueling my workouts with the best nutrition from @healthkart 🔥 #Nutrition #Fitness",
        "MuscleBlaze protein helping me achieve my goals! 💯 #MuscleBlaze #ProteinPower",
        "HK Vitals keeping me healthy and strong! 🌟 #HKVitals #Wellness",
        "Pre-workout game strong with @healthkart supplements! ⚡ #PreWorkout #Energy",
        "Recovery is key! Thanks @healthkart for the best supplements 🙏 #Recovery #Health",
        "Consistency + Right Nutrition = Results! @healthkart #HealthyLiving #Supplements",
        "Building muscle the right way with quality supplements! 💪 #Bodybuilding #HealthKart"
    ]
    
    for _ in range(num_posts):
        influencer = influencers_df.sample(1).iloc[0]
        post_date = start_date + timedelta(days=random.randint(0, 364))
        
        # Engagement rates based on follower count and platform
        base_engagement = 0.03  # 3% base engagement
        if influencer['follower_count'] < 50000:
            engagement_rate = random.uniform(0.05, 0.12)  # Micro influencers have higher engagement
        elif influencer['follower_count'] < 200000:
            engagement_rate = random.uniform(0.03, 0.08)
        else:
            engagement_rate = random.uniform(0.01, 0.05)  # Macro influencers have lower engagement
        
        reach = int(influencer['follower_count'] * random.uniform(0.1, 0.6))
        likes = int(reach * engagement_rate * random.uniform(0.7, 1.0))
        comments = int(likes * random.uniform(0.02, 0.08))
        
        posts.append({
            'influencer_id': influencer['id'],
            'platform': influencer['platform'],
            'date': post_date.strftime('%Y-%m-%d'),
            'url': f'http://{influencer["platform"].lower()}.com/post/{random.randint(100000, 999999)}',
            'caption': random.choice(captions),
            'reach': reach,
            'likes': likes,
            'comments': comments
        })
    
    return pd.DataFrame(posts)

def generate_realistic_tracking_data(influencers_df, num_tracking_entries=1000):
    """Generate realistic tracking data with actual HealthKart products"""
    tracking_data = []
    
    # Actual HealthKart products from their website
    products = [
        'MuscleBlaze Biozyme Performance Whey Protein',
        'MuscleBlaze PRE Workout 200 Xtreme',
        'MuscleBlaze Creatine Monohydrate',
        'HK Vitals Multivitamin',
        'HK Vitals Fish Oil',
        'HK Vitals Vitamin C Face Serum',
        'HK Vitals Skin Radiance Collagen',
        'ON Gold Standard 100% Whey Protein',
        'GNC Pro Performance Power Protein',
        'MuscleTech NitroTech Whey Protein',
        'Fuel One Whey Protein Powder',
        'TrueBasics Multivitamin',
        'Wellcore Creatine Monohydrate',
        'SteelX Protein Shaker',
        'MuscleBlaze WrathX Pre Workout'
    ]
    
    # Realistic campaigns
    campaigns = [
        'New Year Fitness Challenge',
        'Summer Body Transformation',
        'Monsoon Immunity Boost',
        'Festive Season Special',
        'Back to Gym Campaign',
        'Protein Power Month',
        'Wellness Wednesday',
        'Fitness Friday'
    ]
    
    # Product price ranges (in INR)
    product_prices = {
        'MuscleBlaze Biozyme Performance Whey Protein': (2500, 3500),
        'MuscleBlaze PRE Workout 200 Xtreme': (800, 1200),
        'MuscleBlaze Creatine Monohydrate': (600, 900),
        'HK Vitals Multivitamin': (400, 800),
        'HK Vitals Fish Oil': (500, 700),
        'HK Vitals Vitamin C Face Serum': (500, 650),
        'HK Vitals Skin Radiance Collagen': (900, 1400),
        'ON Gold Standard 100% Whey Protein': (7000, 9000),
        'GNC Pro Performance Power Protein': (2200, 3600),
        'MuscleTech NitroTech Whey Protein': (5500, 7800),
        'Fuel One Whey Protein Powder': (2200, 3300),
        'TrueBasics Multivitamin': (600, 1000),
        'Wellcore Creatine Monohydrate': (500, 800),
        'SteelX Protein Shaker': (300, 600),
        'MuscleBlaze WrathX Pre Workout': (1500, 2500)
    }
    
    start_date = datetime(2024, 1, 1)

    for _ in range(num_tracking_entries):
        influencer = influencers_df.sample(1).iloc[0]
        entry_date = start_date + timedelta(days=random.randint(0, 364))
        product = np.random.choice(products)
        
        # Orders based on influencer reach and engagement
        base_conversion = 0.001  # 0.1% base conversion rate
        if influencer['follower_count'] < 50000:
            conversion_rate = random.uniform(0.002, 0.005)  # Higher conversion for micro influencers
        else:
            conversion_rate = random.uniform(0.0005, 0.002)
        
        estimated_reach = influencer['follower_count'] * random.uniform(0.1, 0.4)
        orders = max(1, int(estimated_reach * conversion_rate))
        orders = min(orders, 50)  # Cap at 50 orders per entry
        
        # Revenue calculation
        price_range = product_prices.get(product, (500, 2000))
        unit_price = random.uniform(price_range[0], price_range[1])
        revenue = round(orders * unit_price, 2)
        
        tracking_data.append({
            'source': influencer['platform'],
            'campaign': np.random.choice(campaigns),
            'influencer_id': influencer['id'],
            'user_id': f'user_{random.randint(100000, 999999)}',
            'product': product,
            'date': entry_date.strftime('%Y-%m-%d'),
            'orders': orders,
            'revenue': revenue
        })
    
    return pd.DataFrame(tracking_data)

def generate_realistic_payouts(influencers_df, tracking_data_df):
    """Generate realistic payout data"""
    payouts = []
    
    for _, influencer in influencers_df.iterrows():
        # Payout basis based on influencer tier
        if influencer['follower_count'] < 50000:
            basis = np.random.choice(['post', 'order'], p=[0.8, 0.2])  # Micro influencers mostly per post
        elif influencer['follower_count'] < 200000:
            basis = np.random.choice(['post', 'order'], p=[0.6, 0.4])  # Mid-tier mixed
        else:
            basis = np.random.choice(['post', 'order'], p=[0.4, 0.6])  # Macro influencers more performance-based
        
        # Rate calculation based on follower count and platform
        if basis == 'post':
            if influencer['platform'] == 'Instagram':
                if influencer['follower_count'] < 50000:
                    rate = random.uniform(2000, 8000)
                elif influencer['follower_count'] < 200000:
                    rate = random.uniform(8000, 25000)
                else:
                    rate = random.uniform(25000, 100000)
            elif influencer['platform'] == 'YouTube':
                if influencer['follower_count'] < 25000:
                    rate = random.uniform(5000, 15000)
                elif influencer['follower_count'] < 100000:
                    rate = random.uniform(15000, 50000)
                else:
                    rate = random.uniform(50000, 200000)
            else:  # Twitter, Facebook
                rate = random.uniform(1000, 10000)
        else:  # per order
            rate = random.uniform(50, 300)  # Commission per order
        
        total_orders = tracking_data_df[tracking_data_df['influencer_id'] == influencer['id']]['orders'].sum()
        
        if basis == 'post':
            # Assume 1-8 posts per influencer based on campaign duration
            num_posts = random.randint(1, 8)
            total_payout = rate * num_posts
        else:
            total_payout = rate * total_orders
            
        payouts.append({
            'influencer_id': influencer['id'],
            'basis': basis,
            'rate': round(rate, 2),
            'orders': total_orders,
            'total_payout': round(total_payout, 2)
        })
    
    return pd.DataFrame(payouts)

if __name__ == '__main__':
    output_dir = '/home/ubuntu/healthkart_dashboard/data'
    os.makedirs(output_dir, exist_ok=True)

    print("Generating realistic HealthKart influencer data...")
    
    influencers_df = generate_realistic_influencers()
    posts_df = generate_realistic_posts(influencers_df)
    tracking_data_df = generate_realistic_tracking_data(influencers_df)
    payouts_df = generate_realistic_payouts(influencers_df, tracking_data_df)
    
    # Save to CSV files
    influencers_df.to_csv(os.path.join(output_dir, 'influencers.csv'), index=False)
    posts_df.to_csv(os.path.join(output_dir, 'posts.csv'), index=False)
    tracking_data_df.to_csv(os.path.join(output_dir, 'tracking_data.csv'), index=False)
    payouts_df.to_csv(os.path.join(output_dir, 'payouts.csv'), index=False)
    
    print("✅ Realistic datasets generated successfully!")
    print(f"📊 Generated {len(influencers_df)} influencers")
    print(f"📱 Generated {len(posts_df)} posts")
    print(f"📈 Generated {len(tracking_data_df)} tracking entries")
    print(f"💰 Generated {len(payouts_df)} payout records")
    
    # Display sample data
    print("\n📋 Sample Influencer Data:")
    print(influencers_df.head())
    
    print("\n🛍️ Sample Products:")
    print(tracking_data_df['product'].value_counts().head(10))
    
    print("\n💵 Revenue Summary:")
    total_revenue = tracking_data_df['revenue'].sum()
    total_orders = tracking_data_df['orders'].sum()
    print(f"Total Revenue: ₹{total_revenue:,.2f}")
    print(f"Total Orders: {total_orders:,}")
    print(f"Average Order Value: ₹{total_revenue/total_orders:.2f}")

