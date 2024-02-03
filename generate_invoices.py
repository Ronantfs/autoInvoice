# Imports
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.colors import Color
import pandas as pd
import os
import utils
import constants

# Configuration
INVOICES_FOLDER_PATH = constants.INVOICES_FOLDER_PATH
LOGO_PATH = constants.LOGO_PATH

# Ensure invoice folder exists
if not os.path.exists(INVOICES_FOLDER_PATH):
    os.makedirs(INVOICES_FOLDER_PATH)


def draw_static_elements(canvas, width, height, student, tutor, total_fee, month, invoice_number, invoice_type):
    '''Draws static elements (like logo, text) on the canvas'''

    # Draws static elements (like logo, text) on the canvas
    canvas.drawImage(LOGO_PATH, 40, height - 180, width=120, height=160, mask='auto')

    #top right corner
    canvas.setFont("Helvetica-Bold", 24)
    canvas.drawRightString(width - 50, height - 50, "UNDERSTANDING TUTORS")
    canvas.setFont("Helvetica-Bold", 12)
    canvas.setFillColor(colors.lightgrey)
    canvas.drawRightString(width - 50, height - 70, "Premium Online STEM & Humanities Tuition")

    #right text
    canvas.setFillColor(colors.black)
    canvas.drawRightString(width - 50, height - 155, "Ronan Twomey Friedlander")
    canvas.drawRightString(width - 50, height - 170, f"Understanding Tutors Invoice")
    canvas.drawRightString(width - 50, height - 185, f"{invoice_number}")
    canvas.drawRightString(width - 50, height - 200, f"{month}")

    #left tex (bank stuff)
    canvas.setFont("Helvetica-Bold", 18)
    canvas.drawString(75, height - 220, f"{student} Understanding Tutors Tuition")
    canvas.setFont("Helvetica-Bold", 16)
    if invoice_type == 'hourly':
        canvas.drawString(75, height - 260, f"Total Invoice: £{total_fee}")
    if invoice_type == 'prepaid':
        canvas.drawString(75, height - 260, f"Total Hours: {total_fee}")
    # Draw a horizontal line

    #bank details with divider lines
    #lines
    x_start = 75  # Start x-coordinate
    y_position = height - 270  # Y-coordinate for the line
    x_end = width / 2.5  # End x-coordinate, adjust as needed
    line_thickness = 0.5  # Thickness of the line

    canvas.setLineWidth(line_thickness)
    canvas.setStrokeColor(utils.ut_lgreen)
    canvas.line(x_start, y_position, x_end, y_position)
    canvas.setStrokeColor(colors.black)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(75, height - 285, f"Bank Details:")
    canvas.drawString(75, height - 300, "Ronan A T Friedlander")
    canvas.drawString(75, height - 315, "ronantftutors")
    canvas.drawString(75, height - 330, f"04 - 00 - 04")
    canvas.drawString(75, height - 345, f"72315333")
    canvas.setStrokeColor(utils.ut_lgreen)
    canvas.line(x_start, 415, x_end, 415)
    canvas.setStrokeColor(colors.black)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(75, height - 365, f"Please include a clear reference with payments.")
    canvas.setFont("Helvetica-Bold", 14)

    # footer
    canvas.setFont("Helvetica-Bold", 18)
    canvas.setFillColor(colors.lightblue)
    canvas.drawString(75, 75, "www.understandingtutors.com")
    canvas.setFont("Helvetica-Bold", 13)
    canvas.setFillColor(utils.ut_green)
    canvas.drawString(75, 55, "Maths Physics Chemistry Biology Economics")
    canvas.setFillColor(utils.ut_purple)
    canvas.drawString(75, 35, "English History French Spanish")

def create_data_table(month_df, canvas, width, height,tutor):
    '''Creates a table for the invoice data (used for all invoices) '''
    data_for_report = [month_df.columns.to_list()] + month_df.values.tolist()
    style = TableStyle([
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('BACKGROUND', (0, 0), (-1, 0), utils.ut_green),  # Header row background
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for header
        ('BOX', (0,0), (-1,-1), 1, colors.black),  # Black border around the table
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.black),  # Lines below each row
    ])
    table = Table(data_for_report, colWidths=[100] * len(month_df.columns), style=style)
    table.wrapOn(canvas, width, height)
    table.drawOn(canvas, 75, 100)  # Adjust Y-position as needed

def create_an_invoice_pdf(student, month_df, month, tutor, total_fee, cumulative_total_value, invoice_name, invoice_number, invoice_type ='hourly'):
    '''Creates a single PDF invoice based on the given data'''

    #TODO adapt this for pre paid invoices to utilise the cumulative total

    #create folder for student if it doesn't exist:
    invoice_pdf_folder_path = utils.create_student_invoice_folder(student)
    invoice_pdf_path = os.path.join(invoice_pdf_folder_path, f"{invoice_name}.pdf")

    #create the canvas
    canv = canvas.Canvas(invoice_pdf_path, pagesize=letter)
    width, height = letter

    # Draw static elements
    draw_static_elements(canv, width, height, student, tutor, total_fee, month,invoice_number, invoice_type)

    # Draw data table
    create_data_table(month_df, canv, width, height, tutor)

    # Save the PDF
    canv.save()
    print(f"{invoice_type} PDF generated: {invoice_name}")


def process_invoice_data(student, students_invoices_dfs, invoice_type):
    total_prepaid_hours_used = 0

    processed_data = {}

    print(student)
    for month, month_df in students_invoices_dfs.items():
        # Common variables for invoice
        tutor = month_df['Tutor'].iloc[0]
        invoice_name = f"{student}_UT Invoice_{month}"
        invoice_number = utils.generate_invoice_number()

        # Select columns and rename for the invoice based on invoice_type
        if invoice_type == 'hourly':
            invoice_columns = ['Lesson Date', 'Lesson Length (Hours)', r'Invoice Rate', 'Lesson fee, parent', 'Tutor']
            invoice_columns_rename = {
                'Lesson Date': 'Lesson Date',
                'Lesson Length (Hours)': 'Duration (Hours)',
                'Invoice Rate': 'Hourly rate (£/hr)',
                'Lesson fee, parent': 'Lesson Fee',
                'Tutor': 'Tutor'.title()
            }
            month_df = month_df[invoice_columns]
            month_df = month_df.rename(columns=invoice_columns_rename)
            month_df['Lesson Fee'] = pd.to_numeric(month_df['Lesson Fee'])
            total_value = month_df['Lesson Fee'].sum()
            month_df['Lesson Fee'] = month_df['Lesson Fee'].astype(str)


        elif invoice_type == 'prepaid':
            # import data from pre paid sheet
            invoice_columns = ['Lesson Date', 'Lesson Length (Hours)', 'Tutor', 'Payment Type']
            invoice_columns_rename = {
                'Lesson Date': 'Lesson Date',
                'Lesson Length (Hours)': 'Duration (Hours)',
                'Tutor': 'Tutor'.title(),
                'Payment Type': 'Payment Status'
            }
            month_df = month_df[invoice_columns]
            month_df = month_df.rename(columns=invoice_columns_rename)
            month_df['Duration (Hours)'] = pd.to_numeric(month_df['Duration (Hours)'])
            total_value = month_df['Duration (Hours)'].sum()

        # Additional common data processing
        month_df['Duration (Hours)'] = pd.to_numeric(month_df['Duration (Hours)'], errors='coerce')

        # Store processed data
        processed_data[month] = {
            "month_df": month_df,
            "tutor": tutor,
            "invoice_name": invoice_name,
            "invoice_number": invoice_number,
            "total_value": total_value
        }
        total_prepaid_hours_used += total_value

    return processed_data, total_prepaid_hours_used

def generate_invoice_pdfs(all_invoice_data, student, invoice_type):

    '''Handles the generation of PDF invoices for a given student based on the given data.

    Will maange all the 'meta-data' needed for excetuion/ imnitlization of a single invoice creation (using create_an_invoice_pdf)'''


    invoice_data = all_invoice_data['invoices']
    prepaid_blocks = all_invoice_data.get('prepaid_blocks', pd.DataFrame())  # Safe access as might be empty

    cumulative_total_value = 0
    student = student.strip()

    for month, data in invoice_data.items():

        cumulative_total_value += data['total_value']

        if invoice_type == 'prepaid':
            print(student, month, cumulative_total_value)

        create_an_invoice_pdf(student,
                              data['month_df'],
                              month,
                              data['tutor'],
                              data['total_value'],
                              cumulative_total_value,
                              data['invoice_name'],
                              data['invoice_number'],
                              invoice_type)






if __name__ == "__main__":
    print("please run via main.py :) ")

