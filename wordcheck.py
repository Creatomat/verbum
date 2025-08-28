import nltk
import subprocess
import sys

try:
    nltk.data.find("corpora")
    wordnet_exists = True
except LookupError:
    wordnet_exists = False

if wordnet_exists:
    sys.exit(0)
else:
    subprocess.run(["python3", "Six_Letter_Words.py"])
    sys.exit(0)
