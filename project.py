"""
Project for Week 2 of "Python Data Analysis".
This project includes functions to read from and write to CSV files.
"""

import csv

def read_csv_fieldnames(filename, separator=',', quote='"'):
    """
    Reads the field names from a CSV file.

    Args:
        filename (str): The name of the CSV file.
        separator (str): The character used to separate fields.
        quote (str): The character used to quote fields.

    Returns:
        list: A list of strings containing the field names.
    """
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=separator, quotechar=quote)
        # The fieldnames are the first row in the CSV file
        fieldnames = next(reader)
    return fieldnames


def read_csv_as_list_dict(filename, separator=',', quote='"'):
    """
    Reads a CSV file and returns its contents as a list of dictionaries.

    Args:
        filename (str): The name of the CSV file.
        separator (str): The character used to separate fields.
        quote (str): The character used to quote fields.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row.
    """
    table = []
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in reader:
            table.append(dict(row))
    return table


def read_csv_as_nested_dict(filename, keyfield, separator=',', quote='"'):
    """
    Reads a CSV file and returns its contents as a nested dictionary.
    The outer dictionary is keyed by the values in the 'keyfield' column.

    Args:
        filename (str): The name of the CSV file.
        keyfield (str): The name of the column to use as the key.
        separator (str): The character used to separate fields.
        quote (str): The character used to quote fields.

    Returns:
        dict: A nested dictionary where keys are from the keyfield column
              and values are the corresponding row dictionaries.
    """
    nested_dict = {}
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in reader:
            key = row[keyfield]
            nested_dict[key] = dict(row)
    return nested_dict


def write_csv_from_list_dict(filename, table, fieldnames, separator=',', quote='"'):
    """
    Writes a list of dictionaries to a CSV file.

    Args:
        filename (str): The name of the CSV file to write to.
        table (list): A list of dictionaries to write.
        fieldnames (list): A list of strings for the header row.
        separator (str): The character to use for separating fields.
        quote (str): The character to use for quoting fields.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=fieldnames,
                                delimiter=separator,
                                quotechar=quote,
                                quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(table)


def run_example():
    """
    A simple example to demonstrate the functionality of the CSV functions.
    This will create a sample CSV, read from it, and print the results.
    """
    # Create a sample CSV file for demonstration
    fieldnames = ['name', 'age', 'city']
    data = [
        {'name': 'Alice', 'age': '30', 'city': 'New York'},
        {'name': 'Bob', 'age': '25', 'city': 'Los Angeles'},
        {'name': 'Charlie', 'age': '35', 'city': 'Chicago'}
    ]
    write_csv_from_list_dict('sample.csv', data, fieldnames)

    # 1. Test read_csv_fieldnames
    print("Fieldnames:", read_csv_fieldnames('sample.csv'))

    # 2. Test read_csv_as_list_dict
    print("\nList of Dictionaries:", read_csv_as_list_dict('sample.csv'))

    # 3. Test read_csv_as_nested_dict
    print("\nNested Dictionary (keyed by 'name'):", read_csv_as_nested_dict('sample.csv', 'name'))

# To run the example, you can uncomment the line below.
# The grading system will import your functions, so this part won't run.
# if __name__ == "__main__":
#     run_example()