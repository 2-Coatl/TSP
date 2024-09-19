import unittest
from modules.pdf_handler import extract_text_from_pdf

class TestPdfHandler(unittest.TestCase):

    def test_extract_text_from_valid_pdf(self):
        result = extract_text_from_pdf('tests/test_files/sample.pdf')
        self.assertIn('Expected text', result)

    def test_extract_text_from_invalid_pdf(self):
        with self.assertRaises(RuntimeError):
            extract_text_from_pdf('tests/test_files/invalid.pdf')

if __name__ == '__main__':
    unittest.main()
