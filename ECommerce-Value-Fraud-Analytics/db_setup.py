import sqlite3
import pandas as pd

# 1. قراءة ملف الـ CSV (تأكدي أن الاسم مطابق لاسم الملف اللي جوه فولدر data)
# لو الاسم لسه طويل زي ما هو، غيري 'ecommerce_data.csv' لاسم الملف الحالي عندك
csv_path = 'data/ecommerce_data.csv'
df = pd.read_csv(csv_path)

# تنظيف أسماء الأعمدة من المسافات لتجنب المشاكل في SQL
df.columns = df.columns.str.strip().str.replace(' ', '_')

# 2. إنشاء الاتصال بقاعدة البيانات (سيتم إنشاء ملف باسم الـ db تلقائياً)
conn = sqlite3.connect('ecommerce_analytics.db')

# 3. حفظ الداتا جوه جدول اسمه customers_behavior
df.to_sql('customers_behavior', conn, if_exists='replace', index=False)

print("تم إنشاء قاعدة البيانات وحفظ الجدول بنجاح! 🎉")

# 4. إغلاق الاتصال
conn.close()