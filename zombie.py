import re
import json

def parse_config(input_text):
    # Удаление комментариев
    input_text = re.sub(r'\|\|.*', '', input_text)  # Удаляем однострочные комментарии
    input_text = re.sub(r'<!--.*?-->', '', input_text, flags=re.DOTALL)  # Удаляем многострочные комментарии

    # Обработка констант
    constants = {}
    constant_declarations = re.findall(r'var\s+([a-zA-Z_]+)\s*:=\s*(.+?);', input_text)
    for name, value in constant_declarations:
        constants[name] = eval(value) if re.match(r'^\d+$', value) else value.strip('"')
    input_text = re.sub(r'var\s+[a-zA-Z_]+\s*:=\s*.+?;', '', input_text)

    def replace_constants(match):
        const_name = match.group(1)
        if const_name in constants:
            return str(constants[const_name])
        else:
            raise ValueError(f"Undefined constant: {const_name}")

    input_text = re.sub(r'@\(([a-zA-Z_]+)\)', replace_constants, input_text)


