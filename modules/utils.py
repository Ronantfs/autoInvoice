from datetime import datetime  # Import the datetime class from the datetime module
import secrets  # For generating the random string
from reportlab.lib.colors import Color
from modules import constants
import os
from datetime import datetime
import calendar
from collections import OrderedDict

def hex_to_reportlab_color(hex_color):
    """
    Convert a hex color string to a ReportLab Color object.
    :param hex_color: Hex color string (e.g., "#FF5733")
    :return: ReportLab Color object
    """
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    r = int(hex_color[:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return Color(r, g, b)



ut_green = hex_to_reportlab_color("#34745a")
ut_lgreen = hex_to_reportlab_color("#95d0b8")
ut_yellow = hex_to_reportlab_color("#e3ba44")
ut_purple = hex_to_reportlab_color("#5151b4")
ut_rouge = hex_to_reportlab_color("#900C3F")


def generate_invoice_number():
    current_date = datetime.now().strftime("%Y%m%d")
    random_string = secrets.token_hex(3)  # Generates a 6-character hexadecimal string
    return f"{current_date}-{random_string}"


def ensure_invoice_folder_exists():
    # Ensure invoice folder exists
    if not os.path.exists(constants.INVOICES_FOLDER_PATH):
        os.makedirs(constants.INVOICES_FOLDER_PATH)
        print(f"Created folder: {constants.INVOICES_FOLDER_PATH}")
    else:
        return




def create_student_invoice_folder(student_name):

    INVOICES_FOLDER_PATH = constants.INVOICES_FOLDER_PATH
    # Construct the path for the new student's folder
    student_folder_path = os.path.join(INVOICES_FOLDER_PATH, student_name)

    # Check if the folder already exists
    if not os.path.exists(student_folder_path):
        # Create the folder if it does not exist
        os.makedirs(student_folder_path)
        print(f"Folder created at: {student_folder_path}")
    else:
        pass
        #print(f"Folder already exists at: {student_folder_path}")

    return student_folder_path

def asses_pre_paid_balance():

    '''fucntion that compares total pre paid balance hours to total hours used'''
        #TODO
    pass


def sort_invoices_chronologically(processed_data):
    """
    Sorts the invoices in chronological order based on their keys.

    Parameters:
        processed_data: Dictionary with month-year as keys and data frames as values.

    Returns:
        OrderedDict with sorted keys.
    """

    # Convert keys to datetime objects for sorting
    date_keys = []
    for key in processed_data.keys():
        month, year = key.split(' ')
        month_number = list(calendar.month_name).index(month)
        date_obj = datetime(int(year), month_number, 1)
        date_keys.append((date_obj, key))

    # Sort keys chronologically and create an ordered dictionary
    sorted_keys = sorted(date_keys)
    ordered_invoices = OrderedDict((key, processed_data[key]) for _, key in sorted_keys)

    return ordered_invoices
