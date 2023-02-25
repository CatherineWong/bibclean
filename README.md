### bibclean
Tested with python3.9.7.
1. Install [bibtexparser](https://bibtexparser.readthedocs.io/en/master/bibtexparser.html).
2. Usage: `python bibclean.py --bib <BIBFILE_TO_CLEAN> --aux <OUTPUT.AUX>`

Developer notes: uses the .aux result of compilation. Removes bib entries that do not appear in this .aux file; does not add citations that were not already there.