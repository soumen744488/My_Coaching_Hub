# ❓ Frequently Asked Questions (FAQ)

## Getting Started

### Q: How do I run the application?
**A:** 
```bash
pip install -r requirements.txt
streamlit run app.py
```
The app opens at http://localhost:8501

### Q: What's the default password?
**A:** `admin123` (change this before deploying!)

### Q: Do I need an internet connection?
**A:** No, it works completely offline on your computer. Internet is only needed for Streamlit Cloud deployment.

### Q: What if I forget the password?
**A:** Edit `app.py` line 86 and change the password check:
```python
if password == "your_new_password":
```

---

## Data Management

### Q: Where is my data stored?
**A:** In `coaching_data.xlsx` in the same folder as `app.py`. It's a regular Excel file you can open manually.

### Q: Can I edit data directly in Excel?
**A:** Yes! You can open `coaching_data.xlsx` with Excel and edit the Batches, Students, or Payments sheets directly. Just make sure to close Excel before refreshing the app.

### Q: How do I backup my data?
**A:** Simply copy `coaching_data.xlsx` to a safe location. Do this daily:
```bash
cp coaching_data.xlsx coaching_data_backup_$(date +%Y%m%d).xlsx
```

### Q: Can I export data to CSV?
**A:** Yes, you can:
```python
import pandas as pd
df = pd.read_excel('coaching_data.xlsx', sheet_name='Payments')
df.to_csv('payments.csv', index=False)
```

### Q: What if the Excel file gets corrupted?
**A:** Restore from a backup copy. If no backup exists, data is lost. **Always backup regularly!**

### Q: Can I use Google Sheets instead of Excel?
**A:** Yes, see DEPLOYMENT.md → "Google Sheets Integration" for setup instructions.

---

## Features & Functionality

### Q: How do batch IDs get generated?
**A:** Automatically as BATCH_001, BATCH_002, etc. You can't change them (unless you edit Excel directly).

### Q: How do student IDs get generated?
**A:** Automatically as STU_001, STU_002, etc. Sequential based on enrollment order.

### Q: How do payment IDs work?
**A:** Automatically as PAY_00001, PAY_00002, etc. Each payment gets a unique receipt number.

### Q: Can I enroll a student in multiple batches?
**A:** Currently no - each student belongs to one batch. To move a student, edit Excel directly or delete and re-enroll.

### Q: How is a student marked as a "defaulter"?
**A:** A student is a defaulter if:
- No payment in the last 30 days, OR
- Never made a payment at all

### Q: Can I change the 30-day threshold?
**A:** Yes, in `config.py`:
```python
DEFAULTER_THRESHOLD_DAYS = 30
```
Change 30 to any number you want.

### Q: How are monthly revenue reports calculated?
**A:** It's the sum of all payments made in the current calendar month (1st to last day).

### Q: Can I see reports for past months?
**A:** Currently the dashboard shows only this month. For past reports, export to CSV and analyze in Excel.

---

## Technical Questions

### Q: What Python version is required?
**A:** Python 3.8 or higher. Check with:
```bash
python --version
```

### Q: What if pip install fails?
**A:** Try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Q: Can I modify the code?
**A:** Yes! The code is yours. All files are well-commented for easy modification.

### Q: How do I add new features?
**A:** 
1. Write new functions in `utils.py`
2. Add new tabs/sections in `app.py`
3. Update `config.py` if needed
4. Test thoroughly

### Q: What's the maximum number of students I can have?
**A:** Theoretically unlimited, but performance may degrade with 10,000+ records in Excel. Consider migrating to a database for larger datasets.

---

## Deployment Questions

### Q: Can I use this on a website?
**A:** Yes! Use Streamlit Cloud (free) or self-host on a server. See DEPLOYMENT.md

### Q: How do I deploy to Streamlit Cloud?
**A:** 
1. Push code to GitHub
2. Visit share.streamlit.io
3. Select your repo
4. Click Deploy

Detailed steps in DEPLOYMENT.md → "Streamlit Cloud"

### Q: Can my team access it from different locations?
**A:** Yes, if you deploy to cloud or self-hosted server with internet access.

### Q: Is it secure for production use?
**A:** For single-user or small team: Yes
For large organization: Add user authentication and use a real database

### Q: Do I need special hosting?
**A:** Streamlit Cloud is free and easiest. Or any Linux/Windows server with Python.

### Q: Can I use it offline?
**A:** Yes, run it locally without internet. Data stays on your computer.

---

## Payment & Revenue Questions

### Q: Can I record partial payments?
**A:** Yes, just enter the amount paid. You can log multiple payments per student.

### Q: What payment methods can I record?
**A:** Any - just type in the remarks field. Common ones: UPI, Cash, Bank Transfer, Cheque, Card

### Q: Can I track pending amounts?
**A:** Not automatically, but you can calculate manually:
```
Total fees (from Batches sheet) - Total paid (from Payments sheet)
```

### Q: Can I record discounts or refunds?
**A:** Yes, use negative amounts for refunds:
```
Amount: -500  # This is a refund
```

### Q: How do I handle installment payments?
**A:** Log each installment as a separate payment. Use remarks to note "Installment 1 of 3" etc.

---

## Student & Batch Questions

### Q: Can I close a batch?
**A:** Yes, change status from "Active" to "Closed" in Excel's Batches sheet.

### Q: What happens when a batch ends?
**A:** Nothing automatic - status remains as you set it. Students remain associated with the batch.

### Q: Can I delete students or batches?
**A:** Yes, delete from Excel directly. **But backup first!**

### Q: Can I transfer a student to another batch?
**A:** Edit in Excel - change the batch_id in Students sheet.

### Q: How do I track attendance?
**A:** Currently not supported. Add as future feature or track separately.

---

## Report & Analytics Questions

### Q: Why are my revenue calculations different?
**A:** Check:
- Payment dates (system uses calendar month)
- Duplicate entries
- Excel file has correct data

### Q: Can I get detailed reports?
**A:** Export data to CSV/Excel and use pivot tables:
```python
import pandas as pd
df = pd.read_excel('coaching_data.xlsx', sheet_name='Payments')
pivot = df.pivot_table(values='amount', index='student_id', aggfunc='sum')
```

### Q: How do I print reports?
**A:** Take screenshots or export to Excel, then print from there.

### Q: Can I schedule automated reports?
**A:** Yes, using Python script + email (requires additional setup). See utils.py for examples.

---

## Troubleshooting Questions

### Q: App crashes on startup?
**A:** Check:
```bash
pip install -r requirements.txt  # Reinstall deps
python app.py  # See error message
```

### Q: "Module not found" error?
**A:** 
```bash
pip install streamlit pandas openpyxl python-dateutil
```

### Q: Excel file won't open in app?
**A:** 
- Close Excel if open
- Ensure file not read-only
- Check file isn't corrupted

### Q: Data disappears after restart?
**A:** Excel file wasn't properly closed. Restart and check coaching_data.xlsx exists.

### Q: Port 8501 already in use?
**A:** 
```bash
streamlit run app.py --server.port=8502
```

### Q: How do I clear all data and start fresh?
**A:** Delete `coaching_data.xlsx` and restart the app. It will create a new empty one.

---

## Security Questions

### Q: Is my data safe?
**A:** Completely - it's stored locally on your computer. No internet communication.

### Q: Can I share the system with multiple users?
**A:** Yes, with same password. For different users, add multi-user authentication (future feature).

### Q: Should I change the default password?
**A:** **Absolutely!** Before deploying anywhere. Change in `config.py`:
```python
DEFAULT_PASSWORD = "your_super_secret_password"
```

### Q: Can I add user roles (admin, teacher, viewer)?
**A:** Yes, would require code modification. See utils.py for starting point.

---

## Performance Questions

### Q: Is the app slow with many students?
**A:** With <5000 records: Very fast
With 5000-20000: Acceptable
With 20000+: Consider migrating to database

### Q: How do I speed up the app?
**A:** 
1. Archive old data (move to backup file)
2. Clear unused batches
3. Use Google Sheets instead of Excel
4. Migrate to PostgreSQL for large datasets

---

## Integration Questions

### Q: Can I connect to other systems?
**A:** Yes! The code is modular. You can add API integrations to:
- Email system (send payment reminders)
- SMS system (send notifications)
- Accounting software (export data)
- Website (display public class info)

### Q: Can I create an API for the system?
**A:** Yes, add Flask/FastAPI to create REST endpoints. See config.py → API_SETTINGS

---

## License & Usage Questions

### Q: Can I modify and sell this?
**A:** Yes, it's open source. No restrictions.

### Q: Can I use it for my coaching center?
**A:** Absolutely! That's what it's built for.

### Q: Can I use it for other businesses?
**A:** Yes! Works for any batch-based service business.

### Q: Do I need to give credit?
**A:** Not required, but appreciated!

---

## Still Have Questions?

1. **Check README.md** for comprehensive documentation
2. **Check DEPLOYMENT.md** for deployment options
3. **Check QUICKSTART.md** for quick tutorials
4. **Check code comments** in app.py, utils.py, config.py
5. **Try the sample data** generator first

---

**Last Updated:** December 31, 2024
**Version:** 1.0
