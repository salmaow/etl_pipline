import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import store_to_csv, store_to_postgre, store_to_sheets

class TestLoad(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame([{
            "Title": "Cool Jacket",
            "Price": 639840.0,
            "Rating": 4.5,
            "Colors": 3,
            "Size": "M",
            "Gender": "Unisex"
        }])

    def test_store_to_csv(self):
        import tempfile, os
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_path = os.path.join(tmpdirname, "fashion-products.csv")
            store_to_csv(self.df, file_path)
            loaded = pd.read_csv(file_path)
            self.assertFalse(loaded.empty)
            self.assertIn("Title", loaded.columns)

    @patch("utils.load.create_engine")
    def test_store_to_postgre(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__.return_value = MagicMock()

        store_to_postgre(self.df, "postgresql+psycopg2://admin:admin123@localhost:5432/fashiondb")
        mock_create_engine.assert_called_once()

    @patch("utils.load.build")
    @patch("utils.load.Credentials.from_service_account_file")
    def test_store_to_sheets(self, mock_credentials, mock_build):
        mock_service = MagicMock()
        mock_sheet = MagicMock()
        mock_build.return_value = mock_service
        mock_service.spreadsheets.return_value = mock_sheet
        mock_sheet.values.return_value.update.return_value.execute.return_value = {}

        store_to_sheets(self.df)
        mock_build.assert_called_once()

if __name__ == '__main__':
    unittest.main()