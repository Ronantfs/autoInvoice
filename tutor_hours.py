import gspread
import pandas as pd
import numpy as np
import constants


# Service account setup
sa = gspread.service_account(filename=constants.google_sa_json)
list_of_ut_tutors = constants.list_of_ut_tutors

def get_master_data():
    # Open the Master Data Base Google Sheet
    UT_Master_Data_Base_GS = sa.open("UT_Master_Invoice_Data_Base")
    UT_Master_Data_Base_Sheet = UT_Master_Data_Base_GS.worksheet("Master Data Base")

    # Load data from the Master Data Base sheet
    mastersheet_data = UT_Master_Data_Base_Sheet.get_all_values()
    mastersheet_data_df = pd.DataFrame(mastersheet_data[1:], columns=mastersheet_data[0]).dropna(subset=['Student Name'])

    return (mastersheet_data_df, UT_Master_Data_Base_Sheet)

# Open the Tutor Log Test Google Sheet
def get_all_tutors_lesson_log_df(list_of_ut_tutors):
    '''function that gets all tutors lesson logs and returns as single df'''
    # Initialize an empty dataframe
    all_tutors_lesson_log_dfs_list = []

    #setup service account
    for tutor in list_of_ut_tutors:
        print(f'getting {tutor} hours...')
        # Get tutor lesson log sheet and add to list
        file_name = f'{tutor} Lesson Log'
        tutorLogTestSheet = sa.open(file_name)
        wks = tutorLogTestSheet.worksheet("Lesson Log")
        log_data = wks.get_all_values()
        log_data_df = pd.DataFrame(log_data[1:], columns=log_data[0])
        log_data_df['Student Name'].replace('', pd.NA, inplace=True)
        log_data_df = log_data_df.dropna(subset=['Student Name'])
        all_tutors_lesson_log_dfs_list.append(log_data_df)

    # Concatenate all dataframes in the list
    all_tutors_lesson_log_df = pd.concat(all_tutors_lesson_log_dfs_list, ignore_index=True)
    all_tutors_lesson_log_df.reset_index(drop=True, inplace=True)

    return all_tutors_lesson_log_df

def add_new_tutor_lessons_to_master(mastersheet_data_df, all_tutors_lesson_log_df, UT_Master_Data_Base_Sheet):
    # Append new (unique) rows to the Master Data Base dataframe
    # Convert 'Unique ID' to string for comparison (if necessary)

    mastersheet_data_df['Unique ID'] = mastersheet_data_df['Unique ID'].astype(str)
    all_tutors_lesson_log_df['Unique ID'] = all_tutors_lesson_log_df['Unique ID'].astype(str)

    new_rows = all_tutors_lesson_log_df[~all_tutors_lesson_log_df['Unique ID'].isin(mastersheet_data_df['Unique ID'])]
    updated_mastersheet_data_df = pd.concat([mastersheet_data_df, new_rows])

    # Convert the updated dataframe to a list of lists for uploading to Google Sheets
    updated_master_data_to_upload = [updated_mastersheet_data_df.columns.tolist()] + updated_mastersheet_data_df.values.tolist()

    # Clear the existing data in the Master Data Base sheet, without clearing the headers
    UT_Master_Data_Base_Sheet.clear() #TODO DON'T CLEAR HEADERS

    # Update the Master Data Base sheet with the new data
    UT_Master_Data_Base_Sheet.update('A1', updated_master_data_to_upload)
    print('New Hours Added')


def process_master_data_to_df():
    '''function that gets dfs of all unpaid invcoies, for each student, split by month

    strucutre of output: {student: {jan: unpaid_df}}
    requires student names are unique in the invoice master database'''

    UT_Master_Data_Base_GS = sa.open("UT_Master_Invoice_Data_Base")
    UT_Master_Data_Invoice_Sheet = UT_Master_Data_Base_GS.worksheet("Invoice Master Database")

    invoice_mastersheet_data = UT_Master_Data_Invoice_Sheet.get_all_values()
    invoice_mastersheet_data_df = pd.DataFrame(invoice_mastersheet_data[1:],
                                               columns=invoice_mastersheet_data[0]).dropna(subset=['Student Name'])

    unique_student_names = invoice_mastersheet_data_df['Student Name'].unique().tolist()

    student_invoice_dfs = {}

    all_students_unpaid_monthly_dfs = {}

    for student in unique_student_names:
        # Filter the original DataFrame for each student and store it in the dictionary
        student_invoice_dfs[student] = invoice_mastersheet_data_df[
            invoice_mastersheet_data_df['Student Name'] == student]

    for student in student_invoice_dfs:
        #df with all invoice items for a student in master db
        student_df = student_invoice_dfs[student]
        unique_months = student_df['Month'].unique() #TODO this wil be an issue when months repeat next year !

        students_unpaid_monthly_dfs = {}

        for month in unique_months: #TODO can add functionality here so if 'paid' == pre; process as pre paid block etc.
            '''unpaid invoices split by month'''
            # Filter for the specific month and where 'Paid' is not 1
            student_month_df = student_df[(student_df['Month'] == month)]
            student_month_unpaid_df = student_month_df[student_month_df['Paid'] == '']

            # If the filtered DataFrame is not empty, store it in the dictionary
            if not student_month_unpaid_df.empty:
                students_unpaid_monthly_dfs[month] = student_month_unpaid_df

        all_students_unpaid_monthly_dfs[student] = students_unpaid_monthly_dfs

    return all_students_unpaid_monthly_dfs


if __name__ == '__main__':
    print('run via main script please :)')





