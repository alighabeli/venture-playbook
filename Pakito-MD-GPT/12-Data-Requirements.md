---
artifact_id: 12-Data-Requirements
artifact_version: 0.1
status: extracted
source_document: Pakito Business Definition v1.4
stage: Governance
owner: Venture Team
---

# Data Requirements

## Purpose

این سند مشخص می‌کند چه داده‌هایی باید جمع‌آوری شوند تا:

- عملیات قابل مدیریت باشد.
- پایلوت قابل ارزیابی باشد.
- فرضیات قابل اعتبارسنجی باشند.
- System State قابل استخراج باشد.

---

# Data Principles

## Principle 1

هر داده باید مصرف مشخص داشته باشد.

---

## Principle 2

هر KPI باید منبع داده مشخص داشته باشد.

---

## Principle 3

هر تصمیم باید قابل ردیابی به داده باشد.

---

## Principle 4

داده‌های غیرضروری نباید جمع‌آوری شوند.

---

# Data Domains

پاکیتو به پنج حوزه داده نیاز دارد:

1. Customer Data
2. Order Data
3. Supply Data
4. Operational Data
5. Financial Data

---

# Customer Data

## Customer Profile

### Required Fields

- Customer ID
- Mobile Number
- Name
- Zone
- Registration Date

---

## Customer Activity

### Required Fields

- Total Orders
- First Order Date
- Last Order Date
- Repeat Order Count

---

## Customer Satisfaction

### Required Fields

- Rating
- Complaint Count
- Resolution History

---

# Order Data

## Order Identity

### Required Fields

- Order ID
- Customer ID
- Provider ID
- Order Date

---

## Order Content

### Required Fields

- Service Type
- Item Count
- Order Value

---

## Order Lifecycle

### Required Fields

- Created Time
- Accepted Time
- Picked Up Time
- Ready Time
- Delivered Time

---

## Order Status

### Required States

- Created
- Accepted
- Picked Up
- Processing
- Ready
- Delivered
- Cancelled

---

# Supply Data

## Provider Profile

### Required Fields

- Provider ID
- Provider Type
- Zone
- Join Date

---

## Provider Performance

### Required Fields

- Acceptance Rate
- Delay Rate
- Complaint Rate
- Average Rating

---

## Provider Capacity

### Required Fields

- Active Orders
- Monthly Orders
- Capacity Estimate

---

# Operational Data

## Logistics Data

### Required Fields

- Pickup Time
- Delivery Time
- Delay Events

---

## Support Data

### Required Fields

- Ticket Count
- Resolution Time
- Complaint Type

---

## Quality Data

### Required Fields

- Complaint Reason
- Damage Events
- Refund Events

---

# Financial Data

## Transaction Data

### Required Fields

- Order Value
- Provider Share
- Platform Share

---

## Revenue Data

### Required Fields

- Commission Amount
- Total Revenue

---

## Cost Data

### Required Fields

- CAC
- Refund Cost
- Support Cost
- Operational Cost

---

# Validation Data

## Customer Validation Metrics

Must Be Measurable:

- Conversion Rate
- Repeat Order Rate
- Satisfaction Rate

---

## Supply Validation Metrics

Must Be Measurable:

- Acceptance Rate
- Retention Rate
- Quality Score

---

## Operational Validation Metrics

Must Be Measurable:

- Completion Rate
- Delay Rate
- Complaint Rate

---

## Economic Validation Metrics

Must Be Measurable:

- AOV
- Gross Profit Per Order
- CAC
- LTV
- LTV/CAC

---

# Derived Metrics

## Customer Metrics

Calculated From:

Customer Data + Order Data

Examples:

- Repeat Rate
- Cohort Retention
- Orders Per Customer

---

## Supply Metrics

Calculated From:

Provider Data + Order Data

Examples:

- Provider Utilization
- Provider Quality Score

---

## Operational Metrics

Calculated From:

Order Lifecycle Data

Examples:

- Cycle Time
- SLA Compliance

---

## Financial Metrics

Calculated From:

Revenue + Cost Data

Examples:

- Contribution Margin
- Unit Economics
- Payback Period

---

# Data Retention Requirements

Minimum Retention:

- Customer Data
- Order Data
- Financial Data
- Complaint Data

Must be retained for audit and analysis purposes.

---

# Data Access Model

## Customer Support

Access:

Limited

---

## Operations Team

Access:

Operational Data

---

## Management

Access:

Aggregated Reports

---

## Providers

Access:

Own Performance Only

---

# Reporting Requirements

## Daily Reports

- Orders
- Revenue
- Operational Issues

---

## Weekly Reports

- Customer Trends
- Provider Performance
- Complaints

---

## Monthly Reports

- Unit Economics
- Retention
- Growth Metrics

---

# Critical Data Dependencies

بدون داده‌های زیر اعتبارسنجی مدل ممکن نیست:

- Repeat Orders
- Order Value
- Provider Acceptance
- Completion Rate
- Complaint Rate
- CAC

---

# Governance Rule

هیچ KPI نباید بدون:

Metric
↓
Formula
↓
Data Source

تعریف شود.

و هیچ تصمیم مدیریتی نباید بدون داده پشتیبان اتخاذ شود.

