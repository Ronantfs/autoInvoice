import gspread
import pandas as pd
import numpy as np
import constants


# Service account setup
sa = gspread.service_account(filename=constants.google_sa_json)
list_of_ut_tutors = constants.list_of_ut_tutors

def get_master_data():
    # Open the Master Data Base Google Sheet
    UT_Master_Data_Base_GS = sa.open("UT_Master_Invoice_Data_Base_Doc")
    UT_Master_Data_Base_Sheet = UT_Master_Data_Base_GS.worksheet("Master Data Base")

    # Load data from the Master Data Base sheet
    mastersheet_data = UT_Master_Data_Base_Sheet.get_all_values()
    mastersheet_data_df = pd.DataFrame(mastersheet_data[1:], columns=mastersheet_data[0]).dropna(subset=['Student'])

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
        log_data_df['Student'].replace('', pd.NA, inplace=True)
        log_data_df = log_data_df.dropna(subset=['Student'])
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
    '''Function that gets DataFrames of all unpaid invoices for each student, split by month.'''

    def get_dataframe_from_sheet(sheets_object, sheet_name):
        """Get DataFrame from a specified Google Sheets worksheet."""
        worksheet = sheets_object.worksheet(sheet_name)
        data = worksheet.get_all_values()
        return pd.DataFrame(data[1:], columns=data[0]).dropna(subset=['Student'])

    def filter_data_for_student(df, student_name):
        """Filter the DataFrame for a given student."""
        return df[df['Student'] == student_name]

    def process_invoice_data_master(df):
        """Process invoice data and categorize by month and payment type."""
        students_monthly_dfs = {}
        students_monthly_dfs_pre_paid = {}

        for student in df['Student'].unique():
            student_df = filter_data_for_student(df, student)

            student_hourly_dfs = {}
            student_prepaid_dfs = {}

            for month in student_df['Month'].unique():
                month_df = student_df[student_df['Month'] == month]

                hourly_month_df = month_df[month_df['Payment Type'] == '']
                prepaid_month_df = month_df[month_df['Payment Type'] == 'pre']

                # Only add to dict if not empty
                if not hourly_month_df.empty:
                    student_hourly_dfs[month] = hourly_month_df

                if not prepaid_month_df.empty:
                    student_prepaid_dfs[month] = prepaid_month_df


            # Add the student's monthly DataFrames to the main dictionary
            if student_hourly_dfs:
                students_monthly_dfs[student] = student_hourly_dfs
            if student_prepaid_dfs:
                students_monthly_dfs_pre_paid[student] = student_prepaid_dfs

        return students_monthly_dfs, students_monthly_dfs_pre_paid

    def process_prepaid_records(df):
        """Process prepaid records data."""
        prepaid_blocks = {}

        #filter dateframe for select headers:
        df = df[['Student',
                 "Received",
                 "Amount, £",
                 "#Hours",
                 "Hourly Rate",
                 "Block Number",
                 "Block ID",]]

        for student in df['Student'].unique():
            student_records = filter_data_for_student(df, student)
            if not student_records.empty:
                prepaid_blocks[student] = student_records

        return prepaid_blocks

    # Open and read data from Google Sheets
    UT_Master_Data_Base_GS = sa.open("UT_Master_Invoice_Data_Base_Doc")

    # Invoice Master Database and Prepaid Records Sheet
    invoice_df = get_dataframe_from_sheet(UT_Master_Data_Base_GS, "Invoice Master Database")
    prepaid_df = get_dataframe_from_sheet(UT_Master_Data_Base_GS, "Prepaid Records")

    # Process the data
    unpaid_dfs, prepaid_dfs = process_invoice_data_master(invoice_df)
    prepaid_blocks = process_prepaid_records(prepaid_df)

    return unpaid_dfs, prepaid_dfs, prepaid_blocks

#TODO: refactor , to meet the same input output requirements; but the function is more comncise:



if __name__ == '__main__':
    print('run via main script please :)')





