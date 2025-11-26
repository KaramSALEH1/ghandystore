# تعليمات رفع المشروع على السيرفر

## المتطلبات الأساسية
- Python 3.8 أو أحدث
- pip (مدير حزم Python)

## خطوات التنصيب

### 1. إنشاء بيئة افتراضية (Virtual Environment)
```bash
python -m venv venv
```

### 2. تفعيل البيئة الافتراضية
**على Windows:**
```bash
venv\Scripts\activate
```

**على Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 4. إعداد قاعدة البيانات
```bash
python manage.py migrate
```

### 5. إنشاء مستخدم الأدمن (اختياري)
```bash
python manage.py createsuperuser
```

### 6. جمع الملفات الثابتة (Static Files)
```bash
python manage.py collectstatic
```

### 7. تشغيل السيرفر
**للتطوير:**
```bash
python manage.py runserver
```

**للإنتاج:** استخدم WSGI server مثل Gunicorn أو uWSGI

## ملاحظات مهمة

1. **قاعدة البيانات:** المشروع يستخدم SQLite افتراضياً. للبيئة الإنتاجية، يُنصح باستخدام PostgreSQL أو MySQL.

2. **الملفات الثابتة:** تأكد من إعداد STATIC_ROOT و MEDIA_ROOT في settings.py بشكل صحيح.

3. **ALLOWED_HOSTS:** في settings.py، أضف نطاق السيرفر الخاص بك إلى ALLOWED_HOSTS.

4. **SECRET_KEY:** في البيئة الإنتاجية، استخدم SECRET_KEY مختلف وامن. لا تشارك SECRET_KEY.

5. **DEBUG:** في البيئة الإنتاجية، ضع DEBUG = False.

## إعدادات السيرفر الإنتاجي

للإنتاج، تأكد من:
- تغيير `DEBUG = False` في settings.py
- إضافة نطاق السيرفر إلى `ALLOWED_HOSTS`
- إعداد قاعدة بيانات إنتاجية (PostgreSQL/MySQL)
- إعداد خادم ويب (Nginx/Apache)
- إعداد WSGI server (Gunicorn/uWSGI)
- إعداد HTTPS/SSL
- إعداد backup للقاعدة البيانات

## البنية الأساسية للمشروع
- `ghandyStore/` - إعدادات المشروع الرئيسية
- `base/` - التطبيق الأساسي (الواجهة الرئيسية)
- `item/` - تطبيق المنتجات
- `media/` - ملفات الصور التي يرفعها المستخدمون
- `staticfiles/` - الملفات الثابتة المجمعة
- `db.sqlite3` - قاعدة البيانات (يُنشأ تلقائياً)

