import unittest
from nexler.utils import str_util
from xml.etree.ElementTree import Element, tostring


class TestStringUtil(unittest.TestCase):

    def test_str_encode_base64(self):
        result = str_util.str_encode('Hello, World!')
        self.assertEqual(result, 'SGVsbG8sIFdvcmxkIQ==')

    def test_str_encode_hex(self):
        result = str_util.str_encode('Hello, World!', strType="hex")
        self.assertEqual(result, '48656c6c6f2c20576f726c6421')

    def test_str_decode_base64(self):
        result = str_util.str_decode('SGVsbG8sIFdvcmxkIQ==')
        self.assertEqual(result, 'Hello, World!')

    def test_str_decode_hex(self):
        result = str_util.str_decode('48656c6c6f2c20576f726c6421', strType="hex")
        self.assertEqual(result, 'Hello, World!')

    def test_parse_json(self):
        result = str_util.parse('{"test": "Hello, World!"}')
        self.assertEqual(result, {"test": "Hello, World!"})

    def test_parse_xml(self):
        root = Element('root')
        child = Element('child')
        child.text = 'Hello, World!'
        root.append(child)
        result = str_util.parse(tostring(root, encoding='unicode'), datatype='xml')
        self.assertEqual(result.tag, 'root')
        self.assertEqual(result[0].tag, 'child')
        self.assertEqual(result[0].text, 'Hello, World!')

    def test_parse_yaml(self):
        result = str_util.parse("test: 'Hello, World!'", datatype='yaml')
        self.assertEqual(result, {"test": "Hello, World!"})

    def test_remove_punctuation(self):
        result = str_util.remove_punctuation('Hello, World!')
        self.assertEqual(result, 'Hello World')

    def test_remove_whitespace(self):
        result = str_util.remove_whitespace('Hello, World!')
        self.assertEqual(result, 'Hello,World!')

    def test_capitalize(self):
        result = str_util.capitalize('hello world')
        self.assertEqual(result, 'Hello World')

    def test_snake_case(self):
        result = str_util.snake_case('Hello, World!')
        self.assertEqual(result, 'hello_world')

    def test_camel_case(self):
        result = str_util.camel_case('hello_world')
        self.assertEqual(result, 'helloWorld')

    def test_extract_numbers(self):
        result = str_util.extract_numbers('123abc456def7890')
        self.assertEqual(result, '1234567890')


if __name__ == "__main__":
    unittest.main()
