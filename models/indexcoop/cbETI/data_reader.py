import openpyxl
import requests
from io import BytesIO

def read_xlsx_from_github(raw_url):
    response = requests.get(raw_url)
    response.raise_for_status()  
    workbook = openpyxl.load_workbook(BytesIO(response.content))
    sheet = workbook.active  
    headers, data = [], []
    for index, row in enumerate(sheet.iter_rows(values_only=True)):
        if index == 0:  
            headers = list(row)
        else:
            data.append(list(row))
    return headers, data
