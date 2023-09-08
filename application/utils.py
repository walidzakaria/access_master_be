import imp
import io
import os
from django.http import HttpResponse
from docxtpl import DocxTemplate
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

COUNTRY_LIST = (
    ('EG', 'EGYPT'),
    ('SA', 'SAUDI ARABIA'),
    ('KW', 'KUWAIT'),
    ('AE', 'UNITED ARAB EMIRATES'),
    ('AF', 'AFGHANISTAN'),
    ('AL', 'ALBANIA'),
    ('DZ', 'ALGERIA'),
    ('AS', 'AMERICAN SAMOA'),
    ('AD', 'ANDORRA'),
    ('AO', 'ANGOLA'),
    ('AR', 'ARGENTINA'),
    ('AM', 'ARMENIA'),
    ('AW', 'ARUBA'),
    ('AU', 'AUSTRALIA'),
    ('AT', 'AUSTRIA'),
    ('AZ', 'AZERBAIJAN'),
    ('BS', 'BAHAMAS'),
    ('BH', 'BAHRAIN'),
    ('BD', 'BANGLADESH'),
    ('BB', 'BARBADOS'),
    ('BY', 'BELARUS'),
    ('BE', 'BELGIUM'),
    ('BZ', 'BELIZE'),
    ('BJ', 'BENIN'),
    ('BM', 'BERMUDA'),
    ('BT', 'BHUTAN'),
    ('BO', 'BOLIVIA'),
    ('BA', 'BOSNIA'),
    ('BW', 'BOTSWANA'),
    ('BV', 'BOUVET ISLAND'),
    ('BR', 'BRAZIL'),
    ('BG', 'BULGARIA'),
    ('BF', 'BURKINA FASO'),
    ('BI', 'BURUNDI'),
    ('KH', 'CAMBODIA'),
    ('CM', 'CAMEROON'),
    ('CA', 'CANADA'),
    ('CV', 'CAPE VERDE'),
    ('KY', 'CAYMAN ISLANDS'),
    ('TD', 'CHAD'),
    ('CL', 'CHILE'),
    ('CN', 'CHINA'),
    ('CX', 'CHRISTMAS ISLAND'),
    ('CO', 'COLOMBIA'),
    ('KM', 'COMOROS'),
    ('CG', 'CONGO'),
    ('CR', 'COSTA RICA'),
    ('CI', 'CÔTE D'),
    ('HR', 'CROATIA'),
    ('CU', 'CUBA'),
    ('CY', 'CYPRUS'),
    ('CZ', 'CZECH REPUBLIC'),
    ('DK', 'DENMARK'),
    ('DJ', 'DJIBOUTI'),
    ('DM', 'DOMINICA'),
    ('DO', 'DOMINICAN REPUBLIC'),
    ('EC', 'ECUADOR'),
    ('SV', 'EL SALVADOR'),
    ('GQ', 'EQUATORIAL GUINEA'),
    ('ER', 'ERITREA'),
    ('EE', 'ESTONIA'),
    ('ET', 'ETHIOPIA'),
    ('FK', 'FALKLAND ISLANDS (MALVINAS)'),
    ('FO', 'FAROE ISLANDS'),
    ('FJ', 'FIJI'),
    ('FI', 'FINLAND'),
    ('FR', 'FRANCE'),
    ('GF', 'FRENCH GUIANA'),
    ('GA', 'GABON'),
    ('GM', 'GAMBIA'),
    ('GE', 'GEORGIA'),
    ('DE', 'GERMANY'),
    ('GH', 'GHANA'),
    ('GI', 'GIBRALTAR'),
    ('GR', 'GREECE'),
    ('GL', 'GREENLAND'),
    ('GD', 'GRENADA'),
    ('GP', 'GUADELOUPE'),
    ('GU', 'GUAM'),
    ('GT', 'GUATEMALA'),
    ('GN', 'GUINEA'),
    ('GY', 'GUYANA'),
    ('HT', 'HAITI'),
    ('HN', 'HONDURAS'),
    ('HK', 'HONG KONG'),
    ('HU', 'HUNGARY'),
    ('IS', 'ICELAND'),
    ('IN', 'INDIA'),
    ('ID', 'INDONESIA'),
    ('IR', 'IRAN'),
    ('IQ', 'IRAQ'),
    ('IE', 'IRELAND'),
    ('IL', 'ISRAEL'),
    ('IT', 'ITALY'),
    ('JM', 'JAMAICA'),
    ('JP', 'JAPAN'),
    ('JO', 'JORDAN'),
    ('KZ', 'KAZAKHSTAN'),
    ('KE', 'KENYA'),
    ('KI', 'KIRIBATI'),
    ('KP', 'KOREA'),
    ('KG', 'KYRGYZSTAN'),
    ('LV', 'LATVIA'),
    ('LB', 'LEBANON'),
    ('LS', 'LESOTHO'),
    ('LR', 'LIBERIA'),
    ('LY', 'LIBYA'),
    ('LI', 'LIECHTENSTEIN'),
    ('LT', 'LITHUANIA'),
    ('LU', 'LUXEMBOURG'),
    ('MO', 'MACAO'),
    ('MK', 'MACEDONIA'),
    ('MG', 'MADAGASCAR'),
    ('MW', 'MALAWI'),
    ('MY', 'MALAYSIA'),
    ('MV', 'MALDIVES'),
    ('ML', 'MALI'),
    ('MT', 'MALTA'),
    ('MQ', 'MARTINIQUE'),
    ('MR', 'MAURITANIA'),
    ('MU', 'MAURITIUS'),
    ('YT', 'MAYOTTE'),
    ('MX', 'MEXICO'),
    ('FM', 'MICRONESIA'),
    ('MD', 'MOLDOVA'),
    ('MC', 'MONACO'),
    ('MN', 'MONGOLIA'),
    ('ME', 'MONTENEGRO'),
    ('MS', 'MONTSERRAT'),
    ('MA', 'MOROCCO'),
    ('MZ', 'MOZAMBIQUE'),
    ('MM', 'MYANMAR'),
    ('NA', 'NAMIBIA'),
    ('NR', 'NAURU'),
    ('NP', 'NEPAL'),
    ('NL', 'NETHERLANDS'),
    ('NC', 'NEW CALEDONIA'),
    ('NZ', 'NEW ZEALAND'),
    ('NI', 'NICARAGUA'),
    ('NE', 'NIGER'),
    ('NG', 'NIGERIA'),
    ('NU', 'NIUE'),
    ('NF', 'NORFOLK ISLAND'),
    ('NO', 'NORWAY'),
    ('OM', 'OMAN'),
    ('PK', 'PAKISTAN'),
    ('PW', 'PALAU'),
    ('PS', 'PALESTINE'),
    ('PA', 'PANAMA'),
    ('PY', 'PARAGUAY'),
    ('PE', 'PERU'),
    ('PH', 'PHILIPPINES'),
    ('PN', 'PITCAIRN'),
    ('PL', 'POLAND'),
    ('PT', 'PORTUGAL'),
    ('PR', 'PUERTO RICO'),
    ('QA', 'QATAR'),
    ('RE', 'RÉUNION'),
    ('RO', 'ROMANIA'),
    ('RU', 'RUSSIAN FEDERATION'),
    ('RW', 'RWANDA'),
    ('SH', 'SAINT HELENA'),
    ('LC', 'SAINT LUCIA'),
    ('WS', 'SAMOA'),
    ('SM', 'SAN MARINO'),
    ('SN', 'SENEGAL'),
    ('RS', 'SERBIA'),
    ('SC', 'SEYCHELLES'),
    ('SL', 'SIERRA LEONE'),
    ('SG', 'SINGAPORE'),
    ('SK', 'SLOVAKIA'),
    ('SI', 'SLOVENIA'),
    ('SB', 'SOLOMON ISLANDS'),
    ('SO', 'SOMALIA'),
    ('ZA', 'SOUTH AFRICA'),
    ('SS', 'SOUTH SUDAN'),
    ('ES', 'SPAIN'),
    ('LK', 'SRI LANKA'),
    ('SD', 'SUDAN'),
    ('SR', 'SURINAME'),
    ('SZ', 'SWAZILAND'),
    ('SE', 'SWEDEN'),
    ('CH', 'SWITZERLAND'),
    ('SY', 'SYRIAN ARAB REPUBLIC'),
    ('TW', 'TAIWAN'),
    ('TJ', 'TAJIKISTAN'),
    ('TZ', 'TANZANIA'),
    ('TH', 'THAILAND'),
    ('TL', 'TIMOR-LESTE'),
    ('TG', 'TOGO'),
    ('TK', 'TOKELAU'),
    ('TO', 'TONGA'),
    ('TT', 'TRINIDAD AND TOBAGO'),
    ('TN', 'TUNISIA'),
    ('TR', 'TURKEY'),
    ('TM', 'TURKMENISTAN'),
    ('TV', 'TUVALU'),
    ('UG', 'UGANDA'),
    ('UA', 'UKRAINE'),
    ('GB', 'UNITED KINGDOM'),
    ('US', 'UNITED STATES'),
    ('UY', 'URUGUAY'),
    ('UZ', 'UZBEKISTAN'),
    ('VU', 'VANUATU'),
    ('VE', 'VENEZUELA'),
    ('VN', 'VIET NAM'),
    ('YE', 'YEMEN'),
    ('ZM', 'ZAMBIA'),
    ('ZW', 'ZIMBABWE'),
)

LEVEL = (
    ('E', 'Excellent'),
    ('G', 'Good'),
    ('F', 'Fair'),
)


def doc_application(request, context, export_name):
    doc = DocxTemplate(r"media/application/application_template.docx")
    doc.render(context)
    doc_io = io.BytesIO()  # create a file-like object
    doc.save(doc_io)  # save data to file-like object
    doc_io.seek(0)  # go to the beginning of the file-like object
    response = HttpResponse(doc_io.read())
    # Content-Disposition header makes a file downloadable
    response["Content-Disposition"] = f"attachment; filename={export_name}.docx"

    # Set the appropriate Content-Type for docx file
    response["Content-Type"] = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    return response


def send_message(sender_name, sender_email, subject, message):
    message = message.replace('\n', '<br>')
    mail_body = f"""
    <body style="font-family: Calibri;">
        <h3>Message from Red Sea App</h3>
        <table>
        <tr>
            <th></th>
            <th></th>
        </tr>
        <tr>
            <td><b>Sender: </b></td>
            <td>{sender_name}</td>
        </tr>
        <tr>
            <td><b>Email: </b></td>
            <td><a href="mailto:{sender_email}">{sender_email}</a></td>
        </tr>
        <tr>
            <td><b>Subject: </b></td>
            <td>{subject}</td>
        </tr>
        <tr style="vertical-align: top">
            <td><b>Message: </b></td>
            <td><p>{message}</p></td>
        </tr>
        </table>
        </body>
    """
    mail_to_send = EmailMultiAlternatives('Message from RS App',
        mail_body, settings.DEFAULT_FROM_EMAIL, ['info@redsea24.com'])
    
    mail_to_send.attach_alternative(mail_body, 'text/html')
    m = EmailMultiAlternatives()
    return mail_to_send.send()

def send_resume(name, mobile, email, status, resume, message, job):
    message = message.replace('\n', '<br>')
    mail_body = f"""
    <body style="font-family: Calibri;">
        <h3>An Application Has Been Submitted</h3>
        <table>
        <tr>
            <th></th>
            <th></th>
        </tr>
        <tr>
            <td><b>Full Name: </b></td>
            <td>{name}</td>
        </tr>
        <tr>
            <td><b>Mobile Number: </b></td>
            <td><a href="tel:{mobile}">{mobile}</a></td>
        </tr>
        <tr>
            <td><b>Email: </b></td>
            <td><a href="mailto:{email}">{email}</a></td>
        </tr>
        <tr>
            <td><b>Status: </b></td>
            <td>{status}</td>
        </tr>
        <tr>
            <td><b>Job: </b></td>
            <td>{job}</td>
        </tr>
        <tr style="vertical-align: top">
            <td><b>Message: </b></td>
            <td>{message}</td>
        </tr>
        </table>
        </body>
    """
    mail_to_send = EmailMultiAlternatives('New Application',
        mail_body, settings.DEFAULT_FROM_EMAIL, ['recruitment@redsea24.com', 'info@redsea24.com'])
    print(resume)
    
    # mail_to_send.attach(resume.name, resume.read(), resume.content_type)
    mail_to_send.attach_file(resume)
    mail_to_send.attach_alternative(mail_body, 'text/html')
    return mail_to_send.send()

def send_confirmation(name, email, job):
    mail_body = f"""
    <body style="font-family: Calibri;">
        <h3>Red Sea 24 Application Submission Confirmation</h3>
        <p>Dear {name},</p>
        <p>Thanks for your interest to join our <b>Red Sea 24</b> team!</p>
        <p>This is to confirm that our Recruitment Team has received your application for the position <b>{job}</b>.</p>
        <p>We will get back to you soon.</p>
        <br>
        <p>Kind Regards</p>
        <p>Red Sea 24 Recruitment Team</p>
        </body>
    """
    mail_to_send = EmailMultiAlternatives('Red Sea 24 - Application Received',
        mail_body, settings.DEFAULT_FROM_EMAIL, [email])
    
    mail_to_send.attach_alternative(mail_body, 'text/html')
    
    print('sending confirmation mail')
    result = mail_to_send.send()
    print(result)
    return result
