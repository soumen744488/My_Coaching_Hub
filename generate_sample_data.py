"""
Sample Data Generator for Coaching Management System
Run this script to generate sample data for testing
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def generate_sample_data(filename='coaching_data_sample.xlsx'):
    """
    Generate sample data for testing the coaching management system
    """
    
    # ==================== GENERATE SAMPLE BATCHES ====================
    batches = [
        {
            'batch_id': 'BATCH_001',
            'batch_name': 'Physics - Morning Batch',
            'duration': 6,
            'start_date': datetime(2024, 1, 1).date(),
            'fees': 5000,
            'status': 'Active'
        },
        {
            'batch_id': 'BATCH_002',
            'batch_name': 'Chemistry - Evening Batch',
            'duration': 6,
            'start_date': datetime(2024, 1, 15).date(),
            'fees': 4500,
            'status': 'Active'
        },
        {
            'batch_id': 'BATCH_003',
            'batch_name': 'Mathematics - Night Batch',
            'duration': 3,
            'start_date': datetime(2024, 2, 1).date(),
            'fees': 3000,
            'status': 'Active'
        },
        {
            'batch_id': 'BATCH_004',
            'batch_name': 'Biology - Morning Batch',
            'duration': 6,
            'start_date': datetime(2023, 6, 1).date(),
            'fees': 5500,
            'status': 'Closed'
        },
        {
            'batch_id': 'BATCH_005',
            'batch_name': 'English - Communication',
            'duration': 4,
            'start_date': datetime(2024, 1, 10).date(),
            'fees': 3500,
            'status': 'Active'
        },
    ]
    
    batches_df = pd.DataFrame(batches)
    
    # ==================== GENERATE SAMPLE STUDENTS ====================
    first_names = ['Arjun', 'Sneha', 'Rohan', 'Priya', 'Aditya', 'Neha', 'Vikram', 'Ananya', 
                   'Rajesh', 'Divya', 'Sameer', 'Pooja', 'Karan', 'Isha', 'Nikhil']
    last_names = ['Sharma', 'Kumar', 'Singh', 'Patel', 'Gupta', 'Verma', 'Mishra', 'Iyer']
    
    students = []
    student_id_counter = 1
    
    for batch in batches:
        batch_id = batch['batch_id']
        # 5-12 students per batch
        num_students = random.randint(5, 12)
        
        for _ in range(num_students):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            students.append({
                'student_id': f'STU_{student_id_counter:03d}',
                'name': f'{first_name} {last_name}',
                'phone': f'98{random.randint(10000000, 99999999)}',
                'join_date': batch['start_date'],
                'batch_id': batch_id
            })
            student_id_counter += 1
    
    students_df = pd.DataFrame(students)
    
    # ==================== GENERATE SAMPLE PAYMENTS ====================
    payments = []
    payment_id_counter = 1
    today = datetime.now().date()
    
    payment_methods = ['UPI', 'Cash', 'Bank Transfer', 'Cheque', 'Card']
    
    for idx, student in enumerate(students_df.to_dict('records')):
        student_id = student['student_id']
        join_date = pd.to_datetime(student['join_date']).date()
        
        # Most students have multiple payments
        num_payments = random.randint(2, 5)
        
        for i in range(num_payments):
            # Payment dates scattered across months
            days_since_join = (today - join_date).days
            payment_days_ago = random.randint(1, max(days_since_join, 1))
            payment_date = today - timedelta(days=payment_days_ago)
            
            # Skip future dates
            if payment_date > today:
                payment_date = today
            
            payments.append({
                'payment_id': f'PAY_{payment_id_counter:05d}',
                'student_id': student_id,
                'amount': round(random.uniform(2000, 5000), 2),
                'pay_date': payment_date,
                'remarks': random.choice(payment_methods)
            })
            payment_id_counter += 1
    
    # Add some students with no recent payments (potential defaulters)
    for student_id in students_df['student_id'].sample(n=min(5, len(students_df))):
        # This student's last payment is more than 30 days ago
        old_payment_date = today - timedelta(days=random.randint(31, 90))
        
        payments.append({
            'payment_id': f'PAY_{payment_id_counter:05d}',
            'student_id': student_id,
            'amount': 3000,
            'pay_date': old_payment_date,
            'remarks': 'UPI'
        })
        payment_id_counter += 1
    
    payments_df = pd.DataFrame(payments)
    
    # ==================== WRITE TO EXCEL ====================
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        batches_df.to_excel(writer, sheet_name='Batches', index=False)
        students_df.to_excel(writer, sheet_name='Students', index=False)
        payments_df.to_excel(writer, sheet_name='Payments', index=False)
    
    # ==================== PRINT SUMMARY ====================
    print("=" * 60)
    print("SAMPLE DATA GENERATED SUCCESSFULLY")
    print("=" * 60)
    print(f"\nFile: {filename}")
    print(f"\nBatches: {len(batches_df)}")
    print(f"  - Active: {len(batches_df[batches_df['status'] == 'Active'])}")
    print(f"  - Closed: {len(batches_df[batches_df['status'] == 'Closed'])}")
    
    print(f"\nStudents: {len(students_df)}")
    for batch_id in batches_df['batch_id']:
        count = len(students_df[students_df['batch_id'] == batch_id])
        batch_name = batches_df[batches_df['batch_id'] == batch_id]['batch_name'].values[0]
        print(f"  - {batch_id} ({batch_name}): {count} students")
    
    print(f"\nPayments: {len(payments_df)}")
    print(f"  - Total Revenue: ₹ {payments_df['amount'].sum():,.2f}")
    print(f"  - Average Payment: ₹ {payments_df['amount'].mean():,.2f}")
    
    # Defaulter statistics
    thirty_days_ago = today - timedelta(days=30)
    payments_df['pay_date'] = pd.to_datetime(payments_df['pay_date']).dt.date
    
    last_payments = payments_df.groupby('student_id')['pay_date'].max()
    defaulters = last_payments[last_payments < thirty_days_ago]
    students_no_payment = set(students_df['student_id']) - set(payments_df['student_id'])
    
    total_defaulters = len(defaulters) + len(students_no_payment)
    print(f"\nDefaulters (>30 days): {total_defaulters}")
    print(f"  - With old payments: {len(defaulters)}")
    print(f"  - With no payments: {len(students_no_payment)}")
    
    print("\n" + "=" * 60)
    print("✅ Ready to use with the Coaching Management System!")
    print("=" * 60)

if __name__ == "__main__":
    generate_sample_data()
    
    # Optional: Generate with custom filename
    # generate_sample_data('my_sample_data.xlsx')
