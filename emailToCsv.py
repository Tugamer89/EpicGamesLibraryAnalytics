import os
import re
import csv
from email import policy
from bs4 import BeautifulSoup
from email.parser import BytesParser

def convert_date(date):
    day, month, year = date.split(" ")
    month_numbers = {
        "gen": "01", "feb": "02", "mar": "03", "apr": "04", "mag": "05", "giu": "06", "lug": "07", "ago": "08", "set": "09", "ott": "10", "nov": "11", "dic": "12",
        "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06", "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12",
    }
    return f"{day}/{month_numbers[month[0:3]]}/{year}"

def extract_html_from_eml(eml_path):
    with open(eml_path, 'rb') as eml_file:
        msg = BytesParser(policy=policy.default).parse(eml_file)

    html_content = None
    for part in msg.iter_parts():
        if part.get_content_type() == 'text/html':
            html_content = part.get_payload(decode=True)
            break

    return html_content

def process_eml_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".eml"):
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0].split(' ')[-1] + ".html"
            output_path = os.path.join(output_folder, output_filename)

            html_content = extract_html_from_eml(input_path)

            if html_content:
                with open(output_path, 'wb') as html_file:
                    html_file.write(html_content)

def parse_new_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        order_info_div = soup.select_one('table[style="width: 100%;word-wrap:break-word;overflow-wrap:break-word;word-break:break-word;font-size:16px;line-height:24px;border-spacing:0;margin-bottom:20px;border-top:1px solid #e2e3e4;"]')
        if order_info_div is None:
            order_info_div = soup.select_one('table[style="width: 100%;font-size:16px;line-height:24px;border-spacing:0;margin-bottom:20px;border-top:1px solid #e2e3e4;"]')
        order_info_div_rows = order_info_div.find_all('tr')
        order_id = order_info_div_rows[2].find_all('td')[0].text.strip()
        order_date = order_info_div_rows[4].find_all('td')[0].text.strip()

        order_items = soup.select_one('table[style="width: 100%;border-spacing: 0;margin-bottom: 20px;border-top: 1px solid #e2e3e4;"]')
        rows = order_items.find_all('tr')[1:]
        items_info = []

        for row in rows:
            columns = row.find_all('td')
            description = columns[0].text.strip()
            distributor = columns[1].text.strip()
            price_text = columns[2].text.strip()
            price_match = re.search(r'\d+\.\d{2}', price_text)
            price = price_match.group() if price_match else None

            items_info.append([description, distributor, price])

        return order_id, order_date, items_info

def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        order_id = soup.find('td', class_='wrapword order-info-value').text.strip()
        order_date = soup.find_all('td', class_='wrapword order-info-value')[1].text.strip()
        if not re.search(r'\b\d{1,2}\s(?:gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s\d{4}\b', order_date):
            order_date = soup.find_all('td', class_='wrapword order-info-value')[2].text.strip()

        order_items = soup.find('table', class_='order-item')
        rows = order_items.find_all('tr')[1:]
        items_info = []

        for row in rows:
            columns = row.find_all('td')
            description = columns[0].text.strip()
            distributor = columns[1].text.strip()
            price_text = columns[2].text.strip()
            price_match = re.search(r'\d+\.\d{2}', price_text)
            price = price_match.group() if price_match else None

            items_info.append([description, distributor, price])

        return order_id, order_date, items_info

def parse_old_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        order_info_div = soup.select_one('div[style="font-family:Ariel, Helvetica, sans-serif; mso-line-height-rule: exactly; font-size:16px; color:#313131; text-align:left; line-height:24px"]')

        order_id = order_info_div.text.strip().split('\n')[1].replace('\t', '')
        order_date = order_info_div.text.strip().split('\n')[-1].replace('\t', '')

        items_info = []
        description_div = soup.select_one('div[style="font-family:Ariel, Helvetica, sans-serif; mso-line-height-rule: exactly; font-size:14px; color:#313131; text-align:left; line-height:20px; word-break:break-all; padding:5px 5px 5px 0"]')
        distributor = description_div.find_next('div').text.strip()
        price = soup.select_one('div[style="font-family:Ariel, Helvetica, sans-serif; mso-line-height-rule: exactly; font-size:14px; color:#313131; text-align:right; line-height:20px; word-break:break-all; padding:5px 0 5px 0"]').text.strip().split(' ')[-1]

        items_info.append([description_div.text.strip(), distributor, price])

        return order_id, order_date, items_info

def process_html_files(folder_path, csv_file_path):
    existing_orders = set()
    exists = False

    if os.path.exists(csv_file_path):
        exists = True
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for row in csv_reader:
                order_id, order_date, distributor = row[:3]
                existing_orders.add((order_id, order_date, distributor))

    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        if not exists:
            csv_writer.writerow(['Order ID', 'Date', 'Description', 'Distributor', 'Price'])

        for filename in os.listdir(folder_path):
            if filename.endswith(".html"):
                file_path = os.path.join(folder_path, filename)
                try:
                    order_id, order_date, items_info = parse_html(file_path)
                except:
                    try:
                        order_id, order_date, items_info = parse_old_html(file_path)
                    except:
                        order_id, order_date, items_info = parse_new_html(file_path)

                order_date = convert_date(order_date)
                for item_info in items_info:
                    if (order_id, order_date, item_info[0]) not in existing_orders:
                        csv_writer.writerow([order_id, order_date] + item_info)
                        existing_orders.add((order_id, order_date, item_info[1]))


if __name__ == "__main__":
    emls_folder = './emls'
    htmls_folder = './htmls'
    output_csv = 'output.csv'
    process_eml_files(emls_folder, htmls_folder)
    process_html_files(htmls_folder, output_csv)
