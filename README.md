# merge-csv

Description
==========
Merge two CSV files. This is done by going through each CSV file and match with the other.
It looks by using a specific column in each CSV file to compare if there is a match. If there is no match the data is still appended, but only with the data from the current csv.
A column named 'Data' is appended to each row that indicates if the data is from both CSV 1 and CSV 2 or only CSV 1 or CSV 2.

How to use
==========
Run `python mergeCsv.py` and input the needed information.

`CSV 1`: Path to the existing file CSV 2

`CSV 1 name`: Naming CSV 1

`CSV 2`: Path to the existing file CSV 2

`CSV 2 name`: Naming CSV 2

`Output path`: Where to output the final CSV

`CSV 1 column name`: Name to look up in CSV 1

`CSV 2 column name`: Name to look up in CSV 2

`Separator`: Separator for CSV 1, CSV 2 and final CSV
