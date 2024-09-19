import unittest
from src.utils.file_utils import save_translation_to_file

class TestFileUtils(unittest.TestCase):
    
    def test_save_translation_to_file(self):
        test_text = "Texto de prueba"
        test_path = 'test_output.txt'
        
        save_translation_to_file(test_text, test_path)
        
        with open(test_path, 'r') as file:
            content = file.read()
        
        self.assertEqual(content, test_text)
    
    def test_save_translation_to_file_error(self):
        # Simular un error, por ejemplo, un path no válido.
        with self.assertRaises(RuntimeError):
            save_translation_to_file("Texto de prueba", '/invalid_path/test_output.txt')

if __name__ == '__main__':
    unittest.main()
