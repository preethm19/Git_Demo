from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Database configuration
DATABASE = 'feedback.db'

def init_db():
    """Initialize the database with feedback table"""
    conn = sqlite3.connect(DATABASE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            rating INTEGER,
            feedback TEXT NOT NULL,
            category TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        feedback = request.form.get('feedback', '').strip()
        rating = request.form.get('rating', 5)
        category = request.form.get('category', 'General')
        
        # Basic validation
        if not name or not email or not feedback:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('index'))
        
        # Save to database
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO feedback (name, email, rating, feedback, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, int(rating), feedback, category))
        conn.commit()
        conn.close()
        
        flash('🎉 Thank you for your amazing feedback! Your submission has been recorded.', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        flash('❌ An error occurred while submitting your feedback. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/admin')
def admin():
    """Admin dashboard to view all submissions"""
    try:
        conn = get_db_connection()
        submissions = conn.execute('''
            SELECT * FROM feedback 
            ORDER BY timestamp DESC
        ''').fetchall()
        conn.close()
        
        return render_template('admin.html', submissions=submissions)
    except Exception as e:
        return f"Error reading submissions: {str(e)}"

@app.route('/api/feedback')
def api_feedback():
    """API endpoint to get feedback data as JSON"""
    try:
        conn = get_db_connection()
        submissions = conn.execute('''
            SELECT id, name, email, rating, feedback, category, timestamp 
            FROM feedback 
            ORDER BY timestamp DESC
        ''').fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        feedback_list = []
        for row in submissions:
            feedback_list.append({
                'id': row['id'],
                'name': row['name'],
                'email': row['email'],
                'rating': row['rating'],
                'feedback': row['feedback'],
                'category': row['category'],
                'timestamp': row['timestamp']
            })
        
        return jsonify(feedback_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    init_db()  # Initialize database on startup
    app.run(debug=True, host='0.0.0.0', port=5000)
