import pandas as pd

list_of_ut_tutors = [
    'Aarif',
    'Danish',
    'Finn',
'Gabba',
'Misc',
'Nikhil',
    'Ronan',
    'Will',
    'Louis'
]

google_sa_json = "utautoinvoicing_service_account.json"

INVOICES_FOLDER_PATH = r'C:\Repositories\code_repos\UT\autoInvoice\invoices'
LOGO_PATH = r"C:\Repositories\code_repos\UT\autoinvoice\static\logo sbg.png"


#invoice_records_csv_file_path = r'C:\Repositories\code_repos\UT\autoinvoice\invoice_records_archive'



#TODO reimplemnt this
invoice_records = pd.DataFrame(
        columns=['Invoice Number', 'Tutor', 'Student', 'Amount', 'Number of Hours', 'Date Created', 'Status',
                 'Lesson Date', 'Invoice Path','Permanent ID'])

'''
total_hours = month_df['Duration (Hours)'].sum()
        invoice_month = month_df['Lesson Date'].iloc[0]
        invoice_path = os.path.join(INVOICES_FOLDER_PATH, f"{invoice_name}.pdf")

invoice_record = {
            'Invoice Number': invoice_number,
            'Tutor': tutor,
            'Student': student,
            'Amount': total_fee,
            'Number of Hours': total_hours,
            'Date Created': datetime.now().strftime("%Y-%m-%d"),
            'Status': 'Unpaid',
            'Lesson Date': month_df['Lesson Date'].min(),
            'Invoice Path': '',
            'Permanent ID': str(invoice_month) + student
        }'''