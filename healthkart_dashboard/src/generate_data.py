import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_influencers(num_influencers=100):
    categories = ['Fitness', 'Nutrition', 'Lifestyle', 'Beauty', 'Sports']
    genders = ['Male', 'Female', 'Other']
    platforms = ['Instagram', 'YouTube', 'Twitter']
    
    data = {
        'id': [i for i in range(1, num_influencers + 1)],
        'name': [f'Influencer_{i}' for i in range(1, num_influencers + 1)],
        'category': np.random.choice(categories, num_influencers),
        'gender': np.random.choice(genders, num_influencers),
        'follower_count': np.random.randint(10000, 1000000, num_influencers),
        'platform': np.random.choice(platforms, num_influencers, p=[0.6, 0.3, 0.1])
    }
    return pd.DataFrame(data)

def generate_posts(influencers_df, num_posts=500):
    posts = []
    start_date = datetime(2024, 1, 1)
    
    for _ in range(num_posts):
        influencer = influencers_df.sample(1).iloc[0]
        post_date = start_date + timedelta(days=random.randint(0, 364))
        
        posts.append({
            'influencer_id': influencer['id'],
            'platform': influencer['platform'],
            'date': post_date.strftime('%Y-%m-%d'),
            'url': f'http://{influencer["platform"]}.com/post/{random.randint(1000, 9999)}',
            'caption': f'Check out this amazing product from #HealthKart!',
            'reach': np.random.randint(int(influencer['follower_count'] * 0.1), int(influencer['follower_count'] * 0.5)),
            'likes': np.random.randint(100, 50000),
            'comments': np.random.randint(10, 2000)
        })
    return pd.DataFrame(posts)

def generate_tracking_data(influencers_df, num_tracking_entries=1000):
    tracking_data = []
    products = ['MuscleBlaze Whey Protein', 'HKVitals Multivitamin', 'Gritzo SuperMilk', 'MuscleBlaze Creatine', 'HKVitals Fish Oil']
    campaigns = ['SummerSale', 'NewProductLaunch', 'FitnessChallenge']
    start_date = datetime(2024, 1, 1)

    for _ in range(num_tracking_entries):
        influencer = influencers_df.sample(1).iloc[0]
        entry_date = start_date + timedelta(days=random.randint(0, 364))
        orders = random.randint(1, 50)
        revenue = round(orders * random.uniform(200, 1000), 2)
        
        tracking_data.append({
            'source': influencer['platform'],
            'campaign': np.random.choice(campaigns),
            'influencer_id': influencer['id'],
            'user_id': f'user_{random.randint(10000, 99999)}',
            'product': np.random.choice(products),
            'date': entry_date.strftime('%Y-%m-%d'),
            'orders': orders,
            'revenue': revenue
        })
    return pd.DataFrame(tracking_data)

def generate_payouts(influencers_df, tracking_data_df):
    payouts = []
    for _, influencer in influencers_df.iterrows():
        basis = np.random.choice(['post', 'order'], p=[0.7, 0.3])
        rate = round(random.uniform(500, 5000) if basis == 'post' else random.uniform(10, 50), 2)
        
        total_orders = tracking_data_df[tracking_data_df['influencer_id'] == influencer['id']]['orders'].sum()
        
        if basis == 'post':
            total_payout = rate * random.randint(1, 5) # Assume 1-5 posts per influencer
        else:
            total_payout = rate * total_orders
            
        payouts.append({
            'influencer_id': influencer['id'],
            'basis': basis,
            'rate': rate,
            'orders': total_orders,
            'total_payout': round(total_payout, 2)
        })
    return pd.DataFrame(payouts)

if __name__ == '__main__':
    output_dir = '/home/ubuntu/healthkart_dashboard/data'
    os.makedirs(output_dir, exist_ok=True)

    influencers_df = generate_influencers()
    posts_df = generate_posts(influencers_df)
    tracking_data_df = generate_tracking_data(influencers_df)
    payouts_df = generate_payouts(influencers_df, tracking_data_df)
    
    influencers_df.to_csv(os.path.join(output_dir, 'influencers.csv'), index=False)
    posts_df.to_csv(os.path.join(output_dir, 'posts.csv'), index=False)
    tracking_data_df.to_csv(os.path.join(output_dir, 'tracking_data.csv'), index=False)
    payouts_df.to_csv(os.path.join(output_dir, 'payouts.csv'), index=False)
    
    print("Simulated datasets generated successfully in the 'data' directory.")


