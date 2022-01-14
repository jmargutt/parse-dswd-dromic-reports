import textract
import re
import os
import click
import pandas as pd
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

# specify which tables you want to parse, their number in the report and the column names
tables = [
    {
        "title": "affected_people",
        "number": 1,
        "columns": ['location', 'barangays', 'families', 'persons']
    },
    {
        "title": "displaced_people_inside_evacuation_centers",
        "number": 2,
        "columns": ['location',
                    'number of evacuation centers (cumulative)',
                    'number of evacuation centers (now)',
                    'number of displaced families (cumulative)',
                    'number of displaced families (now)',

                    'number of displaced people (cumulative)',
                    'number of displaced people (now)']
    },
    {
        "title": "displaced_people_outside_evacuation_centers",
        "number": 3,
        "columns": ['location',
                    'number of displaced families (cumulative)',
                    'number of displaced families (now)',
                    'number of displaced people (cumulative)',
                    'number of displaced people (now)']
    },
    {
        "title": "displaced_people_total",
        "number": 4,
        "columns": ['location',
                    'number of displaced families (cumulative)',
                    'number of displaced families (now)',
                    'number of displaced people (cumulative)',
                    'number of displaced people (now)']
    },
    {
        "title": "damaged_houses",
        "number": 5,
        "columns": ['location',
                    'damaged houses',
                    'totally damaged houses',
                    'partially damaged houses']
    }
]


@click.command()
@click.option('--report', help='report to parse (.docx)')
@click.option('--dest', default='.', help='output directory')
def main(report, dest):

    if not report:
        raise ValueError("--report cannot be empty, please specify file path")

    # load report and convert to string
    text = textract.process(report)
    text = str(text)

    # loop over tables to parse
    for table_parameters in tables:
        logging.info(f"parsing table {table_parameters['number']}: {table_parameters['title']}")
        table = re.search(rf'(?<=Table {table_parameters["number"]}.)(.*)(?=Table {table_parameters["number"]+1}.)', text)
        if table:
            table = table.group()
            # remove crap at the beginning
            table = "MIMAROPA" + table.split("MIMAROPA", 1)[1]
            # remove crap at the end
            table = table.split("Note: This version", 1)[0]
            # divide by newline
            table = table.split(r'\n\n')
            # remove empty elements
            table = [x for x in table if x != '']
            # transform in list of lists, where each list is a row of length n_columns
            n_columns = len(table_parameters['columns'])
            table = [table[i:i + n_columns] for i in range(0, len(table), n_columns)]
            # map to dataframe and save as csv
            df = pd.DataFrame(table, columns=table_parameters['columns'])
            df.to_csv(os.path.join(dest, f"{table_parameters['title']}.csv"))
        else:
            logging.warning(f"table {table_parameters['number']} not found")


if __name__ == "__main__":
    main()