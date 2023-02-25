"""
bibclean. Cleans one or more bib files to remove unused entries. Uses the output.aux result of compilation to determine citations. Outputs the same bib files with '_bibclean' appended.

bibclean.py --bib main.bib --aux output.aux

Requires bibtexparser (https://bibtexparser.readthedocs.io/en/master/tutorial.html)
"""
import sys
import os
import re
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--bib", type=str, help="Bib file to clean.",
)
parser.add_argument(
    "--aux", type=str, help="Aux files.",
)


def get_aux_citation_keys(args):
    with open(args.aux) as f:
        aux_lines = [l.strip() for l in f.readlines()]
    # Match: \citation{<CITE>,fodor2008lot}
    citation_keys = set()
    for l in aux_lines:
        keys = re.findall("citation{(.*)}", l)
        if len(keys) > 0:
            keys = keys[0].split(",")
        citation_keys.update(keys)
    print(f"Found {len(citation_keys)} keys.")
    return citation_keys


def clean_bibs(args, citation_keys):
    bibparser = BibTexParser()
    bibparser.ignore_nonstandard_types = False

    print(f"Now cleaning: {args.bib}")
    with open(args.bib) as bibtex_file:
        bibtex_str = bibtex_file.read()

    bib_database = bibtexparser.loads(bibtex_str, bibparser)

    clean_entries = [e for e in bib_database.entries if e["ID"] in citation_keys]

    # Clean the database.
    cleanbib_database = BibDatabase()
    cleanbib_database.entries = clean_entries

    writer = BibTexWriter()
    writer.indent = "    "  # indent entries with 4 spaces instead of one
    cleanbib = args.bibe.split(".bib")[0] + "_clean" + ".bib"
    with open(cleanbib, "w") as cleanbib_file:
        cleanbib_file.write(writer.write(cleanbib_database))

    print(f"Clean output to: {cleanbib}")


def main():
    args = parser.parse_args()
    aux_citation_keys = get_aux_citation_keys(args)
    clean_bibs(args, aux_citation_keys)


if __name__ == "__main__":
    main()
