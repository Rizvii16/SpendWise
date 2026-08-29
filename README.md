# 💸 SpendWise — Personal Expense Tracker

SpendWise is a Python and Streamlit-based personal expense tracking and financial analytics application.

It allows users to record, analyze, and visualize their expenses through an interactive dashboard with category-wise analysis, payment method insights, monthly trends, daily spending analysis, and downloadable reports.

---

## 📌 Overview

Managing personal expenses manually can make it difficult to understand spending patterns.

**SpendWise** provides a centralized dashboard to help users:

- Track expenses
- Analyze spending patterns
- Visualize financial trends
- Filter expense data
- Generate CSV reports
- Generate PDF financial reports
- Understand category-wise and payment-method spending

The project demonstrates the practical use of **Python, data analysis, visualization, database management, and dashboard development**.

---

## 🚀 Features

### 📊 Financial Dashboard
- Total spending
- Average expense
- Highest spending category
- Total number of transactions

### 💰 Expense Management
- Add expenses
- Delete expenses
- View stored expenses
- Filter expense records
- Sample dataset included

### 📈 Data Analysis
- Category-wise spending analysis
- Monthly spending trends
- Daily spending analysis
- Payment method distribution
- Spending summaries

### 📑 Report Generation
- Downloadable CSV reports
- Automated financial PDF reports
- Summary statistics

### 🎨 Dashboard
- Interactive Streamlit interface
- Interactive Plotly visualizations
- Responsive financial analytics dashboard

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming |
| Streamlit | Interactive dashboard |
| Pandas | Data processing and analysis |
| Plotly | Interactive visualizations |
| SQLite | Local expense data storage |
| ReportLab | PDF report generation |
| CSV | Dataset and report handling |

---

## 📂 Project Structure

```text
SpendWise/
│
├── app.py
├── main.py
├── analytics.py
├── database.py
├── report_generator.py
├── requirements.txt
├── runtime.txt
├── README.md
│
├── data/
│   └── expenses.csv
│
└── reports/
    └── summary_report.csv