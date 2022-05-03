from bs4 import BeautifulSoup as bs
import requests
import rating
import replacer

URL = "https://dom.ria.com/uk/arenda-kvartir/kiev/"
HEADERS = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}



def clear_files():
    open('final_dataset.csv', 'w').close()
    open('flats.csv', 'w').close()
    open('rating.csv', 'w').close()


def gethtml(url, params):
    print(url + str(params))
    return requests.get(url + str(params), headers=HEADERS)


def getcontent(html):
    soup = bs(html, 'html.parser')
    items = soup.find_all('section', class_='realty-item')
    items = items[:-1]  # removing last element with is not a real listing
    posts = []
    for item in items:
        posts.append({
            'price': item.
                find('div', class_='wrap_desc').
                find_next('div', class_="flex f-space f-center mb-5 mt-15").
                find_next('div', class_="flex f-center").
                find_next('b', class_="size18").
                get_text(strip=True),
            'link': item.
                find('div', class_='wrap_desc').
                find_next('h2', class_="tit").
                find_next('a').get('href'),
            'rooms': item.
                find('div', class_='wrap_desc').
                find_next('div', class_="mt-10 chars grey").
                find_next('span', class_="point-before").
                get_text(strip=True),
            'area': item.
                find('div', class_='wrap_desc').
                find_next('div', class_="mt-10 chars grey").
                find_next('span', class_="point-before").
                find_next('span', class_="point-before").
                get_text(strip=True),
            'district': item.
                find('div', class_='wrap_desc').
                find_next('a', class_="mb-5 i-block grey p-rel").
                get_text(strip=True)

        })
    return posts


def get_pages_count(html):
    soup = bs(html, 'html.parser')
    pagination = soup.find_all('a', class_='page-item button-border')
    print("PAGINATION: " + str(int(pagination[-2].find_next('a').get_text())))
    if pagination:
        return 5
        # return int(pagination[-2].find_next('a').get_text())
    else:
        return 1


def parse():
    html = gethtml(URL, "?page=1")

    if html.status_code == 200:
        posts = []
        pages_count = get_pages_count(html.text)  # 1
        print("pages_count: " + str(pages_count))
        for page in range(1, pages_count + 1):
            print(f'Parsing page {page} from {pages_count}...')
            html = gethtml(URL, params=f'?page={page}')
            posts.extend(getcontent(html.text))
        return posts
    else:
        print('Error')


def tocsv(posts):
    for elem in posts:
        item = elem['rooms'][0] + ',' \
               + elem['area'].rstrip(' м²') + ',' \
               + elem['price'].rstrip(' грн').replace(' ', '') + ',' \
               + elem['district'].rstrip(',') + ',' \
               + "https://dom.ria.com" + elem['link'] + '\n'
        with open("flats.csv", "a") as file:
            file.write(item)


if __name__ == '__main__':
    clear_files()

    posts = parse()
    tocsv(posts)

    ratinglist = rating.parse()
    rating.tocsv(ratinglist)

    replacer.make_final_dataset()

