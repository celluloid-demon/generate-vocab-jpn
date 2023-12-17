#!/usr/bin/env python3

import sys
import regex as re
import nagisa
import requests
import asyncio as aio

API_URL = "https://jisho.org/api/v1/search/words?keyword={}"

class ProgressBar:
    def __init__(self, high, size=50):
        self.high = high
        self.value = 0
        self.size = size

    def __str__(self):
        s = "|"
        s += ((20 * self.value) // self.high) * "█"
        s += ((20 * (self.high - self.value)) // self.high) * " "
        s += "|"
        s += " {}%".format(round(100 * self.value / self.high, 2))

        return s

    def increment(self):
        self.value += 1
        sys.stdout.write("\r{}".format(str(self)))
        sys.stdout.flush()
        

def validate_term(term):
    return (    
            not re.match(r'^\s*$', term)
            and not re.match(r'\W', term)
            and re.match(r'\p{Hiragana}|\p{Katakana}|\p{Han}', term)
            )


async def get_meaning(dictionary, term, progress_bar):
    data = requests.get(API_URL.format(term)).json()['data'][0]

    word     = data['japanese'][0]['word']
    # reading  = data['japanese'][0]['reading']
    # meanings = [x['english_definitions'][0] for x in data['senses']]

    # edit
    dictionary[term] = {'word': word}

    progress_bar.increment()


async def main(meanings):
    words = set()

    with open(sys.argv[1], 'r') as file:
        content = file.read()
        for term in filter(
                validate_term,
                nagisa.wakati(content)):
            words.add(term)

    print("Extracted {} words".format(len(words)))

    progress_bar = ProgressBar(len(words))
    coroutines = [get_meaning(meanings, term, progress_bar) for term in words]
    await aio.wait(coroutines)
    print("\nDone.")


if __name__ == '__main__':
    event_loop = aio.get_event_loop()
    try:
        meanings = {}
        event_loop.run_until_complete(main(meanings))
        for term, data in meanings.items():
            print(term, data)

    finally:
        event_loop.close()
