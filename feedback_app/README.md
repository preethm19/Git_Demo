# Feedback Form Application

A simple, modern feedback form built with Flask that collects user feedback and saves it to a text file.

## Features

- 📝 Clean, responsive feedback form
- ⭐ Star rating system (1-5 stars)
- 💾 Automatic saving to `submissions.txt`
- ✅ Form validation and flash messages
- 📱 Mobile-friendly design
- 🎨 Modern gradient UI with animations

## Directory Structure

```
feedback_app/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── submissions.txt        # Auto-created on first submission
├── templates/
│   └── index.html        # Main feedback form template
└── static/
    └── style.css         # CSS styling
```

## Installation & Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser and visit:**
   ```
   http://localhost:5000
   ```

## Usage

### Main Form
- Fill out the feedback form at `http://localhost:5000`
- All fields marked with * are required
- Select a rating from 1-5 stars
- Submit your feedback

### Admin View
- View all submissions at `http://localhost:5000/admin`
- Raw text format showing all feedback entries

### Submissions File
- All feedback is automatically saved to `submissions.txt`
- Each submission includes timestamp, name, email, rating, and feedback
- File is created automatically on the first submission

## Form Fields

- **Name** (required): User's full name
- **Email** (required): User's email address
- **Rating** (optional): 1-5 star rating (defaults to 5)
- **Feedback** (required): User's comments/feedback

## Technical Details

- **Framework**: Flask 2.3.3
- **Python**: 3.7+
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Storage**: Plain text file (`submissions.txt`)
- **Responsive**: Works on desktop and mobile devices

## Customization

- **Styling**: Modify `static/style.css` for custom colors/layout
- **Form Fields**: Edit `templates/index.html` and `app.py` to add/remove fields
- **Storage**: Replace file storage with database by modifying `app.py`
- **Validation**: Add custom validation rules in the `submit_feedback()` function

## Security Notes

- Change the `secret_key` in `app.py` for production use
- Consider adding CSRF protection for production
- Implement proper input sanitization for production use
- Add rate limiting to prevent spam submissions
