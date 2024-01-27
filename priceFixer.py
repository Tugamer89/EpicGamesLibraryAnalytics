import os
import re
import sys
import csv
import time
import requests
import datetime
from bs4 import BeautifulSoup

def format_file_name(name):
    name_without_special = re.sub(r'[^\w\s]', '', name)
    formatted_name = name_without_special.replace(' ', '_').replace('"', '')
    return formatted_name

def make_google_request(query, max_times=6, ctime=0):
	while True:
		time.sleep(1.5)
		cookies = {
			"AEC": "Ackid1TvCwhptIT98ISoemXSgdRJcc3Zb1b5FkFvrgVCP9PM--HsEm3AiQ",
			"SOCS": "CAISHAgBEhJnd3NfMjAyMzExMjgtMF9SQzEaAml0IAEaBgiAoZ-rBg",
			"GOOGLE_ABUSE_EXEMPTION": "ID=d0c96d78e883a8f4:TM=1701445064:C=r:IP=79.31.126.129-:S=ljP0wMKv4qkODg3iK7H6lig"
		}

		try:
			response = requests.get(f"https://www.google.com/search?q={query}&filter=0", cookies=cookies)
			response.raise_for_status()
		except requests.exceptions.RequestException as e:
			with open("errors.txt", 'a', encoding='utf-8') as f:
				f.write(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}:\t{str(e)}\n')
			if max_times == -1:
				continue
			if ctime < max_times:
				return make_google_request(query, max_times, ctime+1)
			return None

		with open(f"./pages/page-{format_file_name(query.replace('site:egdata.app ', ''))}.html", 'w', encoding='utf-8') as f:
			f.write(response.text)
		return response.text

def extract_price(text, prefer_euro=False):
    dollar_to_euro_exchange_rate = 0.92

    if prefer_euro:
        regex = re.compile(r'((€|[Ee][Uu][Rr][Oo]?[Ss]?)\s?(\d+(,|\.)\d+))|((\d+(,|\.)\d+)\s?(€|[Ee][Uu][Rr][Oo]?[Ss]?))')
    else:
        regex = re.compile(r'((\$|[Dd][Oo][Ll][Ll][Aa][Rr][IiSs]?|[Uu][Ss][Dd]|€|[Ee][Uu][Rr][Oo]?[Ss]?)\s?(\d+(,|\.)\d+))|((\d+(,|\.)\d+)\s?(\$|[Dd][Oo][Ll][Ll][Aa][Rr][IiSs]?|[Uu][Ss][Dd]|€|[Ee][Uu][Rr][Oo]?[Ss]?))')

    match = regex.search(text)
    if match:
        value_group_1 = match.group(3) or match.group(6)
        currency_group_2 = match.group(2) or match.group(8)
        value = float(value_group_1.replace(',', '.'))

        if currency_group_2 is not None:
            if currency_group_2.upper() == 'EUR' or currency_group_2 == '€' or 'eur' in currency_group_2.lower():
                return str(round(value, 2))
            elif currency_group_2 == '$' or currency_group_2.upper() == 'USD' or 'dollar' in currency_group_2.lower():
                return str(round(value * dollar_to_euro_exchange_rate, 2))

    if prefer_euro:
        return extract_price(text, False)
    return None

def extract_price_from_web(data):
    content = make_google_request(f'site:egdata.app "{row["Description"]}" "€"', -1)
    if content and ('non ha prodotto risultati in nessun documento' not in content or 'did not match any documents' not in content):
        soup = BeautifulSoup(content, 'html.parser')
        div = soup.find('div', id='main')
        price = extract_price(str(div), True)
        if price:
            return price

    content = make_google_request(f'{row["Description"]} {row["Distributor"]} epic games')
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        div = soup.find_all('div', id='main')
        price = extract_price(str(div), True)
        if price:
            return price
    return '0.00'

def update_price(row):
    if row['Price'] != '0.00':
        return row['Price']

    new_price = extract_price_from_web(row)
    print(f"{row['Description']} _ {row['Distributor']}: {new_price}")

    if new_price:
        return new_price
    return row['Price']


if __name__ == "__main__":
    use_freeGamesList = len(sys.argv) > 1

    if not os.path.exists("./pages"):
        os.makedirs("./pages")

    with open('output.csv', 'r') as input_file:
        reader = csv.DictReader(input_file)
        rows = list(reader)

    freeGames = []
    if use_freeGamesList and os.path.exists("freeGames-list.txt"):
        with open("freeGames-list.txt", 'r') as file:
            freeGames = [line.strip() for line in file.readlines() if line.strip()]

    for row in rows:
        if row['Description'] in freeGames:
            continue
        row['Price'] = update_price(row)
        if use_freeGamesList and row['Price'] == '0.00':
            with open("freeGames-list.txt", 'a') as file:
                file.write(row['Description'] + '\n')

    fieldnames = reader.fieldnames
    with open('new_output.csv', 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
