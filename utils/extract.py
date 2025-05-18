import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    session = requests.Session()
    response = session.get(url, headers=HEADERS)
    
    try:
        response.raise_for_status()
        return response.content
    
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None

def extract_fashion_data(article):
    try:
        # Title
        title_element = article.find('h3', class_='product-title')
        title = title_element.text.strip() if title_element else "Unknown Product"
        
        # Price
        price_container = article.find('div', class_='price-container')
        price_span = price_container.find('span', class_='price') if price_container else article.find('p', class_='price')
        price = price_span.text.strip() if price_span else "Price Unavailable"

        # Default values
        rating = ""
        color = ""
        size = ""
        gender = ""

        # All <p> elements
        p_tags = article.find_all('p')
        
        for p in p_tags:
            text = p.text.lower()
            if "rating" in text:
                rating = p.text.replace("Rating:", "").strip()
            elif "colors" in text:
                color = p.text.replace("Colors:", "").strip()
            elif "size" in text:
                size = p.text.replace("Size:", "").strip()
            elif "gender" in text:
                gender = p.text.replace("Gender:", "").strip()
        
        timestamp = datetime.now().isoformat()
        fashion = {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": color,
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp
        }
        
        return fashion
    
    except Exception as e:
        print(f'Gagal mengekstrak data fashion: {e}')
        return {
            "Title": "Unknown Product",
            "Price": "Price Unavailable",
            "Rating": "",
            "Colors": "",
            "Size": "",
            "Gender": "",
            "Timestamp": datetime.now().isoformat()
        }

def scrape_fashion(base_url, start_page=1, delay=2):
    data = []
    page_number = start_page
    
    try:
        while True:
            if page_number == 1:
                url = 'https://fashion-studio.dicoding.dev'
            else:
                url = base_url.format(page_number)
            
            print(f"Scraping halaman: {url}")
            
            content = fetching_content(url)
            if content:
                soup = BeautifulSoup(content, "html.parser") 
                articles_element = soup.find_all('div', class_='product-details')
                
                for article in articles_element:
                    fashion = extract_fashion_data(article)
                    data.append(fashion)
                
                next_button = soup.find('li', class_='page-item next')
                if next_button:
                    page_number += 1
                    time.sleep(delay)
                else:
                    break
            else:
                break
        
        return data
    
    except requests.exceptions.RequestException as e:
        print(f'Terjadi kesalahan saat mengakses situs web: {e}')
        return None
    
    except Exception as e:
        print(f'Terjadi kesalahan saat proses scraping: {e}')
        return None

def main():
    base_url='https://fashion-studio.dicoding.dev/page{}'
    products = scrape_fashion(base_url)
    df = pd.DataFrame(products)
    print(df)

if __name__ == '__main__':
    main()