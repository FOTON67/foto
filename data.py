import random
import pandas as pd
from datetime import datetime, timedelta
import string
import os

def generate_iban():
    """توليد رقم IBAN سعودي عشوائي"""
    return f"SA{''.join([str(random.randint(0, 9)) for _ in range(22)])}"

def generate_national_id():
    """توليد رقم هوية وطنية سعودية عشوائية"""
    return f"{''.join([str(random.randint(0, 9)) for _ in range(10)])}"

def generate_deed_number():
    """توليد رقم صك عقاري عشوائي"""
    return f"{''.join([str(random.randint(0, 9)) for _ in range(10)])}"

def generate_serial_number():
    """توليد رقم تسلسلي عشوائي"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=8))

def generate_arabic_name():
    """توليد اسم عربي عشوائي من ثلاثة مقاطع"""
    first_names = ["محمد", "أحمد", "عبدالله", "سعد", "خالد", "فهد", "عمر", "علي", "إبراهيم", "سلطان"]
    middle_names = ["سعيد", "محمد", "عبدالرحمن", "فهد", "سعود", "عبدالعزيز", "ناصر", "صالح"]
    last_names = ["السعدي", "العمري", "الحربي", "القحطاني", "الدوسري", "المطيري", "الشهري", "العتيبي"]
    
    return f"{random.choice(first_names)} {random.choice(middle_names)} {random.choice(last_names)}"

def generate_property_location():
    """توليد موقع عقار عشوائي"""
    cities = ["الرياض", "جدة", "الدمام", "مكة المكرمة", "المدينة المنورة", "الخبر", "تبوك", "أبها"]
    districts = ["حي النرجس", "حي الياسمين", "حي الملقا", "حي القيروان", "حي الصحافة", "حي المروج", "حي العليا"]
    
    return f"{random.choice(cities)}، {random.choice(districts)}"

def generate_property_value():
    """توليد قيمة عقار عشوائية"""
    return random.randint(500000, 15000000)

def generate_and_save_real_estate_notices(n_samples=100, output_file="real_estate_notices.xlsx"):
    """
    توليد بيانات اصطناعية لإشعارات الإفراغ العقاري وحفظها في ملف Excel
    
    المعلمات:
    n_samples (int): عدد الإشعارات المراد توليدها
    output_file (str): اسم ملف Excel المراد حفظ البيانات فيه
    
    تُرجع:
    str: مسار الملف المحفوظ
    """
    data = []
    
    for _ in range(n_samples):
        # توليد تاريخ عشوائي خلال السنة القادمة
        transaction_date = datetime.now() + timedelta(days=random.randint(1, 365))
        
        # توليد قيمة العقار
        property_value = generate_property_value()
        
        record = {
            "الرقم_التسلسلي": generate_serial_number(),
            "رقم_ايبان_المالك": generate_iban(),
            "رقم_هوية_المالك": generate_national_id(),
            "نوع_هوية_المالك": "هوية وطنية",
            "اسم_المالك": generate_arabic_name(),
            "رقم_هوية_المشتري": generate_national_id(),
            "نوع_هوية_المشتري": "هوية وطنية",
            "اسم_المشتري": generate_arabic_name(),
            "رقم_الصك": generate_deed_number(),
            "قيمة_العقار": property_value,
            "موقع_العقار": generate_property_location(),
            "نوع_العقار": random.choice(["سكني", "تجاري", "سكني تجاري"]),
            "وسيلة_الدفع": "مدى",
            "تاريخ_الصفقة": transaction_date.strftime("%d/%m/%Y"),
        }
        data.append(record)
    
    # تحويل البيانات إلى DataFrame
    df = pd.DataFrame(data)
    
    # حفظ البيانات في ملف Excel
    df.to_excel(output_file, index=False, engine='openpyxl')
    
    return os.path.abspath(output_file)

# توليد 1000 إشعار وحفظها في ملف Excel
file_path = generate_and_save_real_estate_notices(10000, "real_estate_dataset.xlsx")
print(f"تم حفظ البيانات في الملف: {file_path}")

# قراءة عينة من البيانات للتحقق
sample_data = pd.read_excel("real_estate_dataset.xlsx").head()
print("\nعينة من البيانات المولدة:")
print(sample_data.to_string())