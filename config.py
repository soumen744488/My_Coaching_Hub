"""
Configuration file for Coaching Management System
Modify these settings to customize the application
"""

# ==================== SECURITY SETTINGS ====================
# Default password - CHANGE THIS BEFORE DEPLOYING
DEFAULT_PASSWORD = "admin123"

# Enable password change feature
ENABLE_PASSWORD_CHANGE = True

# ==================== APPLICATION SETTINGS ====================
# Application title and icon
APP_TITLE = "Coaching Management System"
APP_ICON = "📚"
APP_LAYOUT = "wide"

# Excel file name
DATA_FILE = "coaching_data.xlsx"

# ==================== BUSINESS LOGIC SETTINGS ====================
# Default batch status options
BATCH_STATUS_OPTIONS = ["Active", "Closed", "On Hold"]

# Payment methods for dropdown
PAYMENT_METHODS = [
    "Cash",
    "UPI",
    "Bank Transfer",
    "Cheque",
    "Credit Card",
    "Other"
]

# Days threshold for defaulter identification
DEFAULTER_THRESHOLD_DAYS = 30

# ==================== UI SETTINGS ====================
# Sidebar width ratio
SIDEBAR_WIDTH = 300

# Color scheme
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#667eea"
ACCENT_COLOR = "#764ba2"

# Date format
DATE_FORMAT = "%Y-%m-%d"

# Currency symbol
CURRENCY_SYMBOL = "₹"
CURRENCY_FORMAT = "₹ {:.2f}"

# ==================== REPORT SETTINGS ====================
# Export format options
EXPORT_FORMATS = ["Excel", "CSV"]

# Reports to include in dashboard
DASHBOARD_REPORTS = [
    "total_metrics",
    "revenue_trend",
    "defaulter_list",
    "batch_occupancy"
]

# ==================== LOGGING SETTINGS ====================
# Enable debug logging
DEBUG_MODE = False

# Log file location
LOG_FILE = "coaching_system.log"

# ==================== EMAIL NOTIFICATION SETTINGS ====================
# Enable email notifications (requires additional setup)
ENABLE_EMAIL_NOTIFICATIONS = False

# Email configuration
EMAIL_SETTINGS = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',
    'sender_password': 'your_app_password',
}

# Email templates
EMAIL_TEMPLATES = {
    'defaulter_reminder': {
        'subject': 'Payment Reminder - Coaching Classes',
        'body': 'Dear {student_name},\n\nYou have pending payment for your coaching classes.\n\nPlease make the payment at your earliest convenience.\n\nRegards,\nCoaching Management'
    }
}

# ==================== DATABASE SETTINGS ====================
# Current database type
DATABASE_TYPE = "excel"  # Options: "excel", "google_sheets", "postgresql"

# Google Sheets configuration (if using Google Sheets)
GOOGLE_SHEETS_CONFIG = {
    'credentials_file': 'credentials.json',
    'spreadsheet_id': 'your_spreadsheet_id_here',
    'sheet_names': ['Batches', 'Students', 'Payments']
}

# PostgreSQL configuration (future use)
POSTGRESQL_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'coaching_db',
    'user': 'admin',
    'password': 'password'
}

# ==================== FEATURE FLAGS ====================
# Enable/disable features
FEATURES = {
    'batch_management': True,
    'student_enrollment': True,
    'payment_tracking': True,
    'analytics_dashboard': True,
    'email_notifications': False,
    'sms_notifications': False,
    'attendance_tracking': False,
    'performance_tracking': False,
}

# ==================== VALIDATION RULES ====================
# Student phone number validation (regex)
PHONE_REGEX = r'^[0-9]{10}$'

# Student name validation
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 100

# Amount validation
MIN_AMOUNT = 0.0
MAX_AMOUNT = 999999.99

# ==================== DISPLAY SETTINGS ====================
# Number of records to show per page
PAGE_SIZE = 10

# Maximum number of recent records to show
MAX_RECENT_RECORDS = 5

# Chart settings
CHART_HEIGHT = 400
CHART_WIDTH = 600

# ==================== API SETTINGS ====================
# For future API development
API_SETTINGS = {
    'enable_api': False,
    'api_host': '0.0.0.0',
    'api_port': 8000,
    'api_debug': False,
}

# ==================== DEPLOYMENT SETTINGS ====================
# Streamlit Cloud settings
STREAMLIT_CLOUD_CONFIG = {
    'repo_url': 'https://github.com/yourusername/coaching-system',
    'branch': 'main',
}

# ==================== HELPER FUNCTIONS ====================

def get_config(key, default=None):
    """
    Get configuration value with fallback to default
    Usage: get_config('DEFAULT_PASSWORD')
    """
    return globals().get(key, default)

def validate_phone(phone_number):
    """Validate phone number format"""
    import re
    pattern = get_config('PHONE_REGEX')
    return bool(re.match(pattern, str(phone_number)))

def validate_name(name):
    """Validate student name"""
    min_len = get_config('MIN_NAME_LENGTH', 2)
    max_len = get_config('MAX_NAME_LENGTH', 100)
    return min_len <= len(name) <= max_len

def format_currency(amount):
    """Format amount as currency"""
    fmt = get_config('CURRENCY_FORMAT', '₹ {:.2f}')
    return fmt.format(amount)
