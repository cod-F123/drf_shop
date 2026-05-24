# DRF-SHOP

یک backend تمیز و ماژولار ساخته‌شده با **Django** و **Django REST Framework** برای نمونه‌ای از فروشگاه آنلاین. این مخزن پایه‌ای مناسب برای نمونه‌سازی سریع، آموزش یا شروع یک پروژهٔ کوچک تا متوسط فراهم می‌کند.

<!-- ## فهرست محتوا

- [ویژگی‌ها](#ویژگیها)
- [فناوری‌ها](#فناوریها)
- [شروع سریع](#شروع_سریع)
- [اجرای با Docker](#docker)
- [متغیرهای محیطی (.env)](#env)
- [مستندات API](#api-docs)
- [ساختار پروژه](#structure)
- [نکات پیکربندی](#configuration)
- [تست‌ها](#tests)
- [مشارکت](#contributing)
- [لایسنس](#license) -->

## ویژگی‌ها

- احراز هویت با JWT (`rest_framework_simplejwt`)
- API برای مدیریت محصولات، سفارش/پرداخت و تیکت‌های پشتیبانی
- مستندات Swagger و Redoc (`drf-yasg`)
- ویرایشگر محتوای HTML با `tinymce`
- فیلترینگ (`django-filter`)، pagination و پشتیبانی از CORS

## فناوری‌ها

- Python 3.10+
- Django 6.x
- Django REST Framework
- drf-yasg, django-filter, django-tinymce, django-cors-headers

## شروع سریع

نحوهٔ اجرا به صورت محلی (بدون Docker):

```bash
git clone https://github.com/cod-F123/drf_shop.git
cd drf_shop
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # یا فایل .env خود را بسازید
python core/manage.py migrate
python core/manage.py createsuperuser  # اختیاری
python core/manage.py runserver
```

پس از اجرا، توصیه می‌شود که به آدرس `http://localhost:8000` مراجعه کنید.

## اجرای با Docker

```bash
docker-compose up --build
```

سرویس به صورت پیش‌فرض روی `http://localhost:8000` در دسترس خواهد بود.

## متغیرهای محیطی (.env)

نمونهٔ متغیرهای حداقلی که باید در `.env` قرار بگیرند:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

این پروژه از `python-decouple` برای بارگذاری متغیرهای محیطی استفاده می‌کند.

## مستندات API

- Swagger: `/swagger/`
- Redoc: `/redoc/`

(آدرس‌ها در `core/core/urls.py` ثبت شده‌اند.)

## ساختار پروژه (خلاصه)

- `core/` — پروژهٔ اصلی و تنظیمات
- `core/accounts/` — اپ مربوط به کاربران و احراز هویت
- `core/shop/` — اپ فروشگاه (محصولات، فیلترها، pagination)
- `core/payment/` — اپ پرداخت
- `core/tickets/` — مدیریت تیکت‌ها

برای مشاهده جزئیات بیشتر هر اپ به پوشهٔ مربوطه مراجعه کنید.

## نکات پیکربندی

- `AUTH_USER_MODEL = 'accounts.User'` — از مدل کاربر سفارشی استفاده می‌شود.
- تنظیمات JWT در `core/core/settings.py` قرار دارد.
- پایگاه دادهٔ پیش‌فرض `SQLite` است؛ برای محیط تولید از PostgreSQL یا دیتابیس مشابه استفاده کنید.

## تست‌ها

در صورت وجود تست‌ها، می‌توانید آن‌ها را با دستور زیر اجرا کنید:

```bash
python core/manage.py test
```

## مشارکت (Contributing)

برای مشارکت لطفاً یک issue باز کنید یا یک pull request ارسال نمایید. پیش از ارسال PR مطمئن شوید که تغییرات شما تست و مستند شده‌اند.

## لایسنس

این پروژه تحت مجوز **MIT** منتشر شده است — متن کامل لایسنس در فایل `LICENSE` موجود است.

## نگهدارنده

- مخزن: https://github.com/cod-F123/drf_shop


