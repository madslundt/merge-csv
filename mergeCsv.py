import csv
import os
import statistics as s
import re
import difflib
import pandas as pd
import sys

def loadCSV(file_path, delimiter=','):
    f = open(file_path, 'r')
    reader = csv.DictReader(f, delimiter=delimiter)
    return reader.fieldnames, list(reader)

def findBest(csv, csv_column_name, row, row_column_name):
    filter = row[row_column_name].split(' ')
    csv_data = [csv_data for csv_data in csv if set(csv_data[csv_column_name].split(' ')).intersection(filter)]
    data = [data for data in csv if set(data[csv_column_name].split(' ')).intersection(filter)]

    best_match = None
    if len(data) > 1:
        data_names = [p[csv_column_name] for p in data]
        best_data_name = sorted(data_names, key=lambda x: difflib.SequenceMatcher(None, x, row[row_column_name]).ratio(), reverse=True)
        if best_data_name and len(best_data_name) > 0:
            best_match = [p for p in csv if p[csv_column_name] == best_data_name[0]]

    elif len(data) == 1:
        best_match = data

    return best_match

def mapCsvs(
    csv1_path,
    csv1_name,
    csv2_path,
    csv2_name,
    output_path,
    csv1_column_name='Agent',
    csv2_column_name='Name',
    separator=';'
    ):

    csv1_fieldnames, csv1 = loadCSV(csv1_path, separator)
    csv2_fieldnames, csv2 = loadCSV(csv2_path, separator)

    columns = reduce(lambda l, x: l if x in l else l+[x], (csv1_fieldnames + csv2_fieldnames + ['Data']), [])
    columns.remove(csv2_column_name)

    df = pd.DataFrame(columns = columns)

    for row in csv2:
        best_csv = findBest(csv1, csv1_column_name, row, csv2_column_name)

        csv2_data = {}
        for p in csv2_fieldnames:
            if best_csv == None and p == csv2_column_name:
                csv2_data[csv1_column_name] = row.get(p)
            elif not p == csv2_column_name:
                csv2_data[p] = row.get(p, 0)

        if best_csv == None:
            print('%s has no %s: %s'%(csv2_column_name, csv1_column_name, row[csv2_column_name]))
            csv1_data = {}
            for p in csv1_fieldnames:
                csv1_data[p] = 0

            data = dict(csv1_data)
            data.update(csv2_data)
            data[csv1_column_name] = row[csv2_column_name]
            data['Data'] = csv2_name
            df = df.append(data, ignore_index=True)
        else:
            print('%s\t => \t%s'%(best_csv[0][csv1_column_name], row[csv2_column_name]))
            for p in best_csv:
                data = p
                data.update(csv2_data)
                data['Data'] = '%s+%s'%(csv1_name, csv2_name)
                df = df.append(data, ignore_index=True)

    for row in csv1:
        best_csv = findBest(csv2, csv2_column_name, row, csv1_column_name)

        if best_csv == None:
            print('%s has no %s: %s'%(csv1_column_name, csv2_column_name, row[csv1_column_name]))

            csv_data = {}
            for p in csv2_fieldnames:
                if not p == csv2_column_name:
                    csv_data[p] = 0

            data = row
            data.update(csv_data)
            data['Data'] = csv1_name
            df = df.append(data, ignore_index=True)

    df.to_csv(output_path, sep=separator)

def main():
    csv1_path = raw_input('Enter path to CSV 1: ')
    csv1_name = raw_input('What do you want to call CSV 1 [CSV1]: ') or 'CSV1'

    csv2_path = raw_input('Enter path to CSV 2: ')
    csv2_name = raw_input('What do you want to call CSV 2 [CSV2]: ') or 'CSV2'

    output_path = raw_input('Where to output the merged CSV file? ')

    csv1_column_name = raw_input('Enter the column in CSV 1 that should be looked up: ')
    csv2_column_name = raw_input('Enter the column in CSV 2 that should be looked up: ')

    separator = raw_input('How do you separate CSV files [;]? ') or ';'

    mapCsvs(csv1_path, csv1_name, csv2_path, csv2_name, output_path, csv1_column_name, csv2_column_name, separator)


if __name__ == "__main__":
    main()