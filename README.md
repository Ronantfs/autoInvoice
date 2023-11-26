# autoInvoice Project

**Aims of project:
**
1) Develop an internal tool for UnderstadningTutors to manage their invoicing of parents (time for this is is main marginal cost of operations)
2) In doing so, prototype a porduct for my future Saas start up.

**File 1)'Add new tutor hours:**

Script manages and invoices tutoring lessons using Google Sheets:

1. **Setup**: Authenticates with Google Sheets using `gspread` and a service account- authentication details imported from json:
2. **Reading Sheets**: Master sheet, "UT_Master_Invoice_Data_Base", containing central repo of all past tutor hours ; "Lesson Log" sheets are live cloud google sheets that tutors log their hours into.  All google sheets converted to DFs.
4. **Updating Master Database**: Adds new lessons to the Master Data Base sheet, identifying new entries using 'Unique ID'.
5. **Invoice Processing**: Extracts invoice data, identifying unpaid invoices per student and month; for use in linked scripts (see below)

**Note!**: To update the master db, script clears existing data in the Master Data Base sheet before updating, so handle with care to avoid data loss.
**TODO** add export of master database tot an export.


**File 2) Invoice_csv_to_pdf:**

Takes invoice data - identified as unpaid - from _Add new tutors hours script_ and generates PDF invoices for tutoring services + exports invoice records for databasing

**Invoice Generation**: Processes unpaid invoices for each student, creating a detailed PDF invoice with a data table and branding elements.
**Data Processing**: Compiles invoice records into a DataFrame, then exports it as a CSV file for record-keeping.
**Execution**: The `main()` function orchestrates the process, using data from a previously run script (`add_new_tutor_hours`).


**File 3) update invoice recrds** 

Using google API, adds new invoice records from _invoice_csv_to_pdf_ script to master file on google drive , via google sheets API.

Invoice data for a given sutdent and month are generated using a 'Permanent ID


**Key external links:**
How to set up google API credentials: https://mljar.com/blog/authenticate-python-google-sheets-service-account-json-credentials/#:~:text=Creating%20JSON%20file%20with%20credentials,Download%20JSON%20file%20with%20credentials

