import re
import spacy
import fr_core_news_sm
from spacy.lang.fr import French
import time

### Fonctions de base

def read_file(file):

    with open(file, 'r', encoding='utf-8') as f:
        return f.read()
    

def output(tokens, output_file):

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<text>\n')
        for i, token in enumerate(tokens):
            cleaned_token = token.strip()
            f.write(f'<token id="{i}">{cleaned_token}\n</token>\n')
        f.write('</text>')

##### Découpage en phrases #####
        
### 1.1

def decoupe_phrases_regex(fichier):

    texte = read_file(fichier)
    phrases = re.findall(r'[^\.|\!|\?\n]+[\.|\!|\?\n]', texte)

    return phrases

### 1.2.1

def decoupe_phrases_spacy(fichier):

    nlp = French()
    nlp.add_pipe('sentencizer')
    texte = read_file(fichier)
    doc = nlp(texte)
    phrases = [phrase.text for phrase in doc.sents]

    return phrases


### 1.2.2


def decoupe_phrases_spacy_senter(fichier):
    
        nlp = fr_core_news_sm.load()
        texte = read_file(fichier)
        doc = nlp(texte)
        phrases = [phrase.text for phrase in doc.sents]
    
        return phrases

# Mesure de temps

print('Mesure de temps : Découpage en phrases\n\n')

start = time.time()
output(decoupe_phrases_regex('./conte.txt'), 'o_regex_phrases.xml')
end = time.time()
print(f"Temps d'exécution regex: {end - start} secondes")

start = time.time()
output(decoupe_phrases_spacy('./conte.txt'), 'o_spacy_phrases.xml')
end = time.time()
print(f"Temps d'exécution spacy: {end - start} secondes")

start = time.time()
output(decoupe_phrases_spacy_senter('./conte.txt'), 'o_spacy_senter_phrases.xml')
end = time.time()
print(f"Temps d'exécution spacy_senter: {end - start} secondes")



##### Découpage en mots #####


### 2.1

def decoupe_mots_regex(fichier):
   
    texte = read_file(fichier)
    mots = re.findall(r'[A-Za-zÀ-ÖØ-öø-ž]+', texte)

    return mots

# Mesure de temps

print('\n\nMesure de temps : Découpage en mots\n\n')

start = time.time()
output(decoupe_mots_regex('./phrase.txt'), 'o_regex_mots.xml')
end = time.time()
print(f"Temps d'exécution regex: {end - start} secondes")

output(decoupe_mots_regex('./conte.txt'), 'o_regex_mots_conte.xml')

### 2.2

import nltk

from nltk.tag import StanfordPOSTagger
from textblob import TextBlob

start = time.time()
tokenizer = nltk.data.load('/home/kali/nltk_data/tokenizers/punkt/french.pickle')
words_generator = tokenizer._tokenize_words("Depuis huit jours, j'avais déchiré mes bottines Aux cailloux des chemins. J'entrais à Charleroi. - Au Cabaret-Vert : je demandai des tartines De beurre et du jambon qui fût à moitié froid.")
words = [word for word in words_generator]
end = time.time()
print(f"Temps d'exécution nltk: {end - start} secondes")
# print(words) # --> résultats corrects, apostrophes incluses donc mauvaise segmentation, mais les mots sont bien séparés. les types des mots ne sont pas indiqués, et si ils le sont, ces types sont incorrects. 

### 2.3 spacy tokenization

def decoupe_mots_spacy(fichier):
    nlp = spacy.load('fr_core_news_sm')
    texte = read_file(fichier)
    doc = nlp(texte)
    mots = [mot.text for mot in doc]

    return mots

start = time.time()
output(decoupe_mots_spacy('./conte.txt'), 'o_spacy_mots.xml')
end = time.time()
print(f"Temps d'exécution spacy: {end - start} secondes")


### 2.4 Tokéniseur custom


def output_mots_phrases_regex(phrases, output_file):

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<text>\n')
        for i, phrase in enumerate(phrases):
            f.write(f'<sentence id="{i}">\n')
            mots_phrase = re.findall(r'[A-Za-zÀ-ÖØ-öø-ž]+', phrase)
            for j, mot in enumerate(mots_phrase):
                f.write(f'<mot id="{j}">{mot}\n</mot>\n')
            f.write('</sentence>\n')
        f.write('</text>')



def output_mots_phrases_spacy(phrases, output_file):

    nlp = spacy.load('fr_core_news_sm')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<text>\n')
        for i, phrase in enumerate(phrases):
            f.write(f'<sentence id="{i}">\n')

            doc = nlp(phrase)
            mots_phrase = [mot.text for mot in doc]

            for j, mot in enumerate(mots_phrase):
                f.write(f'<mot id="{j}">{mot}\n</mot>\n')
            f.write('</sentence>\n')
        f.write('</text>')

# Mesure de temps

print('\n\nMesure de temps : Découpage en mots et phrases\n\n')

start = time.time()
output_mots_phrases_regex(decoupe_phrases_regex('./conte.txt'), 'o_regex_mots_phrases.xml')
end = time.time()
print(f"Temps d'exécution regex: {end - start} secondes")

start = time.time()
output_mots_phrases_spacy(decoupe_phrases_spacy('./conte.txt'), 'o_spacy_mots_phrases.xml')
end = time.time()
print(f"Temps d'exécution spacy: {end - start} secondes")



##### Annotation morphosyntaxique #####


def output_mots_phrases_spacy_morpho(phrases, output_file):

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<text>\n')
        for i, phrase in enumerate(phrases):
            f.write(f'<sentence id="{i}">\n')

            nlp = spacy.load('fr_core_news_sm')
            doc = nlp(phrase)

            for j, mot in enumerate(doc):
                f.write(f'<mot id="{j}" pos="{mot.pos_}">{mot.text}\n</mot>\n')
            f.write('</sentence>\n')
        f.write('</text>')

# Mesure de temps
        
print('\n\nMesure de temps : Annotation morphosyntaxique\n\n')

start = time.time()
output_mots_phrases_spacy_morpho(decoupe_phrases_spacy('./conte.txt'), 'o_spacy_mots_phrases_morpho.xml')
end = time.time()
print(f"Temps d'exécution spacy: {end - start} secondes")