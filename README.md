**Schema of arhciteture: https://lucid.app/documents/view/b2986b32-52f2-4eb0-b249-db54e6ec796b**

# autoInvoice Project

# Tutoring Invoice Management System Documentation

## Introduction
This documentation provides an overview of the Tutoring Invoice Management System. The system is designed to manage and generate invoices for tutoring services, integrating with Google Sheets and generating PDF invoices - hopeufully streamlining the process of managing and generating invoices for invoice basedservices.

Invoices can either be done on an hourly basis or with pre-paid lesson credits.  

## Project Structure
The project consists of several Python scripts, each serving a specific function in the overall invoice management process:

### main.py (Described Separately)
Central script orchestrating the control flow of the application.

### Invoice Data Processing and Google Sheets Integration (`tutor_hours.py`)
1) Handles data centralisation on Google Sheets to central cloud database. 
2) Parses and compiles central cloud data-base to local memory (for further usage)  

### Invoice PDF Generation (`generate_invoices.py`)
-Generates detailed PDF invoices based on the processed data.
-Hourly and 'pre-paid' invoice items processed seperately. (see schema of arhciteture)

### Ancillary Scripts (`constants.py, utils.py, data_checks.py`)
For maintainability and organisation, ancillary scripts are used.

## Setup and Configuration
### Prerequisites
- Python 3.9
- Libraries: `pandas`, `gspread`, `numpy`, `reportlab`

### Google Sheets API Setup
1. Enable Google Sheets API in Google Cloud Platform.
2. Create a service account and download the JSON key file.
3. Share your Google Sheets with the service account email.

## Usage Guide
1. **Update Google Sheets Credentials**: Place your Google Sheets JSON key file in the project directory and reference it in `constants.py`.
2. **Run main.py**: This script will interact with other modules to perform tasks like data retrieval, processing, and invoice generation.

## Function Reference
Each module contains several functions, key among them are: [WIP]

### tutor_hours.py.py
- `get_master_data()`: Fetches and returns master data from a Google Sheet.
- `get_all_tutors_lesson_log_df(list_of_ut_tutors)`: Aggregates multiple tutors' lesson logs.
- `add_new_tutor_lessons_to_master(...)`: Updates the master data sheet with new lessons.

### generate_invoices.py
- `draw_static_elements(...)`: Draws static elements on the PDF.
- `create_data_table(...)`: Creates a table for the invoice data.
- `create_an_invoice_pdf(...)`: Main function to create a single PDF invoice.

## Refactoring Notes
The project is an ongoing WIP. 
-----------------------------------------------------

**Useful external links:**
How to set up google API credentials: https://mljar.com/blog/authenticate-python-google-sheets-service-account-json-credentials/#:~:text=Creating%20JSON%20file%20with%20credentials,Download%20JSON%20file%20with%20credentials

