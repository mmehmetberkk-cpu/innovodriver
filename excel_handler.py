"""
Excel dosyası işlemleri için yardımcı modül
Form verilerini Excel'den okur ve günceller
Google Sheets desteği eklendi
Bulut ortamı için optimize edildi
"""
import os
import json
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter

# Streamlit secrets desteği (bulut ortamı için)
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

def get_secret(key, default=""):
    """Streamlit secrets veya environment variable'dan değer okur"""
    if HAS_STREAMLIT:
        try:
            # Streamlit secrets'tan oku
            secrets = st.secrets
            if hasattr(secrets, key):
                return getattr(secrets, key)
            # Nested secrets için (örn: secrets.google_sheets.sheet_id)
            if "." in key:
                parts = key.split(".")
                value = secrets
                for part in parts:
                    if hasattr(value, part):
                        value = getattr(value, part)
                    else:
                        return default
                return value
        except Exception:
            pass
    # Fallback: environment variable
    return os.environ.get(key, default)

# Google Sheets desteği (opsiyonel)
# Streamlit secrets'tan oku (nested veya flat format)
if HAS_STREAMLIT:
    try:
        secrets = st.secrets
        # Nested format kontrolü
        if hasattr(secrets, "google_sheets"):
            gs_config = secrets.google_sheets
            USE_GOOGLE_SHEETS = str(gs_config.get("enabled", "false")).lower() == "true"
            GOOGLE_SHEET_ID = str(gs_config.get("sheet_id", ""))
            GOOGLE_CREDENTIALS_JSON = str(gs_config.get("credentials_json", ""))
        else:
            # Flat format
            USE_GOOGLE_SHEETS = get_secret("USE_GOOGLE_SHEETS", "false").lower() == "true"
            GOOGLE_SHEET_ID = get_secret("GOOGLE_SHEET_ID", "")
            GOOGLE_CREDENTIALS_JSON = get_secret("GOOGLE_CREDENTIALS_JSON", "")
    except Exception:
        # Fallback to environment variables
        USE_GOOGLE_SHEETS = get_secret("USE_GOOGLE_SHEETS", "false").lower() == "true"
        GOOGLE_SHEET_ID = get_secret("GOOGLE_SHEET_ID", "")
        GOOGLE_CREDENTIALS_JSON = get_secret("GOOGLE_CREDENTIALS_JSON", "")
else:
    # Environment variables only
    USE_GOOGLE_SHEETS = get_secret("USE_GOOGLE_SHEETS", "false").lower() == "true"
    GOOGLE_SHEET_ID = get_secret("GOOGLE_SHEET_ID", "")
    GOOGLE_CREDENTIALS_JSON = get_secret("GOOGLE_CREDENTIALS_JSON", "")

# Google Apps Script URL (eski yöntem)
GOOGLE_APPS_SCRIPT_URL = get_secret("GOOGLE_APPS_SCRIPT_URL", "https://script.google.com/macros/s/AKfycbwtLKzCB366hwi1S4cHAUGIWP9dDA6isSDLbKvyOIw9P9WNgbLF6t6dlY7RYWlvQM96/exec")
USE_GOOGLE_APPS_SCRIPT = get_secret("USE_GOOGLE_APPS_SCRIPT", "true").lower() == "true"

if USE_GOOGLE_SHEETS:
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        USE_GOOGLE_SHEETS = False

def get_google_sheets_client():
    """Google Sheets client'ı oluşturur ve döndürür"""
    if not USE_GOOGLE_SHEETS:
        return None
    
    try:
        if not GOOGLE_CREDENTIALS_JSON or not GOOGLE_SHEET_ID:
            return None
        
        # JSON string'ini parse et
        import json as json_module
        if isinstance(GOOGLE_CREDENTIALS_JSON, str):
            creds_dict = json_module.loads(GOOGLE_CREDENTIALS_JSON)
        else:
            creds_dict = GOOGLE_CREDENTIALS_JSON
        
        # Credentials oluştur
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        )
        
        # Client oluştur
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        _log("ERROR", "excel_handler.py:get_google_sheets_client", "Failed to create Google Sheets client", {"error": str(e)})
        return None

# Logging - bulut ortamında devre dışı (opsiyonel olarak Streamlit logging kullanılabilir)
def _log(hypothesis_id, location, message, data):
    # Bulut ortamında logging devre dışı
    # Gerekirse Streamlit'in kendi logging sistemini kullanabilirsiniz
    pass

# Excel dosyası yolu - bulut ortamında geçici dizin kullan
# Google Sheets kullanılıyorsa Excel dosyası kullanılmayacak
import tempfile
TEMP_DIR = tempfile.gettempdir()
EXCEL_FILE = os.path.join(TEMP_DIR, "form_data.xlsx")

def create_default_excel():
    """Default değerlerle Excel dosyası oluşturur"""
    wb = Workbook()
    
    # Varsayılan sheet'i sil
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])
    
    # Vehicles sheet
    ws_vehicles = wb.create_sheet("Vehicles")
    ws_vehicles.append(["Vehicle"])
    ws_vehicles.append(["SPRINTER: BT-48331"])
    ws_vehicles.append(["RAM-Promaster 2500 (2021)"])
    ws_vehicles.append(["MERCEDES-2500 Cargo Van (2013)"])
    
    # FuelLevels sheet
    ws_fuel = wb.create_sheet("FuelLevels")
    ws_fuel.append(["Level"])
    ws_fuel.append(["Full"])
    ws_fuel.append(["3/4"])
    ws_fuel.append(["Half"])
    ws_fuel.append(["1/4"])
    ws_fuel.append(["Other"])
    
    # ExteriorChecks sheet
    ws_exterior = wb.create_sheet("ExteriorChecks")
    ws_exterior.append(["Field"])
    exterior_fields = ["headlights", "break_lights", "indicators", "mirrors", "windows", 
                      "windshield", "wiper_fluid", "wipers", "tires", "body_paint"]
    for field in exterior_fields:
        ws_exterior.append([field])
    
    # EngineChecks sheet
    ws_engine = wb.create_sheet("EngineChecks")
    ws_engine.append(["Field"])
    engine_fields = ["engine_noise", "coolant_level", "brake_fluid", "battery_condition", "belts_hoses"]
    for field in engine_fields:
        ws_engine.append([field])
    
    # SafetyEquipment sheet
    ws_safety = wb.create_sheet("SafetyEquipment")
    ws_safety.append(["Field"])
    safety_fields = ["seatbelts", "fire_extinguisher", "first_aid_kit", "horn", "jumper_cables", "snow_brush"]
    for field in safety_fields:
        ws_safety.append([field])
    
    # InteriorChecks sheet
    ws_interior = wb.create_sheet("InteriorChecks")
    ws_interior.append(["Field"])
    interior_fields = ["cleanliness", "dashboard_lights", "hvac", "seats"]
    for field in interior_fields:
        ws_interior.append([field])
    
    # Items sheet
    ws_items = wb.create_sheet("Items")
    ws_items.append(["Item"])
    ws_items.append(["Fuel Card"])
    ws_items.append(["Measuring Tape"])
    ws_items.append(["Safety Vest"])
    
    # Users sheet
    ws_users = wb.create_sheet("Users")
    ws_users.append(["Username", "Password", "Full Name", "Admin"])
    ws_users.append(["innovodriver", "123456", "Mehmet Berk", "No"])
    ws_users.append(["admin", "admin123", "Admin User", "Yes"])
    
    wb.save(EXCEL_FILE)
    return wb

def get_excel_file():
    """Excel dosyasını açar, yoksa oluşturur"""
    # Google Sheets kullanılıyorsa Excel dosyasına gerek yok
    if USE_GOOGLE_SHEETS:
        # Yine de fallback için varsayılan Excel oluştur
        if not os.path.exists(EXCEL_FILE):
            return create_default_excel()
    
    if not os.path.exists(EXCEL_FILE):
        return create_default_excel()
    
    try:
        return load_workbook(EXCEL_FILE)
    except Exception as e:
        # Dosya bozuksa yeniden oluştur
        _log("E", "excel_handler.py:get_excel_file", "Excel file corrupted, recreating", {"error": str(e)})
        try:
            os.remove(EXCEL_FILE)
        except:
            pass
        return create_default_excel()

def load_vehicles():
    """Vehicles sheet'inden araç listesini okur"""
    # Google Sheets'ten oku
    if USE_GOOGLE_SHEETS:
        client = get_google_sheets_client()
        if client:
            try:
                sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet("Vehicles")
                all_values = sheet.get_all_values()
                vehicles = []
                for row in all_values[1:]:  # İlk satır başlık
                    if row and row[0]:
                        vehicles.append(row[0])
                return vehicles
            except Exception as e:
                _log("E", "excel_handler.py:load_vehicles:google_sheets", "Google Sheets load failed, falling back to Excel", {"error": str(e)})
    
    # Excel'den oku (fallback)
    wb = get_excel_file()
    ws = wb["Vehicles"]
    vehicles = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0]:
            vehicles.append(row[0])
    return vehicles

def load_fuel_levels():
    """FuelLevels sheet'inden yakıt seviyelerini okur"""
    # Google Sheets'ten oku
    if USE_GOOGLE_SHEETS:
        client = get_google_sheets_client()
        if client:
            try:
                sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet("FuelLevels")
                all_values = sheet.get_all_values()
                levels = []
                for row in all_values[1:]:  # İlk satır başlık
                    if row and row[0]:
                        levels.append(row[0])
                return levels
            except Exception as e:
                _log("E", "excel_handler.py:load_fuel_levels:google_sheets", "Google Sheets load failed, falling back to Excel", {"error": str(e)})
    
    # Excel'den oku (fallback)
    wb = get_excel_file()
    ws = wb["FuelLevels"]
    levels = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0]:
            levels.append(row[0])
    return levels

def load_check_fields(category):
    """İlgili sheet'ten kontrolleri okur
    category: 'ExteriorChecks', 'EngineChecks', 'SafetyEquipment', 'InteriorChecks'
    """
    # Google Sheets'ten oku
    if USE_GOOGLE_SHEETS:
        client = get_google_sheets_client()
        if client:
            try:
                sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet(category)
                all_values = sheet.get_all_values()
                fields = []
                for row in all_values[1:]:  # İlk satır başlık
                    if row and row[0]:
                        fields.append(row[0])
                return fields
            except Exception as e:
                _log("E", f"excel_handler.py:load_check_fields:google_sheets:{category}", "Google Sheets load failed, falling back to Excel", {"error": str(e)})
    
    # Excel'den oku (fallback)
    wb = get_excel_file()
    if category not in wb.sheetnames:
        return []
    ws = wb[category]
    fields = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0]:
            fields.append(row[0])
    return fields

def load_items():
    """Items sheet'inden eşya listesini okur"""
    # Google Sheets'ten oku
    if USE_GOOGLE_SHEETS:
        client = get_google_sheets_client()
        if client:
            try:
                sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet("Items")
                all_values = sheet.get_all_values()
                items = []
                for row in all_values[1:]:  # İlk satır başlık
                    if row and row[0]:
                        items.append(row[0])
                return items
            except Exception as e:
                _log("E", "excel_handler.py:load_items:google_sheets", "Google Sheets load failed, falling back to Excel", {"error": str(e)})
    
    # Excel'den oku (fallback)
    wb = get_excel_file()
    ws = wb["Items"]
    items = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0]:
            items.append(row[0])
    return items

def load_users():
    """Users sheet'inden kullanıcıları okur"""
    _log("A", "excel_handler.py:load_users:entry", "load_users called", {})
    
    # Google Sheets'ten oku
    if USE_GOOGLE_SHEETS:
        client = get_google_sheets_client()
        if client:
            try:
                sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet("Users")
                all_values = sheet.get_all_values()
                
                if not all_values or len(all_values) < 2:
                    return {}
                
                headers = all_values[0]
                _log("A", "excel_handler.py:load_users:headers", "Users sheet headers", {"headers": headers})
                
                users = {}
                for row in all_values[1:]:  # İlk satır başlık
                    if row and len(row) >= 3 and row[0] and row[1] and row[2]:
                        users[row[0]] = {
                            "password": row[1],
                            "full_name": row[2]
                        }
                        _log("A", "excel_handler.py:load_users:user_added", "User added to dict", {"username": row[0]})
                
                _log("A", "excel_handler.py:load_users:exit", "load_users returning", {"user_count": len(users), "usernames": list(users.keys())})
                return users
            except Exception as e:
                _log("E", "excel_handler.py:load_users:google_sheets", "Google Sheets load failed, falling back to Excel", {"error": str(e)})
    
    # Excel'den oku (fallback)
    wb = get_excel_file()
    ws = wb["Users"]
    
    headers = [cell.value for cell in ws[1]]
    _log("A", "excel_handler.py:load_users:headers", "Users sheet headers", {"headers": headers})
    
    users = {}
    row_num = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        row_num += 1
        _log("A", "excel_handler.py:load_users:row", f"Processing row {row_num}", {"row": list(row), "row_length": len(row) if row else 0})
        if row[0] and row[1] and row[2]:
            users[row[0]] = {
                "password": row[1],
                "full_name": row[2]
            }
            _log("A", "excel_handler.py:load_users:user_added", "User added to dict", {"username": row[0]})
    
    _log("A", "excel_handler.py:load_users:exit", "load_users returning", {"user_count": len(users), "usernames": list(users.keys())})
    return users

def add_vehicle(vehicle_name):
    """Yeni araç ekler"""
    wb = get_excel_file()
    ws = wb["Vehicles"]
    ws.append([vehicle_name])
    wb.save(EXCEL_FILE)

def add_fuel_level(level):
    """Yeni yakıt seviyesi ekler"""
    wb = get_excel_file()
    ws = wb["FuelLevels"]
    ws.append([level])
    wb.save(EXCEL_FILE)

def add_check_field(category, field_name):
    """Yeni kontrol alanı ekler"""
    wb = get_excel_file()
    if category not in wb.sheetnames:
        wb.create_sheet(category)
        ws = wb[category]
        ws.append(["Field"])
    else:
        ws = wb[category]
    ws.append([field_name])
    wb.save(EXCEL_FILE)

def add_item(item_name):
    """Yeni eşya ekler"""
    wb = get_excel_file()
    ws = wb["Items"]
    ws.append([item_name])
    wb.save(EXCEL_FILE)

def add_user(username, password, full_name, is_admin_user=False):
    """Yeni kullanıcı ekler"""
    wb = get_excel_file()
    ws = wb["Users"]
    
    # Başlık satırını kontrol et ve Admin kolonu ekle
    headers = [cell.value for cell in ws[1]]
    if "Admin" not in headers:
        # Admin kolonunu başlığa ekle
        ws.cell(row=1, column=len(headers) + 1, value="Admin")
        headers.append("Admin")
    
    # Yeni satır ekle
    new_row = [username, password, full_name, "Yes" if is_admin_user else "No"]
    ws.append(new_row)
    wb.save(EXCEL_FILE)

def update_excel_with_admin_column():
    """Mevcut Excel dosyasına Admin kolonu ekler ve admin kullanıcısını ekler
    Google Sheets kullanılıyorsa bu fonksiyon hiçbir şey yapmaz (Google Sheets'te manuel yapılmalı)
    """
    # Google Sheets kullanılıyorsa Excel işlemlerini atla
    if USE_GOOGLE_SHEETS:
        _log("D", "excel_handler.py:update_excel_with_admin_column", "Google Sheets enabled, skipping Excel update", {})
        return
    
    try:
        wb = get_excel_file()
        ws = wb["Users"]
        
        # Başlık satırını kontrol et
        headers = [cell.value for cell in ws[1]]
        
        # Admin kolonu yoksa ekle
        if "Admin" not in headers:
            _log("D", "excel_handler.py:update_excel_with_admin_column", "Adding Admin column to headers", {"current_headers": headers})
            ws.cell(row=1, column=len(headers) + 1, value="Admin")
            headers.append("Admin")
            
            # Mevcut kullanıcılara "No" ekle
            for row_idx in range(2, ws.max_row + 1):
                ws.cell(row=row_idx, column=len(headers), value="No")
        
        # Admin kullanıcısı var mı kontrol et
        admin_exists = False
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row and row[0] == "admin":
                admin_exists = True
                break
        
        # Admin kullanıcısı yoksa ekle
        if not admin_exists:
            _log("D", "excel_handler.py:update_excel_with_admin_column", "Adding admin user", {})
            ws.append(["admin", "admin123", "Admin User", "Yes"])
        
        wb.save(EXCEL_FILE)
        _log("D", "excel_handler.py:update_excel_with_admin_column", "Excel updated successfully", {})
    except Exception as e:
        # Excel dosyası bozuksa veya oluşturulamazsa hata verme, sadece log
        _log("E", "excel_handler.py:update_excel_with_admin_column", "Failed to update Excel file", {"error": str(e)})
        # Bulut ortamında Excel dosyası olmayabilir, bu normal
        pass

# Form gönderimleri için ayrı Excel dosyası - bulut ortamında geçici dizin
SUBMISSIONS_FILE = os.path.join(TEMP_DIR, "form_submissions.xlsx")

def _prepare_submission_row(form_data):
    """Form verilerini Excel/Sheets satırına dönüştürür"""
    from datetime import datetime
    
    # Başlık satırı oluştur
    headers = [
        "Timestamp", "Driver Name", "Vehicle", "Odometer Start", 
        "Fuel Level", "Oil Level", "Fuel Card", "Measuring Tape", 
        "Safety Vest", "Fuel Amount"
    ]
    
    # Exterior checks başlıkları
    exterior_fields = load_check_fields("ExteriorChecks")
    for field in exterior_fields:
        headers.append(f"Exterior_{field}")
    
    # Engine checks başlıkları
    engine_fields = load_check_fields("EngineChecks")
    for field in engine_fields:
        headers.append(f"Engine_{field}")
    
    # Safety equipment başlıkları
    safety_fields = load_check_fields("SafetyEquipment")
    for field in safety_fields:
        headers.append(f"Safety_{field}")
    
    # Interior checks başlıkları
    interior_fields = load_check_fields("InteriorChecks")
    for field in interior_fields:
        headers.append(f"Interior_{field}")
    
    # Veri satırı oluştur
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        form_data.get("driver_name", ""),
        form_data.get("vehicle", ""),
        form_data.get("odometer_start", ""),
        form_data.get("fuel_level", ""),
        form_data.get("oil_level", ""),
        form_data.get("fuel_card", ""),
        form_data.get("measuring_tape", ""),
        form_data.get("safety_vest", ""),
        form_data.get("fuel_amount", "")
    ]
    
    # Exterior checks değerleri
    exterior_checks = form_data.get("exterior_checks", {})
    for field in exterior_fields:
        row.append(exterior_checks.get(field, ""))
    
    # Engine checks değerleri
    engine_checks = form_data.get("engine_checks", {})
    for field in engine_fields:
        row.append(engine_checks.get(field, ""))
    
    # Safety equipment değerleri
    safety_checks = form_data.get("safety_checks", {})
    for field in safety_fields:
        row.append(safety_checks.get(field, ""))
    
    # Interior checks değerleri
    interior_checks = form_data.get("interior_checks", {})
    for field in interior_fields:
        row.append(interior_checks.get(field, ""))
    
    return headers, row

def save_form_submission_to_google_apps_script(form_data):
    """Form verilerini Google Apps Script'e HTTP POST ile gönderir (eski yöntem - Google Sheets formatına uygun)"""
    import urllib.request
    import urllib.parse
    import json
    
    try:
        # Form verilerini Google Sheets formatına uygun şekilde düzleştir
        # Eski HTML formundaki field isimlerini kullan
        flat_data = {}
        
        # Temel alanlar (eski formdaki isimlerle aynı)
        flat_data["driver_name"] = form_data.get("driver_name", "")
        
        # Vehicle - "Other" seçildiyse other_vehicle kullan
        vehicle = form_data.get("vehicle", "")
        if vehicle == "Other":
            flat_data["vehicle"] = "Other"
            flat_data["other_vehicle"] = form_data.get("other_vehicle", "")
        else:
            flat_data["vehicle"] = vehicle
            flat_data["other_vehicle"] = ""
        
        flat_data["odometer_start"] = str(form_data.get("odometer_start", ""))
        
        # Fuel level - "Other" seçildiyse other_fuel kullan
        fuel_level = form_data.get("fuel_level", "")
        if fuel_level == "Other":
            flat_data["fuel_level"] = "Other"
            flat_data["other_fuel"] = form_data.get("other_fuel", "")
        else:
            flat_data["fuel_level"] = fuel_level
            flat_data["other_fuel"] = ""
        
        flat_data["oil_level"] = form_data.get("oil_level", "")
        flat_data["fuel_card"] = form_data.get("fuel_card", "")
        flat_data["measuring_tape"] = form_data.get("measuring_tape", "")
        flat_data["safety_vest"] = form_data.get("safety_vest", "")
        flat_data["fuel_amount"] = form_data.get("fuel_amount", "")
        
        # Dosya yüklemeleri (şimdilik boş, gelecekte eklenebilir)
        flat_data["odometer_file"] = ""
        flat_data["fuel_receipt"] = ""
        
        # Exterior checks - direkt field isimleri (prefix olmadan)
        exterior_checks = form_data.get("exterior_checks", {})
        exterior_fields = ['headlights', 'break_lights', 'indicators', 'mirrors', 'windows', 
                          'windshield', 'wiper_fluid', 'wipers', 'tires', 'body_paint']
        for field in exterior_fields:
            flat_data[field] = exterior_checks.get(field, "Needs Attention")
        
        # Engine checks - direkt field isimleri
        engine_checks = form_data.get("engine_checks", {})
        engine_fields = ['engine_noise', 'coolant_level', 'brake_fluid', 'battery_condition', 'belts_hoses']
        for field in engine_fields:
            flat_data[field] = engine_checks.get(field, "Needs Attention")
        
        # Safety equipment - direkt field isimleri
        safety_checks = form_data.get("safety_checks", {})
        safety_fields = ['seatbelts', 'fire_extinguisher', 'first_aid_kit', 'horn', 'jumper_cables', 'snow_brush']
        for field in safety_fields:
            flat_data[field] = safety_checks.get(field, "Needs Attention")
        
        # Interior checks - direkt field isimleri
        interior_checks = form_data.get("interior_checks", {})
        interior_fields = ['cleanliness', 'dashboard_lights', 'hvac', 'seats']
        for field in interior_fields:
            flat_data[field] = interior_checks.get(field, "Needs Attention")
        
        # HTTP POST isteği gönder (multipart/form-data yerine application/x-www-form-urlencoded)
        data = urllib.parse.urlencode(flat_data).encode('utf-8')
        req = urllib.request.Request(GOOGLE_APPS_SCRIPT_URL, data=data, method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = response.read().decode('utf-8')
            # #region agent log
            _log("F", "excel_handler.py:save_form_submission_to_google_apps_script", "Google Apps Script response", {"status_code": response.status, "result": result[:100]})
            # #endregion agent log
            return True
    except Exception as e:
        # #region agent log
        _log("F", "excel_handler.py:save_form_submission_to_google_apps_script", "Google Apps Script error", {"error": str(e)})
        # #endregion agent log
        return False

def save_form_submission(form_data):
    """Form verilerini Excel dosyasına veya Google Sheets'e kaydeder"""
    from datetime import datetime
    from openpyxl import Workbook
    
    headers, row = _prepare_submission_row(form_data)
    
    # Google Apps Script kullanılıyorsa (eski yöntem - öncelikli)
    if USE_GOOGLE_APPS_SCRIPT and GOOGLE_APPS_SCRIPT_URL:
        success = save_form_submission_to_google_apps_script(form_data)
        if success:
            # #region agent log
            _log("F", "excel_handler.py:save_form_submission", "Saved to Google Apps Script successfully", {})
            # #endregion agent log
            # Yerel Excel'e de kaydet (backup)
            pass  # Fall through to Excel save
    
    # Google Sheets kullanılıyorsa (yeni yöntem)
    if USE_GOOGLE_SHEETS:
        client = get_google_sheets_client()
        if client:
            try:
                sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet("Submissions")
                # Başlık satırını kontrol et
                existing_headers = sheet.row_values(1)
                if not existing_headers or len(existing_headers) < len(headers):
                    sheet.clear()
                    sheet.append_row(headers)
                # Yeni satır ekle
                sheet.append_row(row)
                return
            except Exception as e:
                # #region agent log
                _log("E", "excel_handler.py:save_form_submission:google_sheets", "Google Sheets save failed, falling back to Excel", {"error": str(e)})
                # #endregion agent log
                pass  # Fallback to Excel
    
    # Excel dosyasına kaydet (fallback veya varsayılan)
    if os.path.exists(SUBMISSIONS_FILE):
        wb = load_workbook(SUBMISSIONS_FILE)
        if "Submissions" not in wb.sheetnames:
            ws = wb.create_sheet("Submissions")
            ws.append(headers)
        else:
            ws = wb["Submissions"]
    else:
        wb = Workbook()
        if "Sheet" in wb.sheetnames:
            wb.remove(wb["Sheet"])
        ws = wb.create_sheet("Submissions")
        ws.append(headers)
    
    ws.append(row)
    wb.save(SUBMISSIONS_FILE)

def load_form_submissions():
    """Form gönderimlerini Excel'den veya Google Sheets'ten okur"""
    # Google Sheets kullanılıyorsa
    if USE_GOOGLE_SHEETS:
        client = get_google_sheets_client()
        if client:
            try:
                sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet("Submissions")
                all_values = sheet.get_all_values()
                
                if not all_values or len(all_values) < 2:
                    return []
                
                headers = all_values[0]
                submissions = []
                
                for row in all_values[1:]:
                    if row and row[0]:  # Timestamp varsa
                        submission = {}
                        for i, header in enumerate(headers):
                            submission[header] = row[i] if i < len(row) else None
                        submissions.append(submission)
                
                return submissions
            except Exception as e:
                # #region agent log
                _log("E", "excel_handler.py:load_form_submissions:google_sheets", "Google Sheets load failed, falling back to Excel", {"error": str(e)})
                # #endregion agent log
                pass  # Fallback to Excel
    
    # Excel dosyasından oku (fallback veya varsayılan)
    if not os.path.exists(SUBMISSIONS_FILE):
        return []
    
    wb = load_workbook(SUBMISSIONS_FILE)
    if "Submissions" not in wb.sheetnames:
        return []
    
    ws = wb["Submissions"]
    submissions = []
    
    # Başlık satırını oku
    headers = []
    for cell in ws[1]:
        headers.append(cell.value)
    
    # Veri satırlarını oku
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0]:  # Timestamp varsa
            submission = {}
            for i, header in enumerate(headers):
                submission[header] = row[i] if i < len(row) else None
            submissions.append(submission)
    
    return submissions

def is_admin(username):
    """Kullanıcının admin olup olmadığını kontrol eder"""
    _log("B", "excel_handler.py:is_admin:entry", "is_admin called", {"username": username})
    
    # Google Sheets'ten oku
    if USE_GOOGLE_SHEETS:
        client = get_google_sheets_client()
        if client:
            try:
                sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet("Users")
                all_values = sheet.get_all_values()
                
                if not all_values or len(all_values) < 2:
                    return False
                
                headers = all_values[0]
                _log("B", "excel_handler.py:is_admin:headers", "Users sheet headers", {"headers": headers, "has_admin": "Admin" in headers})
                
                admin_col_idx = None
                if "Admin" in headers:
                    admin_col_idx = headers.index("Admin")
                elif len(headers) > 3:
                    admin_col_idx = 3
                
                for row in all_values[1:]:
                    if row and row[0] == username:
                        if admin_col_idx and len(row) > admin_col_idx:
                            admin_value = row[admin_col_idx]
                            is_admin_result = admin_value == "Yes" or admin_value == True
                            _log("B", "excel_handler.py:is_admin:admin_check", "Admin value check", {"admin_value": admin_value, "is_admin": is_admin_result})
                            return is_admin_result
                        if username == "admin":
                            return True
                
                _log("B", "excel_handler.py:is_admin:user_not_found", "User not found or not admin", {"username": username})
                return False
            except Exception as e:
                _log("E", "excel_handler.py:is_admin:google_sheets", "Google Sheets load failed, falling back to Excel", {"error": str(e)})
    
    # Excel'den oku (fallback)
    wb = get_excel_file()
    ws = wb["Users"]
    
    headers = [cell.value for cell in ws[1]]
    _log("B", "excel_handler.py:is_admin:headers", "Users sheet headers", {"headers": headers, "has_admin": "Admin" in headers})
    admin_col_idx = None
    
    if "Admin" in headers:
        admin_col_idx = headers.index("Admin")
        _log("B", "excel_handler.py:is_admin:admin_col_found", "Admin column found", {"admin_col_idx": admin_col_idx})
    elif len(headers) > 3:
        admin_col_idx = 3
        _log("B", "excel_handler.py:is_admin:admin_col_assumed", "Assuming admin column at index 3", {"admin_col_idx": admin_col_idx})
    
    user_found = False
    for row in ws.iter_rows(min_row=2, values_only=True):
        _log("B", "excel_handler.py:is_admin:checking_row", "Checking row", {"row_username": row[0] if row else None, "matches": row[0] == username if row else False})
        if row[0] == username:
            user_found = True
            _log("B", "excel_handler.py:is_admin:user_found", "User found in sheet", {"username": username, "row_length": len(row), "admin_col_idx": admin_col_idx})
            if admin_col_idx and len(row) > admin_col_idx:
                admin_value = row[admin_col_idx]
                is_admin_result = admin_value == "Yes" or admin_value == True
                _log("B", "excel_handler.py:is_admin:admin_check", "Admin value check", {"admin_value": admin_value, "is_admin": is_admin_result})
                return is_admin_result
            if username == "admin":
                _log("B", "excel_handler.py:is_admin:fallback", "Using fallback admin check", {"username": username, "is_admin": True})
                return True
    
    _log("B", "excel_handler.py:is_admin:user_not_found", "User not found or not admin", {"username": username, "user_found": user_found})
    return False

