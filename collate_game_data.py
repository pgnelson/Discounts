import os
import statistics
outfile = open("steam_dat.txt", 'w')
print("game_name", "date", "day_num", "owners", "price", "ch_sales", "percent_ch_sales", "discount", "discount_duration", "rolling_average", sep = "\t", file = outfile)

os.chdir("#DIRECTORY#/steam_sales/")
for filename in os.listdir("#DIRECTORY#/steam_sales/"):
	curr_file = open(filename, 'r')
	line_num= 0
	prev_owners = 0
	original_price = 0
	game_name = filename.split(".")[0]
	sale_duration = 0
	owners_window = []
	for line in curr_file:
		date = 0
		owners = 0
		price = 0
		line = line.strip()
		line = line.replace('"', '')
		if line_num>0:
			items = line.split(",")
			date = items[0]

			try:
				owners = int(items[1])
			except:
				owners = 0
			try:
				price = float(items[5])
			except:
				price = 0
			ch_sales = owners - prev_owners
			print(game_name, price, prev_owners, original_price, sep = "\t")

			if original_price == 0 and price > 0:
				original_price = price
			if price > original_price:
				original_price = price
			if prev_owners > 0 and original_price > 0 and owners > 0 and price > 0:

				owners_window.append(owners)
				rolling_average = 'NA'
				if len(owners_window)>=30:
					owners_window.pop(0)
					rolling_average = statistics.mean(owners_window)
				percent_ch_sales = ch_sales / prev_owners
				discount = 1 - price / original_price
				if discount > 0:
					if discount_duration == "NA":
						discount_duration = 1
					else:
						discount_duration+=1
						if discount_duration > 20:
							original_price = price
							discount_duration = 0
				else:
					discount_duration = "NA"
				print(game_name, date, line_num, owners, price, ch_sales, percent_ch_sales, discount, discount_duration, rolling_average, sep = "\t", file = outfile)
			prev_owners = owners
		line_num+=1
