# 🗄️ Database Access Guide

## Overview
The Creative Feedback Hub uses SQLite database to store all feedback submissions. This guide explains how to access and interact with the database.

## Database Schema

### Table: `feedback`
```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    rating INTEGER,
    feedback TEXT NOT NULL,
    category TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Access Methods

### 1. 🌐 Web Interface Access

#### Admin Dashboard
- **URL**: `http://localhost:5000/admin`
- **Description**: Visual dashboard showing all feedback submissions
- **Features**: 
  - User-friendly cards layout
  - Rating display with stars
  - Category badges
  - Timestamp information
  - Responsive design

#### Statistics Dashboard  
- **URL**: `http://localhost:5000/stats`
- **Description**: Analytics and insights dashboard
- **Features**:
  - Total feedback count
  - Average rating
  - Satisfaction rate percentage
  - Interactive charts (Chart.js)
  - Rating distribution
  - Category breakdown

### 2. 🔌 API Access

#### Get All Feedback (JSON)
```http
GET http://localhost:5000/api/feedback
```

**Response Format:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "rating": 5,
    "feedback": "Great experience!",
    "category": "General",
    "timestamp": "2025-10-17 19:55:00"
  }
]
```

**Use Cases:**
- External integrations
- Data export
- Third-party analytics
- Mobile app integration

### 3. 💻 Direct Database Access

#### Using SQLite Command Line
```bash
# Navigate to app directory
cd feedback_app

# Open database
sqlite3 feedback.db

# View all tables
.tables

# View table schema
.schema feedback

# Query all feedback
SELECT * FROM feedback ORDER BY timestamp DESC;

# Query by rating
SELECT * FROM feedback WHERE rating >= 4;

# Query by category
SELECT * FROM feedback WHERE category = 'Bug Report';

# Get statistics
SELECT 
    COUNT(*) as total_feedback,
    AVG(rating) as avg_rating,
    MAX(timestamp) as latest_submission
FROM feedback;

# Exit SQLite
.quit
```

#### Using Python Script
```python
import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('feedback.db')
conn.row_factory = sqlite3.Row  # Enable column access by name
cursor = conn.cursor()

# Get all feedback
cursor.execute("SELECT * FROM feedback ORDER BY timestamp DESC")
feedback_list = cursor.fetchall()

for feedback in feedback_list:
    print(f"ID: {feedback['id']}")
    print(f"Name: {feedback['name']}")
    print(f"Email: {feedback['email']}")
    print(f"Rating: {feedback['rating']}/5")
    print(f"Category: {feedback['category']}")
    print(f"Feedback: {feedback['feedback']}")
    print(f"Timestamp: {feedback['timestamp']}")
    print("-" * 50)

# Get statistics
cursor.execute("""
    SELECT 
        COUNT(*) as total,
        AVG(rating) as avg_rating,
        category,
        COUNT(*) as category_count
    FROM feedback 
    GROUP BY category
""")
stats = cursor.fetchall()

print("Statistics by Category:")
for stat in stats:
    print(f"{stat['category']}: {stat['category_count']} submissions")

conn.close()
```

## Database Operations

### 🔍 Common Queries

#### Filter by Date Range
```sql
SELECT * FROM feedback 
WHERE timestamp BETWEEN '2025-10-01' AND '2025-10-31'
ORDER BY timestamp DESC;
```

#### High Rating Feedback
```sql
SELECT name, email, rating, feedback 
FROM feedback 
WHERE rating >= 4
ORDER BY rating DESC, timestamp DESC;
```

#### Category Analysis
```sql
SELECT 
    category,
    COUNT(*) as count,
    AVG(rating) as avg_rating,
    MIN(timestamp) as first_submission,
    MAX(timestamp) as last_submission
FROM feedback 
GROUP BY category
ORDER BY count DESC;
```

#### Recent Feedback (Last 7 days)
```sql
SELECT * FROM feedback 
WHERE timestamp >= datetime('now', '-7 days')
ORDER BY timestamp DESC;
```

### 📊 Analytics Queries

#### Rating Distribution
```sql
SELECT 
    rating,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM feedback), 2) as percentage
FROM feedback 
GROUP BY rating 
ORDER BY rating DESC;
```

#### Monthly Trends
```sql
SELECT 
    strftime('%Y-%m', timestamp) as month,
    COUNT(*) as submissions,
    AVG(rating) as avg_rating
FROM feedback 
GROUP BY strftime('%Y-%m', timestamp)
ORDER BY month DESC;
```

### 🛠️ Maintenance Operations

#### Backup Database
```bash
# Create backup
sqlite3 feedback.db ".backup backup_$(date +%Y%m%d).db"

# Or copy file
cp feedback.db feedback_backup_$(date +%Y%m%d).db
```

#### Export to CSV
```sql
.headers on
.mode csv
.output feedback_export.csv
SELECT * FROM feedback ORDER BY timestamp DESC;
.output stdout
```

#### Clean Old Data (if needed)
```sql
-- Delete feedback older than 1 year
DELETE FROM feedback 
WHERE timestamp < datetime('now', '-1 year');

-- Vacuum to reclaim space
VACUUM;
```

## Security Considerations

### 🔒 Data Protection
- Database file is stored locally (`feedback.db`)
- No external database credentials needed
- SQLite handles concurrent access automatically
- Consider encryption for sensitive data

### 🚨 Access Control
- Admin dashboard has no authentication (add if needed)
- API endpoint is publicly accessible
- Consider adding API keys for production
- Implement rate limiting for API calls

### 🔐 Production Recommendations
```python
# Add to app.py for production
from functools import wraps
from flask import request, abort

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != 'your-secret-api-key':
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/feedback')
@require_api_key
def api_feedback():
    # Your existing code
```

## Integration Examples

### 📱 JavaScript Fetch
```javascript
// Get all feedback
fetch('/api/feedback')
    .then(response => response.json())
    .then(data => {
        console.log('Feedback data:', data);
        // Process data
    })
    .catch(error => console.error('Error:', error));
```

### 🐍 Python Requests
```python
import requests

# Get feedback data
response = requests.get('http://localhost:5000/api/feedback')
if response.status_code == 200:
    feedback_data = response.json()
    print(f"Retrieved {len(feedback_data)} feedback entries")
else:
    print(f"Error: {response.status_code}")
```

### 📊 Data Analysis with Pandas
```python
import pandas as pd
import sqlite3

# Load data into DataFrame
conn = sqlite3.connect('feedback.db')
df = pd.read_sql_query("SELECT * FROM feedback", conn)

# Basic analysis
print(df.describe())
print(df['category'].value_counts())
print(df.groupby('rating')['feedback'].count())

# Visualizations
import matplotlib.pyplot as plt
df['rating'].hist(bins=5)
plt.title('Rating Distribution')
plt.show()

conn.close()
```

## Troubleshooting

### Common Issues

#### Database Locked
```python
# If you get "database is locked" error
import time
import sqlite3

def safe_db_operation():
    for attempt in range(5):
        try:
            conn = sqlite3.connect('feedback.db', timeout=20.0)
            # Your operation here
            conn.close()
            break
        except sqlite3.OperationalError as e:
            if "locked" in str(e):
                time.sleep(1)
                continue
            raise
```

#### Missing Database
The database is created automatically when the app starts. If missing:
```python
python -c "from app import init_db; init_db()"
```

#### Corrupted Database
```bash
# Check integrity
sqlite3 feedback.db "PRAGMA integrity_check;"

# If corrupted, restore from backup
cp feedback_backup_YYYYMMDD.db feedback.db
```

---

## 📞 Support

For additional help:
1. Check the Flask application logs
2. Verify database file permissions
3. Ensure SQLite3 is installed
4. Test with simple queries first

**Database Location**: `feedback_app/feedback.db`
**Backup Recommended**: Daily for production use
**Access Level**: Full read/write access via multiple methods
