from io import BytesIO
import random
import string
from django.http import FileResponse
import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime
import pytz


def generate_code():
    characters = string.ascii_letters + string.digits # include letters and digits
    random_string = ''.join(random.choice(characters) for _ in range(14))
    return random_string


def create_pdf(qr_codes):

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    x, y = 1 * cm, 28 * cm  # Starting position of the first QR code
    qr_size = 2 * cm  # Size of each QR code

    for qr_code in qr_codes:
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=10, border=4)
        qr.add_data(qr_code)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        p.drawInlineImage(img, x, y, width=qr_size, height=qr_size)

        x += qr_size + 0.01 * cm  # Increase the x position for the next QR code

        if x > 19 * cm:  # Check if the next QR code exceeds the page width
            x = 1 * cm  # Reset x position to the starting position
            y -= qr_size + 0.01 * cm  # Move to the next row

            if y < 2 * cm:  # Check if the next QR code exceeds the page height
                p.showPage()  # Create a new page
                x, y = 1 * cm, 28 * cm  # Reset x and y positions

    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='qrcode_report.pdf')


def get_local_date(local_timezone):
    utc_now = datetime.now(pytz.utc)
    local_tz = pytz.timezone(local_timezone)
    local_now = utc_now.astimezone(local_tz)
    local_date = local_now.date()
    return local_date