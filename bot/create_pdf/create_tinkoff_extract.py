from PyPDF2 import PdfWriter, PdfReader, PdfMerger
import io

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Примерные входные данные, из бд ботика
name = 'Свинцов Даниил Дмитриевич'
first_date_registration = '12.06.2023'
first_part_period = '07.08.2023'
second_part_period = '06.06.2022'
number_agreement = '0000000001'  # тут надо чтото придумать
personal_account_number = '40817810400078617673'
lst_data_money = [
    ('18.07.2023 18:07:34', '10 133 000.00 RUB', 'Оплата в SBERMEGAMARKET . Gorod Moskva RUS', '8888'),
    ('12.07.2023 18:03:15', '-50.00 RUB', 'Оплата в MOC RIVER KHAUS Gorod Sankt-P RUS', '1234'),
    ('08.07.2023 00:37:01', '-665.00 RUB', 'Оплата в www s7 Moskva RUS', '8888')
]

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)

fname = 'a010013l'

# faceName - view a010013l.AFM file as a plain text and look at
# row beginning with 'FontName' word (it's usually the fourth row).
# The word after 'FontName' is the faceName ('URWGothicL-Book' in this case).
faceName = 'URWGothicL-Book'

# Define new Type 1 font
cyrFace = pdfmetrics.EmbeddedType1Face(fname + '.afm', fname + '.pfb')

# Create a new encoding called 'CP1251'
cyrenc = pdfmetrics.Encoding('CP1251')

# Fill in the tuple with Unicode glyphs in accordance with cp1251 (win1251)
# encoding
cp1251 = (
    'afii10051', 'afii10052', 'quotesinglbase', 'afii10100', 'quotedblbase',
    'ellipsis', 'dagger', 'daggerdbl', 'Euro', 'perthousand', 'afii10058',
    'guilsinglleft', 'afii10059', 'afii10061', 'afii10060', 'afii10145',
    'afii10099', 'quoteleft', 'quoteright', 'quotedblleft', 'quotedblright',
    'bullet', 'endash', 'emdash', 'tilde', 'trademark', 'afii10106',
    'guilsinglright', 'afii10107', 'afii10109', 'afii10108', 'afii10193',
    'space', 'afii10062', 'afii10110', 'afii10057', 'currency', 'afii10050',
    'brokenbar', 'section', 'afii10023', 'copyright', 'afii10053',
    'guillemotleft', 'logicalnot', 'hyphen', 'registered', 'afii10056',
    'degree', 'plusminus', 'afii10055', 'afii10103', 'afii10098', 'mu1',
    'paragraph', 'periodcentered', 'afii10071', 'afii61352', 'afii10101',
    'guillemotright', 'afii10105', 'afii10054', 'afii10102', 'afii10104',
    'afii10017', 'afii10018', 'afii10019', 'afii10020', 'afii10021',
    'afii10022', 'afii10024', 'afii10025', 'afii10026', 'afii10027',
    'afii10028', 'afii10029', 'afii10030', 'afii10031', 'afii10032',
    'afii10033', 'afii10034', 'afii10035', 'afii10036', 'afii10037',
    'afii10038', 'afii10039', 'afii10040', 'afii10041', 'afii10042',
    'afii10043', 'afii10044', 'afii10045', 'afii10046', 'afii10047',
    'afii10048', 'afii10049', 'afii10065', 'afii10066', 'afii10067',
    'afii10068', 'afii10069', 'afii10070', 'afii10072', 'afii10073',
    'afii10074', 'afii10075', 'afii10076', 'afii10077', 'afii10078',
    'afii10079', 'afii10080', 'afii10081', 'afii10082', 'afii10083',
    'afii10084', 'afii10085', 'afii10086', 'afii10087', 'afii10088',
    'afii10089', 'afii10090', 'afii10091', 'afii10092', 'afii10093',
    'afii10094', 'afii10095', 'afii10096', 'afii10097'
)

# Replace glyphs from code 128 to code 256 with cp1251 values
for i in range(128, 256):
    cyrenc[i] = cp1251[i - 128]

# Register newly created encoding
pdfmetrics.registerEncoding(cyrenc)

# Register type face
pdfmetrics.registerTypeFace(cyrFace)

# Register the font with adding '1251' to its name
pdfmetrics.registerFont(pdfmetrics.Font(faceName + '1251', faceName, 'CP1251'))

# Use this font and set font size
can.setFont(faceName + '1251', 10)
can.drawString(70, 690, name)
print(can.getAvailableFonts())
can.setFont("Helvetica", 9)
can.drawString(494.5, 717, first_part_period)
can.setFont("Helvetica", 8)  # заменить на OlegSans 9
can.drawString(161.5, 619, first_date_registration)
can.drawString(122, 601, number_agreement)
can.drawString(144, 583, personal_account_number)
step_low = 0
can.setFont(faceName + '1251', 9)
for transaction in lst_data_money:
    can.drawString(55, 505 - step_low, transaction[0])
    can.drawString(55, 495 - step_low, transaction[0])
    can.drawString(165, 500 - step_low, transaction[1])
    can.drawString(260, 500 - step_low, transaction[1])
    can.drawString(355, 500 - step_low, transaction[2])
    can.drawString(500, 500 - step_low, transaction[3])
    step_low += 25

can.save()

# move to the beginning of the StringIO buffer
packet.seek(0)

# create a new PDF with Reportlab
new_pdf = PdfReader(packet)
# read your existing PDF
existing_pdf = PdfReader(open("base_tinkoff_first_page.pdf", "rb"))
output = PdfWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.pages[0]
page.merge_page(new_pdf.pages[0])
output.add_page(page)
# finally, write "output" to a real fil
output.write("aaaa.pdf")
qwe = open("tinkoff_last_page.pdf", "rb")
merger = PdfWriter()
merger.append("aaaa.pdf")
merger.append(qwe)
merger.write("qweqweqwe.pdf")
merger.close()
