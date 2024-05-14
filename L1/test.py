import re
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

def parse_js_code(file_path):
    with open(file_path, "r") as file:
        js_code = file.read()
    pattern = r"\+\+|--|===|!==|==|!=|<=|>=|&&|\|\||\+=|-=|\*=|\/=|%=\*\*=|<<=|>>=|>>>=|&=|\|=|\^=|(?<![\+\-*/=()])=(?!=)|[+\-*/%&|^<>~!?:,;.{}()[\]]"
    # Находим все операторы в JavaScript коде
    operators = re.findall(pattern, js_code)
    return operators


def find_function_calls(file_path):
    with open(file_path, "r") as file:
        js_code = file.read()
    # Регулярное выражение для поиска вызовов функций
    pattern = r"\b(\w+)\s*\("

    # Находим все совпадения
    matches = re.findall(pattern, js_code)

    # Возвращаем уникальные имена функций
    return matches


js_file_path = "/home/abobus/test/file.js"

function_calls = find_function_calls(js_file_path)

javascript_operators = parse_js_code(js_file_path)
# Вывод списка операторов
print("Список операторов JavaScript:")
print(javascript_operators)

# print("Имена функций и методов:")
# for name in names:
#     print(name)

# print("Вызовы функций:")
# for function_call in function_calls:
#     print(function_call)

oper_dict_for_search = dict(Counter(javascript_operators))

operators = dict(Counter(function_calls + javascript_operators))
sorted_operators = dict(sorted(operators.items(), key=lambda item: item[0]))
print("Операторы:")
for key, value in sorted_operators.items():
    print(key, ":", value)

# Список ключевых слов на JavaScript
javascript_keywords = [
    "break",
    "case",
    "catch",
    "class",
    "const",
    "continue",
    "debugger",
    "default",
    "delete",
    "do",
    "else",
    "export",
    "extends",
    "finally",
    "for",
    "function",
    "if",
    "import",
    "in",
    "instanceof",
    "new",
    "return",
    "super",
    "switch",
    "this",
    "throw",
    "try",
    "typeof",
    "var",
    "void",
    "while",
    "with",
    "yield",
]


def is_valid_operand(operand):
    # Функция для проверки валидности операнда
    # Здесь можно добавить дополнительные условия,
    # если необходимо исключить определенные операнды
    return operand.isidentifier() and operand not in javascript_keywords


def operand_search():
    operands_and_values = []
    with open(js_file_path, "r") as file:
        js_code = file.read()
        # Пройдемся по каждому оператору и найдем операнды слева и справа от него
        for operator, _ in oper_dict_for_search.items():
            if operator == ".":
                continue
            positions = [pos for pos, char in enumerate(js_code) if char == operator]
            for pos in positions:
                # Найдем операнд слева от оператора
                left_operand = ""
                i = 1
                while pos - i >= 0 and js_code[pos - i].isalnum():
                    left_operand = js_code[pos - i] + left_operand
                    i += 1
                # Проверяем валидность левого операнда
                if is_valid_operand(left_operand):
                    operands_and_values.append(left_operand)
                # Найдем операнд справа от оператора
                right_operand = ""
                i = 1
                while pos + i < len(js_code) and js_code[pos + i].isalnum():
                    right_operand += js_code[pos + i]
                    i += 1
                # Проверяем валидность правого операнда
                if is_valid_operand(right_operand):
                    operands_and_values.append(right_operand)
    return operands_and_values


operands_list = operand_search()
operands = dict(Counter(operand_search()))
sorted_operands = dict(sorted(operands.items(), key=lambda item: item[0]))
for key, value in sorted_operators.items():
    # Если ключ содержится в dict2, удаляем его из dict2
    if key in sorted_operands:
        del sorted_operands[key]

a = 5        
if '(' in sorted_operators:
    a = sorted_operators['(']
    del sorted_operators['(']
    sorted_operators['()']=a
if ')' in sorted_operators:
    del sorted_operators[')'] 
        
if '[' in sorted_operators:
    a = sorted_operators['[']
    del sorted_operators['[']
    sorted_operators["[]"]=a
if ']' in sorted_operators:
    del sorted_operators[']']         
        
        
# Создание списков ключей и значений
keys = list(sorted_operands.keys())
values = list(sorted_operands.values())
# Создание списков ключей и значений
# Преобразование списков ключей и значений в двумерный массив
table_data = np.array([keys, values,values]).T

fig, ax = plt.subplots()
ax.axis('off')  # Отключение осей

# Создание таблицы
table = ax.table(cellText=table_data, colLabels=['Operands','Programm operands','My operands'], loc='center')

# Добавление прокрутки
plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)  # Изменение размеров области графика
plt.axis('off')  # Отключение осей

plt.show()
