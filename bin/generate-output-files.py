#!/usr/bin/env python
import hashlib

import pandas as pd
import logging
import re
import sys

from pathlib import Path
from zipfile import ZipFile

logger = logging.getLogger(__name__)

root_dir = Path(__file__).parent.parent

columns = ['pcd', 'oseast1m', 'osnrth1m', 'laua']


def main(input_file=None):
    if input_file is None:
        file_list = list((root_dir / "source").glob("*.zip"))
        if len(file_list) > 1:
            logger.error("Multiple input files found. Quitting.")
            sys.exit(10)
        input_file = file_list[0]

    ptn = re.compile(".*NSPL_.*_UK.csv")
    df = None
    with ZipFile(input_file, 'r') as zipObject:
        listOfFileNames = zipObject.namelist()
        for fileName in listOfFileNames:
            if ptn.match(fileName):
                with zipObject.open(fileName) as file:
                    print("Parsing", fileName)
                    df = pd.read_csv(file, usecols=columns, low_memory=False)

    if df is None:
        print("No postcode file found in Zip")
        sys.exit(20)

    df['first_letter'] = df['pcd'].str[0]
    for letter in df['first_letter'].unique():
        letter_codes = df[df.first_letter == letter]
        del letter_codes['first_letter']
        print(f"Writing {letter_codes.shape[0]} entries for the letter {letter}.")

        zip_filename = root_dir / f"qlacref_postcodes/postcodes_{letter}.pickle.gz"
        letter_codes.to_pickle(zip_filename)


    with open(root_dir / "qlacref_postcodes/hashes.txt", 'wt') as file:
        file.writelines([f"{k}: {v}\n" for k, v in hashes.items()])

        # zip_filename = root_dir / f"qlacref_postcodes/postcodes_{letter}.json.gz"
        # letter_codes.to_json(zip_filename, orient="records")


if __name__ == "__main__":
    main()
