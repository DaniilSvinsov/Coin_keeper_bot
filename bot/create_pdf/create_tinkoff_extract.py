from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from add_cyrillic_font import faceName
from io import BytesIO
from time import time
from create_number_agreement import random_number_agreement
from user_transactions_data import dict_transaction_data, result_sums_money


def create_page(p: BytesIO, pdf_file: str, output_pdf_file: str) -> None:
    p.seek(0)

    new_pdf = PdfReader(p)
    existing_pdf = PdfReader(open(pdf_file, "rb"))
    output = PdfWriter()

    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    output.write(output_pdf_file)


def create_last_page():
    packet1 = BytesIO()
    can_last = canvas.Canvas(packet1, pagesize=letter)
    can_last.setFont("Helvetica", 9)
    can_last.drawString(110.5, 773.5, f'{result_sums_money[0]} RUB')
    can_last.drawString(93, 752.5, f'{result_sums_money[1]} RUB')
    can_last.save()
    create_page(packet1, "tinkoff_last_template.pdf", "tinkoff_last_page.pdf")


def create_tinkoff_add_template():
    packet_add = BytesIO()
    can_add = canvas.Canvas(packet_add, pagesize=letter)
    can_add.setFont("Helvetica", 9)
    return can_add, packet_add


def add_payment(page_template: canvas, step: int, new_page=False) -> None:
    flag = 0
    step_to_add = 0
    if new_page:
        page_template, packet_add1 = create_tinkoff_add_template()
        flag = 2
        step_to_add = 355.5

    page_template.setFont(faceName + '1251', 9)
    if transaction[0][0] == '0':
        page_template.drawString(56, 505 - step + step_to_add, transaction[0])
        page_template.drawString(56, 492.5 - step + step_to_add, transaction[0])
    else:
        page_template.drawString(55, 505 - step + step_to_add, transaction[0])
        page_template.drawString(55, 492.5 - step + step_to_add, transaction[0])
    page_template.drawString(165, 500 - step + step_to_add, transaction[1])
    page_template.drawString(260, 500 - step + step_to_add, transaction[1])
    if len(transaction[2]) >= 43:
        page_template.drawString(355, 504 - step + step_to_add, transaction[2][:21])
        page_template.drawString(355, 494 - step + step_to_add, transaction[2][21:43] + '...')
    elif len(transaction[2]) >= 21:
        page_template.drawString(355, 504 - step + step_to_add, transaction[2][:21])
        page_template.drawString(355, 494 - step + step_to_add, transaction[2][21:])
    else:
        page_template.drawString(355, 500 - step + step_to_add, transaction[2])
    page_template.drawString(500, 500 - step + step_to_add, transaction[3])
    page_template.line(56.5, 489.5 - step + step_to_add + flag, 539.5, 489.5 - step + step_to_add + flag)

    if flag == 2:
        page_template.save()
        create_page(packet_add1, "tinkoff_add_template.pdf", "tinkoff.pdf")


s = time()
packet = BytesIO()

can_first = canvas.Canvas(packet, pagesize=letter)

can_first.setFont(faceName + '1251', 10)
can_first.drawString(55, 690, dict_transaction_data['name'])

can_first.setFont('Helvetica-Bold', 11)
can_first.drawString(245, 554, dict_transaction_data['first_part_period'])
can_first.drawString(325, 554, dict_transaction_data['second_part_period'])

can_first.setFont("Helvetica", 8)  # заменить на OlegSans 9
can_first.drawString(161.5, 619, dict_transaction_data['first_date_registration'])
can_first.drawString(122, 601, dict_transaction_data['number_agreement'])
can_first.drawString(144, 583, dict_transaction_data['personal_account_number'])

can_first.setFont(faceName + '1251', 9)
can_first.drawString(66, 716, random_number_agreement)
can_first.drawString(494.5, 717, dict_transaction_data['first_part_period'])

# Проход по транзакциям взятым из бд
step_between_payments = 25
for count in range(
        (len(dict_transaction_data['lst_data_money']) + 10) // 27 + 1):  # 10 получается из (-16 + 27 - 1)
    print(count)  # и теперь сюда передается количество страниц и они будут создаваться в add_payment
    """if count > 16 and count % 17 == 0:
        add_payment('', step_between_payments * (count - 16), True)
    elif count <= 16:
        add_payment(can_first, step_between_payments * (count - 1))
    else:
        pass"""
can_first.save()

create_page(packet, "first_tinkoff_template.pdf", "first_tinkoff_page.pdf")

create_last_page()

merger = PdfWriter()
merger.append("first_tinkoff_page.pdf")
merger.append("tinkoff_last_page.pdf")
merger.write("result_tinkoff.pdf")
merger.close()

print(time() - s)
