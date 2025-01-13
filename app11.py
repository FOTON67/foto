import random
import requests
from datetime import datetime
from sklearn.ensemble import IsolationForest
from sklearn import confusion_matrix,  precision_score, recall_score, f1_score
import numpy as np
import pandas as pd
import streamlit as st

# استدعاء البيانات من ملف Excel
def load_data_from_excel(file_path):
    try:
        df = pd.read_excel("C:\Users\user\foto\real_estate_dataset.xlsx")
        return df
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

def fetch_real_estate_price(property_location, property_type):
    # استدعاء API للحصول على سعر البورصة العقارية
    # هنا يمكن إدخال عنوان IP الخاص بالخدمة
    api_url = "https://real-estate-api.example.com/getPrice"
    try:
        response = requests.get(api_url, params={"location": property_location, "type": property_type})
        if response.status_code == 200:
            return response.json().get("price", None)
        else:
            st.warning("Failed to fetch data from API.")
            return None
    except Exception as e:
        st.error(f"Error fetching real estate data: {e}")
        return None

# واجهة Streamlit
st.title("نظام كشف الشذوذ والتهرب الضريبي للعقارات")

uploaded_file = st.file_uploader("تحميل ملف الفواتير (Excel)", type="pdf")
if uploaded_file:
    data = load_data_from_excel(uploaded_file)

    if data is not None:
        # تحويل النصوص إلى أرقام
        data["نوع_العقار"] = data["نوع_العقار"].astype("category").cat.codes
        data["موقع_العقار"] = data["موقع_العقار"].astype("category").cat.codes

        # تحديد الأعمدة المهمة فقط
        data = data[["قيمة_العقار", "نوع_العقار", "موقع_العقار"]]

        # إعداد بيانات التدريب
        X = data.values

        # تدريب نموذج Isolation Forest
        model = IsolationForest(contamination=0.1, random_state=42)
        model.fit(X)

        # فحص الشذوذ للسجلات
        data["anomaly_score"] = model.decision_function(X)
        data["anomaly"] = model.predict(X)

        # تحديد الشذوذ
        data["anomaly"] = data["anomaly"].apply(lambda x: "شاذ" if x == -1 else "طبيعي")

        # عرض النتائج
        st.write("### النتائج")
        st.dataframe(data)

        # خيار فحص فاتورة محددة
        st.write("### فحص فاتورة جديدة")
        property_value = st.number_input("قيمة العقار", min_value=0, step=1000)
        property_location = st.selectbox("موقع العقار", data["موقع_العقار"].astype("category").cat.categories)
        property_type = st.selectbox("نوع العقار", data["نوع_العقار"].astype("category").cat.categories)

        if st.button("فحص الفاتورة"):
            location_code = data["موقع_العقار"].astype("category").cat.codes.loc[data["موقع_العقار"] == property_location].iloc[0]
            type_code = data["نوع_العقار"].astype("category").cat.codes.loc[data["نوع_العقار"] == property_type].iloc[0]

            real_estate_price = fetch_real_estate_price(property_location, property_type)

            if real_estate_price:
                st.write(f"سعر البورصة للعقار: {real_estate_price}")

                # فحص إذا ما كانت الصفقة أقل من سعر السوق
                if property_value < real_estate_price:
                    st.error("⚠️ تهرب ضريبي محتمل: قيمة العقار أقل من سعر السوق")
                else:
                    st.success("✅ الفاتورة طبيعية")

            # فحص الشذوذ باستخدام النموذج
            test_record = [[property_value, type_code, location_code]]
            anomaly = model.predict(test_record)

            if anomaly[0] == -1:
                st.error("⚠️ تم الكشف عن شذوذ في الصفقة")
            else:
                st.success("✅ الصفقة تبدو طبيعية")

        if st.button("عرض تقرير الأداء"):
            # حساب مقاييس الأداء
            threshold = np.percentile(data["anomaly_score"], 100 * model.contamination)
            true_labels = [1 if score >= threshold else -1 for score in data["anomaly_score"]]

            conf_matrix = confusion_matrix(true_labels, data["anomaly"].map({"شاذ": -1, "طبيعي": 1}))
            precision = precision_score(true_labels, data["anomaly"].map({"شاذ": -1, "طبيعي": 1}), pos_label=-1)
            recall = recall_score(true_labels, data["anomaly"].map({"شاذ": -1, "طبيعي": 1}), pos_label=-1)
            f1 = f1_score(true_labels, data["anomaly"].map({"شاذ": -1, "طبيعي": 1}), pos_label=-1)

            st.write("### تقرير الأداء")
            st.write(f"عدد البيانات الشاذة: {len(data[data['anomaly'] == 'شاذ'])}")
            st.write(f"متوسط anomaly score: {np.mean(data['anomaly_score'])}")
            st.write("#### Confusion Matrix:")
            st.write(conf_matrix)
            st.write(f"Precision: {precision:.4f}")
            st.write(f"Recall: {recall:.4f}")
            st.write(f"F1-Score: {f1:.4f}")

    else:
        st.error("تعذر تحميل البيانات من ملف Excel.")
