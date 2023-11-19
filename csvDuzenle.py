import pandas as pd

while True:
	try:
		CSV = input("CSV dosyası: ")
		table = pd.read_csv(f'raw/{CSV}.csv', encoding='utf-8')
		while True:
			row_names = table[f'{table.columns[0]}'].tolist()
			column_names = table.columns.tolist()
			print(f"Sütun Adları\n{column_names}\nSatır Adları\n{row_names}\n")
			menu_selection = int(
				input("1-) Tek Sütun Silme\n2-) Çoklu Sütun Silme\n3-) Satır Silme\n0-) Exit\nInput: "))

			if menu_selection == 1:
				column_to_delete = input("Sütun ismi: ")
				if column_to_delete in column_names:
					table.drop(column_to_delete, axis=1, inplace=True)

			elif menu_selection == 2:
				menu_selection = input("(r/l) <index>\nExample: (r 3)\nInput: ")
				command, index = menu_selection.split()
				index = int(index)
				if command.lower() == "r":
					table = table.iloc[:, :index]
				elif command.lower() == "l":
					table = table.iloc[:, (index + 1):]
				else:
					print("Hatalı giriş.")

			elif menu_selection == 3:
				index_to_delete = int(input("Silinecek değerin indeksi: "))
				table.drop(index_to_delete, inplace=True)
				print(table.head())

			elif menu_selection == 0:
				break

			else:
				print("Hatalı giriş.")

		save_path = f"refined/{CSV.replace('-raw', '-refined')}deneme.csv"
		table.to_csv(save_path, index=False, encoding='utf-8')
		print("Klasöre kaydedildi.")

	except Exception as e:
		print(f"Hata: {str(e)}")

