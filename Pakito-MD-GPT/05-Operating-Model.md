---
artifact_id: 05-Operating-Model
artifact_version: 0.1
status: extracted
source_document: Pakito Business Definition v1.4
stage: Business Architecture
owner: Venture Team
---

# Operating Model

## Operating Principle

پاکیتو خود ارائه‌دهنده مستقیم خدمات خشکشویی نیست.

پاکیتو یک لایه هماهنگ‌کننده است که:

- مشتری را جذب می‌کند.
- سفارش را مدیریت می‌کند.
- سرویس‌دهنده مناسب را متصل می‌کند.
- وضعیت اجرا را کنترل می‌کند.
- تجربه مشتری را مدیریت می‌کند.

---

# Core Operating Actors

## Customer

مالک تقاضا

مسئول:

- انتخاب سرویس
- ثبت سفارش
- پرداخت
- ارزیابی نهایی

---

## Laundry Partner

مالک اجرای خدمت

مسئول:

- پذیرش سفارش
- پردازش سفارش
- کنترل کیفیت
- آماده‌سازی سفارش

---

## Logistics Partner

مالک جابه‌جایی

مسئول:

- دریافت سفارش
- تحویل سفارش
- رعایت زمان‌بندی

---

## Pakito

مالک فرآیند

مسئول:

- مدیریت سفارش
- هماهنگی بازیگران
- پشتیبانی
- کیفیت تجربه
- ثبت داده

---

# Value Flow

Customer
    ↓
Order Creation
    ↓
Provider Selection
    ↓
Pickup
    ↓
Service Execution
    ↓
Delivery
    ↓
Feedback


---

# Order Lifecycle

## Stage 1 — Discovery

مشتری:

* وارد پلتفرم می‌شود.
* سرویس‌دهندگان را مشاهده می‌کند.
* گزینه‌ها را مقایسه می‌کند.

Output:

Provider Selected

---

## Stage 2 — Order Creation

مشتری:

* آیتم‌ها را انتخاب می‌کند.
* زمان دریافت را تعیین می‌کند.
* سفارش را ثبت می‌کند.
* پرداخت انجام می‌دهد.

Output:

Confirmed Order

---

## Stage 3 — Provider Acceptance

خشکشویی:

* سفارش را مشاهده می‌کند.
* سفارش را می‌پذیرد یا رد می‌کند.

Output:

Accepted Order

---

## Stage 4 — Pickup

سفارش از مشتری دریافت می‌شود.

Output:

Items Received

---

## Stage 5 — Processing

خشکشویی:

* سفارش را اجرا می‌کند.
* وضعیت را به‌روزرسانی می‌کند.

Output:

Ready For Delivery

---

## Stage 6 — Delivery

سفارش به مشتری تحویل داده می‌شود.

Output:

Completed Order

---

## Stage 7 — Feedback

مشتری:

* امتیاز ثبت می‌کند.
* شکایت احتمالی را اعلام می‌کند.

Output:

Performance Data

---

# Operational Control Points

## Provider Acceptance Rate

هدف:

کنترل همکاری‌پذیری تأمین‌کنندگان

---

## Processing Time

هدف:

کنترل زمان آماده‌سازی

---

## Delivery Performance

هدف:

کنترل کیفیت لجستیک

---

## Customer Satisfaction

هدف:

کنترل کیفیت تجربه

---

## Complaint Rate

هدف:

کنترل ریسک عملیاتی

---

# Operational Zones

## Deployment Unit

واحد اصلی توسعه:

Zone

---

## Zone Structure

هر زون شامل:

* مجموعه مشتریان
* مجموعه خشکشویی‌ها
* ظرفیت عملیاتی مشخص

---

## Expansion Rule

توسعه جغرافیایی فقط پس از تثبیت عملکرد زون قبلی انجام می‌شود.

---

# Supply Management Model

## Provider Onboarding

فرآیند:

1. شناسایی
2. ارزیابی
3. تست اولیه
4. عقد قرارداد
5. فعال‌سازی

---

## Provider Governance

ابزارهای کنترل:

* امتیازدهی
* اخطار
* جریمه
* تعلیق
* حذف

---

# Quality Management

## Quality Signals

* امتیاز مشتری
* نرخ شکایت
* نرخ تأخیر
* نرخ پذیرش
* کیفیت بسته‌بندی

---

## Quality Actions

عملکرد مناسب:

* نمایش بیشتر
* سفارش بیشتر
* مزایای تشویقی

عملکرد ضعیف:

* کاهش رتبه
* تعلیق
* حذف

---

# Customer Support Model

پاکیتو نقطه تماس واحد مشتری است.

مشتری نباید میان:

* خشکشویی
* لجستیک
* پلتفرم

جابجا شود.

---

# Data Capture Model

برای هر سفارش ثبت می‌شود:

## Customer Data

* شناسه مشتری
* منطقه
* سابقه سفارش

---

## Order Data

* آیتم‌ها
* مبلغ
* وضعیت
* زمان‌ها

---

## Provider Data

* سرویس‌دهنده
* عملکرد
* کیفیت

---

## Logistics Data

* دریافت
* تحویل
* تأخیر

---

## Financial Data

* مبلغ سفارش
* سهم پاکیتو
* سهم سرویس‌دهنده

---

# Scaling Logic

## Stage 1

Pilot Zone

---

## Stage 2

Multi-Zone Operations

---

## Stage 3

City Expansion

---

## Stage 4

Multi-City Expansion

---

# Operating Model Success Conditions

عملیات زمانی موفق است که:

* سفارش‌ها بدون اصطکاک اجرا شوند.
* کیفیت پایدار باشد.
* تأخیرها کنترل شوند.
* شکایت‌ها قابل مدیریت باشند.
* هزینه عملیاتی رشد کنترل‌شده داشته باشد.
* مدل در زون‌های جدید قابل تکرار باشد.

---

# Critical Dependencies

* شبکه تأمین‌کنندگان قابل اعتماد
* لجستیک پایدار
* ثبت داده دقیق
* پشتیبانی پاسخگو
* کیفیت عملیاتی قابل اندازه‌گیری

اختلال در هر یک از این موارد می‌تواند عملکرد کل سیستم را تضعیف کند.


