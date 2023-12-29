import subprocess
import nltk

#install bs4 and requests
subprocess.run(['pip', 'install', 'requests'])
subprocess.run(['pip', 'install', 'bs4'])
subprocess.run(['pip', 'install', 'ingredient-parser-nlp'])

# Download NLTK resources
nltk.download('averaged_perceptron_tagger')
