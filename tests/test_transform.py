import unittest
import pandas as pd
from utils.transform import transform_data, transform_to_DataFrame

class TestTransform(unittest.TestCase):
    def setUp(self):
        self.sample_data = [{
            "Title": "Stylish Jacket",
            "Price": "$50.00",
            "Rating": "⭐ 4.5",
            "Colors": "Colors: 2",
            "Size": "Size: L",
            "Gender": "Gender: Female"
        }]

    def test_transform_to_DataFrame(self):
        df = transform_to_DataFrame(self.sample_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("Title", df.columns)

    def test_transform_data(self):
        df = transform_to_DataFrame(self.sample_data)
        transformed_df = transform_data(df, kurs=16000)
        self.assertEqual(transformed_df.iloc[0]["Price"], 800000.0)
        self.assertEqual(transformed_df.iloc[0]["Rating"], 4.5)
        self.assertEqual(transformed_df.iloc[0]["Size"], "L")
        self.assertEqual(transformed_df.iloc[0]["Gender"], "Female")
        self.assertEqual(transformed_df.iloc[0]["Colors"], 2)

if __name__ == '__main__':
    unittest.main()