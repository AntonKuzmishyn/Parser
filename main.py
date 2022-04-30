from bs4 import BeautifulSoup as bs
import requests
import sqlite3 as sq

URL = "https://dom.ria.com/uk/arenda-kvartir/kiev/"
HOST = "https://dom.ria.com"
HEADERS = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}


def gethtml(url, params):
    print(url + str(params))
    return requests.get(url + str(params), headers=HEADERS)


def getcontent(html):
    soup = bs(html, 'html.parser')
    items = soup.find_all('section', class_='realty-item')
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
    pagination = soup.find_all('span', class_='page-item')
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
        posts2 = []
        pages_count = get_pages_count(html.text)  # 1
        print("pages_count" + str(pages_count))
        for page in range(1, pages_count + 1):
            print(f'Parsing page {page} from {pages_count}...')
            html = gethtml(URL, params=f'?page={page}')
            posts.append(getcontent(html.text))
            posts2.extend(getcontent(html.text))
        return posts, posts2
    else:
        print('Error')


# def Db(posts):
#     connection = sq.connect("posts2.db")
#     cursor = connection.cursor()
#
#     cursor.execute("""CREATE TABLE posts_table(
#     id INTEGER,
#     rooms TEXT,
#     link TEXT,
#     price TEXT,
#     area TEXT
#     )""")
#
#     id = 1
#     for post in posts:
#         cursor.execute("INSERT INTO posts_table VALUES (?,?,?,?,?)", [id, post['rooms'],
#                                                                       post['link'],
#                                                                       post['price'],
#                                                                       post['area']])
#
#         id = id + 1
#
#     connection.commit()
#
#     cursor.close()
#     connection.close()
#
#
# def Queries():
#     connection = sq.connect("posts2.db")
#     cursor = connection.cursor()
#     cursor.execute(
#         """select rooms, link, area, price from posts_table
#
#             """)
#     rows = cursor.fetchall()
#
#     for row in rows:
#         print(row)
#     cursor.close()
#     connection.close()


def tocsv(posts):
    for elem in posts:
        item = elem['rooms'][0] + ',' \
               + elem['area'].rstrip(' м²') + ',' \
               + elem['price'].rstrip(' грн').replace(' ', '') + ',' \
               + elem['district'].rstrip(',') + '\n'
        with open("flats.csv", "a") as file:
            file.write(item)


if __name__ == '__main__':
    posts, posts2 = parse()
    # for i in range(len(posts)):
    #     print(f"{i+1} {str(len(posts[i]))}")
    # print(posts2)
    tocsv(posts2)
    # Db(posts2)
    # Queries()
