import argparse

from qlacref_postcodes import Postcodes


def search_postcodes(postcodes):
    pc = Postcodes()

    postcodes = [p.upper() for p in postcodes]
    letters = [p[0] for p in postcodes]

    pc.load_postcodes(letters)
    df = pc.dataframe

    for pc in postcodes:
        abbr_pc = pc.replace(' ', '')
        print(df[df.pcd_abbr == abbr_pc])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search the postcode database")
    parser.add_argument('postcodes', metavar='POSTCODE', type=str, nargs='+', help='Postcode(s) to search for')

    args = parser.parse_args()

    search_postcodes(args.postcodes)