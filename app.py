"""
Streamlit Araç Kontrol Formu Uygulaması
FastAPI uygulamasının Streamlit versiyonu
"""
import streamlit as st
from excel_handler import (
    load_vehicles, load_fuel_levels, load_check_fields,
    load_items, load_users, save_form_submission,
    load_form_submissions, is_admin, update_excel_with_admin_column
)

# Uygulama başlangıcında Excel dosyasını güncelle (sadece Excel kullanılıyorsa)
# Google Sheets kullanılıyorsa bu fonksiyon hiçbir şey yapmaz
try:
    update_excel_with_admin_column()
except Exception as e:
    # Bulut ortamında Excel dosyası olmayabilir, bu normal
    pass

# Sayfa yapılandırması
st.set_page_config(
    page_title="Araç Kontrol Formu",
    page_icon="🚗",
    layout="wide"
)

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

def login_page():
    """Login sayfası"""
    # Logging bulut ortamında devre dışı
    def _log(hypothesis_id, location, message, data):
        pass
    
    st.title("🔐 Giriş Yap")
    
    # Excel'den kullanıcıları yükle
    # #region agent log
    _log("C", "app.py:login_page:before_load_users", "About to load users", {})
    # #endregion agent log
    users = load_users()
    # #region agent log
    _log("C", "app.py:login_page:after_load_users", "Users loaded", {"user_count": len(users), "usernames": list(users.keys())})
    # #endregion agent log
    
    with st.form("login_form"):
        username = st.text_input("Kullanıcı Adı", key="login_username")
        password = st.text_input("Şifre", type="password", key="login_password")
        submit_button = st.form_submit_button("Giriş Yap")
        
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
                st.success("Giriş başarılı!")
                st.rerun()
            else:
                # #region agent log
                _log("C", "app.py:login_page:login_failed", "Login failed", {"username": username, "user_found": user is not None, "password_match": user["password"] == password if user else False})
                # #endregion agent log
                st.error("Kullanıcı adı veya şifre hatalı!")

def form_page():
    """Araç kontrol formu sayfası"""
    st.title("🚗 Araç Kontrol Formu")
    st.write(f"Hoş geldiniz, **{st.session_state.full_name}**")
    
    # Excel'den verileri yükle
    vehicles = load_vehicles()
    fuel_levels = load_fuel_levels()
    items = load_items()
    
    # Kontrol kategorileri
    exterior_fields = load_check_fields("ExteriorChecks")
    engine_fields = load_check_fields("EngineChecks")
    safety_fields = load_check_fields("SafetyEquipment")
    interior_fields = load_check_fields("InteriorChecks")
    
    # Form oluştur
    with st.form("vehicle_inspection_form"):
        st.subheader("Temel Bilgiler")
        
        # Driver Name (readonly)
        driver_name = st.text_input(
            "Driver Name",
            value=st.session_state.full_name,
            disabled=True
        )
        
        # Vehicle seçimi
        vehicle_options = [""] + vehicles + ["Other"]
        selected_vehicle = st.selectbox(
            "Vehicle",
            options=vehicle_options,
            key="vehicle_select"
        )
        
        # Other Vehicle (koşullu)
        other_vehicle = None
        if selected_vehicle == "Other":
            other_vehicle = st.text_input(
                "Manuel Araç Girişi",
                placeholder="Aracı manuel girin",
                key="other_vehicle_input"
            )
        
        # Odometer Reading
        odometer_start = st.number_input(
            "Odometer Reading (Başlangıç KM)",
            min_value=0,
            step=1,
            key="odometer_input"
        )
        
        # Fuel Level
        fuel_options = [""] + fuel_levels
        fuel_level = st.selectbox(
            "Fuel Level",
            options=fuel_options,
            key="fuel_level_select"
        )
        
        # Other Fuel (koşullu)
        other_fuel = None
        if fuel_level == "Other":
            other_fuel = st.text_input(
                "Manuel Yakıt Seviyesi",
                placeholder="Yakıt seviyesini manuel girin",
                key="other_fuel_input"
            )
        
        # Oil Level
        oil_level = st.text_input(
            "Oil Level",
            placeholder="Oil Level",
            key="oil_level_input"
        )
        
        st.divider()
        
        # Exterior Checks
        st.subheader("Exterior Checks")
        with st.expander("Exterior Checks Detayları", expanded=False):
            # Exterior Checks için emoji mapping
            exterior_icons = {
                "headlights": "💡",
                "break_lights": "🛑",
                "indicators": "➡️",
                "mirrors": "🪞",
                "windows": "🪟",
                "windshield": "🚗",
                "wiper_fluid": "💧",
                "wipers": "🧹",
                "tires": "⚙️",
                "body_paint": "🎨"
            }
            
            exterior_checks = {}
            for field in exterior_fields:
                field_display = field.replace("_", " / ").title()
                icon = exterior_icons.get(field, "✅")
                exterior_checks[field] = st.radio(
                    f"{icon} {field_display}",
                    options=["OK", "Needs Attention"],
                    horizontal=True,
                    key=f"exterior_{field}"
                )
        
        # Engine & Mechanical Checks
        st.subheader("Engine & Mechanical Checks")
        with st.expander("Engine & Mechanical Checks Detayları", expanded=False):
            engine_checks = {}
            for field in engine_fields:
                field_display = field.replace("_", " / ").title()
                engine_checks[field] = st.radio(
                    field_display,
                    options=["OK", "Needs Attention"],
                    horizontal=True,
                    key=f"engine_{field}"
                )
        
        # Safety Equipment
        st.subheader("Safety Equipment")
        with st.expander("Safety Equipment Detayları", expanded=False):
            safety_checks = {}
            for field in safety_fields:
                field_display = field.replace("_", " / ").title()
                safety_checks[field] = st.radio(
                    field_display,
                    options=["OK", "Needs Attention"],
                    horizontal=True,
                    key=f"safety_{field}"
                )
        
        # Interior Checks
        st.subheader("Interior Checks")
        with st.expander("Interior Checks Detayları", expanded=False):
            interior_checks = {}
            for field in interior_fields:
                field_display = field.replace("_", " / ").title()
                interior_checks[field] = st.radio(
                    field_display,
                    options=["OK", "Needs Attention"],
                    horizontal=True,
                    key=f"interior_{field}"
                )
        
        st.divider()
        
        # Items in Vehicle
        st.subheader("Items in Vehicle")
        
        # Fuel Card
        fuel_card = st.radio(
            "Fuel Card",
            options=["Yes", "No"],
            horizontal=True,
            key="fuel_card_radio"
        )
        
        # Measuring Tape
        measuring_tape = st.radio(
            "Measuring Tape",
            options=["Yes", "No"],
            horizontal=True,
            key="measuring_tape_radio"
        )
        
        # Safety Vest
        safety_vest = st.radio(
            "Safety Vest",
            options=["Yes", "No"],
            horizontal=True,
            key="safety_vest_radio"
        )
        
        # Fuel Amount
        fuel_amount = st.text_input(
            "Fuel Amount ($)",
            placeholder="Fuel Amount",
            key="fuel_amount_input"
        )
        
        st.divider()
        
        # Submit button
        submit_button = st.form_submit_button("📝 Formu Kaydet", use_container_width=True)
        
        if submit_button:
            # Form verilerini topla
            form_data = {
                "driver_name": driver_name,
                "vehicle": selected_vehicle,  # "Other" veya seçilen araç
                "other_vehicle": other_vehicle if selected_vehicle == "Other" else "",  # "Other" seçildiyse manuel giriş
                "odometer_start": odometer_start,
                "fuel_level": fuel_level,  # "Other" veya seçilen seviye
                "other_fuel": other_fuel if fuel_level == "Other" else "",  # "Other" seçildiyse manuel giriş
                "oil_level": oil_level,
                "exterior_checks": exterior_checks,
                "engine_checks": engine_checks,
                "safety_checks": safety_checks,
                "interior_checks": interior_checks,
                "fuel_card": fuel_card,
                "measuring_tape": measuring_tape,
                "safety_vest": safety_vest,
                "fuel_amount": fuel_amount
            }
            
            # Excel'e kaydet
            try:
                from datetime import datetime
                save_form_submission(form_data)
                
                # Başarı mesajı
                st.success("✅ Form başarıyla kaydedildi!")
                st.balloons()
                
                # Detaylı geri bildirim
                with st.container():
                    st.info("📋 **Kaydedilen Bilgiler:**")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Sürücü:** {form_data.get('driver_name', 'N/A')}")
                        st.write(f"**Araç:** {form_data.get('vehicle', 'N/A')}")
                        st.write(f"**KM:** {form_data.get('odometer_start', 'N/A')}")
                        st.write(f"**Yakıt Seviyesi:** {form_data.get('fuel_level', 'N/A')}")
                    
                    with col2:
                        st.write(f"**Yağ Seviyesi:** {form_data.get('oil_level', 'N/A')}")
                        st.write(f"**Yakıt Kartı:** {form_data.get('fuel_card', 'N/A')}")
                        st.write(f"**Ölçü Bandı:** {form_data.get('measuring_tape', 'N/A')}")
                        st.write(f"**Güvenlik Yeleği:** {form_data.get('safety_vest', 'N/A')}")
                    
                    st.write(f"**Kayıt Zamanı:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write(f"**Kayıt Yeri:** `form_submissions.xlsx`")
                
            except Exception as e:
                st.error(f"❌ Form kaydedilirken hata oluştu: {str(e)}")
                with st.expander("🔍 Hata Detayları"):
                    st.exception(e)
            
            # Formu temizle (rerun)
            st.rerun()

def admin_panel():
    """Admin paneli - Form gönderimlerini görüntüleme"""
    st.title("👨‍💼 Admin Paneli")
    st.write("Form gönderimlerini görüntüleyebilir ve yönetebilirsiniz.")
    
    try:
        submissions = load_form_submissions()
        
        if not submissions:
            st.info("📭 Henüz form gönderimi bulunmamaktadır.")
            return
        
        st.metric("Toplam Gönderim", len(submissions))
        
        # Filtreleme seçenekleri
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_driver = st.selectbox(
                "Sürücüye Göre Filtrele",
                options=["Tümü"] + list(set([s.get("Driver Name", "N/A") for s in submissions if s.get("Driver Name")]))
            )
        with col2:
            filter_vehicle = st.selectbox(
                "Araca Göre Filtrele",
                options=["Tümü"] + list(set([s.get("Vehicle", "N/A") for s in submissions if s.get("Vehicle")]))
            )
        with col3:
            sort_by = st.selectbox(
                "Sıralama",
                options=["En Yeni", "En Eski"]
            )
        
        # Filtreleme
        filtered_submissions = submissions
        if filter_driver != "Tümü":
            filtered_submissions = [s for s in filtered_submissions if s.get("Driver Name") == filter_driver]
        if filter_vehicle != "Tümü":
            filtered_submissions = [s for s in filtered_submissions if s.get("Vehicle") == filter_vehicle]
        
        # Sıralama
        if sort_by == "En Yeni":
            filtered_submissions = sorted(filtered_submissions, key=lambda x: x.get("Timestamp", ""), reverse=True)
        else:
            filtered_submissions = sorted(filtered_submissions, key=lambda x: x.get("Timestamp", ""))
        
        st.write(f"**Gösterilen:** {len(filtered_submissions)} / {len(submissions)}")
        
        # Detaylı görünüm
        view_mode = st.radio(
            "Görünüm Modu",
            options=["Tablo", "Kart"],
            horizontal=True
        )
        
        if view_mode == "Tablo":
            # Tablo görünümü
            import pandas as pd
            df = pd.DataFrame(filtered_submissions)
            st.dataframe(df, use_container_width=True, height=400)
            
            # CSV indirme
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 CSV Olarak İndir",
                data=csv,
                file_name=f"form_submissions_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            # Kart görünümü
            for idx, submission in enumerate(filtered_submissions):
                with st.expander(
                    f"📋 {submission.get('Driver Name', 'N/A')} - {submission.get('Vehicle', 'N/A')} - {submission.get('Timestamp', 'N/A')}",
                    expanded=False
                ):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Temel Bilgiler**")
                        st.write(f"**Sürücü:** {submission.get('Driver Name', 'N/A')}")
                        st.write(f"**Araç:** {submission.get('Vehicle', 'N/A')}")
                        st.write(f"**KM:** {submission.get('Odometer Start', 'N/A')}")
                        st.write(f"**Yakıt Seviyesi:** {submission.get('Fuel Level', 'N/A')}")
                        st.write(f"**Yağ Seviyesi:** {submission.get('Oil Level', 'N/A')}")
                    
                    with col2:
                        st.write("**Ekipmanlar**")
                        st.write(f"**Yakıt Kartı:** {submission.get('Fuel Card', 'N/A')}")
                        st.write(f"**Ölçü Bandı:** {submission.get('Measuring Tape', 'N/A')}")
                        st.write(f"**Güvenlik Yeleği:** {submission.get('Safety Vest', 'N/A')}")
                        st.write(f"**Yakıt Miktarı:** {submission.get('Fuel Amount', 'N/A')}")
                        st.write(f"**Tarih:** {submission.get('Timestamp', 'N/A')}")
                    
                    # Kontroller detayları
                    st.write("**Kontroller**")
                    
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
        st.error(f"❌ Veriler yüklenirken hata oluştu: {str(e)}")
        with st.expander("🔍 Hata Detayları"):
            st.exception(e)

def main():
    """Ana uygulama akışı"""
    # Sidebar menü
    if st.session_state.logged_in:
        with st.sidebar:
            st.write(f"Kullanıcı: **{st.session_state.full_name}**")
            if st.session_state.is_admin:
                st.write("👨‍💼 **Admin**")
            
            st.divider()
            
            # Sayfa seçimi
            if st.button("📝 Form", use_container_width=True, 
                        type="primary" if st.session_state.current_page == "form" else "secondary"):
                st.session_state.current_page = "form"
                st.rerun()
            
            if st.session_state.is_admin:
                if st.button("👨‍💼 Admin Paneli", use_container_width=True,
                            type="primary" if st.session_state.current_page == "admin" else "secondary"):
                    st.session_state.current_page = "admin"
                    st.rerun()
            
            st.divider()
            
            if st.button("🚪 Çıkış Yap", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.full_name = None
                st.session_state.is_admin = False
                st.session_state.current_page = "form"
                st.rerun()
    
    # Sayfa yönlendirme
    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.current_page == "admin" and st.session_state.is_admin:
            admin_panel()
        else:
            form_page()

if __name__ == "__main__":
    main()

