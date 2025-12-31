# 🎓 Coaching Management System

A complete web-based coaching management system built with Python and Streamlit. Manage batches, students, and payments with an intuitive interface.

## 📋 Features

### 🔐 **Secure Login**
- Password-protected dashboard
- Simple authentication system
- Change password functionality

### 📋 **Batch Management**
- Create new coaching batches
- Set batch duration and start dates
- Track batch status (Active/Closed)
- View batch statistics and occupancy

### 👥 **Student Enrollment**
- Enroll students into specific batches
- Track student contact information
- Auto-generated student IDs
- Filter students by batch

### 💰 **Payment Tracking**
- Log student payments with remarks
- Track payment history per student
- Payment date and method recording
- Running payment statistics

### 📊 **Analytics Dashboard**
- Total revenue tracking
- Monthly revenue calculation
- Defaulter identification (no payment in 30 days)
- Batch occupancy visualization
- Revenue trend analysis
- Real-time metrics

## 🏗️ Data Architecture

### Excel Sheets Structure

#### **Batches Sheet**
| Column | Type | Purpose |
|--------|------|---------|
| batch_id | String | Unique batch identifier (BATCH_001) |
| batch_name | String | Name of the course |
| duration | Integer | Duration in months |
| start_date | Date | Batch start date |
| fees | Decimal | Course fees |
| status | String | Active/Closed |

#### **Students Sheet**
| Column | Type | Purpose |
|--------|------|---------|
| student_id | String | Unique student identifier (STU_001) |
| name | String | Student's full name |
| phone | String | Contact number |
| join_date | Date | Enrollment date |
| batch_id | String | Associated batch |

#### **Payments Sheet**
| Column | Type | Purpose |
|--------|------|---------|
| payment_id | String | Unique payment receipt (PAY_00001) |
| student_id | String | Student who paid |
| amount | Decimal | Payment amount |
| pay_date | Date | Payment date |
| remarks | String | Payment method/notes |

## 📊 Entity Relationship Diagram

```
┌─────────┐         ┌──────────┐         ┌──────────┐
│ Batches │ 1 ──← N│ Students │ 1 ──← N │ Payments │
└─────────┘         └──────────┘         └──────────┘
```

- One Batch has many Students
- One Student has many Payments
- Relationships maintained via IDs

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download
```bash
cd /path/to/coaching-system
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Step 4: Login
- **Default Password:** `admin123`
- Change this in the code before deploying to production!

## 📖 Usage Guide

### 1️⃣ **Creating a Batch**
1. Navigate to "Batch Manager"
2. Go to "Create New Batch" tab
3. Enter batch name, duration, start date, and fees
4. Click "Create Batch"

### 2️⃣ **Enrolling Students**
1. Go to "Student Enrollment"
2. Select an existing batch from dropdown
3. Enter student's name and phone number
4. Set joining date
5. Click "Enroll Student"

### 3️⃣ **Logging Payments**
1. Navigate to "Payment Tracker"
2. Go to "Log Payment" tab
3. Select student from dropdown
4. Enter amount and payment date
5. Add optional remarks (e.g., "UPI", "Cash")
6. Click "Log Payment"

### 4️⃣ **Viewing Reports**
1. Click "Dashboard" to see:
   - Total revenue and monthly revenue
   - Students with overdue payments (30+ days)
   - Batch occupancy chart
   - Revenue trend graph

## 🔒 Security Notes

⚠️ **Important:** Before deploying:
1. Change the default password in `app.py` (line 86)
2. Use strong, unique passwords
3. Consider using environment variables for passwords
4. Do not commit passwords to version control

## 📁 File Structure

```
coaching-system/
├── app.py                  # Main application
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── coaching_data.xlsx     # Data file (auto-created)
```

## 🔄 Data Flow

```
User Login
    ↓
Authentication Check
    ↓
Dashboard / Batch Manager / Enrollment / Payments
    ↓
Read/Write to coaching_data.xlsx
    ↓
Display Results
```

## 📊 Key Features Explained

### Dashboard Metrics
- **Total Batches:** Count of all batches
- **Total Students:** Sum of all enrolled students
- **Total Revenue:** Sum of all payments
- **Monthly Revenue:** Sum of payments in current month

### Defaulter Detection Logic
- Scans payment history for each student
- Identifies students with no payments in last 30 days
- Includes students with no payment history
- Shows student ID, name, and phone for follow-up

### Batch Occupancy
- Bar chart showing student count per batch
- Helps identify under-utilized batches
- Useful for course planning

## 🎨 User Interface

### Clean, Intuitive Design
- Tabbed interfaces for organized workflows
- Color-coded metrics
- Responsive layout for desktop and tablet
- Balloons animation on successful actions
- Inline help messages and validations

## 🚀 Deployment Options

### Option 1: Local Machine
Simply run `streamlit run app.py`

### Option 2: Streamlit Cloud (Free)
1. Push code to GitHub
2. Visit https://share.streamlit.io
3. Deploy from your repository
4. Access anywhere via URL

### Option 3: Self-Hosted Server
1. Install Python on your server
2. Install dependencies
3. Run with a production WSGI server (Gunicorn)
4. Use SSL certificate for HTTPS

## 📝 Common Operations

### Export Data to CSV
```python
# In Python terminal
import pandas as pd
df = pd.read_excel('coaching_data.xlsx', sheet_name='Payments')
df.to_csv('payments_export.csv', index=False)
```

### Backup Data
```bash
# Backup the Excel file
cp coaching_data.xlsx coaching_data_backup_$(date +%Y%m%d).xlsx
```

### Generate Reports
All reports are dynamically generated from the Dashboard tab based on current data.

## 🐛 Troubleshooting

### Excel File Permission Error
- Close the file if open in Excel
- Ensure file is not locked
- Try restarting the application

### Password Not Working
- Default is `admin123`
- Check for typos
- Ensure CAPS LOCK is off

### Data Not Saving
- Check file permissions
- Ensure disk space available
- Verify Excel file is not corrupted

## 🔧 Advanced Customization

### Change Default Password
Edit `app.py` line 86:
```python
if password == "your_new_password":
```

### Add More Sheets
In `initialize_excel_file()` function, add:
```python
new_df = pd.DataFrame(columns=['col1', 'col2', ...])
new_df.to_excel(writer, sheet_name='SheetName', index=False)
```

### Modify Batch Duration Calculation
Edit the `batch_manager()` function:
```python
from dateutil.relativedelta import relativedelta
end_date = start_date + relativedelta(months=duration)
```

## 📞 Support & Maintenance

### Regular Maintenance
- Backup data weekly
- Monitor file size
- Update dependencies monthly
- Review security settings

### Adding Features
The codebase is modular - new features can be added as new functions and integrated into the sidebar navigation.

## 📄 License

This project is open-source and available for personal and commercial use.

## 🎯 Future Enhancements

- [ ] Email notifications for defaulters
- [ ] SMS reminders for payments
- [ ] Student performance tracking
- [ ] Attendance management
- [ ] Certificate generation
- [ ] Multi-user roles and permissions
- [ ] Database migration (PostgreSQL)
- [ ] Mobile app version

## 💡 Tips & Tricks

1. **Bulk Operations:** Export to Excel, modify, then re-import
2. **Reporting:** Use Excel's pivot tables on exported data
3. **Backup:** Keep daily backups of coaching_data.xlsx
4. **Security:** Use a strong, complex password before going live

---

**Happy Teaching! 📚✨**

Built with ❤️ using Python and Streamlit
