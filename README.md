# Dynamic RBAC Platform

A complete Django-based Dynamic Role-Based Access Control (RBAC) platform with multi-organization support, feature-level permissions, tenant data isolation, audit logging, and REST APIs.

Built with Django 5, Django REST Framework, PostgreSQL, and Bootstrap 5, this project demonstrates a practical, database-driven RBAC architecture for enterprise-style applications.

---

## Key Features

- Multi-organization tenancy with tenant-scoped users, roles, and permissions
- Dynamic role and feature permission management
- Fine-grained View/Create/Update/Delete permission flags
- Audit trail for user, role, permission, and organization changes
- Permission-aware UI rendering for dashboards and admin panels
- REST API endpoints for roles, features, permissions, and audit logs
- Backend enforcement of organization scoping and permission checks

---

## Architecture Overview

This project is organized into Django apps and supporting directories that keep tenancy, permissions, audit trails, and UI rendering separated.

### Project Directory

```text
Dynamic-RBAC-Platform/
│
├── accounts/           # Authentication and user management
├── organizations/      # Organization management
├── roles/              # Roles, features and permissions
├── permissions_app/    # Permission utilities and mixins
├── audit_logs/         # Audit trail services
├── dashboard/          # Dashboard views
├── api/                # REST APIs
│
├── templates/          # Django templates
├── static/             # CSS and static assets
│
├── rbac_system/        # Django project settings
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Data Model

### Organization
Tenant entity that isolates users, roles, and permissions.

### Role
Organization-scoped role with a name, description, and optional defaults.

### Feature
Represents a functional area such as Dashboard, User Management, Role Management, or Audit Logs.

### RoleFeaturePermission
Maps each role to features and stores boolean permissions for:
- `can_view`
- `can_create`
- `can_update`
- `can_delete`

### UserProfile
Ties Django users to an organization and a role.

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
git checkout main
cd Dynamic-RBAC-Platform
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root with the following values:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DJANGO_ALLOWED_HOSTS=example.com
DATABASE_URL=postgres://username:password@db-host:5432/rbac_db
```

If you prefer SQLite for local development, update `DATABASE_URL` appropriately.

---

## PostgreSQL Setup

Create the database and optional user:

```sql
CREATE DATABASE rbac_db;
CREATE USER rbac_user WITH PASSWORD 'ChangeMe123!';
GRANT ALL PRIVILEGES ON DATABASE rbac_db TO rbac_user;
```

Then ensure `.env` points to the created database.

---

## Run Migrations

```bash
python manage.py migrate
```

---

## Seed Initial Data

```bash
python manage.py seed_data
```

This command typically creates:

- organizations
- features
- default roles
- initial permission mappings
- sample users

---

## Run the Project

```bash
python manage.py runserver
```

---

## Useful Commands

- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py seed_data`
- `python manage.py check`

---

## Notes

- The application enforces permission checks both at the view layer and in the template UI.
- Organization-scoped queries prevent users from accessing data outside their tenant.
- Audit logging captures who changed what and when, preserving a trace for admin actions.

---

## License

This repository is provided as-is for demonstration and learning purposes.

---

## Contact

For questions or improvements, edit the repository documentation or open an issue in the source repository.

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
