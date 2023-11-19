import requests
from bs4 import BeautifulSoup
import csv


def get_headers():
	# İstemci Kimliği
	user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
	return {'User-Agent': user_agent}


def get_soup(url, headers):
	# Response 200 ise başarılı yanıt alır ve HTML içeriğini döndürür.
	page = requests.get(url, headers=headers)
	return BeautifulSoup(page.content, 'html.parser')


def save_to_csv(file_path, column_headers, row_datas):
	with open(file_path, mode='w', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow(column_headers)
		for row in row_datas:
			writer.writerow(row)


def get_table(page_content):
	try:
		row_datas = list()
		column_names = list()

		# Tablo başlığını alır
		table_head = page_content.find('thead')
		if table_head is None:
			table_head = page_content.find('body')
		header_rows = table_head.find_all('tr')
		for header_row in header_rows:
			header_cols = header_row.find_all('th')
			if header_cols:
				for header_col in header_cols:
					if header_col.get_text(strip=True) not in ['']:
						column_names.append(header_col.get_text(strip=True))

		# Tablo gövdesindeki satırları alır
		table_body = page_content.find('tbody')
		rows = table_body.find_all('tr')
		for row in rows:
			columns = row.find_all('td')
			if columns:
				row_data = [col.get_text(strip=True) for col in columns]
				row_datas.append(row_data)
		return column_names, row_datas

	except Exception as e:
		print("Hata: " + str(e))
		return [], []


def main():
	try:
		headers = get_headers()
		while True:
			print("1-) URL")
			print("0-) Exit")
			menu_selection = input("Bir sayı giriniz: ")
			if menu_selection == "1":
				URL = input("URL: ")
				output_file_name = URL.replace('http://', '').replace('https://', '').split('/')[0:3]
				page_content = get_soup(URL, headers)  # Ayıklanmış HTML içeriği
				column_names, rows_data = get_table(page_content)  # Sütun isimleri ve satırlardaki veriler
				print(f"Sütun sayısı: {len(column_names)}")
				print(f"Satır sayısı: {len(rows_data)} (Sütun isimleri dahil değil)")
				if not (len(column_names) == 0 and len(rows_data) == 0):
					save_to_csv(f'raw/{output_file_name}-raw.csv', column_names, rows_data)
			elif menu_selection == "0":
				break
			else:
				print("Hatalı giriş")
	except Exception as e:
		print("Hata :" + str(e))


if __name__ == "__main__":
	main()
