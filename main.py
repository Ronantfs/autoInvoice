import pandas as pd

from modules import tutor_hours
from modules import generate_invoices
from modules import constants
from modules import utils
from modules import data_checks

#fucntionality to update invoice records:

class InvoiceManager:
    def __init__(self):
        self.all_students_unpaid_monthly_dfs = None
        self.all_students_unpaid_monthly_dfs_pre_paid = None
        self.all_students_prepaid_blocks = None

        self.students_pre_paid_hours_used = {}
        self.students_hourly_totals = {}

        #self.all_invoice_records_df = None


    def update_invoice_records(self):
        # invoice records and confirmed hours
        all_tutors_lesson_log_df, all_tutors_confirmed_hours_df = tutor_hours.get_all_tutors_lesson_log_df(constants.list_of_ut_tutors)
        # master data
        mastersheet_data = tutor_hours.get_master_data()
        # master hour logs
        mastersheet_lesson_log_data_df = mastersheet_data[0]
        UT_Master_Data_Base_Sheet = mastersheet_data[1]
        # master confirmed hours
        UT_Master_Confirmed_Hours_df = mastersheet_data[2]
        UT_Master_Confirmed_Hours_Sheet = mastersheet_data[3]


        #update_master_record lesson hours
        tutor_hours.add_new_tutor_lessons_to_master(mastersheet_lesson_log_data_df,
                                                     all_tutors_lesson_log_df,
                                                     UT_Master_Data_Base_Sheet)

        #update_master_record confirmed hours ...
        tutor_hours.pull_confirmed_hours_to_master(all_tutors_confirmed_hours_df,UT_Master_Confirmed_Hours_df, UT_Master_Confirmed_Hours_Sheet)

    def compile_unpaid_monthly_records(self):
        '''Sets self.all_students_unpaid_monthly_dfs to a df of all unpaid records:
        unpaid records: dict[student: monthly dfs of unpaid records]'''

        # compile unpaid records into df to then be used to create invoices
        dfs: tuple = tutor_hours.process_master_data_to_df()
        self.all_students_unpaid_monthly_dfs = dfs[0]
        self.all_students_unpaid_monthly_dfs_pre_paid = dfs[1]
        self.all_students_prepaid_blocks = dfs[2]

        if self.all_students_unpaid_monthly_dfs is not None:
            print("Hourly DataFrames are available for use.")
            print(self.all_students_unpaid_monthly_dfs.keys())


        if self.all_students_unpaid_monthly_dfs_pre_paid is not None:
            print("Pre paid DataFrames are available for use.")
            print(self.all_students_unpaid_monthly_dfs_pre_paid.keys())

    def generate_invoice_records(self, invoice_type: str):
        '''Generates PDF invoices of unpaid hours

        If invoice type == pre-paid, then the function will also sum the total pre-paid hours used for each student,
        and store this in self.students_pre_paid_hours_used'''

        if invoice_type not in ['hourly', 'prepaid']:
            print("Invalid invoice type specified.")
            return


        #define set of student dfs to use to generate invoices
        if invoice_type == 'hourly':
            if self.all_students_unpaid_monthly_dfs is None:
                print(
                    "DataFrame for hourly invoices is not available. Please run the appropriate option to compile first.")
                return
            student_dfs = self.all_students_unpaid_monthly_dfs
            print("\nGenerating unpaid invoices\n...")

        elif invoice_type == 'prepaid':
            if self.all_students_unpaid_monthly_dfs_pre_paid is None:
                print("DataFrame for pre-paid invoices is not available. Please run the appropriate option to compile first.")
                return
            student_dfs = self.all_students_unpaid_monthly_dfs_pre_paid
            print("\nGenerating pre-paid invoices\n...")

        #generate invoices for each student
        for student in student_dfs:
            print(f'\nprocessing {student} invoices... Generating PDFs and summing any prepaid hours used.')



            # Process the invoice data
            processed_data, students_total_hours = generate_invoices.process_invoice_data(student,
                                                                                          student_dfs[student],
                                                                                          invoice_type)

            ordered_invoices = utils.sort_invoices_chronologically(processed_data)

            # Initialize the data structure
            all_invoice_data = {
                'invoices': ordered_invoices
            }

            # Add prepaid blocks data if invoice type is 'prepaid'
            if invoice_type == 'prepaid':
                all_invoice_data['prepaid_blocks'] = self.all_students_prepaid_blocks.get(student, pd.DataFrame())

            # Generate the invoice PDFs
            generate_invoices.generate_invoice_pdfs(all_invoice_data, student, invoice_type)

            #set invoice records
            if invoice_type == 'prepaid':
                self.students_pre_paid_hours_used[student] = students_total_hours
            if invoice_type == 'hourly':
                self.students_hourly_totals[student] = students_total_hours


    def function_4(self):
        pass

    def run(self):
        '''Control flow for the program'''

        while True:
            print('\nSelect a function to run:')
            print('1. Centralise all tutor hours onto master (cloud) [Get new tutor hours]')
            print('2. Compile unpaid monthly records to class variable')
            print('3. Generate invoices and set invoice records') #TODO add processing for pre paid invoices
            print('4. Check student balances')
            print('5. Exit')

            try:
                choice = int(input("Enter an appropriate integer: "))
                if choice == 1:
                    self.update_invoice_records()

                elif choice == 2:
                    self.compile_unpaid_monthly_records()
                    data_checks.check_invoice_master_data()
                    print(0)

                elif choice == 3:

                    # Early exit if the data checks fail
                    if not (data_checks.check_invoice_master_data() and data_checks.check_student_tutor_names_unique()):
                        print(
                            "DataFrame is not available. ")
                        return

                    # Check if both DataFrames are None
                    if self.all_students_unpaid_monthly_dfs is None and self.all_students_unpaid_monthly_dfs_pre_paid is None:
                        print("No unpaid invoices available for processing. If there are unpaid invoice, Please run option 2 to compile df from google sheets first.")
                        return

                    # Process only hourly rate invoices
                    if self.all_students_unpaid_monthly_dfs is not None:
                        self.generate_invoice_records('hourly')
                        # If prepaid invoices are also available, process them
                        if self.all_students_unpaid_monthly_dfs_pre_paid is not None:
                            self.generate_invoice_records('prepaid')

                elif choice == 4:

                    if self.students_pre_paid_hours_used or self.students_hourly_totals:
                        print('Prepaid hours log:',self.students_pre_paid_hours_used)
                        print('Hourly totals log:',self.students_hourly_totals)
                        gross_hourly_money = sum(self.students_hourly_totals.values())
                        print('Gross hourly money:', gross_hourly_money)

                    else:
                        print('')
                        print("Pre-paid hours have not been calculated yet. Please run option 3 first.")

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


