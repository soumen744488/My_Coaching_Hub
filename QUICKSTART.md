# ⚡ Quick Start Guide - Coaching Management System

Get up and running in 5 minutes!

## 📦 What You Have

A complete coaching management system with:
- ✅ Secure login
- ✅ Batch management
- ✅ Student enrollment
- ✅ Payment tracking
- ✅ Analytics dashboard
- ✅ Excel data storage

## 🚀 Start in 3 Steps

### Step 1: Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application (1 minute)
```bash
streamlit run app.py
```

The app will open automatically. If not, go to: **http://localhost:8501**

### Step 3: Login (30 seconds)
- **Password:** `admin123`
- Click "Login"

**That's it! You're in! 🎉**

---

## 📚 5-Minute Usage Guide

### 1. Create Your First Batch (1 min)
1. Go to **"Batch Manager"** in sidebar
2. Click **"Create New Batch"**
3. Fill in:
   - Batch Name: e.g., "Physics Class"
   - Duration: 6 months
   - Start Date: Today
   - Fees: 5000
4. Click **"Create Batch"**

✅ **Batch Created!**

### 2. Enroll Your First Student (1 min)
1. Go to **"Student Enrollment"**
2. Click **"Add Student"**
3. Fill in:
   - Select Batch: (choose the batch you created)
   - Student Name: "Arjun Kumar"
   - Phone Number: "9876543210"
   - Joining Date: Today
4. Click **"Enroll Student"**

✅ **Student Enrolled!**

### 3. Log a Payment (1 min)
1. Go to **"Payment Tracker"**
2. Click **"Log Payment"**
3. Fill in:
   - Select Student: (choose the student)
   - Amount Paid: 5000
   - Payment Date: Today
   - Remarks: UPI
4. Click **"Log Payment"**

✅ **Payment Recorded!**

### 4. View Dashboard (1 min)
1. Click **"Dashboard"** in sidebar
2. See:
   - Total revenue
   - Monthly revenue
   - Payment defaulters
   - Batch occupancy chart
   - Revenue trend

✅ **All your metrics at a glance!**

---

## 🧪 Test with Sample Data (Optional)

Want to see how it works with realistic data?

```bash
python generate_sample_data.py
```

This creates `coaching_data_sample.xlsx` with:
- 5 batches
- 50+ students
- 150+ payments
- Ready-made analytics

Then rename/replace `coaching_data.xlsx` with the sample.

---

## 🎯 Common Tasks

### Check Student's Payment History
1. Go to **Payment Tracker**
2. Click **"Payment History"** tab
3. Select student from dropdown
4. See all their payments with dates and amounts

### Find Students Who Haven't Paid (Defaulters)
1. Go to **Dashboard**
2. Scroll to **"Payment Defaulters"**
3. See all students with overdue payments (30+ days)
4. Call or email them for payment follow-up

### View All Students in a Batch
1. Go to **Student Enrollment**
2. Click **"View Students"** tab
3. Select batch from "Filter by Batch"
4. See all students in that batch

### Change Password
1. In sidebar, check **"Change Password"**
2. Enter current password: `admin123`
3. Enter new password (twice)
4. Click "Update Password"

---

## 💾 Files Explained

| File | Purpose |
|------|---------|
| `app.py` | Main application (the thing you run) |
| `config.py` | Settings you can customize |
| `utils.py` | Helper functions for data operations |
| `requirements.txt` | Python packages needed |
| `coaching_data.xlsx` | Your data (auto-created) |
| `generate_sample_data.py` | Create test data |

---

## 🔑 Remember

- **Default Password:** `admin123` → Change this!
- **Data Location:** `coaching_data.xlsx` (same folder as app.py)
- **Browser:** Works best on Chrome/Firefox
- **Backup:** Copy `coaching_data.xlsx` regularly

---

## 🆘 Troubleshooting

### "Module not found" error?
```bash
pip install -r requirements.txt
```

### App won't start?
```bash
# Check if port 8501 is free
# If not, use a different port:
streamlit run app.py --server.port=8502
```

### Password not working?
- Default: `admin123` (exactly as shown)
- Check CAPS LOCK is off

### Data not saving?
- Close Excel if it's open
- Make sure file isn't read-only
- Try restarting the app

---

## 📖 Next Steps

1. ✅ Get familiar with the interface
2. ✅ Try all features with sample data
3. ✅ Add your real batches and students
4. ✅ Track payments regularly
5. ✅ Check dashboard weekly for insights

See **README.md** for full documentation.
See **DEPLOYMENT.md** for hosting options.

---

## 🚀 Ready to Deploy?

### Local Computer
Already done! You're running it now.

### Share with Team (Internet)
See **DEPLOYMENT.md** → "Streamlit Cloud"

### Your Own Server
See **DEPLOYMENT.md** → "Self-Hosted Server"

---

## 💡 Pro Tips

1. **Batch Name Tip:** Use format like "Physics_JAN2024" to make sorting easier
2. **Phone Numbers:** Store with country code if using international
3. **Monthly Payments:** Log payments on the same day of month for consistency
4. **Backup:** Copy `coaching_data.xlsx` every week to a backup location
5. **Defaulters:** Check dashboard every Friday to identify payment follow-ups

---

## 🎓 Examples

### Example Batch Entry
```
Batch Name: Physics Advanced - Morning Batch
Duration: 6 months
Start Date: Jan 1, 2024
Fees: 5000
```

### Example Student Entry
```
Batch: BATCH_001 (Physics Advanced - Morning Batch)
Name: Rohan Kumar Sharma
Phone: 9876543210
Joining Date: Jan 5, 2024
```

### Example Payment Entry
```
Student: STU_001 (Rohan Kumar Sharma)
Amount: 5000
Date: Jan 5, 2024
Remarks: UPI
```

---

**Questions? See README.md for detailed documentation.**

**Need to deploy? See DEPLOYMENT.md for server options.**

**Ready to use? Happy coaching! 📚✨**
