from datetime import date, time, datetime, timedelta
from decimal import Decimal

DATE_FORMAT = '%Y-%m-%d'
goods = {
    'Хлеб': [
        {'amount': Decimal('1'), 'expiration_date': None},
        {'amount': Decimal('1'), 'expiration_date': date(2024, 2, 2)}
    ],
    'Яйца': [
        {'amount': Decimal('2'), 'expiration_date': date(2024, 2, 5)},
        {'amount': Decimal('3'), 'expiration_date': date(2024, 2, 4)}
    ],
    'Вода': [{'amount': Decimal('100'), 'expiration_date': None}]
}


def add(items, title, amount, expiration_date=None): #
    if expiration_date:
        expiration_date = datetime.strptime(expiration_date, DATE_FORMAT).date()
        
    try:
        items[title].append({'amount': Decimal(amount), 'expiration_date': expiration_date})
    except KeyError: 
        items[title] = [{'amount': Decimal(amount), 'expiration_date': expiration_date}]


def add_by_note(items, note): # добавляет продукт в словарь goods, преобразуя текстовое описание продукта в структурированные данные;
    note = note.split()
    try:
        note[-1].split('-')
        year, month, day = note[-1].split('-')
        name = ' '.join(note[:-2])
        amount = note[-2]
        expiration_date = date(int(year), int(month), int(day))
    except ValueError:
        name = ' '.join(note[:-1])
        amount = note[-1]
        expiration_date = None
    
    if name in items:
        items[name].append({'amount': Decimal(amount), 'expiration_date': expiration_date})
    else: items[name] = [{'amount': Decimal(amount), 'expiration_date': expiration_date}]


def find(items, needle): # ищет в словаре goods заданное слово или строку и возвращает список продуктов, в названии которых есть это слово;
    res = []
    st = needle.lower()
    for keys in items:
        if st in keys.lower():
            res.append(keys)
    return res


def amount(items, needle): # возвращает количество запрошенного продукта;
    res_list = find(items, needle)
    count = []
    for key, val in items.items():
        if key in res_list:
            for j in val:
                count.append(j.get('amount'))
    return Decimal(sum(count))
    

def expire(items, in_advance_days=0): # возвращает список просроченных продуктов
    res = {}
    for key, val in items.items():
        for j in val:
            y = j.get('expiration_date')
            z = j.get('amount')
            x = date.today()
            if y != None:
                result = y - x
                if int(result.days) <= in_advance_days:
                    if key not in res:
                        res[key] = [int(z)]
                    else: res[key].append(int(z))
    a = [(k, Decimal(sum(v))) for k, v in res.items()]
    return a

print('--- add ---')
add(goods, 'Яйца Фабрики №1', Decimal('3'), '2023-10-15')
add(goods, 'Макароны завода №55', Decimal('3'))
add(goods, 'Макароны завода №55', Decimal('3'), None)
print('--- add ---')
print()
print('--- amount ---')
print(amount(goods, 'яйца')) # Вывод: 1
print(amount(goods, 'морковь')) # Вывод: 5
print('--- amount ---')
print()
print('--- expire ---')
print(expire(goods)) # Вывод: [('Хлеб', Decimal('1'))]
print(expire(goods, 1))# Вывод: [('Хлеб', Decimal('1')), ('Яйца', Decimal('3'))]
print(expire(goods, 2))# Вывод: [('Хлеб', Decimal('1')), ('Яйца', Decimal('5'))] 
print('--- expire ---')
print()
print('--- test - test ---')

for k, v in goods.items():
    print(k, v)