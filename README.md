# Fundivis

> **A Behavioral Financial Visibility Platform built to help people understand where their money is—not just where it went.**

Fundivis is a modern financial visibility platform designed to help individuals develop healthier financial habits through awareness, behavioral insights, and intentional money management.

Unlike traditional budgeting applications that primarily focus on recording transactions, Fundivis helps users understand the current state of their finances by providing meaningful insights into spending behavior, savings progress, financial discipline, and overall financial health.

Built with Python, FastAPI, PostgreSQL, SQLAlchemy, and modern web technologies, Fundivis demonstrates production-ready backend engineering principles while introducing a behavior-first approach to personal finance.

---

# Project Overview

Fundivis was created to solve a problem that many existing personal finance applications fail to address.

Most finance applications answer only one question:

> **"Where did my money go?"**

Fundivis answers a much more important question:

> **"Where is my money today, and is my financial behavior improving?"**

Instead of functioning as a digital expense tracker, Fundivis serves as a financial awareness platform that helps users understand how their daily financial decisions affect their long-term financial wellbeing.

The platform combines transaction management with behavioral analytics to encourage consistent financial discipline rather than occasional budgeting.

---

# The Problem

Most personal finance applications focus heavily on bookkeeping.

Users can record income and expenses, categorize transactions, and generate reports, but these applications often fail to provide meaningful insight into financial behavior.

As a result, users frequently experience problems such as:

* Spending without understanding financial patterns.
* Tracking transactions without improving financial habits.
* Focusing on historical data instead of present financial position.
* Saving inconsistently without measurable progress.
* Difficulty understanding whether their financial discipline is improving over time.
* Information overload without actionable guidance.

Many budgeting applications become digital notebooks instead of decision-making tools.

Fundivis was designed to change that.

---

# Why Fundivis Exists

Fundivis was built on the belief that financial awareness should come before financial planning.

Rather than encouraging users to simply record transactions, the platform helps them develop a continuous understanding of their financial behavior through meaningful indicators, behavioral trends, and actionable insights.

The objective is not simply to organize financial records.

The objective is to help people make better financial decisions every day.

---

# Product Philosophy

Fundivis follows four fundamental principles.

## 1. Visibility Creates Awareness

People cannot improve what they cannot clearly see.

Fundivis transforms financial information into understandable metrics that reveal spending habits, saving behavior, and financial progress.

---

## 2. Awareness Improves Decision Making

Once users understand their financial patterns, they become more intentional about future financial decisions.

The platform encourages informed choices rather than reactive spending.

---

## 3. Discipline Builds Financial Freedom

Long-term financial success is rarely the result of isolated budgeting sessions.

Instead, it comes from consistent daily financial behavior.

Fundivis measures and encourages that consistency.

---

## 4. Simplicity Increases Adoption

Financial software should reduce anxiety rather than create it.

Every dashboard, report, and insight inside Fundivis is designed to simplify complex financial information into practical guidance that users can immediately understand.

---

# Core Objectives

Fundivis was designed to help users:

* Understand where their money currently exists.
* Monitor income and expenses.
* Track financial progress over time.
* Build consistent saving habits.
* Reduce unnecessary spending.
* Improve financial awareness.
* Make informed financial decisions.
* Develop long-term financial discipline.

Rather than replacing financial advisors or accounting software, Fundivis complements them by helping individuals develop healthier financial behaviors through continuous visibility.

---

---

# Platform Features

Fundivis is organized into several interconnected modules that work together to provide a complete financial visibility experience.

Rather than treating every financial activity as an isolated transaction, each module contributes to a broader understanding of the user's financial behavior.

---

# Authentication & User Management

The platform provides secure account management using industry-standard authentication practices.

### Features

* User registration
* Secure login
* JWT authentication
* Password hashing
* Protected API endpoints
* User profile management
* Multi-user account isolation
* Session validation

---

# Income Management

Income management allows users to record and monitor every source of income while building a complete picture of their earning patterns.

### Features

* Record multiple income sources
* Categorize income
* Payment method tracking
* Income history
* Pagination
* Search and filtering
* Real-time updates

---

# Expense Management

Expense tracking goes beyond simple transaction recording by encouraging users to understand where money is being spent and how spending habits evolve over time.

### Features

* Record expenses
* Expense categorization
* Essential vs Non-Essential spending
* Payment method tracking
* Transaction history
* Pagination
* Search and filtering
* Real-time updates

---

# Financial Dashboard

The dashboard provides a consolidated overview of the user's financial position.

Instead of presenting raw numbers, it transforms financial data into meaningful indicators that support better financial decisions.

### Daily Summary

* Total income
* Total expenses
* Net balance
* Daily financial activity

### Monthly Summary

* Monthly income
* Monthly expenses
* Total savings
* Savings rate
* Financial performance

---

# Savings Trend Analysis

Fundivis continuously compares current financial performance with previous periods to help users understand whether they are improving financially.

The Savings Trend module displays:

* Current month savings
* Previous month savings
* Savings growth
* Savings decline
* Monthly comparison
* Financial trend analysis

This allows users to identify progress instead of viewing isolated monthly reports.

---

# Financial Insights Engine

The Financial Insights Engine transforms financial data into actionable behavioral insights.

Instead of displaying only transaction records, Fundivis identifies spending patterns that influence long-term financial health.

Examples include:

* Highest spending category
* Largest individual expense
* Average daily spending
* Essential spending ratio
* Non-essential spending ratio
* Monthly financial behavior summary

These insights help users understand why their financial position changes over time.

---

# Financial Consistency Tracking

One of the strongest indicators of financial improvement is consistency.

Fundivis rewards consistent financial tracking through a streak system that encourages users to maintain healthy financial habits.

The platform tracks:

* Current tracking streak
* Longest tracking streak
* Today's financial activity
* Overall consistency

This feature promotes long-term engagement without relying on unnecessary gamification.

---

# Transaction History

Users can easily review historical financial records through a searchable transaction history.

### Income History

* Chronological listing
* Pagination
* Search support
* Source filtering

### Expense History

* Chronological listing
* Pagination
* Category filtering
* Search support

The transaction history is designed to remain fast and organized even as financial records grow.

---

# Responsive User Experience

Fundivis is designed to deliver a consistent experience across multiple devices.

Supported platforms include:

* Desktop
* Laptop
* Tablet
* Mobile devices

Responsive features include:

* Adaptive layouts
* Responsive navigation
* Mobile sidebar
* Flexible dashboards
* Responsive transaction tables
* Optimized cards and charts

---

# Security

Security is treated as a core platform requirement rather than an optional feature.

Fundivis implements multiple layers of protection including:

* JWT Authentication
* Secure password hashing
* Protected routes
* Multi-user data isolation
* Rate limiting
* Request validation
* CORS protection
* Environment variable configuration

These measures help ensure that each user's financial information remains secure and isolated from every other account.

---

---

# System Architecture

Fundivis follows a layered architecture that separates presentation, business logic, and data access into independent components.

This approach improves maintainability, scalability, and long-term extensibility while keeping the codebase organized and easy to understand.

```text
                        Client Browser
                               │
                               ▼
                   HTML • CSS • JavaScript
                               │
                               ▼
                     FastAPI REST API Layer
                               │
                               ▼
              Authentication & Authorization
                               │
                               ▼
                  Business Logic (Services)
                               │
                               ▼
              Database Layer (SQLAlchemy ORM)
                               │
                               ▼
                      PostgreSQL Database
```

Each layer has a clearly defined responsibility, reducing coupling and making the application easier to extend as new financial modules are introduced.

---

# Backend Architecture

The backend is built using FastAPI and follows modern REST API development practices.

The architecture emphasizes:

* Modular project organization
* Separation of concerns
* Service-oriented business logic
* Database abstraction through SQLAlchemy ORM
* Secure authentication using JWT
* Database migrations using Alembic
* Request validation using Pydantic
* RESTful API design principles

The backend exposes a clean API that can support multiple frontend clients, including web and future mobile applications.

---

# Frontend Architecture

The frontend is intentionally lightweight and communicates with the backend exclusively through REST APIs.

The application is built using:

* HTML5
* Tailwind CSS
* Vanilla JavaScript (ES Modules)

The frontend architecture focuses on:

* Component-based organization
* API-driven rendering
* Responsive layouts
* Modular JavaScript files
* Separation of presentation from business logic

All financial calculations and business rules remain on the backend to ensure consistency and security.

---

# Technology Stack

| Layer                | Technology                      |
| -------------------- | ------------------------------- |
| Programming Language | Python                          |
| Backend Framework    | FastAPI                         |
| ORM                  | SQLAlchemy                      |
| Database             | PostgreSQL                      |
| Database Migrations  | Alembic                         |
| Authentication       | JWT                             |
| Password Security    | Password Hashing                |
| Rate Limiting        | SlowAPI                         |
| API Documentation    | Swagger / OpenAPI               |
| Frontend             | HTML5                           |
| Styling              | Tailwind CSS                    |
| JavaScript           | Vanilla JavaScript (ES Modules) |
| Deployment           | Railway                         |
| Frontend Hosting     | Netlify                         |
| Version Control      | Git & GitHub                    |

---

# Project Structure

## Backend

```text
fundivis/
│
├── app/
│   ├── core/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── database.py
│   └── main.py
│
├── alembic/
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

## Frontend

```text
fundivis-frontend/
│
├── assets/
│   ├── css/
│   └── js/
│       ├── api.js
│       ├── auth.js
│       ├── dashboard.js
│       ├── expense.js
│       ├── income.js
│       ├── insights.js
│       ├── savingsTrend.js
│       ├── streaks.js
│       ├── summary.js
│       └── transactions.js
│
├── index.html
├── login.html
├── register.html
└── dashboard.html
```

---

# Database Design

Fundivis uses a relational database model designed to ensure data integrity while supporting multiple independent users.

The database architecture emphasizes:

* Multi-user account isolation
* Normalized relational tables
* Referential integrity
* Efficient querying
* Scalable financial record storage

Core entities include:

* User
* Income
* Expense
* Category
* Payment Method
* Financial Summary
* Tracking Streak

Relationships are modeled using SQLAlchemy ORM, making the application easier to maintain while reducing database complexity.

---

# Engineering Principles

Fundivis was developed with the following software engineering principles in mind:

* Clean and readable code
* Separation of concerns
* RESTful API design
* Secure authentication
* Scalable architecture
* Reusable business logic
* Modular application structure
* Consistent validation
* Maintainable codebase
* Extensible platform design

These principles allow new financial modules to be added with minimal impact on existing functionality.

---

---

# Getting Started

Follow the steps below to set up Fundivis locally.

## Clone the Repository

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
DATABASE_URL=postgresql://username:password@localhost:5432/fundivis

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

## Start the Backend Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

# Frontend Setup

The frontend can be served using any static web server.

For local development, you can use the VS Code Live Server extension.

Update the API base URL inside your frontend configuration to point to your backend server.

Example:

```javascript
const BASE_URL = "http://127.0.0.1:8000";
```

For production deployments, update the base URL to your Railway deployment.

---

# API Documentation

Fundivis provides automatically generated API documentation through FastAPI.

After starting the backend server, visit:

## Swagger UI

```
http://127.0.0.1:8000/docs
```

## ReDoc

```
http://127.0.0.1:8000/redoc
```

These interactive interfaces allow developers to explore every available endpoint, inspect request and response models, and test the API directly from the browser.

---

# Deployment

Fundivis is deployed using modern cloud platforms.

## Frontend

Netlify

https://fundivis.netlify.app

---

# Security

Security has been incorporated throughout the platform to protect user accounts and financial information.

Current security measures include:

* JWT Authentication
* Password Hashing
* Protected API Endpoints
* Multi-user Data Isolation
* Request Validation
* Rate Limiting
* CORS Protection
* Environment-based Configuration

Future releases will introduce additional security improvements including refresh tokens, audit logging, and advanced monitoring.

---

# Product Roadmap

## Version 1.0

Completed features include:

* User Authentication
* Income Tracking
* Expense Tracking
* Daily Financial Summary
* Monthly Financial Summary
* Savings Tracking
* Savings Trends
* Financial Insights
* Tracking Streaks
* Responsive Dashboard
* Transaction History
* Multi-user Architecture

---

## Version 2.0

Planned improvements include:

* Financial Status Card
* Spending Goals
* Weekly Financial Reports
* CSV Export
* Smart Notifications
* Charts and Advanced Visualizations
* Improved Mobile Experience
* AI Spending Insights

---

## Long-Term Vision

Fundivis is evolving beyond a finance tracker into a complete Behavioral Financial Visibility Platform.

Future capabilities include:

* Safe-to-Spend Engine
* Protected Wealth Buckets
* Committed Bills
* Income Intelligence
* Financial Health Score
* Pre-Spend Checker
* Behavioral Analytics Dashboard
* Multi-Currency Support
* Bank Integrations
* AI Financial Assistant

---

# Screenshots

The following screenshots will be added as the platform continues to evolve:

* Login Page
* Registration Page
* Financial Dashboard
* Income Management
* Expense Management
* Financial Insights
* Savings Trends
* Mobile Dashboard
* Swagger Documentation

---

# Contributing

Contributions are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

Bug reports, feature requests, and suggestions are always appreciated.

---

# License

This project is licensed under the MIT License.

See the LICENSE file for additional information.

---

# Author

## Johnson Gabriel Ohimai

Python Backend Engineer

I build scalable backend systems, REST APIs, SaaS platforms, and AI-powered applications using Python, FastAPI, and PostgreSQL.

**Portfolio**

https://gabbydev.netlify.app

**GitHub**

https://github.com/codewithgabby

**LinkedIn**

https://www.linkedin.com/in/johnson-gabriel-b716aa212/

**Email**

[j.gabriel.dev77@gmail.com](mailto:j.gabriel.dev77@gmail.com)

---

# Acknowledgements

Fundivis was designed and developed as part of my journey toward becoming a world-class Backend Engineer.

The project reflects my passion for building software that solves real-world problems while combining thoughtful product design with scalable backend architecture.

It also serves as a foundation for future AI-powered financial tools that promote financial awareness, discipline, and long-term decision-making.

---

**If you find this project interesting or useful, consider starring the repository. Feedback, suggestions, and contributions are always welcome.**

