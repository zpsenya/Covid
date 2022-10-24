import datetime

from fpdf import FPDF


class PDF(FPDF):
    pass


def create_pdf(name: str, surname: str, status: bool, email: str):
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.output(f'{name} {surname} {datetime.datetime.now()}.pdf')


create_pdf('ad', 'asd', False, 'sd')
