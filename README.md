# Fundivis

> **Know where your money is—not just where it went.**

A Behavioral Financial Visibility Engine that helps people understand the true state of their finances through visibility, intentional money allocation, and behavioral insights.

Fundivis reimagines personal finance by moving beyond traditional budgeting and expense tracking. Instead of focusing only on historical transactions, it helps users answer a more important question:

> **"Where is my money right now?"**

Built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and modern backend engineering practices, Fundivis demonstrates how thoughtful product design and scalable software architecture can work together to solve real-world financial problems.

---

## Table of Contents

- Overview
- The Money Visibility Problem
- Why Fundivis Exists
- The Three States of Money
- Core Product Philosophy
- Why Fundivis is Different
- Product Vision

---

# Overview

Fundivis is a **Behavioral Financial Visibility Engine** designed to help individuals gain clarity over their financial lives.

Unlike traditional budgeting applications that primarily record transactions, Fundivis focuses on the current state of a person's money.

Instead of asking:

> **"Where did my money go?"**

Fundivis asks:

> **"Where is my money today?"**

This seemingly simple shift changes the entire financial experience.

Rather than encouraging users to constantly analyze past spending, Fundivis helps them understand:

- How much money is truly available to spend
- How much money is intentionally protected
- How much wealth has already been spent
- Whether today's financial decisions improve tomorrow's financial position

The result is a calmer, more intentional approach to personal finance built around clarity instead of complexity.

---

# The Money Visibility Problem

Most personal finance applications are built around transactions.

They allow users to:

- Record income
- Record expenses
- Categorize spending
- Generate monthly reports
- Export historical data

While these features are useful, they fail to answer the question that matters most in everyday life.

Most people don't wake up wondering:

> "How much did I spend last Tuesday?"

Instead, they wonder:

- Can I actually afford this purchase?
- How much money is safe to spend?
- Have I already set aside my rent?
- Is my emergency fund protected?
- Am I making financial progress?

Traditional budgeting applications rarely answer these questions directly because they focus on recording financial history rather than representing financial reality.

As a result, many users experience:

- Financial anxiety despite having money
- Confusion about their true financial position
- Difficulty distinguishing savings from spending
- Poor visibility into their available cash
- Budget fatigue caused by overly complex financial tools

Fundivis was created to solve this problem.

---

# Why Fundivis Exists

Fundivis was built on one simple belief:

> **Financial clarity reduces financial anxiety.**

People don't necessarily make poor financial decisions because they lack money.

They often make poor decisions because they lack visibility.

Without understanding where money currently exists, every purchase becomes uncertain.

Savings feel invisible.

Budgets feel restrictive.

Financial planning becomes overwhelming.

Fundivis transforms financial information into something people can understand immediately.

Instead of overwhelming users with spreadsheets, categories, and dozens of reports, it provides a clear picture of where every unit of money currently exists.

The goal isn't simply to organize financial records.

The goal is to improve financial confidence.

---

# The Three States of Money

Fundivis is built around a simple but powerful principle:

> **Every unit of money exists in only one of three states.**

Understanding these states allows users to see their financial position instantly without relying on complicated budgets or accounting knowledge.

---

## Available Money

Available Money represents funds that are immediately safe to spend.

This is the amount users can use today without affecting money already committed to future responsibilities.

Examples include:

- Wallet balance
- Checking account
- Cash available after protected allocations

When users ask:

> "How much can I safely spend today?"

Fundivis answers using Available Money.

---

## Protected Money

Protected Money represents wealth that has been intentionally reserved for a future purpose.

Examples include:

- Emergency Fund
- Rent
- School Fees
- Vacation
- Business Capital
- Investments
- House Deposit
- Wedding Fund

Protected Money is **not spending**.

The money still belongs to the user.

It has simply changed its financial purpose.

Traditional budgeting applications frequently treat moving money into savings as an expense.

Fundivis does not.

Protected Money remains part of the user's wealth.

---

## Spent Money

Spent Money represents wealth that has permanently left the user's financial position.

Examples include:

- Groceries
- Transportation
- Electricity Bills
- Dining
- Fuel
- Shopping
- Subscriptions
- Medical Expenses

Once money enters the Spent state, it no longer contributes to the user's current wealth.

Unlike Protected Money, Spent Money cannot simply return through reclassification.

---

# Core Product Philosophy

Everything inside Fundivis is built around a small set of principles.

These principles influence every feature, every API endpoint, every dashboard, and every financial calculation.

---

## 1. Visibility Creates Awareness

People cannot improve what they cannot clearly see.

Fundivis transforms financial information into meaningful visibility rather than overwhelming users with endless transaction records.

Every dashboard exists to answer practical financial questions quickly.

---

## 2. Awareness Improves Decisions

Better financial decisions begin with better financial understanding.

When users clearly understand where their money exists, they naturally become more intentional about future spending, saving, and planning.

Fundivis encourages informed decision-making rather than reactive budgeting.

---

## 3. Saving Is Not Spending

This is one of Fundivis' defining principles.

Moving money into an Emergency Fund does not reduce wealth.

It simply changes the state of the money.

Example:

```
Wallet
₦100,000

↓

Emergency Fund
₦100,000
```

Traditional budgeting applications often record this as:

Expense → ₦100,000

Fundivis records it as:

Protected Money → ₦100,000

No wealth was lost.

Only visibility changed.

---

## 4. Transfers Are Not Income

Moving money between financial buckets should never create artificial income.

For example:

```
Emergency Fund

↓

Main Wallet
```

This movement is **not income**.

It is simply a reclassification of existing wealth.

This prevents misleading financial reports while maintaining an accurate picture of net worth.

---

## 5. Simplicity Reduces Anxiety

Financial software should make users feel calmer, not more overwhelmed.

Every screen inside Fundivis is intentionally designed to reduce cognitive load.

Instead of presenting dozens of metrics, Fundivis surfaces only the information necessary to help users make confident financial decisions.

---

# Why Fundivis Is Different

Most finance applications are built around bookkeeping.

Fundivis is built around financial visibility.

| Traditional Finance Apps | Fundivis |
|---------------------------|-----------|
| Focus on past transactions | Focus on current financial position |
| Saving is often treated as spending | Saving becomes Protected Money |
| Transfers distort financial reports | Transfers are treated as reclassification |
| Budget-centric | Visibility-centric |
| Expense tracking | Wealth awareness |
| Historical reporting | Real-time financial state |
| Transaction management | Behavioral financial clarity |

Fundivis doesn't try to replace accounting software.

It complements financial planning by helping people understand the true state of their money before they make their next financial decision.

---

# Product Vision

Fundivis is more than a finance tracker.

It is the foundation for a new way of thinking about personal finance.

Our long-term vision is to build a **Financial Operating System** that empowers people to:

- Understand where every unit of money exists
- Build intentional saving habits
- Protect future financial commitments
- Develop healthier financial behaviors
- Make confident spending decisions
- Reduce financial anxiety through clarity
- Improve long-term financial wellbeing

The future of personal finance isn't better budgeting.

It's better visibility.

Welcome to Fundivis.

---

# Core Features

Fundivis is not organized around transactions.

It is organized around **financial visibility**.

Every module inside the platform exists to answer one question:

> **"Does this help the user understand where their money is?"**

Rather than overwhelming users with dozens of disconnected financial tools, Fundivis combines several intelligent modules into one unified Financial Visibility Engine.

---

# The Money Movement Engine

Every financial activity inside Fundivis is classified into one of four money movements.

Unlike traditional finance applications, these movements are not treated equally.

Each movement has a unique effect on the user's financial position.

---

## Income

Income represents money entering the user's financial ecosystem.

Examples include:

- Salary
- Freelance payments
- Business income
- Gifts
- Refunds
- Investment returns

Income increases Available Money.

---

## Expenses

Expenses represent money permanently exchanged for goods or services.

Examples include:

- Groceries
- Transportation
- Fuel
- Utility bills
- Shopping
- Entertainment
- Subscriptions

Expenses reduce both Available Money and Net Worth.

---

## Allocations

Allocations move money into a Protected Bucket.

Examples:

```
Wallet

↓

Emergency Fund
```

```
Checking Account

↓

Vacation Bucket
```

Allocations are **not expenses.**

Instead, they convert Available Money into Protected Money while preserving total wealth.

---

## Reclassifications

Reclassifications move money between financial locations without changing ownership.

Examples:

```
Emergency Fund

↓

Wallet
```

```
Rent Bucket

↓

Checking Account
```

Reclassifications are:

- Not income
- Not expenses
- Not savings

They simply change where money exists.

This prevents inaccurate reports that commonly occur in traditional budgeting applications.

---

# Wealth Protection Engine

One of Fundivis' defining innovations is the Wealth Protection Engine.

Instead of treating savings as an expense, Fundivis allows users to intentionally protect portions of their wealth using financial buckets.

Protected money remains visible at all times.

Users always know:

- What is available
- What is protected
- What has already been spent

---

## Financial Buckets

Users can create unlimited purpose-driven buckets.

Examples include:

- Emergency Fund
- Rent
- School Fees
- Vacation
- House Deposit
- Wedding
- Investment
- Car Maintenance
- Taxes
- Business Capital

Every bucket contains money that still belongs to the user.

The bucket simply defines its purpose.

---

## Bucket Operations

Supported operations include:

- Create Bucket
- Edit Bucket
- Archive Bucket
- Deposit Money
- Withdraw Money
- Transfer Between Buckets
- View Bucket History
- Track Bucket Growth

Because buckets represent Protected Money, none of these operations distort income or expense reports.

---

# Financial Visibility Dashboard

The dashboard is the heart of Fundivis.

Instead of displaying dozens of disconnected reports, it presents the user's financial position in real time.

The dashboard answers questions such as:

- How much money can I safely spend today?
- How much wealth is protected?
- What percentage of my money has already been spent?
- Is my financial position improving?
- Which financial commitments are fully funded?

Every card exists to improve decision-making rather than simply displaying numbers.

---

## Dashboard Overview

The Financial Visibility Dashboard displays:

- Available Money
- Protected Money
- Spent Money
- Total Net Worth
- Monthly Cash Flow
- Recent Financial Activity
- Active Financial Buckets
- Spending Distribution
- Financial Health Indicators

---

## Daily Snapshot

Provides an instant overview of today's financial activity.

Includes:

- Today's Income
- Today's Expenses
- Net Daily Movement
- Current Available Balance

---

## Monthly Financial Summary

Every month Fundivis generates a complete visibility report.

Including:

- Total Income
- Total Spending
- Total Protected Wealth
- Available Money
- Largest Expense
- Largest Income
- Savings Allocation
- Spending Categories

Unlike traditional monthly reports, this summary explains where money currently exists—not just where it went.

---

# Behavioral Insights Engine

Financial awareness requires more than numbers.

Fundivis continuously analyzes financial behavior to surface meaningful insights.

Instead of simply displaying charts, the platform identifies patterns that influence long-term financial wellbeing.

Examples include:

- Highest Spending Category
- Largest Expense
- Spending Frequency
- Income Consistency
- Average Daily Spending
- Savings Consistency
- Bucket Funding Progress
- Financial Discipline Indicators

These insights help users understand *why* their financial position changes over time.

---

# Financial Health Indicators

Fundivis introduces behavioral metrics that go beyond traditional budgeting.

Examples include:

## Wealth Protection Ratio

Measures how much of the user's wealth is intentionally protected.

---

## Spending Ratio

Shows the percentage of income converted into expenses.

---

## Available Cash Ratio

Measures how much money remains safely available after all protected allocations.

---

## Allocation Consistency

Tracks how consistently users protect money before spending it.

---

## Financial Momentum

Measures whether the user's financial position is improving over time.

Instead of focusing on isolated transactions, Fundivis evaluates long-term behavioral trends.

---

# Transaction Intelligence

Every transaction contributes to a larger financial story.

Users can:

- Search transactions
- Filter transactions
- Sort transactions
- View transaction history
- Inspect transaction details
- Track transaction categories
- Review financial timelines

Unlike traditional transaction lists, Fundivis places every transaction within the broader context of financial visibility.

---

# Search & Filtering

Powerful search capabilities allow users to quickly locate financial information.

Supported filters include:

- Date Range
- Transaction Type
- Category
- Bucket
- Payment Method
- Amount Range
- Income Source
- Financial State

This ensures financial records remain easy to navigate as data grows.

---

# Financial Timeline

Fundivis maintains a chronological timeline of financial activity.

Rather than presenting isolated entries, the timeline illustrates how every financial decision contributes to the user's overall financial journey.

Users can review:

- Income Events
- Expense Events
- Bucket Allocations
- Bucket Withdrawals
- Transfers
- Financial Milestones

This transforms transaction history into a story of financial progress.

---

# Notifications & Reminders

Fundivis keeps users informed without becoming intrusive.

Examples include:

- Bucket Goal Reached
- Low Available Balance
- Monthly Financial Summary Ready
- Allocation Reminder
- Weekly Visibility Report
- Unusual Spending Activity

Notifications encourage proactive financial decisions rather than reactive budgeting.

---

# Multi-User Architecture

Fundivis is designed as a scalable multi-tenant platform.

Every user's financial data remains completely isolated.

The platform provides:

- Secure Account Isolation
- Role-Based Authentication
- JWT Security
- Protected API Endpoints
- Independent Financial Dashboards
- User-Specific Buckets
- User-Specific Reports
- Secure Data Ownership

This architecture allows Fundivis to scale from individual users to enterprise-grade deployments while maintaining complete data privacy.

---

# System Architecture

Fundivis is designed using a layered architecture that separates presentation, business logic, and data access into independent, loosely coupled components.

This approach improves maintainability, scalability, testability, and long-term extensibility while ensuring that business rules remain independent of infrastructure concerns.

Rather than allowing application logic to spread across controllers or database models, Fundivis centralizes business rules within dedicated service layers, making the platform easier to evolve as new financial capabilities are introduced.

---

## High-Level Architecture

```text
                        Client Applications
         ┌──────────────────────────────────────────┐
         │                                          │
         │   Web App   │   Mobile App   │   Future APIs
         │                                          │
         └──────────────────────────────────────────┘
                           │
                           ▼
                 FastAPI REST API Layer
                           │
                           ▼
          Authentication & Authorization Layer
                           │
                           ▼
                Business Logic (Services)
                           │
                           ▼
              Repository / Database Layer
                           │
                           ▼
                 PostgreSQL Database
```

Each layer has a clearly defined responsibility.

This separation allows frontend technologies to evolve independently while preserving business logic and financial rules.

---

# Backend Architecture

The backend is built using **FastAPI** and follows modern API engineering principles suitable for production environments.

The application emphasizes:

- Clean Architecture principles
- Separation of Concerns
- RESTful API Design
- Dependency Injection
- Modular Project Structure
- Service Layer Pattern
- SQLAlchemy ORM
- Pydantic Validation
- JWT Authentication
- Alembic Database Migrations

Business rules remain completely independent of presentation logic.

This makes the platform easier to maintain, test, and extend over time.

---

# API Design Philosophy

Fundivis exposes a versioned REST API designed around predictable, resource-oriented endpoints.

Examples include:

```text
/api/v1/auth

/api/v1/users

/api/v1/income

/api/v1/expenses

/api/v1/buckets

/api/v1/transactions

/api/v1/dashboard

/api/v1/insights

/api/v1/reports
```

The API follows consistent conventions for:

- HTTP Status Codes
- Validation
- Error Handling
- Pagination
- Filtering
- Sorting
- Authentication
- Response Models

This consistency improves developer experience and simplifies frontend integration.

---

# Authentication & Authorization

Security is a first-class citizen inside Fundivis.

Authentication is implemented using industry-standard JWT access tokens.

Current authentication features include:

- User Registration
- Secure Login
- Password Hashing
- JWT Access Tokens
- Protected Endpoints
- User Session Validation
- Role-Based Authorization (planned)

Every API request is authenticated before accessing protected financial resources.

---

# Database Architecture

Fundivis uses PostgreSQL as its primary relational database.

The database schema has been designed around one guiding principle:

> **The database should represent financial truth.**

Every movement of money is persisted in a way that preserves historical accuracy while allowing the system to reconstruct a user's financial position at any point in time.

The schema emphasizes:

- Referential Integrity
- Data Consistency
- Financial Accuracy
- Multi-User Isolation
- Scalable Relationships
- Efficient Query Performance

---

# Core Domain Models

The platform revolves around several core entities.

## User

Represents an authenticated platform user.

Responsibilities include:

- Authentication
- Profile Management
- Account Ownership
- Financial Isolation

---

## Account

Represents a financial source.

Examples:

- Cash Wallet
- Checking Account
- Savings Account
- Mobile Money
- Business Account

---

## Transaction

Represents every financial movement.

Each transaction is classified into one of four movement types:

- Income
- Expense
- Allocation
- Reclassification

This ensures accurate financial reporting without misleading calculations.

---

## Bucket

Represents Protected Money.

Buckets allow users to intentionally reserve wealth for future purposes.

Examples:

- Emergency Fund
- Rent
- Tuition
- Investments
- Vacation

Unlike traditional budgeting systems, bucket allocations never reduce net worth.

---

## Category

Provides organizational structure for transactions.

Examples include:

- Food
- Transportation
- Utilities
- Entertainment
- Salary
- Business Income

---

## Dashboard Snapshot

Stores aggregated financial metrics used to generate visibility dashboards efficiently.

---

# Financial Calculation Engine

Unlike traditional finance applications, Fundivis does not rely on simplistic balance calculations.

Instead, balances are derived using business rules based on money movement types.

This ensures that:

- Allocations do not become expenses.
- Reclassifications do not become income.
- Bucket transfers preserve wealth.
- Reports remain financially accurate.

Every dashboard metric is built upon these rules.

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Language | Python 3 |
| Backend Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Authentication | JWT |
| Password Security | Passlib + BCrypt |
| Database Migrations | Alembic |
| API Documentation | Swagger / OpenAPI |
| Rate Limiting | SlowAPI |
| Environment Management | Python-dotenv |
| Testing | Pytest |
| Containerization | Docker *(planned)* |
| Background Tasks | Celery + Redis *(planned)* |
| CI/CD | GitHub Actions *(planned)* |

---

# Project Structure

```text
fundivis/
│
├── app/
│   │
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── routes/
│   │   └── middleware/
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── settings.py
│   │
│   ├── database/
│   │   ├── session.py
│   │   └── base.py
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   ├── repositories/
│   │
│   ├── services/
│   │
│   ├── utils/
│   │
│   ├── main.py
│   │
│   └── __init__.py
│
├── alembic/
├── tests/
├── docs/
├── requirements.txt
├── README.md
└── .env.example
```

The project is intentionally modular.

Every module has a single responsibility, making future features easier to introduce without impacting unrelated components.

---

# Engineering Principles

Fundivis is built around engineering practices commonly used in production software systems.

The project emphasizes:

- Clean Code
- SOLID Principles
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple)
- Separation of Concerns
- Layered Architecture
- Modular Design
- Type Safety
- Explicit Validation
- Scalable API Design
- Reusable Business Logic
- Secure Authentication
- Consistent Error Handling

These principles ensure the codebase remains maintainable as the platform grows.

---

# Performance & Scalability

Although Fundivis is currently focused on individual users, its architecture is designed with future growth in mind.

Scalability considerations include:

- Stateless REST APIs
- Database Indexing
- Efficient Query Design
- Pagination
- Lazy Loading
- Modular Services
- Background Job Support
- Horizontal Scaling Readiness

Future versions will introduce:

- Redis Caching
- Celery Workers
- Event-Driven Processing
- Queue-Based Notifications
- Real-Time Financial Updates

---

# API Documentation

FastAPI automatically generates interactive API documentation.

After starting the application, developers can access:

## Swagger UI

```text
http://localhost:8000/docs
```

## ReDoc

```text
http://localhost:8000/redoc
```

These interfaces allow developers to:

- Explore available endpoints
- Test requests
- Inspect response schemas
- Understand authentication requirements
- Validate request models

without requiring additional documentation.

---

# Why This Architecture?

Fundivis is intended to become much more than an expense tracker.

It is being architected as the foundation of a future Financial Operating System.

This means every design decision prioritizes:

- Maintainability
- Extensibility
- Financial Accuracy
- Developer Experience
- Long-Term Scalability

The current implementation lays the groundwork for future capabilities such as:

- AI Financial Coaching
- Bank Integrations
- Cash Flow Forecasting
- Financial Health Scoring
- Smart Wealth Allocation
- Multi-Currency Support
- Investment Visibility
- Open Banking APIs

Rather than requiring a complete rewrite, these capabilities can be introduced incrementally on top of the existing architecture.

---

# Getting Started

Follow the steps below to run Fundivis locally.

## Prerequisites

Before getting started, ensure the following tools are installed:

- Python 3.12+
- PostgreSQL 15+
- Git
- Virtual Environment (venv)
- Node.js *(optional for frontend development)*

---

# Clone the Repository

```bash
git clone https://github.com/codewithgabby/fundivis.git

cd fundivis
```

---

# Backend Installation

## Create a Virtual Environment

### Windows

```bash
python -m venv env

env\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv env

source env/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/fundivis

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Apply Database Migrations

```bash
alembic upgrade head
```

---

## Run the Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

# Frontend Setup

The frontend communicates entirely through REST APIs.

During development:

1. Update the API Base URL.

Example:

```javascript
const BASE_URL = "http://localhost:8000";
```

2. Launch the frontend using Live Server or any static server.

---

# API Documentation

Fundivis ships with automatically generated interactive API documentation.

## Swagger UI

```
http://localhost:8000/docs
```

## ReDoc

```
http://localhost:8000/redoc
```

Developers can:

- Test endpoints
- Inspect schemas
- Explore authentication
- Validate payloads

without leaving the browser.

---

# Security

Security is a foundational part of Fundivis rather than an afterthought.

Current security features include:

- JWT Authentication
- Password Hashing (BCrypt)
- Protected API Endpoints
- Request Validation
- User Data Isolation
- SQL Injection Protection via ORM
- Environment-Based Configuration
- CORS Protection
- Rate Limiting

Future security enhancements include:

- Refresh Tokens
- Audit Logging
- Device Sessions
- Email Verification
- Two-Factor Authentication (2FA)
- Account Activity Monitoring

---

# Deployment

Fundivis is designed for cloud-native deployment.

Recommended deployment stack:

| Component | Platform |
|------------|----------|
| Backend | Railway |
| Database | PostgreSQL |
| Frontend | Netlify |
| Storage | Cloudflare R2 *(planned)* |
| Background Jobs | Redis + Celery *(planned)* |

---

# Product Roadmap

## Version 1

- User Authentication
- Income Management
- Expense Management
- Financial Dashboard
- Transaction History
- Financial Insights
- Savings Buckets
- Multi-User Support

---

## Version 2

- Protected Wealth Engine
- Smart Bucket Recommendations
- Financial Health Score
- Weekly Financial Reports
- Cash Flow Analytics
- CSV Export
- Spending Forecasts

---

## Version 3

- AI Financial Coach
- Open Banking Integration
- Investment Visibility
- Financial Goals
- Shared Family Accounts
- Smart Notifications
- Predictive Financial Analytics

---

# Long-Term Vision

Fundivis is not being built to become another expense tracker.

The long-term vision is to create a **Financial Operating System** that helps people make better financial decisions through visibility instead of complexity.

Future capabilities include:

- Safe-to-Spend Engine
- Cash Flow Forecasting
- Behavioral Analytics
- Financial Health Index
- AI Wealth Assistant
- Investment Tracking
- Multi-Currency Support
- Open Banking APIs
- Financial Planning Workflows
- Intelligent Wealth Allocation

Our mission is simple:

> Help people understand where their money exists before they decide where it should go.

---

# Screenshots

Screenshots will be added as development progresses.

Planned previews include:

- Login
- Registration
- Dashboard
- Financial Buckets
- Money Allocation
- Insights Dashboard
- Reports
- Mobile View
- Swagger API Documentation

---

# Contributing

Contributions are welcome.

If you'd like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

Bug reports, ideas, and feature requests are always appreciated.

---

# License

This project is licensed under the MIT License.

See the LICENSE file for details.

---

# Author

## Johnson Gabriel Ohimai

Python Backend Engineer

I design scalable backend systems, REST APIs, SaaS platforms, and AI-powered applications using Python, FastAPI, PostgreSQL, and modern software architecture principles.

### Portfolio

https://gabbydev.netlify.app

### GitHub

https://github.com/codewithgabby

### LinkedIn

https://www.linkedin.com/in/johnson-gabriel-b716aa212/

### Email

j.gabriel.dev77@gmail.com

---

# Acknowledgements

Fundivis represents more than a software project.

It reflects my belief that software should solve meaningful problems while remaining elegant, maintainable, and scalable.

This project combines software engineering, product thinking, and behavioral finance into a single platform designed to improve the way people understand their money.

It also serves as a demonstration of production-ready backend engineering practices using FastAPI and PostgreSQL while laying the foundation for a future Financial Operating System.

---

If you found this project interesting, consider giving the repository a star.

Feedback, ideas, and contributions are always welcome.
