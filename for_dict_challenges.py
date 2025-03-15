# Задание 1
# Дан список учеников, нужно посчитать количество повторений каждого имени ученика
# Пример вывода:
# Вася: 1
# Маша: 2
# Петя: 2

students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Петя'},
]
print("Задание 1")
result = {}
count = 1
for student in students:
    for key_name, name in student.items():
        if name not in result:
            result[name] = count
        elif name in result:
            result[name] += 1
for student in result:
    print(f'{student}: {result[student]}')

# Задание 2
# Дан список учеников, нужно вывести самое часто повторящееся имя
# Пример вывода:
# Самое частое имя среди учеников: Маша
students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Оля'},
]
print("Задание 2")
result = {}
count = 1
for student in students:
    for key_name, name in student.items():
        if name not in result:
            result[name] = count
        elif name in result:
            result[name] += 1

print(f'Самое частое имя среди учеников: {max(result, key=result.get)} ')


# Задание 3
# Есть список учеников в нескольких классах, нужно вывести самое частое имя в каждом классе.
# Пример вывода:
# Самое частое имя в классе 1: Вася
# Самое частое имя в классе 2: Маша

school_students = [
    [  # это – первый класс
        {'first_name': 'Вася'},
        {'first_name': 'Вася'},
    ],
    [  # это – второй класс
        {'first_name': 'Маша'},
        {'first_name': 'Маша'},
        {'first_name': 'Оля'},
    ],[  # это – третий класс
        {'first_name': 'Женя'},
        {'first_name': 'Петя'},
        {'first_name': 'Женя'},
        {'first_name': 'Саша'},
    ],
]
print("Задание 3")
result_dict = {}
class_num = 1
result = {}
count = 1
for school_classes in school_students:
    for student in school_classes:
        for key_name, name in student.items():
            if name not in result:
                result[name] = count
            else:
                result[name] += 1
            result_dict[class_num] = max(result, key=result.get)
    class_num += 1
    result = {}
            
for class_num, name in result_dict.items():
    print(f'Самое частое имя в классе {class_num}: {name}')

# Задание 4
# Для каждого класса нужно вывести количество девочек и мальчиков в нём.
# Пример вывода:
# Класс 2a: девочки 2, мальчики 0 
# Класс 2б: девочки 0, мальчики 2

school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '2б', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
    {'class': '2в', 'students': [{'first_name': 'Даша'}, {'first_name': 'Олег'}, {'first_name': 'Маша'}]},
]
is_male = {
    'Олег': True,
    'Маша': False,
    'Оля': False,
    'Миша': True,
    'Даша': False,
}
print("Задание 4")
boys = 0
girls = 0
for class_dict in school:
    for student in class_dict['students']:
        for key_name, name in student.items():
            if is_male[name] == True:
                boys += 1
            else:
                girls += 1
    
    print(f'Класс {class_dict["class"]}: девочки {girls}, мальчики {boys}')
    boys = 0
    girls = 0
    
# Задание 5
# По информации о учениках разных классов нужно найти класс, в котором больше всего девочек и больше всего мальчиков
# Пример вывода:
# Больше всего мальчиков в классе 3c
# Больше всего девочек в классе 2a

school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '3c', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
]
is_male = {
    'Маша': False,
    'Оля': False,
    'Олег': True,
    'Миша': True,
}
print("Задание 5")
result = {}
for class_dict in school:
    boys = 0
    girls = 0
    for student in class_dict['students']:
        for key_name, name in student.items():
            if is_male[name] == True:
                boys += 1
            else:
                girls += 1
    result[class_dict["class"]] = [girls, boys]
max_boys = 0
max_girls = 0
result_boys_class = ''
result_girls_class = ''
for class_num, [girls, boys] in result.items():
    if boys > max_boys:
        max_boys = boys
        result_boys_class = class_num
    if girls > max_girls:
        max_girls = girls
        result_girls_class = class_num
print(f'Больше всего мальчиков в классе {result_boys_class}')
print(f'Больше всего девочек в классе {result_girls_class}')

