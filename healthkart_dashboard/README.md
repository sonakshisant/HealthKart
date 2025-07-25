# HealthKart Influencer Marketing ROI Dashboard

![HealthKart Logo](src/healthkart_logo.png)

A comprehensive, open-source dashboard for tracking and analyzing the Return on Investment (ROI) of influencer marketing campaigns for HealthKart. This dashboard provides data-driven insights to optimize influencer partnerships and maximize campaign effectiveness.

## 🎯 Overview

The HealthKart Influencer Marketing ROI Dashboard is designed to help marketing teams track, analyze, and optimize their influencer campaigns across multiple platforms including Instagram, YouTube, Twitter, and Facebook. The dashboard provides real-time insights into campaign performance, influencer effectiveness, and return on investment metrics.

### Key Features

- **📊 Comprehensive Analytics**: Track campaign performance across multiple metrics including reach, engagement, orders, and revenue
- **💰 ROI Calculation**: Automated calculation of ROAS (Return on Ad Spend) and Incremental ROAS
- **👥 Influencer Insights**: Detailed analysis of influencer performance, including top performers and underperformers
- **🎯 Campaign Tracking**: Monitor campaign effectiveness across different products and time periods
- **📱 Platform Analysis**: Compare performance across Instagram, YouTube, Twitter, and other social platforms
- **💳 Payout Management**: Track influencer payments and commission structures
- **📈 Data Visualization**: Interactive charts and graphs powered by Plotly
- **📤 Export Capabilities**: Download insights and data in CSV and PDF formats
- **🔍 Advanced Filtering**: Filter data by platform, category, campaign, product, and date range

## 🏗️ Architecture

The dashboard is built using a modern Python stack with the following components:

- **Frontend**: Streamlit for interactive web interface
- **Backend**: Python with Pandas for data processing
- **Visualization**: Plotly for interactive charts and graphs
- **Data Storage**: CSV files (easily extensible to databases)
- **Styling**: Custom CSS with HealthKart brand colors and theme

## 📁 Project Structure

```
healthkart_dashboard/
├── data/                          # Data files
│   ├── influencers.csv           # Influencer profiles and metadata
│   ├── posts.csv                 # Social media post data
│   ├── tracking_data.csv         # Campaign tracking and conversion data
│   └── payouts.csv               # Influencer payment information
├── src/                          # Source code
│   ├── dashboard.py              # Main Streamlit application
│   ├── data_processor.py         # Data processing and analytics engine
│   ├── export_utils.py           # Export functionality
│   ├── generate_data.py          # Original data generator
│   ├── generate_realistic_data.py # Realistic HealthKart data generator
│   ├── test_dashboard.py         # Comprehensive test suite
│   └── healthkart_logo.png       # HealthKart logo
├── docs/                         # Documentation
├── README.md                     # This file
└── todo.md                       # Development progress tracker
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd healthkart_dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit plotly pandas numpy
   ```

3. **Generate sample data** (optional)
   ```bash
   cd src
   python generate_realistic_data.py
   ```

4. **Run the dashboard**
   ```bash
   cd src
   streamlit run dashboard.py
   ```

5. **Access the dashboard**
   Open your browser and navigate to `http://localhost:8501`

## 📊 Data Models

### Influencers Dataset
Contains information about influencers and their social media presence.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Unique influencer identifier |
| name | String | Influencer name/handle |
| category | String | Content category (Fitness, Nutrition, etc.) |
| gender | String | Gender (Male, Female, Other) |
| follower_count | Integer | Number of followers |
| platform | String | Primary platform (Instagram, YouTube, etc.) |

### Posts Dataset
Tracks individual social media posts and their performance metrics.

| Column | Type | Description |
|--------|------|-------------|
| influencer_id | Integer | Reference to influencer |
| platform | String | Platform where post was published |
| date | Date | Post publication date |
| url | String | Post URL |
| caption | String | Post caption/description |
| reach | Integer | Number of people reached |
| likes | Integer | Number of likes |
| comments | Integer | Number of comments |

### Tracking Data Dataset
Contains campaign tracking and conversion data.

| Column | Type | Description |
|--------|------|-------------|
| source | String | Traffic source platform |
| campaign | String | Campaign name |
| influencer_id | Integer | Reference to influencer |
| user_id | String | Unique user identifier |
| product | String | Product name |
| date | Date | Transaction date |
| orders | Integer | Number of orders |
| revenue | Float | Revenue generated (INR) |

### Payouts Dataset
Manages influencer payment information and commission structures.

| Column | Type | Description |
|--------|------|-------------|
| influencer_id | Integer | Reference to influencer |
| basis | String | Payment basis (post/order) |
| rate | Float | Payment rate |
| orders | Integer | Total orders attributed |
| total_payout | Float | Total payment amount (INR) |

## 🎨 Dashboard Features

### Overview Page
The main dashboard provides a comprehensive view of campaign performance with:

- **Key Metrics**: Total revenue, orders, ROAS, and influencer count
- **Trend Analysis**: Daily revenue and ROAS trends over time
- **Platform Distribution**: Revenue breakdown by social media platform
- **Campaign Performance**: Revenue comparison across different campaigns

### Campaign Performance
Detailed analysis of individual campaigns including:

- **Campaign Metrics Table**: Comprehensive performance data for each campaign
- **Revenue vs Spend Analysis**: Visual comparison of investment and returns
- **ROAS by Campaign**: Return on ad spend for each campaign
- **Product Performance**: Analysis of which products perform best in campaigns

### ROI & ROAS Analysis
Advanced financial metrics and analysis:

- **ROAS Distribution**: Histogram showing the distribution of returns across influencers
- **Revenue vs ROAS Scatter Plot**: Correlation between revenue generation and efficiency
- **Platform Comparison**: Average ROAS by social media platform
- **Category Analysis**: Performance breakdown by content category

### Influencer Insights
Comprehensive influencer performance analysis:

- **Top Performers**: Highest ROAS influencers with detailed metrics
- **Underperformers**: Lowest ROAS influencers for optimization opportunities
- **Follower Count Analysis**: Correlation between follower count and performance
- **Engagement Analysis**: Relationship between engagement rates and ROI
- **Demographics**: Performance breakdown by gender and category

### Payout Tracking
Financial management and payment tracking:

- **Payment Summary**: Total spend and average payout per influencer
- **Payment Basis Analysis**: Comparison of per-post vs per-order payment models
- **Payout Efficiency**: Analysis of payment effectiveness and ROI
- **Detailed Payment Records**: Comprehensive payout information for all influencers

## 🔧 Configuration

### Customizing Brand Colors
The dashboard uses HealthKart's brand colors. To customize:

1. Edit the CSS in `src/dashboard.py`
2. Update the color variables:
   - Primary: `#2E5A87` (HealthKart Blue)
   - Secondary: `#00BCD4` (HealthKart Cyan)
   - Accent: `#FF6B35` (HealthKart Orange)

### Adding New Data Sources
To integrate with external data sources:

1. Modify `data_processor.py` to add new data loading methods
2. Update the data models to accommodate new fields
3. Extend the dashboard pages to display new metrics

### Customizing Metrics
To add new KPIs or modify existing calculations:

1. Update the calculation methods in `data_processor.py`
2. Add new visualization components in `dashboard.py`
3. Update the export functionality in `export_utils.py`

## 📈 Key Metrics Explained

### ROAS (Return on Ad Spend)
```
ROAS = Total Revenue / Total Ad Spend
```
Measures the direct return on advertising investment. A ROAS of 3.0 means every ₹1 spent generates ₹3 in revenue.

### Incremental ROAS
```
Incremental ROAS = (Campaign Revenue - Baseline Revenue) / Ad Spend
```
Measures the additional revenue generated beyond what would have occurred naturally, providing a more accurate picture of campaign effectiveness.

### Engagement Rate
```
Engagement Rate = (Likes + Comments) / Reach × 100
```
Measures how actively the audience interacts with content, indicating content quality and audience interest.

### Conversion Rate
```
Conversion Rate = Orders / Reach × 100
```
Measures the percentage of people who saw the content and made a purchase, indicating campaign effectiveness.

## 🧪 Testing

The dashboard includes a comprehensive test suite covering:

- **Data Loading**: Verification of CSV file loading and parsing
- **Data Processing**: Testing of all calculation methods and aggregations
- **Filtering**: Validation of data filtering functionality
- **Export Functions**: Testing of CSV and PDF export capabilities
- **Data Integrity**: Ensuring consistency across different data views

Run the test suite:
```bash
cd src
python test_dashboard.py
```

## 📤 Export Capabilities

### CSV Export
- Campaign performance data
- Product performance metrics
- Influencer performance data
- Complete dataset exports

### Insights Report
- Automated insights generation
- Executive summary with key findings
- Recommendations based on data analysis
- Downloadable markdown format

## 🔒 Security Considerations

- **Data Privacy**: All data is processed locally; no external data transmission
- **Access Control**: Dashboard runs locally by default; implement authentication for production use
- **Data Validation**: Input validation and sanitization for all user inputs
- **Error Handling**: Comprehensive error handling to prevent data corruption

## 🚀 Deployment Options

### Local Development
```bash
streamlit run src/dashboard.py
```

### Production Deployment
For production deployment, consider:

1. **Streamlit Cloud**: Easy deployment with GitHub integration
2. **Docker**: Containerized deployment for scalability
3. **Cloud Platforms**: AWS, GCP, or Azure for enterprise deployment
4. **Reverse Proxy**: Nginx or Apache for custom domain and SSL

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "src/dashboard.py", "--server.address", "0.0.0.0"]
```

## 🤝 Contributing

We welcome contributions to improve the dashboard. Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Make your changes** and add tests
4. **Run the test suite** to ensure everything works
5. **Submit a pull request** with a clear description of changes

### Development Guidelines
- Follow PEP 8 style guidelines for Python code
- Add tests for new functionality
- Update documentation for any new features
- Use meaningful commit messages

## 📝 License

This project is open-source and available under the MIT License. See the LICENSE file for more details.

## 🆘 Support

For support and questions:

1. **Documentation**: Check this README and inline code comments
2. **Issues**: Create a GitHub issue for bugs or feature requests
3. **Testing**: Run the test suite to diagnose problems
4. **Community**: Join discussions in the project repository

## 🔮 Future Enhancements

Planned features for future releases:

- **Real-time Data Integration**: Connect with social media APIs for live data
- **Machine Learning**: Predictive analytics for campaign optimization
- **Advanced Segmentation**: More sophisticated audience and performance analysis
- **Mobile App**: Native mobile application for on-the-go monitoring
- **API Integration**: RESTful API for external system integration
- **Advanced Reporting**: Scheduled reports and automated insights delivery

## 📊 Sample Insights

Based on the realistic data generated for HealthKart:

- **Top Performing Platform**: Instagram shows the highest ROAS at 2.1x
- **Best Product Category**: Sports Nutrition products generate 35% higher revenue per campaign
- **Optimal Influencer Size**: Micro-influencers (10K-50K followers) show 40% higher engagement rates
- **Payment Model**: Per-order payments show 25% better ROI than per-post payments for macro-influencers
- **Seasonal Trends**: Fitness campaigns perform 60% better during January and summer months

---

**Built with ❤️ for HealthKart by Sonakshi**

*Last updated: July 2025*

