import requests
import json
from bs4 import BeautifulSoup
# для картинок 300x450
list_films = []

def main():
    session = requests.session()
    cookies = {
        '_yasc' : 'YoZmLpkGM2uQpxMo+3YQq4PiY82pN9ATdyXHxPIjLXq1O1yZnmqbcpjs3EA=',
        'desktop_session_key' : '35a600c4bb5a4692a7941fe5514b62be92a6503cb3a7459585daaabb6b38bd57122844ff6e5b9dbc763eebcc4ef38b17f508429ed15f43331e085bf0d29ccc416369eb94e582f25fc568e0c4bcf0198ca6a6b6d36469a9bf8aec9a25d1621894',
        'desktop_session_key.sig' : '-KPfTGSJYyirz5u1vGFPHzo3Kro',
        'gdpr' : '0',
        '_ym_uid' : '1682946877299802508',
        '_ym_isad' : '2',
        'ya_sess_id' : 'noauth:1682946871',
        'yandex_login' : '',
        'ys' : 'c_chck.1745382381',
        'i' : 'ZBH9fyEdRivgw1Ao43q+B8YTGwR4rtLRkb3q9ExGHYlo3nIar1HWCRVCFjPoju+822rCeVVPfZUmcaNS8FQJIjlLTA4=',
        'yandexuid' : '5764997731682946865',
        'mda2_beacon' : '1682946871626',
        'sso_status' : 'sso.passport.yandex.ru:synchronized',
        '_ym_d' : '1682946873',
        'cycada' : '4wudwxY3j0IZHS0iFtvoD67PYYEk3Fm4S+49G8wSW0o=',
    }
    url = 'https://www.kinopoisk.ru/lists/movies/top500/?page={}'
    for page in range(1,11):
        req_text = session.get(url.format(page), cookies=cookies).text
        l1 = lambda time :  '' if len(time.text.split(',')[1]) == 5 or len(time.text.split(',')[1]) == 4 else time.text.split(',')[1]
        l2 = lambda time : time.text.split(',')[1] if time.text.split(',')[0] == '' else time.text.split(',')[0]
        names_film_page = [name.text for name in BeautifulSoup(req_text,"lxml").find_all('span', class_ = 'styles_activeMovieTittle__kJdJj')]
        img_film_page = ['https:'+img.get('src') for img in BeautifulSoup(req_text,"lxml").find_all('img', class_ = 'styles_root__DZigd')]
        time_film_page = [l1(time)  for time in BeautifulSoup(req_text,"lxml").find_all('span', class_ = 'desktop-list-main-info_secondaryText__M_aus')]
        age_film_page = [l2(time) for time in BeautifulSoup(req_text,"lxml").find_all('span', class_ = 'desktop-list-main-info_secondaryText__M_aus')]
        info_film_page = [info.text for info in BeautifulSoup(req_text,"lxml").find_all('span', class_ = 'desktop-list-main-info_truncatedText__IMQRP')]
        first_film_page = info_film_page[::2] 
        second_film_page = info_film_page[1::2]
        for name, img, time, age, first, second in zip(names_film_page,img_film_page,time_film_page,age_film_page,first_film_page,second_film_page):
            disk_film = {
                'name' : name,
                'img' : img,
                'time':time,
                'age' : age,
                'first' : first,
                'second' : second
            }
            list_films.append(disk_film)


if __name__ == "__main__":
    main()
    with open('out_data.json', 'a') as file:
        json.dump(list_films, file, indent=4, ensure_ascii=False)