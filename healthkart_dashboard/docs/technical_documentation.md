# Technical Documentation
## HealthKart Influencer Marketing ROI Dashboard

**Version:** 1.0  
**Last Updated:** July 22, 2025  
**Author:** Manus AI  

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Data Models and Schema](#data-models-and-schema)
3. [API Reference](#api-reference)
4. [Database Design](#database-design)
5. [Performance Optimization](#performance-optimization)
6. [Security Implementation](#security-implementation)
7. [Testing Framework](#testing-framework)
8. [Deployment Guide](#deployment-guide)
9. [Monitoring and Logging](#monitoring-and-logging)
10. [Troubleshooting](#troubleshooting)

---

## System Architecture

### Overview

The HealthKart Influencer Marketing ROI Dashboard follows a modular, layered architecture designed for scalability, maintainability, and performance. The system is built using Python with Streamlit for the frontend and Pandas for data processing, providing a robust foundation for analytics and visualization.

### Architecture Components

#### Presentation Layer
The presentation layer is implemented using Streamlit, providing an interactive web interface for users to explore data and generate insights. This layer handles user interactions, input validation, and visualization rendering.

**Key Components:**
- `dashboard.py`: Main application entry point and UI orchestration
- Custom CSS styling with HealthKart brand theme
- Interactive filters and controls
- Real-time chart updates and data visualization

#### Business Logic Layer
The business logic layer contains all data processing, calculation, and analysis logic. This layer is designed to be independent of the presentation layer, enabling easy testing and potential migration to different frontend frameworks.

**Key Components:**
- `data_processor.py`: Core analytics engine and data manipulation
- `export_utils.py`: Report generation and data export functionality
- Calculation engines for ROI, ROAS, and performance metrics
- Data aggregation and filtering logic

#### Data Access Layer
The data access layer manages data loading, validation, and persistence. Currently implemented with CSV file handling, this layer is designed to be easily extensible to support database connections and external API integrations.

**Key Components:**
- CSV file readers and parsers
- Data validation and cleaning routines
- Error handling for data inconsistencies
- Caching mechanisms for performance optimization

### Data Flow Architecture

The system follows a unidirectional data flow pattern that ensures consistency and predictability:

1. **Data Ingestion**: Raw data is loaded from CSV files and validated
2. **Data Processing**: Business logic transforms and aggregates data
3. **Caching**: Processed data is cached for performance optimization
4. **Presentation**: UI components render visualizations and insights
5. **Export**: Users can export processed data and insights

### Scalability Considerations

The architecture is designed to handle growing data volumes and user loads through several mechanisms:

- **Caching Strategy**: Streamlit's `@st.cache_data` decorator caches expensive computations
- **Modular Design**: Components can be scaled independently
- **Database Ready**: Data access layer can be extended to support databases
- **Stateless Processing**: Business logic is stateless, enabling horizontal scaling

---

## Data Models and Schema

### Core Data Entities

#### Influencer Entity
Represents individual influencers and their profile information.

```python
class Influencer:
    id: int                    # Unique identifier
    name: str                  # Influencer name/handle
    category: str              # Content category
    gender: str                # Gender (Male/Female/Other)
    follower_count: int        # Number of followers
    platform: str              # Primary platform
```

**Validation Rules:**
- `id` must be unique and positive
- `name` must be non-empty string
- `category` must be from predefined list
- `follower_count` must be positive integer
- `platform` must be from supported platforms list

#### Post Entity
Represents individual social media posts and their performance metrics.

```python
class Post:
    influencer_id: int         # Foreign key to Influencer
    platform: str              # Platform where posted
    date: datetime             # Publication date
    url: str                   # Post URL
    caption: str               # Post caption/description
    reach: int                 # Number of people reached
    likes: int                 # Number of likes
    comments: int              # Number of comments
```

**Validation Rules:**
- `influencer_id` must reference valid influencer
- `date` must be valid datetime
- `reach`, `likes`, `comments` must be non-negative
- `url` must be valid URL format

#### Tracking Data Entity
Contains campaign tracking and conversion information.

```python
class TrackingData:
    source: str                # Traffic source platform
    campaign: str              # Campaign identifier
    influencer_id: int         # Foreign key to Influencer
    user_id: str               # Unique user identifier
    product: str               # Product name
    date: datetime             # Transaction date
    orders: int                # Number of orders
    revenue: float             # Revenue generated (INR)
```

**Validation Rules:**
- `orders` must be positive integer
- `revenue` must be positive float
- `date` must be within valid range
- `product` must be from product catalog

#### Payout Entity
Manages influencer payment information and commission structures.

```python
class Payout:
    influencer_id: int         # Foreign key to Influencer
    basis: str                 # Payment basis (post/order)
    rate: float                # Payment rate
    orders: int                # Total orders attributed
    total_payout: float        # Total payment amount (INR)
```

**Validation Rules:**
- `rate` must be positive
- `total_payout` must be non-negative
- `basis` must be 'post' or 'order'

### Data Relationships

The data model follows a relational structure with clear foreign key relationships:

- **Influencer → Posts**: One-to-many relationship
- **Influencer → Tracking Data**: One-to-many relationship  
- **Influencer → Payouts**: One-to-one relationship
- **Campaign → Tracking Data**: One-to-many relationship
- **Product → Tracking Data**: One-to-many relationship

### Data Integrity Constraints

#### Referential Integrity
- All foreign key references must point to valid parent records
- Cascade delete operations maintain consistency
- Orphaned records are prevented through validation

#### Business Logic Constraints
- Revenue must be positive for valid transactions
- ROAS calculations handle division by zero scenarios
- Date ranges must be logical and within system limits

---

## API Reference

### DataProcessor Class

The `DataProcessor` class serves as the primary interface for data manipulation and analysis operations.

#### Constructor

```python
def __init__(self, data_path='../data'):
    """
    Initialize DataProcessor with data directory path.
    
    Args:
        data_path (str): Path to directory containing CSV files
    """
```

#### Core Methods

##### load_data()
```python
def load_data(self) -> bool:
    """
    Load all CSV files and perform initial validation.
    
    Returns:
        bool: True if all files loaded successfully, False otherwise
        
    Raises:
        FileNotFoundError: If required CSV files are missing
        ValidationError: If data validation fails
    """
```

##### merge_data()
```python
def merge_data(self) -> pd.DataFrame:
    """
    Merge all datasets into a single analytical dataset.
    
    Returns:
        pd.DataFrame: Merged dataset with all relevant columns
        
    Note:
        Performs left joins to preserve all tracking data records
    """
```

##### calculate_roas()
```python
def calculate_roas(self) -> pd.DataFrame:
    """
    Calculate ROAS and Incremental ROAS for all influencers.
    
    Returns:
        pd.DataFrame: Influencer metrics with ROAS calculations
        
    Columns:
        - influencer_id, name, platform, category
        - revenue, total_payout, orders
        - roas, incremental_roas
    """
```

##### get_campaign_performance()
```python
def get_campaign_performance(self) -> pd.DataFrame:
    """
    Aggregate performance metrics by campaign.
    
    Returns:
        pd.DataFrame: Campaign-level performance metrics
        
    Columns:
        - campaign, revenue, orders, total_payout, roas
    """
```

##### filter_data()
```python
def filter_data(self, filters: dict) -> pd.DataFrame:
    """
    Apply filters to the merged dataset.
    
    Args:
        filters (dict): Filter criteria with keys:
            - platform: List of platforms to include
            - category: List of categories to include
            - campaign: List of campaigns to include
            - product: List of products to include
            - date_range: Tuple of (start_date, end_date)
    
    Returns:
        pd.DataFrame: Filtered dataset
    """
```

### Export Utilities

#### create_summary_report()
```python
def create_summary_report(processor: DataProcessor) -> dict:
    """
    Generate comprehensive summary report data.
    
    Args:
        processor: Initialized DataProcessor instance
        
    Returns:
        dict: Report data with keys:
            - summary_stats
            - campaign_performance
            - product_performance
            - platform_performance
            - top_performers
            - underperformers
            - all_influencers
    """
```

#### generate_insights_text()
```python
def generate_insights_text(processor: DataProcessor) -> str:
    """
    Generate automated insights and recommendations.
    
    Args:
        processor: Initialized DataProcessor instance
        
    Returns:
        str: Formatted markdown text with insights and recommendations
    """
```

### Error Handling

The system implements comprehensive error handling across all components:

#### Custom Exceptions
```python
class DataValidationError(Exception):
    """Raised when data validation fails"""
    pass

class CalculationError(Exception):
    """Raised when metric calculations fail"""
    pass

class ExportError(Exception):
    """Raised when export operations fail"""
    pass
```

#### Error Recovery Strategies
- Graceful degradation for missing data
- Default values for invalid calculations
- User-friendly error messages
- Logging for debugging purposes

---

## Database Design

### Current Implementation

The current implementation uses CSV files for data storage, providing simplicity and portability. However, the architecture is designed to support database migration when needed.

#### CSV File Structure
```
data/
├── influencers.csv      # Master influencer data
├── posts.csv            # Social media post metrics
├── tracking_data.csv    # Campaign tracking data
└── payouts.csv          # Payment information
```

### Database Migration Strategy

For production deployments requiring database storage, the following schema is recommended:

#### PostgreSQL Schema
```sql
-- Influencers table
CREATE TABLE influencers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    gender VARCHAR(20),
    follower_count INTEGER NOT NULL,
    platform VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    influencer_id INTEGER REFERENCES influencers(id),
    platform VARCHAR(50) NOT NULL,
    post_date DATE NOT NULL,
    url TEXT,
    caption TEXT,
    reach INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tracking data table
CREATE TABLE tracking_data (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    campaign VARCHAR(255) NOT NULL,
    influencer_id INTEGER REFERENCES influencers(id),
    user_id VARCHAR(255),
    product VARCHAR(255) NOT NULL,
    transaction_date DATE NOT NULL,
    orders INTEGER NOT NULL,
    revenue DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Payouts table
CREATE TABLE payouts (
    id SERIAL PRIMARY KEY,
    influencer_id INTEGER REFERENCES influencers(id) UNIQUE,
    basis VARCHAR(20) NOT NULL CHECK (basis IN ('post', 'order')),
    rate DECIMAL(10,2) NOT NULL,
    total_orders INTEGER DEFAULT 0,
    total_payout DECIMAL(12,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Indexes for Performance
```sql
-- Performance indexes
CREATE INDEX idx_tracking_data_influencer_date ON tracking_data(influencer_id, transaction_date);
CREATE INDEX idx_tracking_data_campaign ON tracking_data(campaign);
CREATE INDEX idx_posts_influencer_date ON posts(influencer_id, post_date);
CREATE INDEX idx_influencers_platform ON influencers(platform);
```

### Data Migration Tools

#### CSV to Database Migration
```python
def migrate_csv_to_database(csv_path: str, db_connection: str):
    """
    Migrate CSV data to database tables.
    
    Args:
        csv_path: Path to CSV files directory
        db_connection: Database connection string
    """
    # Implementation would handle:
    # - Data validation and cleaning
    # - Batch inserts for performance
    # - Error handling and rollback
    # - Progress tracking
```

---

## Performance Optimization

### Caching Strategy

The dashboard implements multiple levels of caching to optimize performance:

#### Application-Level Caching
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_and_process_data():
    """Cache expensive data loading and processing operations"""
    pass

@st.cache_data
def calculate_metrics(data_hash):
    """Cache metric calculations based on data hash"""
    pass
```

#### Data Processing Optimization
- Vectorized operations using Pandas
- Efficient groupby operations for aggregations
- Memory-efficient data types
- Lazy evaluation where possible

### Memory Management

#### Data Loading Optimization
```python
def load_large_dataset(file_path: str, chunk_size: int = 10000):
    """
    Load large datasets in chunks to manage memory usage.
    
    Args:
        file_path: Path to CSV file
        chunk_size: Number of rows per chunk
        
    Yields:
        pd.DataFrame: Data chunks
    """
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        yield chunk
```

#### Memory Profiling
```python
import psutil
import os

def get_memory_usage():
    """Get current memory usage for monitoring"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB
```

### Query Optimization

#### Efficient Filtering
```python
def optimized_filter(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Apply filters in optimal order to minimize processing.
    
    Strategy:
    1. Apply most selective filters first
    2. Use boolean indexing for performance
    3. Avoid chained operations
    """
    # Most selective filters first
    if 'date_range' in filters:
        df = df[df['date'].between(filters['date_range'][0], 
                                  filters['date_range'][1])]
    
    if 'platform' in filters:
        df = df[df['platform'].isin(filters['platform'])]
    
    return df
```

### Visualization Performance

#### Chart Optimization
```python
def create_optimized_chart(data: pd.DataFrame, max_points: int = 1000):
    """
    Create charts with data sampling for large datasets.
    
    Args:
        data: Source data
        max_points: Maximum points to display
        
    Returns:
        plotly.graph_objects.Figure: Optimized chart
    """
    if len(data) > max_points:
        # Sample data while preserving trends
        data = data.sample(n=max_points).sort_index()
    
    return create_chart(data)
```

---

## Security Implementation

### Data Security

#### Input Validation
```python
def validate_input(value: str, input_type: str) -> bool:
    """
    Validate user inputs to prevent injection attacks.
    
    Args:
        value: Input value to validate
        input_type: Type of input (date, number, text)
        
    Returns:
        bool: True if valid, False otherwise
    """
    validators = {
        'date': lambda x: pd.to_datetime(x, errors='coerce') is not pd.NaT,
        'number': lambda x: str(x).replace('.', '').isdigit(),
        'text': lambda x: len(x) < 1000 and x.isprintable()
    }
    
    return validators.get(input_type, lambda x: True)(value)
```

#### Data Sanitization
```python
def sanitize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanitize data to remove potential security risks.
    
    Args:
        df: Input DataFrame
        
    Returns:
        pd.DataFrame: Sanitized DataFrame
    """
    # Remove HTML tags and scripts
    text_columns = df.select_dtypes(include=['object']).columns
    for col in text_columns:
        df[col] = df[col].astype(str).str.replace(r'<[^>]*>', '', regex=True)
    
    return df
```

### Access Control

#### Authentication Framework
```python
def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate user credentials.
    
    Args:
        username: User identifier
        password: User password
        
    Returns:
        bool: True if authenticated, False otherwise
    """
    # Implementation would include:
    # - Password hashing verification
    # - Rate limiting for failed attempts
    # - Session management
    pass
```

#### Authorization Levels
```python
class UserRole(Enum):
    VIEWER = "viewer"
    ANALYST = "analyst"
    ADMIN = "admin"

def check_permission(user_role: UserRole, action: str) -> bool:
    """
    Check if user has permission for specific action.
    
    Args:
        user_role: User's role
        action: Action to perform
        
    Returns:
        bool: True if authorized, False otherwise
    """
    permissions = {
        UserRole.VIEWER: ['view_dashboard', 'export_data'],
        UserRole.ANALYST: ['view_dashboard', 'export_data', 'modify_filters'],
        UserRole.ADMIN: ['*']  # All permissions
    }
    
    user_permissions = permissions.get(user_role, [])
    return action in user_permissions or '*' in user_permissions
```

### Data Privacy

#### Personal Data Handling
```python
def anonymize_data(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Anonymize personal data columns.
    
    Args:
        df: Source DataFrame
        columns: Columns to anonymize
        
    Returns:
        pd.DataFrame: Anonymized DataFrame
    """
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: hashlib.sha256(
                str(x).encode()).hexdigest()[:8])
    
    return df
```

---

## Testing Framework

### Unit Testing

#### Test Structure
```python
import unittest
from unittest.mock import Mock, patch
import pandas as pd
from src.data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = DataProcessor()
        self.sample_data = self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data for testing"""
        return {
            'influencers': pd.DataFrame({
                'id': [1, 2, 3],
                'name': ['Test1', 'Test2', 'Test3'],
                'platform': ['Instagram', 'YouTube', 'Twitter']
            }),
            'tracking_data': pd.DataFrame({
                'influencer_id': [1, 2, 3],
                'revenue': [1000, 2000, 1500],
                'orders': [10, 20, 15]
            })
        }
    
    def test_roas_calculation(self):
        """Test ROAS calculation accuracy"""
        # Test implementation
        pass
    
    def test_data_filtering(self):
        """Test data filtering functionality"""
        # Test implementation
        pass
```

### Integration Testing

#### End-to-End Tests
```python
class TestDashboardIntegration(unittest.TestCase):
    
    def test_complete_workflow(self):
        """Test complete data processing workflow"""
        # 1. Load data
        # 2. Process and calculate metrics
        # 3. Apply filters
        # 4. Generate exports
        # 5. Verify results
        pass
    
    def test_error_handling(self):
        """Test error handling in complete workflow"""
        # Test with invalid data
        # Test with missing files
        # Test with corrupted data
        pass
```

### Performance Testing

#### Load Testing
```python
def test_performance_with_large_dataset():
    """Test performance with large datasets"""
    import time
    
    # Generate large dataset
    large_data = generate_test_data(size=100000)
    
    start_time = time.time()
    processor = DataProcessor()
    processor.load_data_from_dataframe(large_data)
    metrics = processor.calculate_roas()
    end_time = time.time()
    
    # Assert performance requirements
    assert end_time - start_time < 30  # Should complete in 30 seconds
    assert len(metrics) == expected_count
```

### Test Data Generation

#### Realistic Test Data
```python
def generate_test_data(size: int = 1000) -> dict:
    """
    Generate realistic test data for testing.
    
    Args:
        size: Number of records to generate
        
    Returns:
        dict: Test datasets
    """
    # Generate realistic influencer data
    # Generate corresponding posts and tracking data
    # Ensure data consistency and relationships
    pass
```

---

## Deployment Guide

### Local Development Setup

#### Environment Setup
```bash
# Create virtual environment
python -m venv healthkart_dashboard_env
source healthkart_dashboard_env/bin/activate  # Linux/Mac
# or
healthkart_dashboard_env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
cd src
streamlit run dashboard.py
```

#### Development Configuration
```python
# config/development.py
DEBUG = True
DATA_PATH = '../data'
CACHE_TTL = 300  # 5 minutes for development
LOG_LEVEL = 'DEBUG'
```

### Production Deployment

#### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
CMD ["streamlit", "run", "src/dashboard.py", "--server.address", "0.0.0.0"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - ENVIRONMENT=production
      - DATA_PATH=/app/data
    volumes:
      - ./data:/app/data:ro
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - dashboard
    restart: unless-stopped
```

#### Cloud Deployment (AWS)
```yaml
# docker-compose.aws.yml
version: '3.8'

services:
  dashboard:
    image: your-registry/healthkart-dashboard:latest
    ports:
      - "8501:8501"
    environment:
      - AWS_REGION=us-west-2
      - S3_BUCKET=healthkart-dashboard-data
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

### Environment Configuration

#### Production Configuration
```python
# config/production.py
DEBUG = False
DATA_PATH = '/app/data'
CACHE_TTL = 3600  # 1 hour for production
LOG_LEVEL = 'INFO'
ALLOWED_HOSTS = ['dashboard.healthkart.com']
SSL_REQUIRED = True
```

#### Environment Variables
```bash
# .env file
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@localhost/healthkart_dashboard
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
SENTRY_DSN=your-sentry-dsn-here
```

---

## Monitoring and Logging

### Application Monitoring

#### Health Checks
```python
def health_check() -> dict:
    """
    Perform application health check.
    
    Returns:
        dict: Health status information
    """
    status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'checks': {}
    }
    
    # Check data availability
    try:
        processor = DataProcessor()
        processor.load_data()
        status['checks']['data'] = 'healthy'
    except Exception as e:
        status['checks']['data'] = f'unhealthy: {str(e)}'
        status['status'] = 'unhealthy'
    
    # Check memory usage
    memory_usage = get_memory_usage()
    if memory_usage > 1000:  # MB
        status['checks']['memory'] = f'warning: {memory_usage}MB'
    else:
        status['checks']['memory'] = 'healthy'
    
    return status
```

#### Performance Metrics
```python
import time
from functools import wraps

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Log performance metrics
        logger.info(f"{func.__name__} executed in {end_time - start_time:.2f}s")
        
        return result
    return wrapper
```

### Logging Configuration

#### Structured Logging
```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log(self, level: str, message: str, **kwargs):
        """Log structured message"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            **kwargs
        }
        
        self.logger.info(json.dumps(log_entry))
```

#### Error Tracking
```python
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

def setup_error_tracking():
    """Setup error tracking with Sentry"""
    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR
    )
    
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[sentry_logging],
        traces_sample_rate=0.1,
        environment=os.getenv('ENVIRONMENT', 'development')
    )
```

---

## Troubleshooting

### Common Issues

#### Data Loading Problems
```python
def diagnose_data_issues():
    """Diagnose common data loading problems"""
    issues = []
    
    # Check file existence
    required_files = ['influencers.csv', 'posts.csv', 'tracking_data.csv', 'payouts.csv']
    for file in required_files:
        if not os.path.exists(f'../data/{file}'):
            issues.append(f"Missing file: {file}")
    
    # Check file permissions
    for file in required_files:
        if os.path.exists(f'../data/{file}') and not os.access(f'../data/{file}', os.R_OK):
            issues.append(f"Permission denied: {file}")
    
    # Check data format
    try:
        pd.read_csv('../data/influencers.csv')
    except Exception as e:
        issues.append(f"Invalid CSV format in influencers.csv: {str(e)}")
    
    return issues
```

#### Performance Issues
```python
def diagnose_performance():
    """Diagnose performance issues"""
    diagnostics = {}
    
    # Memory usage
    diagnostics['memory_usage'] = get_memory_usage()
    
    # Data size
    try:
        processor = DataProcessor()
        processor.load_data()
        diagnostics['data_size'] = len(processor.merged_df)
    except Exception as e:
        diagnostics['data_load_error'] = str(e)
    
    # Cache status
    diagnostics['cache_info'] = st.cache_data.get_stats()
    
    return diagnostics
```

### Debug Mode

#### Enable Debug Logging
```python
def enable_debug_mode():
    """Enable comprehensive debug logging"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('debug.log'),
            logging.StreamHandler()
        ]
    )
    
    # Enable Streamlit debug mode
    st.set_option('client.showErrorDetails', True)
```

#### Data Validation Tools
```python
def validate_data_integrity():
    """Comprehensive data validation"""
    validation_results = {}
    
    processor = DataProcessor()
    processor.load_data()
    
    # Check for missing values
    validation_results['missing_values'] = {
        'influencers': processor.influencers_df.isnull().sum().to_dict(),
        'posts': processor.posts_df.isnull().sum().to_dict(),
        'tracking_data': processor.tracking_data_df.isnull().sum().to_dict(),
        'payouts': processor.payouts_df.isnull().sum().to_dict()
    }
    
    # Check data consistency
    merged_df = processor.merge_data()
    validation_results['data_consistency'] = {
        'total_revenue_match': abs(
            merged_df['revenue'].sum() - 
            processor.tracking_data_df['revenue'].sum()
        ) < 0.01,
        'influencer_count_match': len(merged_df['influencer_id'].unique()) <= len(processor.influencers_df)
    }
    
    return validation_results
```

---

**Document Version:** 1.0  
**Last Updated:** July 22, 2025  
**Next Review:** October 2025  

*This technical documentation is maintained alongside the codebase and should be updated with any architectural changes or new features.*

