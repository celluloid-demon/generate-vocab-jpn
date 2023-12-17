#!/usr/bin/env python3

import os
import parse
import requests as req

search_words = ["Luffy", "Zoro", "Nami", "Sanji", "Chopper"]
img_dir = "./images/"

for word in search_words:
	dir_path = img_dir + word

	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

urlKeyword = parse.quote(word)
url = 'https://www.google.com/search?hl=jp&q=' + urlKeyword + '&btnG=Google+Search&tbs=0&safe=off&tbm=isch'
headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}
request = req.Request(url=url, headers=headers)
page = req.urlopen(request)
html = page.read().decode('utf-8')
