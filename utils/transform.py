import pandas as pd
from datetime import datetime

def transform_to_DataFrame(data):
    try:
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        return pd.DataFrame()

def transform_data(data, kurs=16000):
    """Transformasi data hasil scraping fashion studio."""
    try:
        # Hapus baris dengan nilai default/error
        data = data[~data['Title'].str.contains("Unknown Product", na=False)]
        data = data[~data['Rating'].str.contains("Invalid Rating", na=False)]
        data = data[~data['Price'].str.contains("Price Unavailable", na=False)]
        
        # Drop duplikat dan nilai kosong
        data = data.drop_duplicates()
        data = data.dropna()

        # Konversi harga ke float, lalu ke Rupiah
        data['Price'] = data['Price'].replace('[\$,]', '', regex=True).astype(float)
        data['Price'] = data['Price'] * kurs

        # Ambil angka rating dari string (misal: 'Rating: ⭐ 4.5')
        data['Rating'] = data['Rating'].str.extract(r'⭐ (\d\.\d)').astype(float)

        # Bersihkan teks tambahan (kalau masih ada)
        data['Size'] = data['Size'].str.replace('Size: ', '', regex=False)
        data['Gender'] = data['Gender'].str.replace('Gender: ', '', regex=False)

        # Ambil jumlah warna dari kolom Colors: 'Colors: 5 Colors' → 5
        data['Colors'] = data['Colors'].str.extract(r'(\d+)').astype(int)

        # Pastikan kolom Timestamp dalam format datetime jika tersedia
        if 'Timestamp' in data.columns:
            data['Timestamp'] = pd.to_datetime(data['Timestamp'], errors='coerce')

        # Ubah Title ke string
        data['Title'] = data['Title'].astype('string')

        return data

    except KeyError as e:
        print(f"Column error: {e}")
    except ValueError as e:
        print(f"Value conversion error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return pd.DataFrame()