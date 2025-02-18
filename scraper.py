import requests
from bs4 import BeautifulSoup
import csv
import json

def scrape_products(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error al acceder a la URL: {url}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    
    # Ejemplo: se asume que cada producto está contenido en un elemento con la clase "product"
    # y que dentro existen elementos con clases "product-title" y "product-price".
    product_elements = soup.select('.product-card')  # Ajusta este selector según la web real
    for prod in product_elements:
        title_tag = prod.select_one('.card-title')
        price_tag = prod.select_one('.product_price')
        img_tag = prod.select_one('img')
        
        title = title_tag.text.strip() if title_tag else "Sin título"
        price = price_tag.text.strip() if price_tag else "Sin precio"
        image = img_tag['src'] if img_tag and img_tag.has_attr('src') else "Sin imagen"
        
        products.append({
            'titulo': title,
            'imagen': image,
            'precio': price
        })
        
        # Limitar a 30 productos
        if len(products) >= 30:
            break
    return products

def save_to_csv(products, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['titulo', 'imagen', 'precio'])
        writer.writeheader()
        for product in products:
            writer.writerow(product)

def convert_csv_to_json(csv_filename, json_filename):
    data = []
    with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    with open(json_filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    # URL de la tienda a scrapear (reemplaza con la URL real)
    url = 'https://www.coolmod.com/tarjetas-graficas/'
    products = scrape_products(url)
    if products:
        csv_file = 'productos.csv'
        json_file = 'productos.json'
        save_to_csv(products, csv_file)
        convert_csv_to_json(csv_file, json_file)
        print(f'Se han guardado {len(products)} productos en {csv_file} y {json_file}')
    else:
        print('No se encontraron productos')

if __name__ == "__main__":
    main()