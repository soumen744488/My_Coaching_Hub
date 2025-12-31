import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Coaching Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== FILE MANAGEMENT ====================
DATA_FILE = "coaching_data.xlsx"

def initialize_excel_file():
    """Create Excel file with required sheets if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        with pd.ExcelWriter(DATA_FILE, engine='openpyxl') as writer:
            # Batches sheet
            batches_df = pd.DataFrame(columns=[
                'batch_id', 'batch_name', 'duration', 'start_date', 'fees', 'status'
            ])
            batches_df.to_excel(writer, sheet_name='Batches', index=False)
            
            # Students sheet (without batch_id - moved to Student_Batches)
            students_df = pd.DataFrame(columns=[
                'student_id', 'name', 'phone', 'address', 'join_date'
            ])
            students_df.to_excel(writer, sheet_name='Students', index=False)
            
            # Student_Batches mapping sheet (many-to-many relationship)
            student_batches_df = pd.DataFrame(columns=[
                'student_id', 'batch_id'
            ])
            student_batches_df.to_excel(writer, sheet_name='Student_Batches', index=False)
            
            # Payments sheet
            payments_df = pd.DataFrame(columns=[
                'payment_id', 'student_id', 'amount', 'pay_date', 'remarks'
            ])
            payments_df.to_excel(writer, sheet_name='Payments', index=False)

def read_sheet(sheet_name):
    """Read data from Excel sheet."""
    try:
        df = pd.read_excel(DATA_FILE, sheet_name=sheet_name)
        return df
    except Exception as e:
        # If sheet doesn't exist, create it with empty dataframe
        if sheet_name == 'Student_Batches':
            return pd.DataFrame(columns=['student_id', 'batch_id'])
        st.warning(f"Sheet {sheet_name} not found. Creating empty sheet.")
        return pd.DataFrame()

def write_sheet(df, sheet_name):
    """Write data to Excel sheet."""
    try:
        with pd.ExcelWriter(DATA_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    except Exception as e:
        st.error(f"Error writing to {sheet_name}: {str(e)}")

def ensure_student_batches_sheet():
    """Ensure Student_Batches sheet exists and migrate data if needed."""
    try:
        student_batches_df = pd.read_excel(DATA_FILE, sheet_name='Student_Batches')
        return student_batches_df
    except:
        # Sheet doesn't exist, create it
        try:
            # Try to migrate from old Students sheet with batch_id column
            students_df = pd.read_excel(DATA_FILE, sheet_name='Students')
            if 'batch_id' in students_df.columns:
                # Create Student_Batches from existing batch_id column
                student_batches_df = students_df[['student_id', 'batch_id']].copy()
                write_sheet(student_batches_df, 'Student_Batches')
                
                # Remove batch_id from Students sheet and ensure address exists
                students_df = students_df.drop(columns=['batch_id'])
                if 'address' not in students_df.columns:
                    students_df['address'] = ''
                write_sheet(students_df, 'Students')
                return student_batches_df
        except:
            pass
        
        # Create empty Student_Batches sheet
        student_batches_df = pd.DataFrame(columns=['student_id', 'batch_id'])
        write_sheet(student_batches_df, 'Student_Batches')
        return student_batches_df

# ==================== AUTHENTICATION ====================
def check_password():
    """Check if user has entered the correct password."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown('<div class="main-header">🔐 Coaching Management System</div>', unsafe_allow_html=True)
        st.info("Please enter your password to access the dashboard")
        
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Change this to your desired password
            if password == "admin123":
                st.session_state.authenticated = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid password")
        return False
    return True

# ==================== BATCH MANAGEMENT ====================
def batch_manager():
    """Batch creation and management interface."""
    st.markdown('<div class="sub-header">📋 Batch Manager</div>', unsafe_allow_html=True)
    
    batches_df = read_sheet('Batches')
    
    tab1, tab2 = st.tabs(["Create New Batch", "View Batches"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            batch_name = st.text_input("Batch Name", placeholder="e.g., Physics Morning Batch")
            duration = st.number_input("Duration (Months)", min_value=1, max_value=24, value=3)
        
        with col2:
            start_date = st.date_input("Start Date")
            fees = st.number_input("Monthly/Total Fees", min_value=0.0, value=0.0)
        
        if st.button("Create Batch", key="create_batch"):
            # Generate batch ID
            batch_id = f"BATCH_{len(batches_df) + 1:03d}"
            
            # Calculate end date
            from dateutil.relativedelta import relativedelta
            end_date = start_date + relativedelta(months=duration)
            
            new_batch = pd.DataFrame({
                'batch_id': [batch_id],
                'batch_name': [batch_name],
                'duration': [duration],
                'start_date': [start_date],
                'fees': [fees],
                'status': ['Active']
            })
            
            batches_df = pd.concat([batches_df, new_batch], ignore_index=True)
            write_sheet(batches_df, 'Batches')
            
            st.balloons()
    
    with tab2:
        if len(batches_df) > 0:
            # Convert dates to string for display
            display_df = batches_df.copy()
            display_df['start_date'] = pd.to_datetime(display_df['start_date']).dt.strftime('%Y-%m-%d')
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "batch_id": st.column_config.TextColumn("Batch ID", width="medium"),
                    "batch_name": st.column_config.TextColumn("Batch Name", width="large"),
                    "duration": st.column_config.NumberColumn("Duration (Months)"),
                    "start_date": st.column_config.TextColumn("Start Date"),
                    "fees": st.column_config.NumberColumn("Fees (₹)", format="₹ %.2f"),
                    "status": st.column_config.TextColumn("Status")
                }
            )
            
            # Delete batch section with checkboxes
            st.markdown("---")
            st.markdown("**Delete Batch(es) - Select using checkboxes:**")
            
            # Create columns for batch selection
            st.markdown("**Select Batches to Delete:**")
            cols = st.columns(3)
            selected_batches = []
            
            for idx, (_, batch) in enumerate(batches_df.iterrows()):
                col_idx = idx % 3
                with cols[col_idx]:
                    if st.checkbox(
                        f"{batch['batch_id']} - {batch['batch_name']}",
                        key=f"batch_check_{batch['batch_id']}"
                    ):
                        selected_batches.append(batch['batch_id'])
            
            if selected_batches:
                st.warning(f"⚠️ {len(selected_batches)} batch(es) selected for deletion")
                if st.button("🗑️ Delete Selected Batches", key="delete_selected_batches"):
                    # Check if any selected batch has students
                    student_batches_df = read_sheet('Student_Batches')
                    batches_with_students = []
                    for batch_id in selected_batches:
                        batch_students = student_batches_df[student_batches_df['batch_id'] == batch_id]
                        if len(batch_students) > 0:
                            batches_with_students.append((batch_id, len(batch_students)))
                    
                    if batches_with_students:
                        error_msg = "❌ Cannot delete these batches (have enrolled students):\n"
                        for batch_id, count in batches_with_students:
                            error_msg += f"  • {batch_id}: {count} student(s)\n"
                        st.error(error_msg)
                    else:
                        batches_df = batches_df[~batches_df['batch_id'].isin(selected_batches)]
                        write_sheet(batches_df, 'Batches')
                        st.success(f"✅ {len(selected_batches)} batch(es) deleted successfully!")
                        st.rerun()
            
            # Batch statistics
            st.markdown("**Batch Statistics:**")
            col1, col2, col3 = st.columns(3)
            
            students_df = read_sheet('Students')
            
            with col1:
                st.metric("Total Batches", len(batches_df))
            with col2:
                st.metric("Active Batches", len(batches_df[batches_df['status'] == 'Active']))
            with col3:
                st.metric("Total Students", len(students_df))
        else:
            st.info("No batches created yet. Create your first batch above!")

# ==================== STUDENT ENROLLMENT ====================
def student_enrollment():
    """Student enrollment interface."""
    st.markdown('<div class="sub-header">👥 Student Enrollment</div>', unsafe_allow_html=True)
    
    # Ensure Student_Batches sheet exists and migrate if needed
    student_batches_df = ensure_student_batches_sheet()
    
    batches_df = read_sheet('Batches')
    students_df = read_sheet('Students')
    
    tab1, tab2, tab3 = st.tabs(["Add Student", "View Students", "Update Student"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            selected_batches = st.multiselect(
                "Select Batches (Optional)",
                options=batches_df['batch_id'].tolist(),
                format_func=lambda x: f"{x} - {batches_df[batches_df['batch_id']==x]['batch_name'].values[0]}" if len(batches_df) > 0 else x
            )
            student_name = st.text_input("Student Name", placeholder="Full name")
            student_address = st.text_input("Address", placeholder="Street address")
        
        with col2:
            student_phone = st.text_input("Phone Number", placeholder="10-digit phone number")
            join_date = st.date_input("Joining Date")
        
        if st.button("Enroll Student", key="enroll_student"):
            if not student_name or not student_phone or not student_address:
                st.error("❌ Please fill in all fields (Name, Phone, Address)")
                st.error("❌ Please fill in all fields (Name, Phone, Address)")
                return
            
            # Generate student ID
            student_id = f"STU_{len(students_df) + 1:03d}"
            
            new_student = pd.DataFrame({
                'student_id': [student_id],
                'name': [student_name],
                'phone': [student_phone],
                'address': [student_address],
                'join_date': [join_date]
            })
            
            students_df = pd.concat([students_df, new_student], ignore_index=True)
            write_sheet(students_df, 'Students')
            
            # Add student to selected batches (only if batches are selected)
            if len(selected_batches) > 0:
                student_batches_df = read_sheet('Student_Batches')
                for batch_id in selected_batches:
                    new_mapping = pd.DataFrame({
                        'student_id': [student_id],
                        'batch_id': [batch_id]
                    })
                    student_batches_df = pd.concat([student_batches_df, new_mapping], ignore_index=True)
                
                write_sheet(student_batches_df, 'Student_Batches')
                st.balloons()
                st.success(f"✅ Student {student_id} ({student_name}) enrolled in {len(selected_batches)} batch(es)!")
            else:
                st.balloons()
                st.success(f"✅ Student {student_id} ({student_name}) added successfully! You can assign batches later in the Update Student tab.")

    
    with tab2:
        if len(students_df) > 0:
            # Filter options
            filter_batch = st.selectbox(
                "Filter by Batch",
                options=['All'] + batches_df['batch_id'].tolist(),
                key="filter_batch"
            )
            
            # Build display dataframe with batch information
            display_data = []
            for idx, student in students_df.iterrows():
                student_id = student['student_id']
                student_batches_df_current = read_sheet('Student_Batches')
                batches_for_student = student_batches_df_current[student_batches_df_current['student_id'] == student_id]['batch_id'].tolist()
                
                if filter_batch != 'All' and filter_batch not in batches_for_student:
                    continue
                
                batch_names = [f"{bid}" for bid in batches_for_student]
                display_data.append({
                    'student_id': student_id,
                    'name': student['name'],
                    'phone': student['phone'],
                    'address': student.get('address', ''),
                    'join_date': pd.to_datetime(student['join_date']).strftime('%Y-%m-%d'),
                    'batches': ', '.join(batch_names) if batch_names else 'None'
                })
            
            if display_data:
                display_df = pd.DataFrame(display_data)
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "student_id": st.column_config.TextColumn("Student ID", width="small"),
                        "name": st.column_config.TextColumn("Name", width="medium"),
                        "phone": st.column_config.TextColumn("Phone", width="medium"),
                        "address": st.column_config.TextColumn("Address", width="large"),
                        "join_date": st.column_config.TextColumn("Join Date", width="medium"),
                        "batches": st.column_config.TextColumn("Batches", width="large")
                    }
                )
                
                st.caption(f"Total: {len(display_df)} students")
                
                # Delete student section with checkboxes
                st.markdown("---")
                st.markdown("**Delete Student(s) - Select using checkboxes:**")
                
                st.markdown("**Select Students to Delete:**")
                cols = st.columns(3)
                selected_students = []
                
                for idx, (_, student) in enumerate(display_df.iterrows()):
                    col_idx = idx % 3
                    with cols[col_idx]:
                        if st.checkbox(
                            f"{student['student_id']} - {student['name']}",
                            key=f"student_check_{student['student_id']}"
                        ):
                            selected_students.append(student['student_id'])
                
                if selected_students:
                    st.warning(f"⚠️ {len(selected_students)} student(s) selected for deletion")
                    if st.button("🗑️ Delete Selected Students", key="delete_selected_students"):
                        # Delete each selected student
                        students_df = read_sheet('Students')
                        student_batches_df = read_sheet('Student_Batches')
                        payments_df = read_sheet('Payments')
                        
                        deleted_students = []
                        for student_id in selected_students:
                            student_name = students_df[students_df['student_id'] == student_id]['name'].values[0]
                            deleted_students.append(f"{student_id} ({student_name})")
                            
                            # Delete from all sheets
                            students_df = students_df[students_df['student_id'] != student_id]
                            student_batches_df = student_batches_df[student_batches_df['student_id'] != student_id]
                            payments_df = payments_df[payments_df['student_id'] != student_id]
                        
                        write_sheet(students_df, 'Students')
                        write_sheet(student_batches_df, 'Student_Batches')
                        write_sheet(payments_df, 'Payments')
                        
                        success_msg = f"✅ {len(selected_students)} student(s) and their records deleted:\n"
                        for student_info in deleted_students:
                            success_msg += f"  • {student_info}\n"
                        st.success(success_msg)
                        st.rerun()
            else:
                st.info("No students in this batch.")
        else:
            st.info("No students enrolled yet.")
    
    with tab3:
        if len(students_df) > 0:
            st.markdown("**Update Student Information:**")
            
            student_to_update = st.selectbox(
                "Select Student to Update",
                options=students_df['student_id'].tolist(),
                format_func=lambda x: f"{x} - {students_df[students_df['student_id']==x]['name'].values[0]}",
                key="student_update_select"
            )
            
            # Get current student data
            current_student = students_df[students_df['student_id'] == student_to_update].iloc[0]
            
            col1, col2 = st.columns(2)
            with col1:
                updated_name = st.text_input("Student Name", value=current_student['name'], key="update_name")
                updated_phone = st.text_input("Phone Number", value=current_student['phone'], key="update_phone")
            
            with col2:
                updated_address = st.text_input("Address", value=current_student.get('address', ''), key="update_address")
                updated_join_date = st.date_input("Joining Date", value=pd.to_datetime(current_student['join_date']).date(), key="update_join_date")
            
            # Get current batches for this student
            student_batches_df_current = read_sheet('Student_Batches')
            current_batches = student_batches_df_current[student_batches_df_current['student_id'] == student_to_update]['batch_id'].tolist()
            
            # Filter current_batches to only include batches that exist in current batches_df
            available_batch_ids = batches_df['batch_id'].tolist()
            valid_current_batches = [b for b in current_batches if b in available_batch_ids]
            
            updated_batches = st.multiselect(
                "Update Batches (Optional)",
                options=available_batch_ids,
                default=valid_current_batches,
                format_func=lambda x: f"{x} - {batches_df[batches_df['batch_id']==x]['batch_name'].values[0]}" if len(batches_df) > 0 else x,
                key="update_batches"
            )
            
            if st.button("Update Student", key="update_student_btn"):
                if not updated_name or not updated_phone or not updated_address:
                    st.error("❌ Please fill in all fields (Name, Phone, Address)")
                    return
                
                # Update student info
                students_df.loc[students_df['student_id'] == student_to_update, 'name'] = updated_name
                students_df.loc[students_df['student_id'] == student_to_update, 'phone'] = updated_phone
                students_df.loc[students_df['student_id'] == student_to_update, 'address'] = updated_address
                students_df.loc[students_df['student_id'] == student_to_update, 'join_date'] = updated_join_date
                
                write_sheet(students_df, 'Students')
                
                # Update batch associations (only if batches are selected)
                student_batches_df_current = read_sheet('Student_Batches')
                student_batches_df_current = student_batches_df_current[student_batches_df_current['student_id'] != student_to_update]
                
                if len(updated_batches) > 0:
                    for batch_id in updated_batches:
                        new_mapping = pd.DataFrame({
                            'student_id': [student_to_update],
                            'batch_id': [batch_id]
                        })
                        student_batches_df_current = pd.concat([student_batches_df_current, new_mapping], ignore_index=True)
                
                write_sheet(student_batches_df_current, 'Student_Batches')
                st.success(f"✅ Student {student_to_update} ({updated_name}) updated successfully!")
                st.rerun()
        else:
            st.info("No students enrolled yet.")

# ==================== PAYMENT TRACKER ====================
def payment_tracker():
    """Payment logging and tracking interface."""
    st.markdown('<div class="sub-header">💰 Payment Tracker</div>', unsafe_allow_html=True)
    
    students_df = read_sheet('Students')
    payments_df = read_sheet('Payments')
    
    tab1, tab2, tab3 = st.tabs(["Log Payment", "View Payments", "Payment History"])
    
    with tab1:
        if len(students_df) == 0:
            st.warning("⚠️ No students enrolled. Please enroll a student first.")
            return
        
        col1, col2 = st.columns(2)
        with col1:
            selected_student = st.selectbox(
                "Select Student",
                options=students_df['student_id'].tolist(),
                format_func=lambda x: f"{x} - {students_df[students_df['student_id']==x]['name'].values[0]}"
            )
            amount = st.number_input("Amount Paid (₹)", min_value=0.0, value=0.0)
        
        with col2:
            pay_date = st.date_input("Payment Date")
            remarks = st.text_input("Remarks (e.g., UPI, Cash, Cheque)", placeholder="Optional")
        
        if st.button("Log Payment", key="log_payment"):
            if amount <= 0:
                st.error("❌ Amount must be greater than 0")
                return
            
            # Generate payment ID
            payment_id = f"PAY_{len(payments_df) + 1:05d}"
            
            new_payment = pd.DataFrame({
                'payment_id': [payment_id],
                'student_id': [selected_student],
                'amount': [amount],
                'pay_date': [pay_date],
                'remarks': [remarks]
            })
            
            payments_df = pd.concat([payments_df, new_payment], ignore_index=True)
            write_sheet(payments_df, 'Payments')
            st.balloons()
    
    with tab2:
        if len(payments_df) > 0:
            display_df = payments_df.copy()
            display_df['pay_date'] = pd.to_datetime(display_df['pay_date']).dt.strftime('%Y-%m-%d')
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "payment_id": st.column_config.TextColumn("Payment ID", width="medium"),
                    "student_id": st.column_config.TextColumn("Student ID", width="medium"),
                    "amount": st.column_config.NumberColumn("Amount (₹)", format="₹ %.2f"),
                    "pay_date": st.column_config.TextColumn("Payment Date", width="medium"),
                    "remarks": st.column_config.TextColumn("Remarks", width="large")
                }
            )
        else:
            st.info("No payments recorded yet.")
    
    with tab3:
        if len(students_df) > 0 and len(payments_df) > 0:
            selected_student_history = st.selectbox(
                "Select Student",
                options=students_df['student_id'].tolist(),
                format_func=lambda x: f"{x} - {students_df[students_df['student_id']==x]['name'].values[0]}",
                key="history_student"
            )
            
            student_payments = payments_df[payments_df['student_id'] == selected_student_history].copy()
            
            if len(student_payments) > 0:
                student_payments['pay_date'] = pd.to_datetime(student_payments['pay_date']).dt.strftime('%Y-%m-%d')
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Payments", len(student_payments))
                with col2:
                    st.metric("Total Amount Paid", f"₹ {student_payments['amount'].sum():.2f}")
                with col3:
                    st.metric("Average Payment", f"₹ {student_payments['amount'].mean():.2f}")
                
                st.dataframe(
                    student_payments,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No payment history for this student.")

# ==================== DASHBOARD / REPORTS ====================
def dashboard():
    """Analytics and reporting dashboard."""
    st.markdown('<div class="sub-header">📊 Dashboard</div>', unsafe_allow_html=True)
    
    batches_df = read_sheet('Batches')
    students_df = read_sheet('Students')
    payments_df = read_sheet('Payments')
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Batches", len(batches_df))
    with col2:
        st.metric("Total Students", len(students_df))
    with col3:
        total_revenue = payments_df['amount'].sum() if len(payments_df) > 0 else 0
        st.metric("Total Revenue", f"₹ {total_revenue:.2f}")
    with col4:
        today = datetime.now().date()
        month_start = datetime(today.year, today.month, 1).date()
        month_payments = payments_df[
            (pd.to_datetime(payments_df['pay_date']).dt.date >= month_start) &
            (pd.to_datetime(payments_df['pay_date']).dt.date <= today)
        ] if len(payments_df) > 0 else pd.DataFrame()
        month_revenue = month_payments['amount'].sum() if len(month_payments) > 0 else 0
        st.metric("This Month's Revenue", f"₹ {month_revenue:.2f}")
    
    st.divider()
    
    # Revenue over time
    if len(payments_df) > 0:
        st.markdown("**Revenue Trend**")
        payments_df_copy = payments_df.copy()
        payments_df_copy['pay_date'] = pd.to_datetime(payments_df_copy['pay_date'])
        payments_df_copy['month'] = payments_df_copy['pay_date'].dt.to_period('M').astype(str)
        
        monthly_revenue = payments_df_copy.groupby('month')['amount'].sum().reset_index()
        monthly_revenue.columns = ['Month', 'Revenue']
        
        st.line_chart(monthly_revenue.set_index('Month'))
    
    st.divider()
    
    # Defaulter list (30 days)
    st.markdown("**⚠️ Payment Defaulters (No payment in last 30 days)**")
    
    if len(students_df) > 0 and len(payments_df) > 0:
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        
        payments_df_copy = payments_df.copy()
        payments_df_copy['pay_date'] = pd.to_datetime(payments_df_copy['pay_date']).dt.date
        
        # Get last payment date for each student
        last_payments = payments_df_copy.groupby('student_id')['pay_date'].max().reset_index()
        last_payments.columns = ['student_id', 'last_payment_date']
        
        # Students who haven't paid in 30 days
        defaulters = last_payments[last_payments['last_payment_date'] < thirty_days_ago]['student_id'].tolist()
        
        # Also add students with no payments
        all_students = students_df['student_id'].tolist()
        students_with_no_payments = [s for s in all_students if s not in last_payments['student_id'].tolist()]
        defaulters.extend(students_with_no_payments)
        
        if len(defaulters) > 0:
            defaulter_details = students_df[students_df['student_id'].isin(defaulters)][['student_id', 'name', 'phone']].copy()
            
            st.dataframe(
                defaulter_details,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "student_id": st.column_config.TextColumn("Student ID"),
                    "name": st.column_config.TextColumn("Name"),
                    "phone": st.column_config.TextColumn("Phone")
                }
            )
        else:
            st.success("✅ No defaulters! All students are up to date.")
    else:
        st.info("No payment data available.")
    
    st.divider()
    
    # Batch occupancy
    st.markdown("**Batch Occupancy**")
    if len(batches_df) > 0 and len(students_df) > 0:
        student_batches_df = read_sheet('Student_Batches')
        if len(student_batches_df) > 0:
            occupancy = student_batches_df['batch_id'].value_counts().reset_index()
            occupancy.columns = ['batch_id', 'students']
            
            occupancy = occupancy.merge(batches_df[['batch_id', 'batch_name']], on='batch_id')
            occupancy = occupancy[['batch_name', 'students']]
            
            st.bar_chart(occupancy.set_index('batch_name'))
        else:
            st.info("Enroll students to batches to see occupancy.")
    else:
        st.info("Create batches and enroll students to see occupancy.")

# ==================== MAIN APP ====================
def main():
    """Main application."""
    initialize_excel_file()
    
    if not check_password():
        return
    
    # Sidebar navigation
    st.sidebar.markdown('<div class="main-header">📚 Coaching Hub</div>', unsafe_allow_html=True)
    
    page = st.sidebar.radio(
        "Navigation",
        ["📊 Dashboard", "📋 Batch Manager", "👥 Student Enrollment", "💰 Payment Tracker"]
    )
    
    st.sidebar.divider()
    
    # Change password (optional)
    if st.sidebar.checkbox("Change Password"):
        old_password = st.sidebar.text_input("Current Password", type="password")
        new_password = st.sidebar.text_input("New Password", type="password")
        confirm_password = st.sidebar.text_input("Confirm Password", type="password")
        
        if st.sidebar.button("Update Password"):
            if old_password == "admin123" and new_password == confirm_password:
                st.sidebar.success("Password update feature - implement as needed")
            else:
                st.sidebar.error("Invalid password")
    
    # Main content
    if "Dashboard" in page:
        dashboard()
    elif "Batch Manager" in page:
        batch_manager()
    elif "Student Enrollment" in page:
        student_enrollment()
    elif "Payment Tracker" in page:
        payment_tracker()
    
    # Footer
    st.sidebar.divider()
    st.sidebar.caption("Coaching Management System v1.0")

if __name__ == "__main__":
    main()
