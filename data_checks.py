import gspread
from gspread_dataframe import get_as_dataframe

import pandas as pd
import numpy as np
import constants

# Service account setup
sa = gspread.service_account(filename=constants.google_sa_json)


def check_invoice_master_data():
    '''function that checks the invoice master database for any issues'''
    UT_Master_Data_Base_GS = sa.open("UT_Master_Invoice_Data_Base_Doc")
    UT_Master_Data_Invoice_Sheet = UT_Master_Data_Base_GS.worksheet("Invoice Master Database")

    invoice_mastersheet_data = UT_Master_Data_Invoice_Sheet.get_all_values()
    invoice_mastersheet_data_df = pd.DataFrame(invoice_mastersheet_data[1:],
                                               columns=invoice_mastersheet_data[0]).dropna(subset=['Student Name'])

    #check for missing refence values:

    #if any value is '#REF!' then print error and row number
    if invoice_mastersheet_data_df.isin(['#REF!']).any().any():

        print('ERROR: #REF! found in Invoice Master Database')
        print('please check Master Sheet on Google Sheets for errors')
        print("To fix #REF errors, either delete the rows on Google Sheet and re-run the script from 1")
        print("or, if it a single cell, look at MAster Data Base Sheet and make sure data is correct")
        print("If need be, look at the individual tutor sheets and make sure data was entered as required")

        print(invoice_mastersheet_data_df[invoice_mastersheet_data_df.isin(['#REF!']).any(axis=1)])
        return False

    if invoice_mastersheet_data_df.isin(['#N/A']).any().any():

            print('ERROR: #N/A found in Invoice Master Database')
            print('please check Master Sheet on Google Sheets for errors')
            print("To fix #N/A errors, either delete the rows on Google Sheet and re-run the script from 1")
            print("or, if it a single cell, look at MAster Data Base Sheet and make sure data is correct")
            print("If need be, look at the individual tutor sheets and make sure data was entered as required")

            print(invoice_mastersheet_data_df[invoice_mastersheet_data_df.isin(['#N/A']).any(axis=1)])
            return False

    # Check for NaN, None, and blank strings in master df columns
    def check_missing_values_in_column(df, column_name):
        """Check for NaN, None, and blank strings in a specified column of a DataFrame.

        Args:
        df (pd.DataFrame): The DataFrame to check.
        column_name (str): The name of the column to check.

        Returns:
        bool: True if no missing values are found, False otherwise.
        """
        missing_values_mask = df[column_name].isnull() | (df[column_name] == '')
        if missing_values_mask.any():
            print(f'\nERROR: Missing {column_name} value found in Invoice Master Database')
            print('Please check Master Sheet on Google Sheets for errors')
            return False
        return True

    if not check_missing_values_in_column(invoice_mastersheet_data_df, 'Lesson Length (Hours)'):
        return False

    if not check_missing_values_in_column(invoice_mastersheet_data_df, 'Invoice Rate'):
        return False

    #Tutor_Student column check:
    if not check_missing_values_in_column(invoice_mastersheet_data_df, 'Tutor_Student'):
        return False

    else:
        return True

def check_student_tutor_names_unique():
    UT_Master_Data_Base_GS = sa.open("UT_Master_Invoice_Data_Base_Doc")
    UT_Parent_contract_Sheet = UT_Master_Data_Base_GS.worksheet("Tutor-UT-Parent Contracts")

    parent_contract_data_df = get_as_dataframe(UT_Parent_contract_Sheet, evaluate_formulas=True)

    parent_contract_data_df = parent_contract_data_df.dropna(subset=['Tutor'])

    if not parent_contract_data_df["Tutor_Student"].is_unique:
        print("Values in the column Tutor_Student are not unique- this will cause processing issues for PDFs; please correct")
        return False
    return True






if __name__ == '__main__':
    print('please run via main.py')