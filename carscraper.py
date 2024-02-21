import requests
from bs4 import BeautifulSoup
import pandas as pd

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
        car_data.append([car_name, year, price, kilometers, shaken_date, rating])

    return car_data

def main():
    url = "https://gazoo.com/U-Car/search_result?Cn=01_%E3%82%B7%E3%82%A8%E3%83%B3%E3%82%BF&Ge=minivan&Ymn=2019&Brkp=1&chk-brake-pedestrian=1&Ldw=1&chk-detail-warning=1&Pvm=1&Drec=1&Ptc=1400&Sc=1&Own=1&Mend=1&Eng=H&Bm=1&Sk=1&Etc=1"
    data = get_data(url)
    df = pd.DataFrame(data, columns=['CarName', 'Year', 'Price', 'Kilometers', 'ShakenDate', 'Rating'])
    # Convert the dataframe to a CSV string
    csv_data = df.to_csv(index=False)

    # Print the CSV data
    print(csv_data)

if __name__ == "__main__":
    main()