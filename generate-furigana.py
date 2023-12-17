#!/usr/bin/env python3

import pykakasi
kks = pykakasi.kakasi()

with open("_list.txt", encoding = 'utf-8') as f:

	for line in f:

		result = kks.convert(line)
		kana = ""

		for item in result:

			kana = kana + "{}".format(item['hira'])

		print( kana, end='' )
