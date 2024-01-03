#TODO refector this project to use the new structure where control flow is in main.py and functions are in other files
import pandas as pd
import gspread
import numpy as np

import tutor_hours
import generate_invoices
#import update_invoice_records
import constants
import utils


#fucntionality to update invoice records:


class InvoiceManager:
    def __init__(self):
        self.all_students_unpaid_monthly_dfs = None
        self.all_invoice_records_df = None

    def update_invoice_records(self):
        # invoice records
        all_tutors_lesson_log_df = tutor_hours.get_all_tutors_lesson_log_df(constants.list_of_ut_tutors)
        # master data
        mastersheet_data = tutor_hours.get_master_data()
        mastersheet_data_df = mastersheet_data[0]
        UT_Master_Data_Base_Sheet = mastersheet_data[1]

        #update_master_record
        tutor_hours.add_new_tutor_lessons_to_master(mastersheet_data_df,
                                                     all_tutors_lesson_log_df,
                                                     UT_Master_Data_Base_Sheet)

    def compile_unpaid_monthly_records(self):
        '''Sets self.all_students_unpaid_monthly_dfs to a df of all unpaid records:
        unpaid records: dict[student: monthly dfs of unpaid records]'''

        # compile unpaid records into df to then be used to create invoices
        self.all_students_unpaid_monthly_dfs = tutor_hours.process_master_data_to_df()

        if self.all_students_unpaid_monthly_dfs is not None:
            print("DataFrames are available for use.")
            print(self.all_students_unpaid_monthly_dfs.keys())


    def generate_invoices_records(self):
        if self.all_students_unpaid_monthly_dfs is not None:
            print("Generating unpaid invoices")

            all_students_unpaid_monthly_dfs = self.all_students_unpaid_monthly_dfs
            all_invoices_records = pd.DataFrame()

            for student in all_students_unpaid_monthly_dfs:
                print(f'processing {student} invoices...')
                student_invoices = generate_invoices.process_data_for_student(student, all_students_unpaid_monthly_dfs[student])
                all_invoices_records = pd.concat([all_invoices_records, student_invoices], ignore_index=True)

                # Save the DataFrame as class variable and generate csv
                self.all_invoice_records_df = all_invoices_records
                utils.ensure_invoice_folder_exists()
                csv_file_path = constants.invoice_records_csv_file_path
                all_invoices_records.to_csv(csv_file_path, index=False)
        else:
            print("DataFrame is not available. Please run option 2 to compile first.")

    def function_4(self):
        pass #TODO

    def run(self):
        '''Control flow for the program'''

        while True:
            print('\nSelect a function to run:')
            print('1. Centralise all tutor hours onto master (cloud) [Get new tutor hours]')
            print('2. Compile unpaid monthly records to class variable')
            print('3. Generate invoices and set invoice records')
            print('4. TODO: Update invoice records...')
            print('5. Exit')

            try:
                choice = int(input("Enter an appropriate integer: "))
                if choice == 1:
                    self.update_invoice_records()
                elif choice == 2:
                    self.compile_unpaid_monthly_records()
                elif choice == 3:
                    if self.all_students_unpaid_monthly_dfs is not None:
                        print("Generating unpaid invoices")
                        self.generate_invoices_records()
                    else:
                        print("DataFrame is not available. Please run option 2 to compile df from google sheets first.")

                elif choice == 4:print('TODO: Update invoice records...')

                elif choice == 5:
                    print("Exiting program.")
                    break
                else:
                    print('Not a valid choice')
            except ValueError:
                print("Invalid input. Please enter an integer.")

if __name__ == '__main__':
    manager = InvoiceManager()
    manager.run()


