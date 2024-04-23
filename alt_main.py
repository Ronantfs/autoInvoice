'''alterntive control flow script to main.py to be run from command line, without user input, so can automate'''
import argparse
import data_checks
from main import InvoiceManager

def main(mode):
    manager = InvoiceManager()

    if mode == 'all':
        # Sequential execution of all required functions (default mode)
        #1. Update records on central cloud masterbase
        manager.update_invoice_records()

        #2. Compile records + perform data checks: cloud -> local
        manager.compile_unpaid_monthly_records()  # Processes these records

        if not data_checks.check_invoice_master_data() or not data_checks.check_student_tutor_names_unique():
            print("Data checks failed or data is not available.")
            return  # Early exit if data checks fail

        #3. Generate invoices
        manager.generate_invoice_records('hourly')
        manager.generate_invoice_records('prepaid')

    elif mode == 'update_records':
        manager.update_invoice_records()

    elif mode == 'compile_records':
        manager.compile_unpaid_monthly_records()

    elif mode == 'generate_invoices_hourly':
        manager.generate_invoice_records('hourly')

    elif mode == 'generate_invoices_prepaid':
        manager.generate_invoice_records('prepaid')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Automate invoice management tasks")
    parser.add_argument('--mode', type=str, default='all',
                        choices=['all', 'update_records', 'compile_records', 'generate_invoices_hourly',
                                 'generate_invoices_prepaid'],
                        help='Specify the mode of operation.')

    args = parser.parse_args()
    main(args.mode)
