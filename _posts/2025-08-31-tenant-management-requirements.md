---
title: "Landlord-Tenant Management System: Requirements and Objectives"
date: 2025-08-31
categories: [Learning, Requirements, Analysis]
tags: [requirements, objectives, user-stories, tenant-management, property-management]
content_type: "requirements"
learning_focus: ["requirements-analysis", "project-planning"]
difficulty: "beginner"
# Evolutionary Project Fields
project: "Tenant Management"
project_type: "evolutionary"
evolution: "Foundation: Requirements & Analysis"
evolution_number: 0
evolution_focus: "Requirements Analysis"
header:
  overlay_image: /assets/images/headers/requirements-blueprint.png
  overlay_filter: 0.5
  teaser: /assets/images/headers/requirements-blueprint.png
---

Today I'm documenting the requirements for a **Landlord-Tenant Management System** - a specialized application designed for individual landlords who manage their own properties and handle all aspects of tenant payments including rent, utilities, and maintenance.

This isn't your typical enterprise property management system. Instead, it's a practical tool for landlords who want to track their properties, tenants, and financial transactions all in one place.


## What We Plan to Create

A web-based landlord-tenant management application that allows individual landlords to:

- **Manage Properties**: Track all owned properties with complete CRUD operations
- **Manage Tenants**: Maintain tenant information and link them to specific properties
- **Track Transactions**: Record all financial transactions related to properties and tenants
- **View Financial Summary**: Get real-time payment status showing positive or negative balances

The application focuses on simplicity and clarity - making it easy for landlords to see the complete financial picture of their properties and tenant relationships at a glance.

## Objectives

### Primary Goals

1. **Centralized Property Management**
   - Single place to manage all property information
   - Easy property creation, updates, and tracking
   - Quick overview of all owned properties

2. **Tenant Relationship Tracking**
   - Maintain comprehensive tenant records
   - Link tenants to their respective properties
   - Track tenant contract details and dates

3. **Comprehensive Financial Tracking**
   - Record all types of transactions (rent, utilities, maintenance, etc.)
   - Track both expenses and payments
   - Automatic calculation of current balances

4. **Clear Financial Visibility**
   - View transaction history at tenant level
   - View transaction history at property level
   - See current account status (positive/negative balance)
   - Identify who owes money or has credit

5. **User-Friendly Interface**
   - Paginated views for easy navigation
   - Simple forms for data entry
   - Responsive design for mobile and desktop access

### Technical Goals

- Build a maintainable single-file application (initial version)
- Use modern web technologies (Flask, React)
- Provide RESTful API for future extensibility
- Store data reliably using SQLite
- Support CSV/Excel exports for reporting

## User Stories

### Property Management

**As a landlord**, I want to:

- ✅ **Add new properties** so I can track all my rental units
  - *Acceptance Criteria*: Form to enter property details (address, type, description)
  - *Acceptance Criteria*: Property appears in the properties list immediately

- ✅ **View all my properties** so I can see my complete portfolio
  - *Acceptance Criteria*: Paginated list showing all properties
  - *Acceptance Criteria*: Each property shows key information at a glance

- ✅ **Edit property details** when information changes
  - *Acceptance Criteria*: Can update any property field
  - *Acceptance Criteria*: Changes are saved and reflected immediately

- ✅ **Delete properties** that are no longer in my portfolio
  - *Acceptance Criteria*: Can remove properties from the system
  - *Acceptance Criteria*: Deletion is confirmed to prevent accidents

### Tenant Management

**As a landlord**, I want to:

- ✅ **Add new tenants** with their complete information
  - *Acceptance Criteria*: Form to enter tenant details (name, contact, contract dates)
  - *Acceptance Criteria*: Link tenant to a specific property
  - *Acceptance Criteria*: Store rent amount and security deposit

- ✅ **View all tenants** across all my properties
  - *Acceptance Criteria*: Paginated list of all tenants
  - *Acceptance Criteria*: See which property each tenant is linked to
  - *Acceptance Criteria*: Quick access to tenant details

- ✅ **Edit tenant information** when details change
  - *Acceptance Criteria*: Update tenant contact information
  - *Acceptance Criteria*: Modify rent amount or contract dates
  - *Acceptance Criteria*: Change property assignment if tenant moves

- ✅ **View tenant transaction summary** to see their payment status
  - *Acceptance Criteria*: See all transactions for a specific tenant
  - *Acceptance Criteria*: View current balance (positive or negative)
  - *Acceptance Criteria*: Identify overdue payments quickly

- ✅ **Delete tenant records** when they move out (after contract ends)
  - *Acceptance Criteria*: Remove tenant from the system
  - *Acceptance Criteria*: Confirmation required to prevent accidental deletion

### Transaction Management

**As a landlord**, I want to:

- ✅ **Record rent payments** when tenants pay
  - *Acceptance Criteria*: Enter payment amount, date, and remarks
  - *Acceptance Criteria*: Link payment to tenant and property
  - *Acceptance Criteria*: Payment is counted as positive in balance

- ✅ **Record expenses** for utilities, maintenance, and repairs
  - *Acceptance Criteria*: Enter expense amount, date, type, and remarks
  - *Acceptance Criteria*: Link expense to tenant and property
  - *Acceptance Criteria*: Expense is counted as negative in balance

- ✅ **View all transactions** in chronological order
  - *Acceptance Criteria*: Paginated transaction list
  - *Acceptance Criteria*: See transaction type, amount, date, and remarks
  - *Acceptance Criteria*: Identify associated tenant and property

- ✅ **Edit transactions** to correct errors
  - *Acceptance Criteria*: Modify any transaction field
  - *Acceptance Criteria*: Updated amounts reflect in balance calculations

- ✅ **Delete incorrect transactions**
  - *Acceptance Criteria*: Remove transactions from the system
  - *Acceptance Criteria*: Balance recalculates automatically

### Financial Summary

**As a landlord**, I want to:

- ✅ **View property-level transaction summary** to see property profitability
  - *Acceptance Criteria*: Filter transactions by property
  - *Acceptance Criteria*: See all income and expenses for the property
  - *Acceptance Criteria*: View net balance (positive/negative)

- ✅ **View tenant-level transaction summary** to track individual accounts
  - *Acceptance Criteria*: Filter transactions by tenant
  - *Acceptance Criteria*: See all payments and charges
  - *Acceptance Criteria*: View current account status

- ✅ **Identify negative balances** to know who owes money
  - *Acceptance Criteria*: Negative balance clearly indicates debt
  - *Acceptance Criteria*: Easy to identify tenants with outstanding payments

- ✅ **Identify positive balances** to track prepayments or credits
  - *Acceptance Criteria*: Positive balance shows credit/advance payment
  - *Acceptance Criteria*: Clear visibility of overpayments

### System Features

**As a landlord**, I want to:

- ✅ **Navigate easily between sections** (Properties, Tenants, Transactions)
  - *Acceptance Criteria*: Clear navigation menu
  - *Acceptance Criteria*: Quick access to all main features

- ✅ **View data in manageable chunks** using pagination
  - *Acceptance Criteria*: All lists show 10 items per page
  - *Acceptance Criteria*: Easy navigation between pages

- ✅ **Export data** for record-keeping and tax purposes
  - *Acceptance Criteria*: Download CSV/Excel reports
  - *Acceptance Criteria*: Export includes all relevant data

## Key Takeaways

### Core Requirements Summary

1. **Three Main Entities**: Properties, Tenants, and Transactions
2. **CRUD Operations**: Complete create, read, update, delete for all entities
3. **Relationship Tracking**: Link tenants to properties, transactions to both
4. **Financial Calculations**: Automatic balance calculation (payments - expenses)
5. **User Experience**: Paginated views, clear navigation, responsive design

### What Makes This Different

Unlike standard enterprise property management systems, this application is designed specifically for:

- **Individual landlords** managing their own properties
- **Direct payment management** where landlord handles all bills
- **Simple transaction tracking** without complex accounting features
- **Clear financial visibility** focusing on current payment status
- **Lightweight deployment** as a single-file or modular application

### Success Metrics

The application is successful when a landlord can:

- Add a new property in under 1 minute
- Link a tenant to a property effortlessly
- Record a transaction in seconds
- View complete financial status instantly
- Identify payment issues immediately

### Next Steps

With these requirements defined, the next phases include:

1. **Database Design**: Define schema for properties, tenants, and transactions
2. **API Design**: Create RESTful endpoints for all operations
3. **UI Development**: Build responsive forms and lists
4. **Financial Logic**: Implement balance calculation algorithms
5. **Testing**: Validate all CRUD operations and calculations

---

This requirements document serves as the foundation for building the Landlord-Tenant Management System. It focuses on simplicity, clarity, and practical utility for individual landlords managing their rental properties.

*Want to see how these requirements evolved into a working application? Check out the [Single-File Implementation](/learning/full-stack-development/python/tenant-management-app-singlefile/) and [Modular Architecture](/learning/architecture/refactoring/tenant-management-modular-monolith/) posts!*
