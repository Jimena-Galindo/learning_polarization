# Processing data
# files to build:
part1 = data/clean/part1.csv
part2 = data/clean/part2.csv
all = data/clean/all.csv

clean_data = 

clean_data += $(part1)
clean_data += $(part2)
clean_data += $(all)

$(part1) $(part2) $(all): data/raw/Part1_2023-06-05.csv data/raw/Part2_2023-06-05.csv data/raw/Part1_2023-06-08_1.csv data/raw/Part2_2023-06-08_1.csv data/scripts/clean_data.py
	@echo "Cleaning our first file!"
	python data/scripts/clean_data.py

clean_data: $(clean_data)
	@echo "Data is now clean!"