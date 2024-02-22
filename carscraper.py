import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sqlite3

# Get the current date and time
now = datetime.now()

# Format the current date and time as a string
timestamp = now.strftime("%Y%m%d")

def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    car_data = []
    carlist = soup.find_all('div', {'id': 'car-list-wrap'})
    for car in carlist[0].find_all('dl'):
        car_name = car.find('p', {'class': 'car_name'}).text
        year = car.find('ul', {'class': 'detail_table'}).find_all('li')[0].find_all('p')[1].text
        price = car.find('div', {'class': 'price'}).find('p', {'class': 'number'}).text
        kilometers = car.find('ul', {'class': 'detail_table'}).find_all('li')[2].find_all('p')[1].text
        kilometers = kilometers.strip()
        shaken_date = car.find('ul', {'class': 'detail_table'}).find_all('li')[1].find_all('p')[1].text
        rating = car.find('ul', {'class': 'detail_table'}).find_all('li')[3].find_all('p')[1].text
        carlink = car.find('a', {'class': 'wrap_link'}).get('href')
        url = f'https://gazoo.com{carlink}'
        car_data.append([timestamp, car_name, year, price, kilometers, shaken_date, rating, url])

    return car_data

def save_to_sqlite(df, table_name):
    # Connect to the SQLite database (create it if it doesn't exist)
    conn = sqlite3.connect('car_data.db')
    
    # Save the DataFrame to the database
    df.to_sql(table_name, conn, if_exists='append', index=False)
    
    # Close the connection
    conn.close()

def main():
    url = "https://gazoo.com/U-Car/search_result?Cn=01_%E3%82%B7%E3%82%A8%E3%83%B3%E3%82%BF&Ge=minivan&Ymn=2019&Brkp=1&chk-brake-pedestrian=1&Ldw=1&chk-detail-warning=1&Pvm=1&Drec=1&Ptc=1400&Sc=1&Own=1&Mend=1&Eng=H&Bm=1&Sk=1&Etc=1"
    data = get_data(url)
    df = pd.DataFrame(data, columns=['Date', 'CarName', 'Year', 'Price', 'Kilometers', 'ShakenDate', 'Rating', 'URL'])
    
    # Save the DataFrame to SQLite
    save_to_sqlite(df, 'car_data')

if __name__ == "__main__":
    main()