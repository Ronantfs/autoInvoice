# Imports
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.colors import Color
import pandas as pd
import os
import secrets  # For generating the random string
from datetime import datetime  # Import the datetime class from the datetime module

#previous script
import tutor_hours

import utils
import constants

# Configuration
INVOICES_FOLDER_PATH = constants.INVOICES_FOLDER_PATH
LOGO_PATH = constants.LOGO_PATH

# Ensure invoice folder exists
if not os.path.exists(INVOICES_FOLDER_PATH):
    os.makedirs(INVOICES_FOLDER_PATH)


def draw_static_elements(canvas, width, height, student, tutor, total_fee, month, invoice_number):
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
    canvas.drawString(75, height - 260, f"Total Invoice: £{total_fee}")
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
    canvas.drawString(75, height - 365, f"Please include a clear reference with the pyament.")
    canvas.setFont("Helvetica-Bold", 14)

    # footer
    canvas.setFont("Helvetica-Bold", 18)
    canvas.setFillColor(colors.lightblue)
    canvas.drawString(75, 75, "www.understandingtutors.com")
    canvas.setFont("Helvetica-Bold", 13)
    canvas.setFillColor(utils.ut_green)
    canvas.drawString(75, 55, "Maths Physics Chemistry Biology Economics")
    canvas.setFillColor(utils.ut_purple)
    canvas.drawString(75, 35, "English History French Spansih")

def create_data_table(month_df, canvas, width, height,tutor):
    '''Creates a table for the invoice data '''
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

def create_invoice_pdf(student, month_df, month, tutor, total_fee, invoice_name, invoice_number):
    '''Creates a PDF invoice based on the given data'''
    invoice_pdf_path = os.path.join(INVOICES_FOLDER_PATH, f"{invoice_name}.pdf")
    canv = canvas.Canvas(invoice_pdf_path, pagesize=letter)
    width, height = letter

    # Draw static elements
    draw_static_elements(canv, width, height, student, tutor, total_fee, month,invoice_number)

    # Draw data table
    create_data_table(month_df, canv, width, height, tutor)

    # Save the PDF
    canv.save()
    print(f"PDF generated: {invoice_name}")


def process_data_for_student(student, student_invoice_dfs):
    invoice_records = pd.DataFrame(
        columns=['Invoice Number', 'Tutor', 'Student', 'Amount', 'Number of Hours', 'Date Created', 'Status',
                 'Lesson Date', 'Invoice Path','Permanent ID'])

    for month in student_invoice_dfs:
        month_df = student_invoice_dfs[month]

        tutor = month_df['Tutor'].iloc[0]
        invoice_name = f"{student}_UT Invoice_{month}"
        invoice_number = utils.generate_invoice_number()

        # Select columns to use for invoice to parent
        invoice_columns = ['Lesson Date', 'Lesson Length (Hours)', r'Invoice Rate', 'Lesson fee, parent','Tutor']
        month_df = month_df[invoice_columns]
        # rename columns for the invoice to be external facing
        invoice_columns_rename = {
            'Lesson Date': 'Lesson Date',
            'Lesson Length (Hours)': 'Duration (Hours)',
            'Invoice Rate': 'Hourly rate (£/hr)',
            'Lesson fee, parent': 'Lesson Fee',
            'Tutor': 'Tutor'.title()
        }
        month_df = month_df.rename(columns=invoice_columns_rename)

        # Calculate total fee
        month_df['Lesson Fee'] = pd.to_numeric(month_df['Lesson Fee'])
        total_fee = month_df['Lesson Fee'].sum()
        month_df['Lesson Fee'] = month_df['Lesson Fee'].astype(str)

        # Additional data for invoice record
        month_df['Duration (Hours)'] = pd.to_numeric(month_df['Duration (Hours)'], errors='coerce')
        total_hours = month_df['Duration (Hours)'].sum()
        invoice_month = month_df['Lesson Date'].iloc[0]
        invoice_path = os.path.join(INVOICES_FOLDER_PATH, f"{invoice_name}.pdf")
        invoice_record = {
            'Invoice Number': invoice_number,
            'Tutor': tutor,
            'Student': student,
            'Amount': total_fee,
            'Number of Hours': total_hours,
            'Date Created': datetime.now().strftime("%Y-%m-%d"),
            'Status': 'Unpaid',
            'Lesson Date': month_df['Lesson Date'].min(),
            'Invoice Path': '',
            'Permanent ID': str(invoice_month) + student
        }

        # Create invoice PDF
        create_invoice_pdf(student, month_df, month, tutor, total_fee, invoice_name, invoice_number)
        # Add record to DataFrame
        invoice_records = pd.concat([invoice_records, pd.DataFrame([invoice_record])], ignore_index=True)


    return invoice_records



if __name__ == "__main__":
    print("please run via main.py :) ")
