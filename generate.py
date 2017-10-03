#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from bs4 import BeautifulSoup
import urllib.request as urllib2
import pandas as pd

URL = "http://hanzidb.org/character-list/by-frequency?page={0}"

def scrape_page(page_num):
    page = urllib2.urlopen(URL.format(page_num))
    soup = BeautifulSoup(page, 'lxml')
    entries = []

    table = soup.find('table')

    for row in table.findAll('tr'):
        entry = {}
        cells = row.findAll('td')

        if len(cells) == 8:
            radical = ''
            radical_code = ''

            if len(cells[3].findAll(text=True)) > 0:
                radical = cells[3].findAll(text=True)[0]
                radical_code = cells[3].findAll(text=True)[1].replace(u'\xa0', '')

            entry = {
                'frequency_rank': cells[7].find(text=True),
                'charcter': cells[0].find(text=True),
                'pinyin': cells[1].find(text=True),
                'definition': cells[2].find(text=True),
                'radical': radical,
                'radical_code': radical_code,
                'stroke_count': cells[4].find(text=True),
                'hsk_levl': cells[5].find(text=True),
                'general_standard_num': cells[6].find(text=True)
            }
        else:
            continue

        entries.append(entry)

    return entries

all_entries = []

# There are 100 pages on the website.
for page_num in range(100):
    words_on_page = scrape_page(page_num)
    all_entries = all_entries + words_on_page

hanzi_db = pd.DataFrame(all_entries, columns=all_entries[0].keys())
hanzi_db.to_json('hanzi_db.json', orient='records', lines=True)

hanzi_db.set_index('frequency_rank', inplace=True)
hanzi_db.to_csv('hanzi_db.csv')
