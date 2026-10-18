# استخدام صورة Python خفيفة
FROM python:3.10-slim

# تحديد مجلد العمل داخل الكونتينر
WORKDIR /app

# نسخ ملف الاعتماديات وتثبيتها أولاً
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# فتح البورت للتطبيق
EXPOSE 5000

# تشغيل التطبيق
CMD ["python", "app.py"]