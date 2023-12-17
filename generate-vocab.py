#!/usr/bin/env python3

import fugashi
import regex as re

def validate_word(word):
	return (    
			not re.match(r'^\s*$', word)
			and not re.match(r'\W', word)
			and re.match(r'\p{Hiragana}|\p{Katakana}|\p{Han}', word)
			)

# The Tagger object holds state about the dictionary. 
tagger = fugashi.Tagger()
word_list = []
word_set = set() # set will remove duplicates for us

with open("_text.txt", encoding = 'utf-8') as file:

	text = file.read()

	# Get lemma (dictionary form) information
	for word in tagger(text):
		word_list += map(str, [word.feature.lemma])

	# Remove "empty words", punctuation, and non-Japanese lemmas
	for word in filter(validate_word, word_list):
		word_set.add(word)

	for word in word_set:
		print(word)
