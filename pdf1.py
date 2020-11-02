import csv
import io
import math
import re

import bs4
import requests
from selenium import webdriver


def csv_writer(data):
    with open('brest2.csv', "w", newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        for row in data:
            writer.writerow([row])


def transliterate(name):
    slovar = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
              'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
              'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'yu', 'ф': 'f', 'х': 'h',
              'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sht', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
              'ю': 'u', 'я': 'ya', 'А': 'a', 'Б': 'b', 'В': 'v', 'Г': 'g', 'Д': 'd', 'Е': 'e', 'Ё': 'yo',
              'Ж': 'zh', 'З': 'z', 'И': 'i', 'Й': 'y', 'К': 'k', 'Л': 'l', 'М': 'm', 'Н': 'n',
              'О': 'o', 'П': 'p', 'Р': 'r', 'С': 's', 'Т': 't', 'У': 'u', 'Ф': 'f', 'Х': 'h',
              'Ц': 'c', 'Ч': 'ch', 'Ш': 'sh', 'Щ': 'sht', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
              'Ю': 'yu', 'Я': 'ya', 'A': 'а', 'B': 'b', 'V': 'v', 'G': 'g', 'D': 'd', 'E': 'e', 'Z': 'z', 'I': 'i',
              'O': 'o', 'P': 'p', 'R': 'r', 'S': 's', 'T': 't', 'U': 'u', 'F': 'f', 'H': 'h', 'W': 'w', '" ': '-',
              'C': 'c', 'K': 'k', 'L': 'l', 'M': 'm', ',': '-', '?': '', ' ': '-', 'ґ': '', 'ї': '', ')': '',
              'Ґ': 'g', 'Ї': 'i', 'Є': 'e', 'N': 'n', ' - ': '-', '/': '-', '(': '', '.': '-', '"': ''}
    for key in slovar:
        name = name.replace(key, slovar[key])
    name = re.sub('-{2,}', '-', name)
    return name


def parse_html():
    d = ["У3.1", "У2", "УХЛ2"]
    p = []
    itog = []
    it = ['Клапан двухпозиционный для газовых сред',
          'Клапан трехпозиционный для газовых сред (ступенчатое регулирование)',
          'Клапан двухпозиционный для жидких сред']
    r = requests.get('https://vanorro228.github.io/price_termobrest/')
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    shor = soup.findAll('div', style="display:inline;layout-flow:horizontal;")
    tab = soup.findAll('tr')
    q = 1
    n1 = ''
    w1 = -1
    count = 0
    for s in tab:
        count += 1
        if count >2:
            n = ''
            name = s.findAll('td', style= 'vertical-align:bottom;')
            for i in name:
                w1+=1
                i = i.find('span', class_='font5', style="font-weight:bold;")
                if w1 %4 != 1 and i is not None and ''.join(i.text.split()).isdigit():
                    q3 = str("{0:.2f}".format(float(math.ceil((int(''.join(i.text.split()))) / 100) * 100)))
                    p.append(q3)
        ##transliterate(name1 + ' ' + 'Клапан' + ' ' + n + 'Термобрест' + n1) + ' ; ' + name1 + ' ' + 'Клапан' + ' ' + n + 'Термобрест' + n1 + ' ' + 'цена, купить' + ' ; ' + name1 + ' ' + 'Клапан' + ' ' + n + 'Термобрест' + n1 +' ' + 'цена, купить ИП Рослевич И.Г.')

        q = 0
    csv_writer(p)


if __name__ == '__main__':
    parse_html()
