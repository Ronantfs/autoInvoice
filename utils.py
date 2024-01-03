from datetime import datetime  # Import the datetime class from the datetime module
import secrets  # For generating the random string
from reportlab.lib.colors import Color
import constants
import os

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


