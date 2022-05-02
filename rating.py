from bs4 import BeautifulSoup as bs
import requests

URL = "https://dom.ria.com/uk/rate-region-stat/15185/"
HEADERS = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}


def gethtml(url):
    return requests.get(url, headers=HEADERS)


def getcontent(html):
    soup = bs(html, 'html.parser')
    items = soup.find_all('tr', class_='t-row')
    rating = []
    for i in range(1, len(items)):
        rating.append({
            'name': items[i].
                find('td', class_='t-cell').
                find_next('a', class_="toggleCharts").
                find_next('span', class_="size15 nowrap").
                get_text(strip=True),
            'rating': items[i].
                find('td', class_='t-cell').
                find_next('td', class_='t-cell bold orange size15').
                get_text(strip=True)
        })
    return rating


def parse():
    html = gethtml(URL)
    if html.status_code == 200:
        rating = getcontent(html.text)
        return rating
    else:
        print('Error')
        

def tocsv(rating):
    for elem in rating:
        item = elem['name'] + ',' + elem['rating'] + '\n'
        with open("rating.csv", "a") as file:
            file.write(item)

#
# if __name__ == '__main__':
#     rating = parse()
#     tocsv(rating)






