import unittest
from modules.translator import translate_text

class TestTranslator(unittest.TestCase):

    def test_translate_text(self):
        input_text = "Hello world"
        result = translate_text(input_text)
        self.assertIn("Hola mundo", result)

    def test_translate_empty_text(self):
        with self.assertRaises(RuntimeError):
            translate_text("")

if __name__ == '__main__':
    unittest.main()
