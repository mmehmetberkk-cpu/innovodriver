"""
Streamlit Araç Kontrol Formu Uygulaması
FastAPI uygulamasının Streamlit versiyonu
"""
import streamlit as st
from excel_handler import (
    load_vehicles, load_fuel_levels, load_check_fields,
    load_items, load_users, save_form_submission,
    load_form_submissions, is_admin, update_excel_with_admin_column,
    get_user_by_email, generate_reset_code, save_reset_code,
    send_reset_code_email, verify_reset_code, update_user_password,
    delete_reset_code, update_user_email,
    add_user, delete_user, update_user,
    add_vehicle, delete_vehicle, update_vehicle,
    add_fuel_level, delete_fuel_level, update_fuel_level,
    add_check_field, delete_check_field, update_check_field,
    add_item, delete_item, update_item
)

# Uygulama başlangıcında Excel dosyasını güncelle (sadece Excel kullanılıyorsa)
# Google Sheets kullanılıyorsa bu fonksiyon hiçbir şey yapmaz
try:
    update_excel_with_admin_column()
except Exception as e:
    # Bulut ortamında Excel dosyası olmayabilir, bu normal
    pass

# Page configuration - Mobile optimization
# Admin panel için sidebar açık, diğer sayfalar için kapalı
st.set_page_config(
    page_title="Vehicle Inspection",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="auto"
)

# Mobile CSS optimization - White & Blue Theme
st.markdown("""
<style>
    /* Main App Background - White */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f0f7ff 100%);
        padding: 0.5rem;
    }
    
    /* Sidebar - Blue Theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 50%, #2563eb 100%);
        box-shadow: 2px 0 10px rgba(30, 58, 138, 0.2);
    }
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        text-align: left;
        padding: 0.85rem 1.2rem;
        margin-bottom: 0.6rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        background-color: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
        font-size: 0.95rem;
        font-weight: 500;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        transform: translateX(8px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.5);
        background-color: rgba(255, 255, 255, 0.25);
        border-color: rgba(255, 255, 255, 0.4);
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background-color: #ffffff;
        color: #1e40af;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background-color: #f0f7ff;
        transform: translateX(8px);
    }
    [data-testid="stSidebar"] h1 {
        color: #ffffff;
        font-size: 1.6rem;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
        font-weight: 700;
    }
    [data-testid="stSidebar"] .stCaption {
        color: #c7d2fe;
        font-size: 0.85rem;
        margin-top: 1rem;
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e7ff;
    }
    
    /* Main Content Area - White Background with Better Spacing */
    .main .block-container {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 2.5rem;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.08);
        max-width: 1400px;
    }
    
    /* Admin Panel Content Styling */
    .element-container {
        margin-bottom: 1rem;
    }
    
    /* Better spacing for admin sections */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column"] > [data-testid="stVerticalBlock"] {
        gap: 1rem;
    }
    
    /* Form containers in admin panel */
    .stForm {
        background-color: #f8fafc;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
    
    /* Radio buttons in admin - better spacing */
    .stRadio > div {
        gap: 1rem;
        padding: 0.5rem 0;
    }
    
    /* Metric cards - better styling */
    [data-testid="stMetricContainer"] {
        background-color: #f0f7ff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dbeafe;
    }
    
    /* Headers - Blue Color */
    h1 {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        color: #1e40af;
        font-weight: 700;
    }
    h2 {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        margin-bottom: 0.3rem;
        color: #2563eb;
        font-weight: 600;
    }
    h3 {
        font-size: 1rem;
        margin-top: 0.3rem;
        margin-bottom: 0.2rem;
        color: #3b82f6;
        font-weight: 600;
    }
    h4 {
        font-size: 0.9rem;
        margin-top: 0.2rem;
        margin-bottom: 0.1rem;
        color: #60a5fa;
    }
    
    /* Buttons - Blue Theme */
    .stButton > button:not([data-testid="stSidebar"] .stButton > button) {
        min-height: 44px;
        font-size: 16px;
        border-radius: 8px;
        background-color: #2563eb;
        color: #ffffff;
        border: none;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    .stButton > button:not([data-testid="stSidebar"] .stButton > button):hover {
        background-color: #1e40af;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        transform: translateY(-2px);
    }
    .stButton > button[kind="secondary"] {
        background-color: #ffffff;
        color: #2563eb;
        border: 2px solid #2563eb;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #eff6ff;
        border-color: #1e40af;
    }
    
    /* Input Fields - White with Blue Border */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        font-size: 16px;
        border: 2px solid #dbeafe;
        border-radius: 8px;
        background-color: #ffffff;
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* Forms - White Background */
    .stForm {
        padding: 0.5rem;
        background-color: #ffffff;
        border-radius: 10px;
        border: 1px solid #dbeafe;
    }
    /* Compact input fields */
    .stTextInput > div > div > input {
        font-size: 16px; /* Prevent iOS zoom */
    }
    .stSelectbox > div > div > select {
        font-size: 16px;
    }
    .stNumberInput > div > div > input {
        font-size: 16px;
    }
    /* Smaller headers */
    h1 {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    h2 {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        margin-bottom: 0.3rem;
    }
    h3 {
        font-size: 1rem;
        margin-top: 0.3rem;
        margin-bottom: 0.2rem;
    }
    h4 {
        font-size: 0.9rem;
        margin-top: 0.2rem;
        margin-bottom: 0.1rem;
    }
    /* Radio Buttons - Blue Theme */
    .stRadio > div {
        gap: 0.5rem;
    }
    .stRadio > div > label {
        color: #1e40af;
        font-weight: 500;
    }
    
    /* Tabs - Blue Theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: #eff6ff;
        border-radius: 8px;
        padding: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        color: #2563eb;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb;
        color: #ffffff;
        font-weight: 600;
    }
    
    /* Success/Error/Info/Warning Messages - Blue Theme */
    .stSuccess {
        background-color: #dbeafe;
        border-left: 4px solid #2563eb;
        color: #1e40af;
        padding: 1rem;
        border-radius: 8px;
    }
    .stError {
        background-color: #fee2e2;
        border-left: 4px solid #dc2626;
        color: #991b1b;
        padding: 1rem;
        border-radius: 8px;
    }
    .stInfo {
        background-color: #e0f2fe;
        border-left: 4px solid #0ea5e9;
        color: #0c4a6e;
        padding: 1rem;
        border-radius: 8px;
    }
    .stWarning {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        color: #92400e;
        padding: 1rem;
        border-radius: 8px;
    }
    
    /* Checkboxes - Blue Theme */
    .stCheckbox > label {
        color: #1e40af;
        font-weight: 500;
    }
    .stCheckbox input[type="checkbox"]:checked {
        background-color: #2563eb;
        border-color: #2563eb;
    }
    
    /* Selectbox - Blue Theme */
    .stSelectbox > div > div {
        background-color: #ffffff;
        border: 2px solid #dbeafe;
        border-radius: 8px;
    }
    
    /* Expander - Blue Theme */
    .streamlit-expanderHeader {
        background-color: #eff6ff;
        color: #1e40af;
        border-radius: 8px;
        padding: 0.75rem;
        font-weight: 600;
    }
    .streamlit-expanderHeader:hover {
        background-color: #dbeafe;
    }
    
    /* Dataframe - White Background */
    .stDataFrame {
        background-color: #ffffff;
        border: 1px solid #dbeafe;
        border-radius: 8px;
    }
    
    /* Metric Cards - Blue Theme */
    [data-testid="stMetricValue"] {
        color: #1e40af;
        font-weight: 700;
    }
    [data-testid="stMetricLabel"] {
        color: #3b82f6;
    }
    
    /* Divider - Blue */
    hr {
        border-color: #dbeafe;
        margin: 1.5rem 0;
    }
    
    /* Logo container */
    [data-testid="stImage"] {
        margin-bottom: 0.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(30, 58, 138, 0.1);
    }
    
    /* Compact form elements */
    .element-container {
        margin-bottom: 0.5rem;
    }
    
    /* Text - Blue accents */
    .stMarkdown {
        color: #1f2937;
    }
    .stMarkdown strong {
        color: #1e40af;
    }
    
    /* Caption - Light Blue */
    .stCaption {
        color: #60a5fa;
    }
</style>
""", unsafe_allow_html=True)

# Session state başlatma
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'full_name' not in st.session_state:
    st.session_state.full_name = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "form"
if 'reset_email' not in st.session_state:
    st.session_state.reset_email = None
if 'reset_code' not in st.session_state:
    st.session_state.reset_code = None
if 'reset_username' not in st.session_state:
    st.session_state.reset_username = None
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'submitted_form_data' not in st.session_state:
    st.session_state.submitted_form_data = None
if 'admin_message' not in st.session_state:
    st.session_state.admin_message = None
if 'admin_message_type' not in st.session_state:
    st.session_state.admin_message_type = None
if 'admin_section' not in st.session_state:
    st.session_state.admin_section = "form_submissions"
if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = False

def thank_you_page():
    """Thank you page after form submission"""
    try:
        st.image("Innovo.PNG", width=200)
    except:
        pass
    
    st.markdown("## 🙏 Thank You!")
    st.markdown("### Your form has been submitted successfully.")
    
    st.balloons()
    st.success("✅ Form submitted successfully!")
    
    if st.session_state.submitted_form_data:
        form_data = st.session_state.submitted_form_data
        st.markdown("---")
        st.markdown("#### 📋 Submitted Information")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Driver:** {form_data.get('driver_name', 'N/A')}")
            st.write(f"**Vehicle:** {form_data.get('vehicle', 'N/A')}")
            st.write(f"**Odometer:** {form_data.get('odometer_start', 'N/A')} KM")
            st.write(f"**Fuel Level:** {form_data.get('fuel_level', 'N/A')}")
        
        with col2:
            st.write(f"**Oil Level:** {form_data.get('oil_level', 'N/A')}")
            st.write(f"**Fuel Card:** {form_data.get('fuel_card', 'N/A')}")
            st.write(f"**Measuring Tape:** {form_data.get('measuring_tape', 'N/A')}")
            st.write(f"**Safety Vest:** {form_data.get('safety_vest', 'N/A')}")
    
    st.markdown("---")
    
    if st.button("📝 Submit Another Form", width='stretch', type="primary"):
        st.session_state.form_submitted = False
        st.session_state.submitted_form_data = None
        st.rerun()

def login_page():
    """Login sayfası"""
    # Logging bulut ortamında devre dışı
    def _log(hypothesis_id, location, message, data):
        pass
    
    st.markdown("### 🔐 Giriş")
    
    # Excel'den kullanıcıları yükle
    # #region agent log
    _log("C", "app.py:login_page:before_load_users", "About to load users", {})
    # #endregion agent log
    try:
        users = load_users()
        # #region agent log
        _log("C", "app.py:login_page:after_load_users", "Users loaded", {"user_count": len(users), "usernames": list(users.keys())})
        # #endregion agent log
        
        # Show warning if no users found
        if not users:
            st.warning("⚠️ No users found. Please check your data source (Excel file or Google Sheets).")
            st.info("💡 If using Excel, make sure `form_data.xlsx` exists. If using Google Sheets, check your credentials in Streamlit secrets.")
    except Exception as e:
        st.error(f"❌ Error loading users: {str(e)}")
        st.info("💡 Please check your data source configuration. For Streamlit Cloud, you may need to configure Google Sheets or ensure the Excel file is accessible.")
        users = {}
    
    with st.form("login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("Login", width='stretch')
        with col2:
            reset_button = st.form_submit_button("🔑 Reset", width='stretch')
        
        if reset_button:
            st.session_state.current_page = "reset_password"
            st.rerun()
        
        if submit_button:
            # #region agent log
            _log("C", "app.py:login_page:submit_clicked", "Login form submitted", {"username": username, "password_provided": bool(password)})
            # #endregion agent log
            user = users.get(username)
            # #region agent log
            _log("C", "app.py:login_page:user_lookup", "User lookup result", {"username": username, "user_found": user is not None, "user_data": user if user else None})
            # #endregion agent log
            if user and user["password"] == password:
                # #region agent log
                _log("C", "app.py:login_page:password_match", "Password matched", {"username": username})
                # #endregion agent log
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.full_name = user["full_name"]
                # #region agent log
                _log("C", "app.py:login_page:before_is_admin", "About to check admin status", {"username": username})
                # #endregion agent log
                admin_status = is_admin(username)
                # #region agent log
                _log("C", "app.py:login_page:after_is_admin", "Admin status checked", {"username": username, "is_admin": admin_status})
                # #endregion agent log
                st.session_state.is_admin = admin_status
                st.session_state.current_page = "form"
                st.session_state.show_welcome = True  # Welcome message flag
                st.success("✅ Login successful!")
                st.rerun()
            else:
                # #region agent log
                _log("C", "app.py:login_page:login_failed", "Login failed", {"username": username, "user_found": user is not None, "password_match": user["password"] == password if user else False})
                # #endregion agent log
                st.error("❌ Invalid username or password!")
                st.info("💡 Forgot your password? Use the 'Reset Password' button above.")

def reset_password_page():
    """Password reset page - Email entry"""
    try:
        st.image("Innovo.PNG", width=150)
    except:
        pass
    
    st.markdown("### 🔑 Password Reset")
    
    if st.session_state.reset_code is None:
        # Email entry stage
        st.write("Enter your registered email address to reset your password.")
        st.info("💡 Your email address must be registered in the Users sheet.")
        
        with st.form("reset_email_form"):
            email = st.text_input("Email Address", key="reset_email_input", placeholder="example@email.com")
            submit_button = st.form_submit_button("Send Code", width='stretch')
            
            if submit_button:
                if email:
                    # Find user by email address
                    username, user_data = get_user_by_email(email)
                    if username and user_data:
                        # Generate and send code
                        code = generate_reset_code()
                        save_reset_code(email, code, username)
                        send_reset_code_email(email, code)
                        
                        st.session_state.reset_email = email
                        st.session_state.reset_code = code
                        st.session_state.reset_username = username
                        
                        st.success(f"✅ Password reset code sent to {email}!")
                        st.info("📧 Please check your email. The code is valid for 10 minutes.")
                        st.rerun()
                    else:
                        st.error("❌ No user found with this email address!")
                        st.info("💡 If your email is not registered in the Users sheet, please contact an administrator.")
                else:
                    st.warning("⚠️ Please enter your email address!")
        
        # Back button
        if st.button("⬅️ Back to Login", width='stretch'):
            st.session_state.current_page = "login"
            st.session_state.reset_email = None
            st.rerun()
    
    elif st.session_state.reset_code and st.session_state.reset_username:
        # Code verification and new password stage
        st.write(f"Email: **{st.session_state.reset_email}**")
        
        with st.form("reset_code_form"):
            entered_code = st.text_input("Reset Code", key="reset_code_input", placeholder="6-digit code")
            new_password = st.text_input("New Password", type="password", key="new_password_input")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password_input")
            submit_button = st.form_submit_button("Update Password", width='stretch')
            
            if submit_button:
                if not entered_code:
                    st.warning("⚠️ Please enter the reset code!")
                elif not new_password:
                    st.warning("⚠️ Please enter your new password!")
                elif new_password != confirm_password:
                    st.error("❌ Passwords do not match!")
                else:
                    # Verify code
                    username, email = verify_reset_code(entered_code)
                    if username and username == st.session_state.reset_username and entered_code == st.session_state.reset_code:
                        # Update password
                        if update_user_password(username, new_password):
                            # Delete code
                            delete_reset_code(entered_code)
                            
                            # Clear session state
                            st.session_state.reset_email = None
                            st.session_state.reset_code = None
                            st.session_state.reset_username = None
                            
                            st.success("✅ Your password has been updated successfully!")
                            st.info("🔐 You can now login with your new password.")
                            
                            if st.button("⬅️ Back to Login", width='stretch'):
                                st.session_state.current_page = "login"
                                st.rerun()
                        else:
                            st.error("❌ An error occurred while updating the password!")
                    else:
                        st.error("❌ Invalid or expired code!")
        
        # Resend code
        if st.button("🔄 Resend Code", width='stretch'):
            code = generate_reset_code()
            save_reset_code(st.session_state.reset_email, code, st.session_state.reset_username)
            send_reset_code_email(st.session_state.reset_email, code)
            st.session_state.reset_code = code
            st.success("✅ New code sent!")
            st.rerun()
        
        # Cancel button
        if st.button("❌ Cancel", width='stretch'):
            st.session_state.reset_email = None
            st.session_state.reset_code = None
            st.session_state.reset_username = None
            st.session_state.current_page = "login"
            st.rerun()

def form_page():
    """Vehicle inspection form page - Mobile optimized"""
    # Check if form was just submitted
    if st.session_state.form_submitted:
        thank_you_page()
        return
    
    # Welcome message (show once after login)
    if st.session_state.get("show_welcome", False):
        st.success(f"🎉 Welcome to InnovoExpress, {st.session_state.full_name}! We're glad to have you here.")
        st.session_state.show_welcome = False  # Clear flag after showing
    
    # Logo and header - Centered and mobile-friendly
    try:
        # Center logo
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("Innovo.PNG", width='stretch')
        st.markdown("### 🚗 Vehicle Inspection")
        st.caption(f"👤 Driver: {st.session_state.full_name}")
    except:
        st.markdown("### 🚗 Vehicle Inspection Form")
        st.caption(f"👤 Driver: {st.session_state.full_name}")
    
    # Excel'den verileri yükle
    vehicles = load_vehicles()
    fuel_levels = load_fuel_levels()
    items = load_items()
    
    # Kontrol kategorileri
    exterior_fields = load_check_fields("ExteriorChecks")
    engine_fields = load_check_fields("EngineChecks")
    safety_fields = load_check_fields("SafetyEquipment")
    interior_fields = load_check_fields("InteriorChecks")
    
    st.markdown("---")
    st.markdown("#### 📋 Basic Information")
    
    # Vehicle selection - Outside form (for auto rerun)
    vehicle_options = [""] + vehicles + ["Other"]
    selected_vehicle = st.selectbox(
        "Vehicle *",
        options=vehicle_options,
        key="vehicle_select"
    )
        
    # Other Vehicle (conditional) - Outside form
    # Clear session state when "Other" is not selected
    if selected_vehicle != "Other":
        if "other_vehicle_input" in st.session_state:
            del st.session_state.other_vehicle_input
        other_vehicle = ""
    else:
        st.markdown("---")
        st.info("ℹ️ **Manual Vehicle Entry:** Please enter the vehicle manually")
        # Get value from session state, or empty string
        current_value = st.session_state.get("other_vehicle_input", "")
        other_vehicle = st.text_input(
            "Vehicle Information *",
            placeholder="e.g., FORD Transit 2020",
            key="other_vehicle_input",
            help="Enter vehicle information here",
            label_visibility="visible",
            value=current_value
        )
        if not other_vehicle or other_vehicle.strip() == "":
            st.warning("⚠️ Please enter vehicle information!")
        st.markdown("---")
    
    # Create form
    with st.form("vehicle_inspection_form"):
        # Compact basic information - 2 columns
        col1, col2 = st.columns(2)
        
        with col1:
            # Driver Name (readonly) - hidden, only for data
            driver_name = st.session_state.full_name
            
            # Show vehicle information in form (readonly)
            if selected_vehicle == "Other" and other_vehicle:
                st.text_input("🚗 Vehicle", value=other_vehicle, disabled=True, key="vehicle_display")
            elif selected_vehicle and selected_vehicle != "Other":
                st.text_input("🚗 Vehicle", value=selected_vehicle, disabled=True, key="vehicle_display")
        
        # Odometer Reading
        odometer_start = st.number_input(
                "📏 Odometer (KM)",
            min_value=0,
            step=1,
                key="odometer_input",
                help="Starting kilometrage"
        )
        
        with col2:
            # Fuel Level
            fuel_options = [""] + fuel_levels
            fuel_level = st.selectbox(
                "⛽ Fuel Level",
                options=fuel_options,
                key="fuel_level_select"
            )
        
            # Other Fuel (conditional)
        other_fuel = None
        if fuel_level == "Other":
            other_fuel = st.text_input(
                    "Fuel Level (Manual)",
                    placeholder="Enter manually",
                key="other_fuel_input"
            )
        
            # Oil Level - Percentage list
            oil_level_options = ["", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%", "Other"]
            oil_level = st.selectbox(
                "🛢️ Oil Level",
                options=oil_level_options,
                key="oil_level_select"
            )
            
            # Other Oil Level (conditional)
            other_oil = None
            if oil_level == "Other":
                other_oil = st.text_input(
                    "Oil Level (Manual)",
                    placeholder="e.g., 15% or Low",
                    key="other_oil_input"
                )
        
        st.markdown("---")
        
        # Mobile tabs to group categories
        tab1, tab2, tab3, tab4 = st.tabs(["🔍 Exterior", "⚙️ Engine", "🛡️ Safety", "🚪 Interior"])
        
        # Exterior Checks
        with tab1:
            exterior_icons = {
                "headlights": "💡", "break_lights": "🛑", "indicators": "➡️",
                "mirrors": "🪞", "windows": "🪟", "windshield": "🚗",
                "wiper_fluid": "💧", "wipers": "🧹", "tires": "⚙️", "body_paint": "🎨"
            }
            exterior_checks = {}
            for field in exterior_fields:
                field_display = field.replace("_", " ").title()
                icon = exterior_icons.get(field, "✅")
                exterior_checks[field] = st.radio(
                    f"{icon} {field_display}",
                    options=["✅ OK", "⚠️ Needs Attention"],
                    horizontal=True,
                    key=f"exterior_{field}",
                    label_visibility="visible"
                )
                # Normalize radio values
                if exterior_checks[field] == "✅ OK":
                    exterior_checks[field] = "OK"
                else:
                    exterior_checks[field] = "Needs Attention"
        
        # Engine & Mechanical Checks
        with tab2:
            engine_checks = {}
            for field in engine_fields:
                field_display = field.replace("_", " ").title()
                engine_checks[field] = st.radio(
                    field_display,
                    options=["✅ OK", "⚠️ Needs Attention"],
                    horizontal=True,
                    key=f"engine_{field}",
                    label_visibility="visible"
                )
                if engine_checks[field] == "✅ OK":
                    engine_checks[field] = "OK"
                else:
                    engine_checks[field] = "Needs Attention"
        
        # Safety Equipment
        with tab3:
            safety_checks = {}
            for field in safety_fields:
                field_display = field.replace("_", " ").title()
                safety_checks[field] = st.radio(
                    field_display,
                    options=["✅ OK", "⚠️ Needs Attention"],
                    horizontal=True,
                    key=f"safety_{field}",
                    label_visibility="visible"
                )
                if safety_checks[field] == "✅ OK":
                    safety_checks[field] = "OK"
                else:
                    safety_checks[field] = "Needs Attention"
        
        # Interior Checks
        with tab4:
            interior_checks = {}
            for field in interior_fields:
                field_display = field.replace("_", " ").title()
                interior_checks[field] = st.radio(
                    field_display,
                    options=["✅ OK", "⚠️ Needs Attention"],
                    horizontal=True,
                    key=f"interior_{field}",
                    label_visibility="visible"
                )
                if interior_checks[field] == "✅ OK":
                    interior_checks[field] = "OK"
                else:
                    interior_checks[field] = "Needs Attention"
        
        st.markdown("---")
        
        # Items in Vehicle - Compact view
        st.markdown("#### 📦 Items in Vehicle")
        
        # 3-column compact view
        col1, col2, col3 = st.columns(3)
        with col1:
            fuel_card = st.radio("Fuel Card", ["✅", "❌"], horizontal=True, key="fuel_card_radio")
            fuel_card = "Yes" if fuel_card == "✅" else "No"
        with col2:
            measuring_tape = st.radio("Measuring Tape", ["✅", "❌"], horizontal=True, key="measuring_tape_radio")
            measuring_tape = "Yes" if measuring_tape == "✅" else "No"
        with col3:
            safety_vest = st.radio("Safety Vest", ["✅", "❌"], horizontal=True, key="safety_vest_radio")
            safety_vest = "Yes" if safety_vest == "✅" else "No"
        
        # Fuel Amount - Compact
        fuel_amount = st.text_input(
            "💰 Fuel Amount ($)",
            placeholder="Amount",
            key="fuel_amount_input"
        )
        
        # Additional Comments and/or Concerns
        additional_comments = st.text_area(
            "Additional Comments and/or Concerns:",
            placeholder="Please let us know here...",
            key="additional_comments_input",
            height=100,
            help="Enter any additional comments or concerns"
        )
        
        st.markdown("---")
        
        # Large, touch-friendly submit button
        submit_button = st.form_submit_button(
            "✅ SUBMIT FORM",
            width='stretch',
            type="primary"
        )
        
        if submit_button:
            # Validation: If "Other" is selected, manual entry is required
            if selected_vehicle == "Other" and not other_vehicle:
                st.error("❌ Please enter vehicle information when 'Other' is selected!")
                st.stop()
            
            # Ensure other_vehicle is only used when "Other" is selected
            if selected_vehicle != "Other":
                other_vehicle = ""  # Clear other_vehicle if not "Other"
            
            # Collect form data
            final_vehicle = other_vehicle if (selected_vehicle == "Other" and other_vehicle) else selected_vehicle
            form_data = {
                "driver_name": driver_name,
                "vehicle": final_vehicle,  # Manual entry if "Other" selected, otherwise selected vehicle
                "other_vehicle": other_vehicle if (selected_vehicle == "Other" and other_vehicle) else "",  # Only if "Other" selected
                "odometer_start": odometer_start,
                "fuel_level": fuel_level,  # "Other" or selected level
                "other_fuel": other_fuel if fuel_level == "Other" else "",  # Manual entry if "Other" selected
                "oil_level": other_oil if (oil_level == "Other" and other_oil) else (oil_level if oil_level else ""),  # Manual entry if "Other" selected, otherwise selected percentage
                "exterior_checks": exterior_checks,
                "engine_checks": engine_checks,
                "safety_checks": safety_checks,
                "interior_checks": interior_checks,
                "fuel_card": fuel_card,
                "measuring_tape": measuring_tape,
                "safety_vest": safety_vest,
                "fuel_amount": fuel_amount,
                "additional_comments": additional_comments if additional_comments else ""
            }
            
            # Save to Excel
            try:
                from datetime import datetime
                save_form_submission(form_data)
                
                # Show thank you screen
                st.session_state.form_submitted = True
                st.session_state.submitted_form_data = form_data
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error saving form: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.exception(e)

def admin_panel():
    """Admin paneli - Form gönderimlerini görüntüleme ve kullanıcı yönetimi"""
    
    # Sidebar menü
    with st.sidebar:
        st.title("👨‍💼 Admin Panel")
        st.markdown("---")
        
        # Menü seçenekleri
        menu_options = {
            "📋 Form Submissions": "form_submissions",
            "👥 User Management": "user_management",
            "🚗 Vehicle Management": "vehicle_management",
            "⛽ Fuel Level Management": "fuel_level_management",
            "✅ Check Fields Management": "check_fields_management",
            "📦 Items Management": "items_management"
        }
        
        # Menu buttons
        for menu_text, section_key in menu_options.items():
            if st.button(
                menu_text,
                key=f"admin_menu_{section_key}",
                width='stretch',
                type="primary" if st.session_state.admin_section == section_key else "secondary"
            ):
                st.session_state.admin_section = section_key
            st.rerun()

        st.markdown("---")
        st.caption(f"👤 {st.session_state.full_name}")
    
    # Main content area
    # Message display (if any)
    if st.session_state.admin_message:
        if st.session_state.admin_message_type == "success":
            st.success(st.session_state.admin_message)
        elif st.session_state.admin_message_type == "error":
            st.error(st.session_state.admin_message)
        elif st.session_state.admin_message_type == "warning":
            st.warning(st.session_state.admin_message)
        elif st.session_state.admin_message_type == "info":
            st.info(st.session_state.admin_message)
        # Clear message
        st.session_state.admin_message = None
        st.session_state.admin_message_type = None
        st.markdown("---")
    
    # Seçili bölüme göre içerik göster
    if st.session_state.admin_section == "form_submissions":
        admin_form_submissions()
    elif st.session_state.admin_section == "user_management":
        admin_user_management()
    elif st.session_state.admin_section == "vehicle_management":
        admin_vehicle_management()
    elif st.session_state.admin_section == "fuel_level_management":
        admin_fuel_level_management()
    elif st.session_state.admin_section == "check_fields_management":
        admin_check_fields_management()
    elif st.session_state.admin_section == "items_management":
        admin_items_management()
    else:
        admin_form_submissions()

def admin_form_submissions():
    """Form gönderimlerini görüntüleme"""
    st.subheader("📋 Form Submissions")
    st.write("View and manage all form submissions.")
    
    try:
        submissions = load_form_submissions()
        
        if not submissions:
            st.info("📭 Henüz form gönderimi bulunmamaktadır.")
            return
        
        st.metric("Total Submissions", len(submissions))
        
        # Filtering options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_driver = st.selectbox(
                "Filter by Driver",
                options=["All"] + list(set([s.get("Driver Name", "N/A") for s in submissions if s.get("Driver Name")]))
            )
        with col2:
            filter_vehicle = st.selectbox(
                "Filter by Vehicle",
                options=["All"] + list(set([s.get("Vehicle", "N/A") for s in submissions if s.get("Vehicle")]))
            )
        with col3:
            sort_by = st.selectbox(
                "Sort By",
                options=["Newest", "Oldest"]
            )
        
        # Filtering
        filtered_submissions = submissions
        if filter_driver != "All":
            filtered_submissions = [s for s in filtered_submissions if s.get("Driver Name") == filter_driver]
        if filter_vehicle != "All":
            filtered_submissions = [s for s in filtered_submissions if s.get("Vehicle") == filter_vehicle]
        
        # Sorting
        if sort_by == "Newest":
            filtered_submissions = sorted(filtered_submissions, key=lambda x: x.get("Timestamp", ""), reverse=True)
        else:
            filtered_submissions = sorted(filtered_submissions, key=lambda x: x.get("Timestamp", ""))
        
        st.write(f"**Showing:** {len(filtered_submissions)} / {len(submissions)}")
        
        # View mode
        view_mode = st.radio(
            "View Mode",
            options=["Table", "Card"],
            horizontal=True
        )
        
        if view_mode == "Table":
            # Table view
            import pandas as pd
            df = pd.DataFrame(filtered_submissions)
            st.dataframe(df, width='stretch', height=400)
            
            # CSV download
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"form_submissions_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            # Card view
            for idx, submission in enumerate(filtered_submissions):
                with st.expander(
                    f"📋 {submission.get('Driver Name', 'N/A')} - {submission.get('Vehicle', 'N/A')} - {submission.get('Timestamp', 'N/A')}",
                    expanded=False
                ):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Basic Information**")
                        st.write(f"**Driver:** {submission.get('Driver Name', 'N/A')}")
                        st.write(f"**Vehicle:** {submission.get('Vehicle', 'N/A')}")
                        st.write(f"**Odometer:** {submission.get('Odometer Start', 'N/A')} KM")
                        st.write(f"**Fuel Level:** {submission.get('Fuel Level', 'N/A')}")
                        st.write(f"**Oil Level:** {submission.get('Oil Level', 'N/A')}")
                    
                    with col2:
                        st.write("**Equipment**")
                        st.write(f"**Fuel Card:** {submission.get('Fuel Card', 'N/A')}")
                        st.write(f"**Measuring Tape:** {submission.get('Measuring Tape', 'N/A')}")
                        st.write(f"**Safety Vest:** {submission.get('Safety Vest', 'N/A')}")
                        st.write(f"**Fuel Amount:** {submission.get('Fuel Amount', 'N/A')}")
                        st.write(f"**Date:** {submission.get('Timestamp', 'N/A')}")
                    
                    # Checks details
                    st.write("**Checks**")
                    
                    # Exterior Checks
                    exterior_cols = [col for col in submission.keys() if col.startswith("Exterior_")]
                    if exterior_cols:
                        st.write("*Exterior Checks:*")
                        for col in exterior_cols:
                            field_name = col.replace("Exterior_", "").replace("_", " ").title()
                            value = submission.get(col, "N/A")
                            status_icon = "✅" if value == "OK" else "⚠️"
                            st.write(f"  {status_icon} {field_name}: {value}")
                    
                    # Engine Checks
                    engine_cols = [col for col in submission.keys() if col.startswith("Engine_")]
                    if engine_cols:
                        st.write("*Engine & Mechanical Checks:*")
                        for col in engine_cols:
                            field_name = col.replace("Engine_", "").replace("_", " ").title()
                            value = submission.get(col, "N/A")
                            status_icon = "✅" if value == "OK" else "⚠️"
                            st.write(f"  {status_icon} {field_name}: {value}")
                    
                    # Safety Equipment
                    safety_cols = [col for col in submission.keys() if col.startswith("Safety_")]
                    if safety_cols:
                        st.write("*Safety Equipment:*")
                        for col in safety_cols:
                            field_name = col.replace("Safety_", "").replace("_", " ").title()
                            value = submission.get(col, "N/A")
                            status_icon = "✅" if value == "OK" else "⚠️"
                            st.write(f"  {status_icon} {field_name}: {value}")
                    
                    # Interior Checks
                    interior_cols = [col for col in submission.keys() if col.startswith("Interior_")]
                    if interior_cols:
                        st.write("*Interior Checks:*")
                        for col in interior_cols:
                            field_name = col.replace("Interior_", "").replace("_", " ").title()
                            value = submission.get(col, "N/A")
                            status_icon = "✅" if value == "OK" else "⚠️"
                            st.write(f"  {status_icon} {field_name}: {value}")
                    
                    st.divider()
    
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        with st.expander("🔍 Error Details"):
            st.exception(e)

def admin_user_management():
    """Kullanıcı yönetimi - Ekleme, düzenleme, silme"""
    st.subheader("👥 User Management")
    st.write("Manage users: add, edit, or delete users.")
    
    try:
        users = load_users()
        
        st.metric("Total Users", len(users) if users else 0)
        
        # Action selection
        action = st.radio(
            "Select Action",
            ["View Users", "Add User", "Edit User", "Delete User"],
            horizontal=True
        )
        
        st.divider()
        
        if action == "View Users":
            if not users:
                st.info("📭 No users found.")
            else:
                import pandas as pd
                user_list = []
                for username, user_data in users.items():
                    user_list.append({
                        "Username": username,
                        "Full Name": user_data.get("full_name", ""),
                        "Email": user_data.get("email", "") or "❌ Not set",
                        "Admin": "✅ Yes" if is_admin(username) else "❌ No"
                    })
                
                df = pd.DataFrame(user_list)
                st.dataframe(df, width='stretch', height=300)
        
        elif action == "Add User":
            st.subheader("➕ Add New User")
            with st.form("add_user_form"):
                new_username = st.text_input("Username *", key="add_username")
                new_password = st.text_input("Password *", type="password", key="add_password")
                new_full_name = st.text_input("Full Name *", key="add_full_name")
                new_email = st.text_input("Email", key="add_email")
                is_admin_user = st.checkbox("Admin User", key="add_is_admin")
                
                submitted = st.form_submit_button("Add User", width='stretch')
                
                if submitted:
                    if not new_username or not new_password or not new_full_name:
                        st.error("❌ Please fill in all required fields (marked with *)")
                    else:
                        if new_username in users:
                            st.error(f"❌ Username '{new_username}' already exists!")
                        else:
                            if add_user(new_username, new_password, new_full_name, new_email, is_admin_user):
                                st.session_state.admin_message = f"✅ User '{new_username}' added successfully!"
                                st.session_state.admin_message_type = "success"
                                st.rerun()
                            else:
                                st.session_state.admin_message = "❌ Failed to add user. Please try again."
                                st.session_state.admin_message_type = "error"
                                st.rerun()
        
        elif action == "Edit User":
            st.subheader("✏️ Edit User")
            if not users:
                st.info("📭 No users to edit.")
            else:
                selected_username = st.selectbox(
                    "Select User to Edit",
                    options=[""] + list(users.keys()),
                    key="edit_user_select"
                )
                
                if selected_username:
                    user_data = users[selected_username]
                    with st.form("edit_user_form"):
                        st.info(f"Editing: **{selected_username}**")
                        
                        new_password = st.text_input(
                            "New Password (leave empty to keep current)",
                            type="password",
                            key="edit_password"
                        )
                        new_full_name = st.text_input(
                            "Full Name",
                            value=user_data.get("full_name", ""),
                            key="edit_full_name"
                        )
                        new_email = st.text_input(
                            "Email",
                            value=user_data.get("email", ""),
                            key="edit_email"
                        )
                        is_admin_user = st.checkbox(
                            "Admin User",
                            value=is_admin(selected_username),
                            key="edit_is_admin"
                        )
                        
                        submitted = st.form_submit_button("Update User", width='stretch')
                        
                        if submitted:
                            password = new_password if new_password else None
                            if update_user(
                                selected_username,
                                password=password,
                                full_name=new_full_name,
                                email=new_email,
                                is_admin=is_admin_user
                            ):
                                st.session_state.admin_message = f"✅ User '{selected_username}' updated successfully!"
                                st.session_state.admin_message_type = "success"
                                st.rerun()
                            else:
                                st.session_state.admin_message = "❌ Failed to update user. Please try again."
                                st.session_state.admin_message_type = "error"
                                st.rerun()
        
        elif action == "Delete User":
            st.subheader("🗑️ Delete User")
            if not users:
                st.info("📭 No users to delete.")
            else:
                selected_username = st.selectbox(
                    "Select User to Delete",
                    options=[""] + list(users.keys()),
                    key="delete_user_select"
                )
                
                if selected_username:
                    user_data = users[selected_username]
                    st.warning(f"⚠️ You are about to delete user: **{selected_username}**")
                    st.write(f"**Full Name:** {user_data.get('full_name', 'N/A')}")
                    st.write(f"**Email:** {user_data.get('email', 'N/A')}")
                    
                    if st.button("🗑️ Confirm Delete", type="primary", width='stretch'):
                        if delete_user(selected_username):
                            st.session_state.admin_message = f"✅ User '{selected_username}' deleted successfully!"
                            st.session_state.admin_message_type = "success"
                            st.rerun()
                        else:
                            st.session_state.admin_message = "❌ Failed to delete user. Please try again."
                            st.session_state.admin_message_type = "error"
                            st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

def admin_vehicle_management():
    """Vehicle management - Add, edit, delete"""
    st.subheader("🚗 Vehicle Management")
    st.write("Manage vehicles: add, edit, or delete vehicles.")
    
    try:
        vehicles = load_vehicles()
        
        st.metric("Total Vehicles", len(vehicles))
        
        action = st.radio(
            "Select Action",
            ["View Vehicles", "Add Vehicle", "Edit Vehicle", "Delete Vehicle"],
            horizontal=True
        )
        
        st.divider()
        
        if action == "View Vehicles":
            if not vehicles:
                st.info("📭 No vehicles found.")
            else:
                import pandas as pd
                df = pd.DataFrame({"Vehicle": vehicles})
                st.dataframe(df, width='stretch', height=300)
        
        elif action == "Add Vehicle":
            st.subheader("➕ Add New Vehicle")
            with st.form("add_vehicle_form"):
                new_vehicle = st.text_input("Vehicle Name *", key="add_vehicle")
                submitted = st.form_submit_button("Add Vehicle", width='stretch')
                
                if submitted:
                    if not new_vehicle:
                        st.error("❌ Please enter a vehicle name")
                    elif new_vehicle in vehicles:
                        st.error(f"❌ Vehicle '{new_vehicle}' already exists!")
                    else:
                        if add_vehicle(new_vehicle):
                            st.session_state.admin_message = f"✅ Vehicle '{new_vehicle}' added successfully!"
                            st.session_state.admin_message_type = "success"
                            st.rerun()
                        else:
                            st.session_state.admin_message = "❌ Failed to add vehicle. Please try again."
                            st.session_state.admin_message_type = "error"
                            st.rerun()
        
        elif action == "Edit Vehicle":
            st.subheader("✏️ Edit Vehicle")
            if not vehicles:
                st.info("📭 No vehicles to edit.")
            else:
                selected_vehicle = st.selectbox(
                    "Select Vehicle to Edit",
                    options=[""] + vehicles,
                    key="edit_vehicle_select"
                )
                
                if selected_vehicle:
                    with st.form("edit_vehicle_form"):
                        new_name = st.text_input(
                            "New Vehicle Name",
                            value=selected_vehicle,
                            key="edit_vehicle_name"
                        )
                        submitted = st.form_submit_button("Update Vehicle", width='stretch')
                        
                        if submitted:
                            if not new_name:
                                st.error("❌ Please enter a vehicle name")
                            elif new_name != selected_vehicle and new_name in vehicles:
                                st.error(f"❌ Vehicle '{new_name}' already exists!")
                            else:
                                if update_vehicle(selected_vehicle, new_name):
                                    st.session_state.admin_message = "✅ Vehicle updated successfully!"
                                    st.session_state.admin_message_type = "success"
                                    st.rerun()
                                else:
                                    st.session_state.admin_message = "❌ Failed to update vehicle. Please try again."
                                    st.session_state.admin_message_type = "error"
                                    st.rerun()
        
        elif action == "Delete Vehicle":
            st.subheader("🗑️ Delete Vehicle")
            if not vehicles:
                st.info("📭 No vehicles to delete.")
            else:
                selected_vehicle = st.selectbox(
                    "Select Vehicle to Delete",
                    options=[""] + vehicles,
                    key="delete_vehicle_select"
                )
                
                if selected_vehicle:
                    st.warning(f"⚠️ You are about to delete vehicle: **{selected_vehicle}**")
                    
                    if st.button("🗑️ Confirm Delete", type="primary", width='stretch'):
                        if delete_vehicle(selected_vehicle):
                            st.session_state.admin_message = f"✅ Vehicle '{selected_vehicle}' deleted successfully!"
                            st.session_state.admin_message_type = "success"
                            st.rerun()
                        else:
                            st.session_state.admin_message = "❌ Failed to delete vehicle. Please try again."
                            st.session_state.admin_message_type = "error"
                            st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

def admin_fuel_level_management():
    """Fuel level management - Add, edit, delete"""
    st.subheader("⛽ Fuel Level Management")
    st.write("Manage fuel levels: add, edit, or delete fuel levels.")
    
    try:
        fuel_levels = load_fuel_levels()
        
        st.metric("Total Fuel Levels", len(fuel_levels))
        
        action = st.radio(
            "Select Action",
            ["View Fuel Levels", "Add Fuel Level", "Edit Fuel Level", "Delete Fuel Level"],
            horizontal=True
        )
        
        st.divider()
        
        if action == "View Fuel Levels":
            if not fuel_levels:
                st.info("📭 No fuel levels found.")
            else:
                import pandas as pd
                df = pd.DataFrame({"Fuel Level": fuel_levels})
                st.dataframe(df, width='stretch', height=300)
        
        elif action == "Add Fuel Level":
            st.subheader("➕ Add New Fuel Level")
            with st.form("add_fuel_level_form"):
                new_level = st.text_input("Fuel Level *", key="add_fuel_level")
                submitted = st.form_submit_button("Add Fuel Level", width='stretch')
                
                if submitted:
                    if not new_level:
                        st.error("❌ Please enter a fuel level")
                    elif new_level in fuel_levels:
                        st.error(f"❌ Fuel level '{new_level}' already exists!")
                    else:
                        if add_fuel_level(new_level):
                            st.session_state.admin_message = f"✅ Fuel level '{new_level}' added successfully!"
                            st.session_state.admin_message_type = "success"
                            st.rerun()
                        else:
                            st.session_state.admin_message = "❌ Failed to add fuel level. Please try again."
                            st.session_state.admin_message_type = "error"
                            st.rerun()
        
        elif action == "Edit Fuel Level":
            st.subheader("✏️ Edit Fuel Level")
            if not fuel_levels:
                st.info("📭 No fuel levels to edit.")
            else:
                selected_level = st.selectbox(
                    "Select Fuel Level to Edit",
                    options=[""] + fuel_levels,
                    key="edit_fuel_level_select"
                )
                
                if selected_level:
                    with st.form("edit_fuel_level_form"):
                        new_level = st.text_input(
                            "New Fuel Level",
                            value=selected_level,
                            key="edit_fuel_level_name"
                        )
                        submitted = st.form_submit_button("Update Fuel Level", width='stretch')
                        
                        if submitted:
                            if not new_level:
                                st.error("❌ Please enter a fuel level")
                            elif new_level != selected_level and new_level in fuel_levels:
                                st.error(f"❌ Fuel level '{new_level}' already exists!")
                            else:
                                if update_fuel_level(selected_level, new_level):
                                    st.session_state.admin_message = "✅ Fuel level updated successfully!"
                                    st.session_state.admin_message_type = "success"
                                    st.rerun()
                                else:
                                    st.session_state.admin_message = "❌ Failed to update fuel level. Please try again."
                                    st.session_state.admin_message_type = "error"
                                    st.rerun()
        
        elif action == "Delete Fuel Level":
            st.subheader("🗑️ Delete Fuel Level")
            if not fuel_levels:
                st.info("📭 No fuel levels to delete.")
            else:
                selected_level = st.selectbox(
                    "Select Fuel Level to Delete",
                    options=[""] + fuel_levels,
                    key="delete_fuel_level_select"
                )
                
                if selected_level:
                    st.warning(f"⚠️ You are about to delete fuel level: **{selected_level}**")
                    
                    if st.button("🗑️ Confirm Delete", type="primary", width='stretch'):
                        if delete_fuel_level(selected_level):
                            st.session_state.admin_message = f"✅ Fuel level '{selected_level}' deleted successfully!"
                            st.session_state.admin_message_type = "success"
                            st.rerun()
                        else:
                            st.session_state.admin_message = "❌ Failed to delete fuel level. Please try again."
                            st.session_state.admin_message_type = "error"
                            st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

def admin_check_fields_management():
    """Check fields management - Add, edit, delete for each category"""
    st.subheader("✅ Check Fields Management")
    st.write("Manage check fields for Exterior, Engine, Safety, and Interior categories.")
    
    try:
        categories = ["Exterior", "Engine", "Safety", "Interior"]
        selected_category = st.selectbox("Select Category", categories, key="check_field_category")
        
        check_fields = load_check_fields(selected_category)
        
        st.metric(f"{selected_category} Check Fields", len(check_fields))
        
        action = st.radio(
            "Select Action",
            ["View Fields", "Add Field", "Edit Field", "Delete Field"],
            horizontal=True
        )
        
        st.divider()
        
        if action == "View Fields":
            if not check_fields:
                st.info(f"📭 No {selected_category.lower()} check fields found.")
            else:
                import pandas as pd
                df = pd.DataFrame({f"{selected_category} Field": check_fields})
                st.dataframe(df, width='stretch', height=300)
        
        elif action == "Add Field":
            st.subheader(f"➕ Add New {selected_category} Field")
            with st.form("add_check_field_form"):
                new_field = st.text_input("Field Name *", key="add_check_field")
                submitted = st.form_submit_button("Add Field", width='stretch')
                
                if submitted:
                    if not new_field:
                        st.error("❌ Please enter a field name")
                    elif new_field in check_fields:
                        st.error(f"❌ Field '{new_field}' already exists!")
                    else:
                        if add_check_field(selected_category, new_field):
                            st.session_state.admin_message = f"✅ Field '{new_field}' added successfully!"
                            st.session_state.admin_message_type = "success"
                            st.rerun()
                        else:
                            st.session_state.admin_message = "❌ Failed to add field. Please try again."
                            st.session_state.admin_message_type = "error"
                            st.rerun()
        
        elif action == "Edit Field":
            st.subheader(f"✏️ Edit {selected_category} Field")
            if not check_fields:
                st.info(f"📭 No {selected_category.lower()} fields to edit.")
            else:
                selected_field = st.selectbox(
                    "Select Field to Edit",
                    options=[""] + check_fields,
                    key="edit_check_field_select"
                )
                
                if selected_field:
                    with st.form("edit_check_field_form"):
                        new_field = st.text_input(
                            "New Field Name",
                            value=selected_field,
                            key="edit_check_field_name"
                        )
                        submitted = st.form_submit_button("Update Field", width='stretch')
                        
                        if submitted:
                            if not new_field:
                                st.error("❌ Please enter a field name")
                            elif new_field != selected_field and new_field in check_fields:
                                st.error(f"❌ Field '{new_field}' already exists!")
                            else:
                                if update_check_field(selected_category, selected_field, new_field):
                                    st.session_state.admin_message = "✅ Field updated successfully!"
                                    st.session_state.admin_message_type = "success"
                                    st.rerun()
                                else:
                                    st.session_state.admin_message = "❌ Failed to update field. Please try again."
                                    st.session_state.admin_message_type = "error"
                                    st.rerun()
        
        elif action == "Delete Field":
            st.subheader(f"🗑️ Delete {selected_category} Field")
            if not check_fields:
                st.info(f"📭 No {selected_category.lower()} fields to delete.")
            else:
                selected_field = st.selectbox(
                    "Select Field to Delete",
                    options=[""] + check_fields,
                    key="delete_check_field_select"
                )
                
                if selected_field:
                    st.warning(f"⚠️ You are about to delete field: **{selected_field}**")
                    
                    if st.button("🗑️ Confirm Delete", type="primary", width='stretch'):
                        if delete_check_field(selected_category, selected_field):
                            st.session_state.admin_message = f"✅ Field '{selected_field}' deleted successfully!"
                            st.session_state.admin_message_type = "success"
                            st.rerun()
                        else:
                            st.session_state.admin_message = "❌ Failed to delete field. Please try again."
                            st.session_state.admin_message_type = "error"
                            st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

def admin_items_management():
    """Items management - Add, edit, delete"""
    st.subheader("📦 Items Management")
    st.write("Manage items: add, edit, or delete items.")
    
    try:
        items = load_items()
        
        st.metric("Total Items", len(items))
        
        action = st.radio(
            "Select Action",
            ["View Items", "Add Item", "Edit Item", "Delete Item"],
            horizontal=True
        )
        
        st.divider()
        
        if action == "View Items":
            if not items:
                st.info("📭 No items found.")
            else:
                import pandas as pd
                df = pd.DataFrame({"Item": items})
                st.dataframe(df, width='stretch', height=300)
        
        elif action == "Add Item":
            st.subheader("➕ Add New Item")
            with st.form("add_item_form"):
                new_item = st.text_input("Item Name *", key="add_item")
                submitted = st.form_submit_button("Add Item", width='stretch')
                
                if submitted:
                    if not new_item:
                        st.error("❌ Please enter an item name")
                    elif new_item in items:
                        st.error(f"❌ Item '{new_item}' already exists!")
                    else:
                        if add_item(new_item):
                            st.session_state.admin_message = f"✅ Item '{new_item}' added successfully!"
                            st.session_state.admin_message_type = "success"
                            st.rerun()
                        else:
                            st.session_state.admin_message = "❌ Failed to add item. Please try again."
                            st.session_state.admin_message_type = "error"
                            st.rerun()
        
        elif action == "Edit Item":
            st.subheader("✏️ Edit Item")
            if not items:
                st.info("📭 No items to edit.")
            else:
                selected_item = st.selectbox(
                    "Select Item to Edit",
                    options=[""] + items,
                    key="edit_item_select"
                )
                
                if selected_item:
                    with st.form("edit_item_form"):
                        new_name = st.text_input(
                            "New Item Name",
                            value=selected_item,
                            key="edit_item_name"
                        )
                        submitted = st.form_submit_button("Update Item", width='stretch')
                        
                        if submitted:
                            if not new_name:
                                st.error("❌ Please enter an item name")
                            elif new_name != selected_item and new_name in items:
                                st.error(f"❌ Item '{new_name}' already exists!")
                            else:
                                if update_item(selected_item, new_name):
                                    st.session_state.admin_message = "✅ Item updated successfully!"
                                    st.session_state.admin_message_type = "success"
                                    st.rerun()
                                else:
                                    st.session_state.admin_message = "❌ Failed to update item. Please try again."
                                    st.session_state.admin_message_type = "error"
                                    st.rerun()
        
        elif action == "Delete Item":
            st.subheader("🗑️ Delete Item")
            if not items:
                st.info("📭 No items to delete.")
            else:
                selected_item = st.selectbox(
                    "Select Item to Delete",
                    options=[""] + items,
                    key="delete_item_select"
                )
                
                if selected_item:
                    st.warning(f"⚠️ You are about to delete item: **{selected_item}**")
                    
                    if st.button("🗑️ Confirm Delete", type="primary", width='stretch'):
                        if delete_item(selected_item):
                            st.session_state.admin_message = f"✅ Item '{selected_item}' deleted successfully!"
                            st.session_state.admin_message_type = "success"
                            st.rerun()
                        else:
                            st.session_state.admin_message = "❌ Failed to delete item. Please try again."
                            st.session_state.admin_message_type = "error"
                            st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

def main():
    """Ana uygulama akışı"""
    # Mobil için üst menü (sidebar yerine)
    if st.session_state.logged_in:
        # Kompakt üst menü
        menu_cols = st.columns([2, 2, 1] if st.session_state.is_admin else [3, 1])
        col_idx = 0
        
        with menu_cols[col_idx]:
            if st.button("📝 Form", width='stretch', 
                        type="primary" if st.session_state.current_page == "form" else "secondary"):
                st.session_state.current_page = "form"
                st.rerun()
        
        if st.session_state.is_admin:
            col_idx += 1
            with menu_cols[col_idx]:
                if st.button("👨‍💼 Admin", width='stretch',
                            type="primary" if st.session_state.current_page == "admin" else "secondary"):
                    st.session_state.current_page = "admin"
                    st.rerun()
        
        col_idx += 1
        with menu_cols[col_idx]:
            if st.button("🚪", width='stretch', help="Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.full_name = None
                st.session_state.is_admin = False
                st.session_state.current_page = "form"
                st.rerun()
        
        st.markdown("---")
    
    # Sayfa yönlendirme
    if not st.session_state.logged_in:
        if st.session_state.current_page == "reset_password":
            reset_password_page()
        else:
            st.session_state.current_page = "login"
        login_page()
    else:
        if st.session_state.current_page == "admin" and st.session_state.is_admin:
            admin_panel()
        else:
            form_page()

if __name__ == "__main__":
    main()

