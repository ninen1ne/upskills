from bs4 import BeautifulSoup
import requests


url = "https://xn--42cah7d0cxcvbbb9x.com/"
response = requests.get(url, timeout=15)
html_doc = response.text
soup = BeautifulSoup(html_doc, "html.parser")

price_table = soup.find('div', {'class': 'goldshopf'})
price_data = price_table.find_all('tbody')[0].find_all('tr')

for row in price_data:
    if(row.find('td', {'class': 'span bg-span al-l'})):
        header = row.find('td', {'class': "span bg-span al-l"}).get_text(strip=True)
        em_cells = row.find_all('td', {'class': "em bg-em g-d"})
        buying = em_cells[0].get_text(strip=True)
        selling = em_cells[1].get_text(strip=True)
        print(f"{header}: รับซื้อ -> {buying} || ขายออก -> {selling}\n")
    elif(row.find('td', {'class': 'span bg-span g-d'})):
        price_diff = row.find('td', {'class': 'em bg-em al-l g-d'}).get_text(strip=True)
        print(f'diff = {price_diff}\n')
    elif(row.find('td', {'class': 'span bg-span txtd al-r'})):
        date = row.find('td', {'class': 'span bg-span txtd al-r'}).get_text(strip=True)
        time = row.find('td', {'class': 'em bg-span txtd al-r'}).get_text(strip=True)
        round = row.find('td', {'class': 'em bg-span txtd al-l'}).get_text(strip=True)
        format =  f"----- ราคา ณ {date} time {time} {round}----\n"
        print(format)