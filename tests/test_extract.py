import unittest
from utils.extract import extract_fashion_data
from bs4 import BeautifulSoup
from datetime import datetime

class TestExtract(unittest.TestCase):

    def setUp(self):
        html = """
        <div class="product-details">
            <h3 class="product-title">Test Product</h3>
            <div class="price-container">
                <span class="price">$29.99</span>
            </div>
            <p>Rating: ⭐ 4.5</p>
            <p>Colors: Red, Blue</p>
            <p>Size: M, L</p>
            <p>Gender: Unisex</p>
        </div>
        """
        self.article = BeautifulSoup(html, "html.parser")

    def test_extract_fashion_data(self):
        data = extract_fashion_data(self.article)
        self.assertEqual(data['Title'], 'Test Product')
        self.assertEqual(data['Price'], '$29.99')
        self.assertEqual(data['Rating'], '⭐ 4.5')
        self.assertEqual(data['Colors'], 'Red, Blue')
        self.assertEqual(data['Size'], 'M, L')
        self.assertEqual(data['Gender'], 'Unisex')

    def test_timestamp_existence(self):
        data = extract_fashion_data(self.article)
        self.assertIn('Timestamp', data)
        # Test apakah Timestamp valid format ISO
        try:
            datetime.fromisoformat(data['Timestamp'])
            valid = True
        except ValueError:
            valid = False
        self.assertTrue(valid, "Timestamp tidak dalam format ISO yang valid")

if __name__ == '__main__':
    unittest.main()