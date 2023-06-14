from pprint import pprint
import re
import csv

with open("src/phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

# Соритую полученный список чтобы однаковые фамилии были рядом
data = sorted(contacts_list)
# Новая переменная для данных
new_data = []
# Паттерн поиска номера телефона
pattern = r"(\+7|8)\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})\s*\(?(доб.\s*\d+)?\)?"
# Паттерн замены номера
substit = r'+7(\2)\3-\4-\5 \6'
# Цикл строк по данным
for row in data:
    # Создаю переменную для создаваемой строки
    new_row = []
    # Создаю строку Фамилия Имя Отчество из элементов row[:3]
    fullname = ' '.join(row[:3]).strip()
    # Если у пользователя нет отчества - создаю пустое отчество, записываю lastname, firstname
    if len(fullname.split(' ')) == 2:
        lastname, firstname = fullname.split(' ')
        surname = ''
    # Если отчество есть - записываю lastname, firstname, surname
    else:
       lastname, firstname, surname = fullname.split(' ')

    # Формирую новую строку из фамилии, имени и отчества
    new_row += lastname, firstname, surname
    # Добавляю в строку исходные данные без ФИО
    new_row += row[3:]
    # Заменяю элемент с номером на изменненный шаблон с номером
    new_row[5] = re.sub(pattern, substit, new_row[5]).strip()
    # Добавляю новую строку данным
    new_data.append(new_row)
    # Удаляю новую строку
    del new_row

i = 0
result = []
# Цикл поиска одинаковых строк их объединения
while i < len(new_data)-1:
    # Если Фамилия и Имя совпадают с Фамилией и Именем следующей строки - создаю новую строку объединяющую дубликаты
    if new_data[i][:2] == new_data[i+1][:2]:
        # Создаю переменную для объединенной строки
        merged_row = []
        # Цикл по элементам списка строки
        for r in range(len(new_data[i])):
            # Если элемент отсутсвует - беру элемент из дубликата строки
            if new_data[i][r] == '' or new_data[i][r] is None:
                # Обрабатываю ошибку IndexError, которая возникает из-за разного количества элементов в строках
                try:
                    # Добавляю в строку существуеющий элемент из дубликата строки
                    merged_row.append(new_data[i+1][r])
                except IndexError:
                    pass
            else:
                # Иначе добавляю элемент из оригинальной строки
                merged_row.append(new_data[i][r]) 
        # Добавляю вновь созданную строку в результат
        result.append(merged_row)
        i += 2
    else:
        # Иначе если дубликатов нет - добавляю оригинальную строку в результат
        result.append(new_data[i])
        i += 1
# Добавляю в результат последний элемент, который не вошел в цикл
result.append(new_data[-1])

# Создаю файл и записываю туда результат
with open("out/phonebook.csv", "w", encoding='utf-8', newline='') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(result)