# Spelling-corrector
Python spelling corrector that generates corrected versions of misspelled words using Bayes' Rule calculating likelihood and prior probabilities.

Requirements: Python3+, 'corpus.txt' file (Moodle did not allow to upload more than 1mb.)
How to run:
> python3 spell_correction.py PARAM1 PARAM2

PARAM1: Essential, meaning which file includes misspelled words seperated by newlines.  
PARAM2: File path for correct versions of misspelled words seperated by newlines:
   If you do not give it, program still generates the results of both version to corresponding files. If you give it, program also calculates accuracy percentages for both versions and log it to the command line.
