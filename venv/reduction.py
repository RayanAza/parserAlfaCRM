import pandas as pd

# вспомогательные функции 
def find_first_number_index(s: str) -> int:
    try:
        index = s.index(next(filter(str.isdigit, s)))
        return index
    except StopIteration:
        return -1
    
def split_FCs(line: str) -> tuple:
    f_ind = find_first_number_index(line)
    fcs = line[:f_ind]
    s_ind = line.find('(')
    age = line[f_ind:s_ind]
    date_of_birth = line[s_ind+1:len(line) - 1]
    return fcs, age, date_of_birth

def find_responsible(line: str) -> str:
    return line[:line.find('Не задано')]

def find_left(line: str) -> str:
    return line[:line.find('/')], line[line.find('/')+1:]

def reduction_clients(df: pd.DataFrame) -> pd.DataFrame:
    labels = [
        'ID', 'ФИО', 'Заказчик', 'Возраст', 'Дата рождения', 'Ответственный', 'Группы', 
        'Статус обучения', 'Источник', "Общий остаток (деньги)", "Бонусный счёт", "Общий остаток (уроки)", 
        "Дата истечения оплаты", "Дата посл. посещения", "Дата след. посещения", "Предмет", "Уровень",
        "Отв. педагог", "Телефон", "E-mail", "Адрес", "Website", "Примечание", "Абонементы", "Номер договоров",
        "Добавлен", "Причина потери", "Активные группы", "Активные абонементы", "Пол", "Статус клиента"
        ]

    res = pd.DataFrame(columns=labels)
    res['ID'] = df['ID']

    fcs, age, date_of_birth = [], [], []
    for f, a, d in df['ФИО'].apply(split_FCs):
        fcs.append(f)
        age.append(a)
        date_of_birth.append(d)

    res['ФИО'] = pd.Series(fcs)
    res.insert(2, "Тип заказчика", "Физ.лицо")
    res['Заказчик'] = pd.Series(fcs)
    res['Возраст'] = pd.Series(age)
    res['Дата рождения'] = pd.Series(date_of_birth)
    res['Ответственный'] = df['Ответственный'].apply(find_responsible)
    res['Группы'] = df['Группы']
    res['Статус обучения'] = df['Статус обучения']
    res['Источник'] = df['Источник']
    
    money, number = [], []
    for m, n in df['Общий остаток'].apply(find_left):
        money.append(m)
        number.append(n)

    res['Общий остаток (деньги)'] = pd.Series(money)
    res['Бонусный счёт'] = df['Бонусный счет']
    res['Общий остаток (уроки)'] = pd.Series(number)
    res['Дата истечения оплаты'] = df['Ожидаем']
    res['Дата посл. посещения'] = df['Дата посл. посещ.']
    res['Дата след. посещения'] = pd.Series(dtype='str')
    res['Предмет'] = pd.Series(dtype='str')
    res['Уровень'] = pd.Series(dtype='str')
    res['Отв. педагог'] = df['Отв. педагог']
    res['Телефон'] = "'" + df['Контакты']
    res['E-mail'] = pd.Series(dtype='str')
    res['Адрес'] = pd.Series(dtype='str')
    res['Website'] = pd.Series(dtype='str')
    res['Примечание'] = df['Примечание']
    res['Абонементы'] = df['Абонементы']
    res['Номер договоров'] = pd.Series(dtype='str')
    res['Добавлен'] = df['Добавлен']
    res['Причина потери'] = df['Причина потери']
    res['Активные группы'] = df['Активные группы']
    res['Активные абонементы'] = df['Активные абонементы']
    res['Пол'] = df['Пол']
    # res['Статус клиента'] = df['Статус Клиента']
    res = res.fillna('')
    
    return res

def str_to_float(line: str) -> float:
    return float(line.replace(',', '.').replace(u'\xa0', '')) 

def reduction_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(['Unnamed: 0'], axis=1)
    df['Сумма'] = df['Сумма'].apply(str_to_float)
    df = df.fillna('')
    return df

def first_color(line: str) -> str:
    return line.split()[0]

def status_of_group(line: str) -> str:
    if len(line.split()) % 2 == 0:
        return 'Заполнена'
    return 'Идет набор'

def reduction_groups(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(['Unnamed: 0', 'Unnamed: 16'], axis=1)
    df = df.fillna('')
    df['Статус'] = df['Статус'].apply(status_of_group)
    df['Цвет'] = df['Цвет'].apply(first_color)
    
    return df