import pandas as pd
import gspread
import numpy as np

# Import the necessary module that contains the function to generate the invoice data DataFrame
import invoice_csv_to_pdf_modular

invoice_csv_to_pdf_modular.main()
new_invoice_records_df = invoice_csv_to_pdf_modular.all_invoice_records_df

# Service account setup
sa = gspread.service_account(filename="utautoinvoicing_service_account.json")

# Open the Invoice Records Data Master Data Base Google Sheet
UT_Master_Data_Base_GS = sa.open("Master Invoice Records")
UT_Master_Invoice_records_Sheet = UT_Master_Data_Base_GS.worksheet("master")

# Load data from the Master Data Base sheet
mastersheet_data = UT_Master_Invoice_records_Sheet.get_all_values()
mastersheet_data_df = pd.DataFrame(mastersheet_data[1:], columns=mastersheet_data[0]).dropna(subset=['Permanent ID'])


def add_new_invoice_records_to_master():
    # Append new (unique) rows to the Master Data Base dataframe
    # Convert 'Invoice Number' to string for comparison
    mastersheet_data_df['Permanent ID'] = mastersheet_data_df['Permanent ID'].astype(str)
    new_invoice_records_df['Permanent ID'] = new_invoice_records_df['Permanent ID'].astype(str)

    new_rows = new_invoice_records_df[~new_invoice_records_df['Permanent ID'].isin(mastersheet_data_df['Permanent ID'])]
    updated_mastersheet_data_df = pd.concat([mastersheet_data_df, new_rows])

    # Convert the updated dataframe to a list of lists for uploading to Google Sheets
    updated_master_data_to_upload = [updated_mastersheet_data_df.columns.tolist()] + updated_mastersheet_data_df.values.tolist()

    # Clear the existing data in the Master Data Base sheet
    UT_Master_Invoice_records_Sheet.clear() #TODO DON'T CLEAR HEADERS

    # Update the Master Data Base sheet with the new data
    UT_Master_Invoice_records_Sheet.update('A1', updated_master_data_to_upload)
    print('New Hours Added')


add_new_invoice_records_to_master()
print('new invoice records added')