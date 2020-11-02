import csv
import xlwt
import re
import openpyxl

wb = xlwt.Workbook()
ws = wb.add_sheet("оплата", cell_overwrite_ok=True)


def transliterate(name):
    slovar = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
              'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
              'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'yu', 'ф': 'f', 'х': 'h',
              'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sht', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
              'ю': 'u', 'я': 'ya', 'А': 'a', 'Б': 'b', 'В': 'v', 'Г': 'g', 'Д': 'd', 'Е': 'e', 'Ё': 'yo',
              'Ж': 'zh', 'З': 'z', 'И': 'i', 'Й': 'о', 'К': 'k', 'Л': 'l', 'М': 'm', 'Н': 'n',
              'О': 'o', 'П': 'p', 'Р': 'r', 'С': 's', 'Т': 't', 'У': 'u', 'Ф': 'f', 'Х': 'h',
              'Ц': 'c', 'Ч': 'ch', 'Ш': 'sh', 'Щ': 'sht', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
              'Ю': 'yu', 'Я': 'ya', 'A': 'а', 'B': 'b', 'V': 'v', 'G': 'g', 'D': 'd', 'E': 'e', 'Z': 'z', 'I': 'i',
              'O': 'o', 'P': 'p', 'R': 'r', 'S': 's', 'T': 't', 'U': 'u', 'F': 'f', 'H': 'h', '" ': '-',
              'C': 'c', 'K': 'k', 'L': 'l', 'M': 'm', ',': '-', '~': '/', ' ': '-', 'ґ': '', '/': '-', '...': '-',
              'Ґ': 'g', 'Ї': 'i', 'Є': 'e', 'N': 'n', ' - ': '-', 'Ø': '', '"': ''}

    # Циклически заменяем все буквы в строке
    for key in slovar:
        name = name.replace(key, slovar[key])
    name = re.sub('-{2,}', '-', name)
    return name


def auff():
    wwb = openpyxl.load_workbook(filename='C:\\Users\\user\\Downloads\\test.xlsx')
    sheet3 = wwb['Тексты']
    vals = [v[0].value for v in sheet3['E17:E41846']]
    i = 5
    while i > 1:
        del vals[::i]
        i -= 1
    del vals[-1]
    vals = ['регулятор GIULIANI ANELLO FSDC50/CE'] + vals
    print(vals)


def csv_writer(data):
    with open('brest5.csv', "w", newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        for row in data:
            writer.writerow([row])


def csv_dict_reader(f):
    p = []
    reader = csv.DictReader(f, delimiter=';')
    for line in reader:
        p.append("https://zipgorelok.ru/catalog/" + transliterate(line["category_path"]) + "/" + line["slug"])
    for n in range(len(p)):
        for j in (range(5)):
            k = n + j
            if n > 0:
                k += 4 * n
            ws.write(k, 0, p[n])
    wb.save("url.xls")


def match(text, alphabet=None):
    if alphabet is None:
        alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789')
    return not alphabet.isdisjoint(text.lower())


def product_name(f):
    artik = []
    p = []
    d = 0
    k = []
    reader = csv.DictReader(f, delimiter=';')
    for line in reader:
       k = line['product_sku'] + '~Термобрест~' + line['category_path'].split('~')[1] + '~' + line['category_path'].split('~')[0]
       p.append(k)
    csv_writer(p)

def link(f):
    artik = []
    p = []
    d = 0
    k = []
    reader = csv.DictReader(f, delimiter=';')
    for line in reader:
        p.append("https://zipgorelok.ru/catalog/" + transliterate(line['category_path']) + '/' + line['slug'])
    for n in range(len(p)):
        ws.write(n, 0, p[n])
    wb.save("new1.xls")

if __name__ == "__main__":
    with open(r'export-product_norm.csv', 'r', encoding='utf-8', newline="") as f:
        product_name(f)
