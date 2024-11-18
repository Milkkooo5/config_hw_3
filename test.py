import unittest
import json
import re
def parse_config(input_text):
    input_text = re.sub(r'\|\|.*', '', input_text)  # Удаляем однострочные комментарии
    input_text = re.sub(r'<!--.*?-->', '', input_text, flags=re.DOTALL)  # Удаляем многострочные комментарии

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

    def parse_dict(text):
        result = {}
        i = 0
        while i < len(text):
            if text[i].isspace():  # Пропускаем пробелы
                i += 1
                continue

            key_match = re.match(r'\b[a-zA-Z_][a-zA-Z_0-9]*\b', text[i:])
            if not key_match:
                raise ValueError(f"Expected key at position {i}, found: {text[i:]}")
            key = key_match.group()
            i += len(key)

            while i < len(text) and text[i].isspace():
                i += 1
            if i >= len(text) or text[i] != '=':
                raise ValueError(f"Expected '=' after key '{key}', found: {text[i:]}")
            i += 1  # Пропускаем '='

            while i < len(text) and text[i].isspace():
                i += 1

            if i < len(text) and text[i] == '{':  # Начало вложенного словаря
                balance = 1
                start = i + 1
                while balance > 0:
                    i += 1
                    if i >= len(text):
                        raise ValueError("Unmatched '{'")
                    if text[i] == '{':
                        balance += 1
                    elif text[i] == '}':
                        balance -= 1
                result[key] = parse_dict(text[start:i].strip())
                i += 1  # Пропускаем '}'
            elif i < len(text) and text[i] == '"':  # Строка
                start = i + 1
                i = text.find('"', start)
                if i == -1:
                    raise ValueError("Unterminated string value")
                result[key] = text[start:i]
                i += 1  # Пропускаем закрывающую кавычку
            else:  # Число
                value_match = re.match(r'\d+', text[i:])
                if not value_match:
                    raise ValueError(f"Expected value after key '{key}', found: {text[i:]}")
                result[key] = int(value_match.group())
                i += len(value_match.group())

            while i < len(text) and text[i].isspace():
                i += 1
            if i >= len(text) or text[i] != ';':
                raise ValueError(f"Expected ';' after value for key '{key}', found: {text[i:]}")
            i += 1  # Пропускаем ';'

        return result

    config_match = re.search(r'\{(.*)\}', input_text, flags=re.DOTALL)
    if not config_match:
        raise ValueError("Invalid configuration format. No top-level dictionary found.")
    config_dict = parse_dict(config_match.group(1).strip())

    return json.dumps(config_dict, indent=4)

class TestConfigParser(unittest.TestCase):

    def test_single_line_comment(self):
        input_text = """
        || This is a comment
        {
            timeout = 30;
        }
        """
        expected_output = '{"timeout": 30}'
        output_text = parse_config(input_text)
        self.assertEqual(json.loads(output_text), json.loads(expected_output))

    def test_multiline_comment(self):
        input_text = """
        <!--
        This is a multi-line comment
        -->
        {
            timeout = 30;
        }
        """
        expected_output = '{"timeout": 30}'
        output_text = parse_config(input_text)
        self.assertEqual(json.loads(output_text), json.loads(expected_output))

    def test_constant_replacement(self):
        input_text = """var timeout := 30;\n{
            setting1 = @(timeout);
            setting2 = 50;
        }"""
        expected_output = '{"setting1": 30, "setting2": 50}'
        output_text = parse_config(input_text)
        self.assertEqual(json.loads(output_text), json.loads(expected_output))

    def test_nested_dict(self):
        input_text = """{
            server = {
                retries = 3;
                timeout = 30;
            };
            port = 8080;
        }"""
        expected_output = '{"server": {"retries": 3, "timeout": 30}, "port": 8080}'
        output_text = parse_config(input_text)
        self.assertEqual(json.loads(output_text), json.loads(expected_output))

    def test_numeric_values(self):
        input_text = """{
            a = 5;
            b = 10;
        }"""
        expected_output = '{"a": 5, "b": 10}'
        output_text = parse_config(input_text)
        self.assertEqual(json.loads(output_text), json.loads(expected_output))

    def test_missing_semicolon(self):
        input_text = """{
            setting1 = 10
            setting2 = 20;
        }"""
        with self.assertRaises(ValueError):
            parse_config(input_text)

    def test_no_top_level_dict(self):
        input_text = "var timeout := 30;"
        with self.assertRaises(ValueError):
            parse_config(input_text)

if __name__ == "__main__":
    unittest.main()
