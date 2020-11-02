import csv
import io
import math
import re

import bs4
import requests
from selenium import webdriver


def csv_writer(data):
    with open('brest3.csv', "w", newline='', encoding='utf-8') as out_file:
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
    p = []
    d = []
    itog = []
    it = ['Клапан двухпозиционный для газовых сред', 'Клапан трехпозиционный для газовых сред (ступенчатое регулирование)','Клапан двухпозиционный для жидких сред']
    r = requests.get('https://vanorro228.github.io/price_termobrest/')
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    shor = soup.findAll('div', style="display:inline;layout-flow:horizontal;")
    tab = soup.findAll('table', border="1")
    q = 0
    z = 0
    n1 = ''
    w1 = -1
    count = 0
    for s in tab:
        n = ''
        name2 = s.findAll('tr')
        w1 += 1
        for s2 in name2:
            s2 = s2.findAll('td')
            for s3 in s2:
                q += 1
                s4 = s3.find('span', class_='font5', style="font-weight:bold;")
                s3 = s3.find('span', class_='font4', style="font-weight:bold;")
                if s4 is not None:
                    if s4.text == 'Н О Р М А Л Ь Н О - О Т К Р Ы Т Ы Е':
                        z = 1
                if s3 is not None:
                    s3 = s3.text
                    if s3.split()[0][0] == 'В':
                        """if s3 is not None:
                            s3 = s3.text
                            if ''.join(s3.split()).isdigit():
                                q+=1
                                try:
                                    if re.findall('[а-я]', s3) is not None:
                                        q3 = str("{0:.2f}".format(float(math.ceil((int(''.join(s3.split())))/ 100) * 100)))
                                        p.append(q3)
                                        ##transliterate(name1 + ' ' + 'Клапан' + ' ' + n + 'Термобрест' + n1) + ' ; ' + name1 + ' ' + 'Клапан' + ' ' + n + 'Термобрест' + n1 + ' ' + 'цена, купить' + ' ; ' + name1 + ' ' + 'Клапан' + ' ' + n + 'Термобрест' + n1 +' ' + 'цена, купить ИП Рослевич И.Г.')
                                except AttributeError and ValueError and IndexError:
                                    w1 -= 1
                            else:
                                q=1"""
                        count += 1
                        if z == 1:
                            n += 'нормально открытый~'
                        if q == 2:
                            n += 'чугунный'
                        else:
                            n += 'стальной'
                        if w1 >= 3:
                            n1 = "взрывозащищённый "
                            n += 'алюминиевый'
                        else:
                            n1 = ''
                        if '**' in s3:
                            n1 += "(обычное исполнение) "
                            s3 = s3[:-3]
                        else:
                            n1 += ''
                        p.append(s3 + ',' + 'Клапан' +',' + ','.join(n.split('~')) + ','+'Термобрест')
                        n = ''
                print(z)
        z = 0
    csv_writer(p)
if __name__ == '__main__':
    parse_html()
