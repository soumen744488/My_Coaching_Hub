"""
Utility functions for Coaching Management System
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Tuple, List, Dict
import os

class CoachingDataManager:
    """Manager class for all coaching data operations"""
    
    def __init__(self, excel_file: str = "coaching_data.xlsx"):
        self.excel_file = excel_file
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        """Ensure Excel file exists with all required sheets"""
        if not os.path.exists(self.excel_file):
            self.initialize_workbook()
    
    def initialize_workbook(self):
        """Initialize Excel workbook with required sheets"""
        with pd.ExcelWriter(self.excel_file, engine='openpyxl') as writer:
            # Batches sheet
            batches_df = pd.DataFrame(columns=[
                'batch_id', 'batch_name', 'duration', 'start_date', 'fees', 'status'
            ])
            batches_df.to_excel(writer, sheet_name='Batches', index=False)
            
            # Students sheet
            students_df = pd.DataFrame(columns=[
                'student_id', 'name', 'phone', 'join_date', 'batch_id'
            ])
            students_df.to_excel(writer, sheet_name='Students', index=False)
            
            # Payments sheet
            payments_df = pd.DataFrame(columns=[
                'payment_id', 'student_id', 'amount', 'pay_date', 'remarks'
            ])
            payments_df.to_excel(writer, sheet_name='Payments', index=False)
    
    def read_sheet(self, sheet_name: str) -> pd.DataFrame:
        """Read data from Excel sheet"""
        try:
            df = pd.read_excel(self.excel_file, sheet_name=sheet_name)
            return df
        except Exception as e:
            print(f"Error reading {sheet_name}: {str(e)}")
            return pd.DataFrame()
    
    def write_sheet(self, df: pd.DataFrame, sheet_name: str) -> bool:
        """Write data to Excel sheet"""
        try:
            with pd.ExcelWriter(self.excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            return True
        except Exception as e:
            print(f"Error writing to {sheet_name}: {str(e)}")
            return False

# ==================== BATCH OPERATIONS ====================

def create_batch(batch_name: str, duration: int, start_date, fees: float, 
                 manager: CoachingDataManager) -> Tuple[bool, str]:
    """
    Create a new batch
    Returns: (success: bool, batch_id: str)
    """
    try:
        batches_df = manager.read_sheet('Batches')
        batch_id = f"BATCH_{len(batches_df) + 1:03d}"
        
        new_batch = pd.DataFrame({
            'batch_id': [batch_id],
            'batch_name': [batch_name],
            'duration': [duration],
            'start_date': [start_date],
            'fees': [fees],
            'status': ['Active']
        })
        
        batches_df = pd.concat([batches_df, new_batch], ignore_index=True)
        success = manager.write_sheet(batches_df, 'Batches')
        
        return success, batch_id
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_active_batches(manager: CoachingDataManager) -> List[Dict]:
    """Get all active batches"""
    batches_df = manager.read_sheet('Batches')
    active = batches_df[batches_df['status'] == 'Active']
    return active.to_dict('records')

def get_batch_statistics(manager: CoachingDataManager) -> Dict:
    """Get batch statistics"""
    batches_df = manager.read_sheet('Batches')
    students_df = manager.read_sheet('Students')
    
    return {
        'total_batches': len(batches_df),
        'active_batches': len(batches_df[batches_df['status'] == 'Active']),
        'total_students': len(students_df),
        'avg_students_per_batch': len(students_df) / len(batches_df) if len(batches_df) > 0 else 0
    }

# ==================== STUDENT OPERATIONS ====================

def enroll_student(name: str, phone: str, join_date, batch_id: str,
                   manager: CoachingDataManager) -> Tuple[bool, str]:
    """
    Enroll a new student
    Returns: (success: bool, student_id: str)
    """
    try:
        students_df = manager.read_sheet('Students')
        student_id = f"STU_{len(students_df) + 1:03d}"
        
        new_student = pd.DataFrame({
            'student_id': [student_id],
            'name': [name],
            'phone': [phone],
            'join_date': [join_date],
            'batch_id': [batch_id]
        })
        
        students_df = pd.concat([students_df, new_student], ignore_index=True)
        success = manager.write_sheet(students_df, 'Students')
        
        return success, student_id
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_batch_students(batch_id: str, manager: CoachingDataManager) -> List[Dict]:
    """Get all students in a batch"""
    students_df = manager.read_sheet('Students')
    batch_students = students_df[students_df['batch_id'] == batch_id]
    return batch_students.to_dict('records')

def get_student_info(student_id: str, manager: CoachingDataManager) -> Dict:
    """Get detailed student information"""
    students_df = manager.read_sheet('Students')
    student = students_df[students_df['student_id'] == student_id]
    
    if len(student) > 0:
        return student.iloc[0].to_dict()
    return {}

# ==================== PAYMENT OPERATIONS ====================

def log_payment(student_id: str, amount: float, pay_date, remarks: str,
                manager: CoachingDataManager) -> Tuple[bool, str]:
    """
    Log a payment
    Returns: (success: bool, payment_id: str)
    """
    try:
        if amount <= 0:
            return False, "Amount must be greater than 0"
        
        payments_df = manager.read_sheet('Payments')
        payment_id = f"PAY_{len(payments_df) + 1:05d}"
        
        new_payment = pd.DataFrame({
            'payment_id': [payment_id],
            'student_id': [student_id],
            'amount': [amount],
            'pay_date': [pay_date],
            'remarks': [remarks]
        })
        
        payments_df = pd.concat([payments_df, new_payment], ignore_index=True)
        success = manager.write_sheet(payments_df, 'Payments')
        
        return success, payment_id
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_student_payment_history(student_id: str, manager: CoachingDataManager) -> List[Dict]:
    """Get payment history for a student"""
    payments_df = manager.read_sheet('Payments')
    student_payments = payments_df[payments_df['student_id'] == student_id]
    return student_payments.to_dict('records')

def get_student_total_paid(student_id: str, manager: CoachingDataManager) -> float:
    """Calculate total amount paid by a student"""
    payments_df = manager.read_sheet('Payments')
    student_payments = payments_df[payments_df['student_id'] == student_id]
    return student_payments['amount'].sum() if len(student_payments) > 0 else 0.0

# ==================== ANALYTICS OPERATIONS ====================

def calculate_monthly_revenue(manager: CoachingDataManager, 
                             year: int = None, month: int = None) -> float:
    """
    Calculate revenue for a specific month
    If year/month not specified, uses current month
    """
    payments_df = manager.read_sheet('Payments')
    
    if len(payments_df) == 0:
        return 0.0
    
    if year is None or month is None:
        today = datetime.now()
        year, month = today.year, today.month
    
    payments_df['pay_date'] = pd.to_datetime(payments_df['pay_date'])
    month_payments = payments_df[
        (payments_df['pay_date'].dt.year == year) &
        (payments_df['pay_date'].dt.month == month)
    ]
    
    return month_payments['amount'].sum()

def get_defaulters(days: int = 30, manager: CoachingDataManager = None) -> List[Dict]:
    """
    Get list of students who haven't paid in specified days
    Returns: List of student dictionaries with payment info
    """
    if manager is None:
        return []
    
    students_df = manager.read_sheet('Students')
    payments_df = manager.read_sheet('Payments')
    
    if len(students_df) == 0:
        return []
    
    cutoff_date = datetime.now().date() - timedelta(days=days)
    
    # Get last payment date for each student
    if len(payments_df) > 0:
        payments_df['pay_date'] = pd.to_datetime(payments_df['pay_date']).dt.date
        last_payments = payments_df.groupby('student_id')['pay_date'].max().reset_index()
        last_payments.columns = ['student_id', 'last_payment_date']
        
        # Students with last payment before cutoff
        defaulters = last_payments[last_payments['last_payment_date'] < cutoff_date]['student_id'].tolist()
    else:
        defaulters = []
    
    # Add students with no payments
    all_students = set(students_df['student_id'].tolist())
    students_with_payments = set(payments_df['student_id'].tolist()) if len(payments_df) > 0 else set()
    students_no_payment = list(all_students - students_with_payments)
    defaulters.extend(students_no_payment)
    
    # Get student details
    defaulter_details = students_df[students_df['student_id'].isin(defaulters)]
    return defaulter_details.to_dict('records')

def get_revenue_trend(manager: CoachingDataManager, months: int = 12) -> List[Dict]:
    """
    Get revenue trend for last N months
    Returns: List of {month, revenue} dictionaries
    """
    payments_df = manager.read_sheet('Payments')
    
    if len(payments_df) == 0:
        return []
    
    payments_df['pay_date'] = pd.to_datetime(payments_df['pay_date'])
    payments_df['month'] = payments_df['pay_date'].dt.to_period('M')
    
    revenue_trend = payments_df.groupby('month')['amount'].sum().reset_index()
    revenue_trend.columns = ['month', 'revenue']
    revenue_trend['month'] = revenue_trend['month'].astype(str)
    
    return revenue_trend.to_dict('records')

def get_batch_occupancy(manager: CoachingDataManager) -> List[Dict]:
    """
    Get occupancy statistics for all batches
    Returns: List of {batch_id, batch_name, student_count} dictionaries
    """
    batches_df = manager.read_sheet('Batches')
    students_df = manager.read_sheet('Students')
    
    occupancy = students_df['batch_id'].value_counts().reset_index()
    occupancy.columns = ['batch_id', 'student_count']
    
    # Merge with batch names
    occupancy = occupancy.merge(
        batches_df[['batch_id', 'batch_name']], 
        on='batch_id', 
        how='left'
    )
    
    return occupancy.to_dict('records')

# ==================== SUMMARY STATISTICS ====================

def get_dashboard_summary(manager: CoachingDataManager) -> Dict:
    """Get all dashboard metrics in one call"""
    batches_df = manager.read_sheet('Batches')
    students_df = manager.read_sheet('Students')
    payments_df = manager.read_sheet('Payments')
    
    total_revenue = payments_df['amount'].sum() if len(payments_df) > 0 else 0.0
    monthly_revenue = calculate_monthly_revenue(manager)
    defaulters = get_defaulters(manager=manager)
    
    return {
        'total_batches': len(batches_df),
        'active_batches': len(batches_df[batches_df['status'] == 'Active']),
        'total_students': len(students_df),
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'defaulter_count': len(defaulters),
        'defaulters': defaulters
    }
