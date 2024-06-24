"""
Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в
текстовом файле
3. Пользователь может ввести одну из
характеристик для поиска определенной
записи(Например имя или фамилию
человека)
4. Использование функций. Ваша программа
не должна быть линейной
 
Дополнить телефонный справочник возможностью изменения и удаления данных.
Пользователь также может ввести имя или фамилию, и Вы должны реализовать функционал
для изменения и удаления данных.
 
Дополнить справочник возможностью копирования данных из одного файла в другой. Пользователь вводит номер строки, которую необходимо перенести из одного файла в другой.

реализовать копирование данных из файла А в файл B.
написать отдельную функцию copy_data:
прочитать список словарей (read_file)
и записать его в новый файл используя функцию standart_write
дополнить функцию main
"""
 
from csv import DictReader, DictWriter
from os.path import exists
 
class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt
 
def get_info():
    flag = False
    while not flag:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise NameError("Слишком короткое имя")
            second_name = input("Введите фамилию: ")
            if len(second_name) < 4:
                raise NameError("Слишком короткая фамилия")
            phone_number = input("Введите номер телефона: ")
            if len(phone_number) < 11:
                raise NameError("Слишком короткий номер телефона")
        except NameError as err:
            print(err)
        else:
            flag = True
    return [first_name, second_name, phone_number]
 
def create_file(file_name):
    with open(file_name, "w", encoding="utf-8", newline="") as data:
        f_w = DictWriter(data, fieldnames=['first_name', 'second_name', 'phone_number'])
        f_w.writeheader()
 
def write_file(file_name):
    user_data = get_info()
    res = read_file(file_name)
    new_obj = {'first_name': user_data[0], 'second_name': user_data[1], 'phone_number': user_data[2]}
    res.append(new_obj)
    standart_write(file_name, res)
 
def read_file(file_name):
    with open(file_name, encoding="utf-8") as data:
        f_r = DictReader(data)
        return list(f_r)
 
def remove_row(file_name):
    search = int(input("Введите номер строки для удаления: "))
    res = read_file(file_name)
    if search <= len(res):
        res.pop(search - 1)
        standart_write(file_name, res)
    else:
        print("Введен неверный номер")
 
def search_record(file_name):
    attribute = input("Введите характеристику для поиска (first_name или second_name): ").strip()
    value = input(f"Введите значение для поиска по {attribute}: ").strip()
    res = read_file(file_name)
    found = [entry for entry in res if entry.get(attribute) == value]
 
    if found:
        print("Найдены следующие записи:")
        for entry in found:
            print(entry)
    else:
        print(f"Записи с {attribute} = {value} не найдены.")
 
def standart_write(file_name, res):
    with open(file_name, "w", encoding="utf-8", newline="") as data:
        f_w = DictWriter(data, fieldnames=['first_name', 'second_name', 'phone_number'])
        f_w.writeheader()
        f_w.writerows(res)
 
def copy_data(source_file, target_file):
    source_data = read_file(source_file)
    row_number = int(input("Номер строки для копирования: "))
    if row_number <= len(source_data):
        row_to_copy = source_data[row_number - 1]
        if not exists(target_file):
            create_file(target_file)
        target_data = read_file(target_file)
        target_data.append(row_to_copy)
        standart_write(target_file, target_data)
        print("Успешно скопировано.")
    else:
        print("Неверный номер строки")
 
file_name = "phone.csv"
target_file_name = "phone2.csv"
 
def main():
    while True:
        command = input("Введите команду: ")
        if command == "q":
            break
        elif command == "w":
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name)
        elif command == "r":
            if not exists(file_name):
                print("Файл отсутствует, пожалуйста создайте его")
                continue
            print(*read_file(file_name))
        elif command == "d":
            if not exists(file_name):
                print("Файл отсутствует, пожалуйста создайте его")
                continue
            remove_row(file_name)
        elif command == "s":
            if not exists(file_name):
                print("Файл отсутствует, пожалуйста создайте его")
                continue
            search_record(file_name)
        elif command == "c":
            if not exists(file_name):
                print("Исходный файл отсутствует, пожалуйста создайте его")
                continue
            copy_data(file_name, target_file_name)
 
main()
