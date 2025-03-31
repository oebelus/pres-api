# Prescription Management System

A Django-based web application for physicians to manage patient prescriptions, medications, and medical records efficiently.

## Features

- **Physician Authentication**: Secure login, registration, and profile management.
- **Patient Management**: CRUD operations for patient records.
- **Prescription Workflow**:
  - Create prescriptions with multiple medications
  - Dynamic medication search using Select2
  - Dosage instructions and duration tracking
- **Medication Database**: Integrated with [medicament.ma](https://medicament.ma) data.
- **Responsive UI**: Bootstrap 5 templates for all devices.

## Tech Stack

- **Backend**: Django 5.1, Django REST Framework
- **Frontend**: HTML5, Bootstrap 5, jQuery, Select2
- **Database**: SQLite
- **APIs**: RESTful endpoints for mobile/third-party integration

## API Endpoints

| Endpoint               | Method     | Description                     |
|------------------------|------------|---------------------------------|
| `/api/login/`          | POST       | Physician login                 |
| `/api/patients/`       | GET/POST   | List all patients or create new |
| `/api/medications/`    | GET        | List all medications            |
| `/api/prescriptions/`  | POST       | Create new prescription         |

## Next Steps

- Import full medication data
- Implement PDF prescription generation
