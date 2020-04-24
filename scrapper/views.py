import pandas as pd
import pdfquery

from os import listdir
from os.path import isfile, join
from django.shortcuts import render
from .forms import URLForm


def index(request):
    form = URLForm()
    content = {'form': form}
    return render(request, 'scrapper/index.html', content)

def scrapper(request):

    if request.method == 'POST':

        url = URLForm(request.POST)
        if url.is_valid():
            path = url.cleaned_data['url']

            files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

            df = scrap(files)

            content = {'data_frame': df}

            return render(request, 'scrapper/data.html', content)

        else:

            return render(request, 'scrapper/index.html')


def scrap(files):
    invoice_data = {"Invoice Number": [],
                    "Date": [],
                    "Total": [],
                    "Country": [],
                    "Note": []}

    for i in files:
        pdf = pdfquery.PDFQuery(i)
        pdf.load()

        invoice_data["Invoice Number"].append(
            clean_text_data(pdf.pq('LTTextLineHorizontal:contains("Invoice Number")').text()))

        invoice_data["Date"].append(clean_text_data(pdf.pq('LTTextLineHorizontal:contains("Date")').text()))

        invoice_data["Total"].append(clean_text_data(pdf.pq('LTTextLineHorizontal:contains("Total")').text()))

        invoice_data["Country"].append(clean_text_data(pdf.pq('LTTextLineHorizontal:contains("Country")').text()))

        invoice_data["Note"].append(clean_text_data(pdf.pq('LTTextLineHorizontal:contains("NOTE")').text()))

    columns = ["Invoice Number", "Date", "Total", "Country", "Note"]

    pdata = pd.DataFrame.from_dict(invoice_data)
    pdata = pdata[columns]

    return pdata

def clean_text_data(text):
    return text.split(':')[1].strip()