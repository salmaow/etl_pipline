from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def store_to_csv(data, filename="products.csv"):
    data.to_csv(filename, index=False)
    print(f"Data berhasil disimpan ke dalam {filename}")
    
def store_to_postgre(data, db_url):
    try:
        engine = create_engine(db_url)
        
        with engine.connect() as con:
            data.to_sql('fashiontoscrape', con=con, if_exists='append', index=False)
            print("Data berhasil ditambahkan ke Postgre!")
    
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")
    
def store_to_sheets(data):
    SERVICE_ACCOUNT_FILE = './google-sheets-api.json'
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    SPREADSHEET_ID = '1ybHyFIxWrJXv1eZP6g7OgkCiiv49AvDWwegooZBdks8'
    RANGE_NAME = 'Sheet1!A2'
    
    try:
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()
        
        values = data.values.tolist()
        
        body = {'values': values}
        
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print("Data berhasil ditambahkan ke Google Sheets! (https://docs.google.com/spreadsheets/d/1ybHyFIxWrJXv1eZP6g7OgkCiiv49AvDWwegooZBdks8/edit?gid=0#gid=0)")
    
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")