# Dynamic RBAC Platform

A Django-based Dynamic Role-Based Access Control (RBAC) platform with Multi-Organization support, feature-level permissions, audit logging, and REST APIs.

This project demonstrates secure access control, tenant isolation, dynamic permission management, and audit tracking using Django, Django REST Framework, PostgreSQL, and Bootstrap 5.

---

# Features

## Multi-Organization Support

* Organization-specific users and roles
* Tenant-level data isolation
* Super Admin access across organizations

## Dynamic RBAC

* Database-driven permissions
* Feature-level access control
* View, Create, Update, Delete permissions
* No hardcoded role checks

## Role Management

* Default roles:

  * Super Admin
  * Organization Admin
  * Manager
  * Employee
* Support for custom roles
* Dynamic permission assignment

## User Management

* Create and manage users
* Assign roles dynamically
* Organization-scoped user access

## Audit Logging

Tracks:

* User creation and updates
* Role changes
* Permission updates
* Organization changes

Includes:

* Who performed the action
* What was changed
* When it occurred

## Security

* Backend permission enforcement
* Permission-based UI rendering
* Direct URL access protection
* Organization-level data isolation

## REST APIs

Built using Django REST Framework (DRF).

---

# Tech Stack

### Backend

* Django 5
* Django REST Framework

### Database

* PostgreSQL

### Frontend

* Django Templates
* Bootstrap 5

### Authentication

* Django Session Authentication

---

# Project Structure

```text
Dynamic-RBAC-Platform/
│
├── accounts/           # Authentication and user management
├── organizations/      # Organization management
├── roles/              # Roles, features and permissions
├── permissions_app/    # Permission utilities and mixins
├── audit_logs/         # Audit trail services
├── dashboard/          # Dashboard views
├── api/                # DRF APIs
│
├── templates/          # Django templates
├── static/             # CSS and static assets
│
├── rbac_system/        # Django project settings
├── manage.py
├── requirements.txt
└── README.md
```

---

# Database Design

## Organization

Stores tenant information.

```text
Organization
├── name
├── description
└── timestamps
```

## Role

Represents organization-specific roles.

```text
Role
├── organization
├── name
├── description
└── is_default
```

## Feature

Represents application modules such as:

* Dashboard
* User Management
* Organization Management
* Role Management
* Audit Logs

## RoleFeaturePermission

Stores dynamic permissions.

```text
RoleFeaturePermission
├── role
├── feature
├── can_view
├── can_create
├── can_update
└── can_delete
```

## UserProfile

Links users with organizations and roles.

```text
UserProfile
├── user
├── organization
├── role
└── is_active
```

---

# Installation

## 1. Clone Repository

```bash
git clone <repository-url>
cd Dynamic-RBAC-Platform
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://username:password@localhost:5432/rbac_db
```

---

# PostgreSQL Setup

Create a database:

```sql
CREATE DATABASE rbac_db;
```

(Optional)

```sql
CREATE USER rbac_user WITH PASSWORD 'ChangeMe123!';
GRANT ALL PRIVILEGES ON DATABASE rbac_db TO rbac_user;
```

---

# Database Migration

```bash
python manage.py migrate
```

---

# Seed Initial Data

```bash
python manage.py seed_data
```

This command creates:

* Organizations
* Features
* Default Roles
* Permission Mappings
* Sample Users

---

# Run Application

```bash
python manage.py runserver
```

Application URL:

```text
http://127.0.0.1:8000/
```

Admin Panel:

```text
http://127.0.0.1:8000/admin/
```

API Root:

```text
http://127.0.0.1:8000/api/
```

---

# Default Credentials

## Super Admin

```text
Username: superadmin
Password: SuperAdmin123!
```

## Organization Admin

```text
Username: orgadmin
Password: OrgAdmin123!
```

## Manager

```text
Username: manager
Password: Manager123!
```

## Employee

```text
Username: employee
Password: Employee123!
```

---

# RBAC Workflow

1. User logs in.
2. User is associated with:

   * Organization
   * Role
3. Permissions are resolved dynamically from the database.
4. Sidebar and UI elements are rendered based on permissions.
5. Backend endpoints validate permissions before granting access.
6. Audit logs record permission-sensitive actions.

---

# API Endpoints

### Authentication

```text
/accounts/login/
/accounts/logout/
```

### Users

```text
/accounts/users/
/accounts/users/create/
/accounts/users/<id>/edit/
```

### Organizations

```text
/organizations/
```

### Roles & Permissions

```text
/roles/
/roles/<id>/permissions/
```

### Audit Logs

```text
/audit-logs/
```

### API

```text
/api/
```

---

# Security Features

* Multi-tenant organization isolation
* Role-based authorization
* Feature-level permissions
* Backend permission enforcement
* Audit trail logging
* Protected CRUD operations

---

# Screenshots

Add screenshots of:

* Dashboard
* User Management
* Role Management
* Permission Management
* Audit Logs

---

# Future Improvements

* JWT Authentication
* Docker Deployment
* Role Templates
* Advanced Reporting
* Activity Analytics
* Email Notifications

---