import streamlit as pd
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# إعدادات الصفحة
st.set_page_config(page_title="E-Commerce Analytics Dashboard", layout="wide")
st.title("📊 E-Commerce Customer Value & Satisfaction Dashboard")
st.write("Welcome to the interactive business intelligence dashboard.")

# الاتصال بقاعدة البيانات وسحب البيانات
conn = sqlite3.connect('ecommerce_analytics.db')
df = pd.read_sql_query("SELECT * FROM customers_behavior", conn)
conn.close()

# تنظيف وتجهيز حسابات سريعة للـ Dashboard
df.columns = df.columns.str.strip().str.replace(' ', '_')

# عمل القائمة الجانبية (Sidebar) للفلاتر
st.sidebar.header("Filter Options")
city_filter = st.sidebar.multiselect("Select City:", options=df['City'].unique(), default=df['City'].unique())
gender_filter = st.sidebar.multiselect("Select Gender:", options=df['Gender'].unique(), default=df['Gender'].unique())

# تطبيق الفلاتر على الداتا
filtered_df = df[(df['City'].isin(city_filter)) & (df['Gender'].isin(gender_filter))]

# عرض أرقام رئيسية (KPIs)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Customers", f"{len(filtered_df)}")
with col2:
    st.metric("Total Revenue ($)", f"{filtered_df['Total_Spend'].sum():,.2f}")
with col3:
    st.metric("Avg Satisfaction", f"{filtered_df['Average_Rating'].mean():.2f} / 5")
with col4:
    st.metric("Avg Days Since Purchase", f"{filtered_df['Days_Since_Last_Purchase'].mean():.1f} Days")

st.markdown("---")

# رسم بياني لتوزيع مستوى الرضا وتأثير المبيعات
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🎯 Satisfaction Level Distribution")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=filtered_df, x='Satisfaction_Level', palette='pastel', ax=ax)
    plt.tight_layout()
    st.pyplot(fig)

with col_right:
    st.subheader("💰 Total Spend vs Items Purchased")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=filtered_df, x='Items_Purchased', y='Total_Spend', hue='Membership_Type', palette='viridis', ax=ax2)
    plt.tight_layout()
    st.pyplot(fig2)

# عرض عينة من البيانات الحقيقية
st.subheader("📋 Sample Filtered Data")
st.dataframe(filtered_df.head(10))