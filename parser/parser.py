import csv

import bs4
import requests
import logging
import collections

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SUPER.KG')

ParseMusic = collections.namedtuple(
    'ParseMusic',
    (
        'title',
        'music_obj',
    ),
)

MUSIC_HOST = 'https://audio.super.kg/media/audio/'
HEADERS = (
    'Name',
    'Track'
)


class Main:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
        self.music = []


    def load_page(self):
        url = 'https://www.super.kg/media/audio/'
        request = self.session.get(url=url)
        request.raise_for_status()
        return request.text


    def pages_count(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        pagination = soup.find('ul', class_='pagers').find_all('a')
        page = pagination[-1].get('href')
        last_page = page.strip('/media/useraudio/?pg=')
        return last_page


    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        items = soup.findAll('div', class_='audio-block')
        # print(items)
        for item in items:
            self.parse_audio(item=item)
        # music = []
        # for block in soup.findAll('div', 'audio-block'):
        #     items = block.find_all('div', class_='audio-item')
        #     self.parse_audio(block=block)
        #     for item in items:
        #         if item.find('div', class_='info').find('div', class_='info-item length').get_text() == '00:00:00':
        #             continue
        #         else:
        #             music.append(
        #                 {
        #                     'title': item.find('div', class_='audio-item-title').get_text(strip=True),
        #                     'music_obj': MUSIC_HOST + item.get('data-file'),
        #                 }
        #             )
        #     return music
        # self.parse_audio(block=block)

    def parse_audio(self, item):
        music = []
        block = item.find_all('div', class_='audio-item')
        # print(block)
        for music in block:
            title = music.find('div', class_='audio-item-title').get_text()
            title = title.replace('"', ' ').strip()
            # print(title)
            if not title:
                logger.error('no title')
                return

            music_obj = MUSIC_HOST + music.get('data-file')
            # print(music_obj)
            if not music_obj:
                logger.error('no data-file')
                return

            self.music.append(ParseMusic(
                title=title,
                music_obj=music_obj
                )
            )

            logger.debug('%s, %s', title, music_obj)


    def save(self, path):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='^', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADERS)
            for item in self.music:
                writer.writerow(item)

    def parse_all():
        html = get_html(URL)
        if html.status_code == 200:
            music = []
            for page in range(1, int(get_pages_count(html.text)) + 1):
                print(f'Parsing page: {page}')  # отладка
                html = get_html(URL, params={'pg': page})
                music.extend(get_content(html.text))
                save(music, CSV)
        else:
            print("404 PAGE DOESN`T EXIST")


    def run(self):
        path = '/home/ragdir/music/music.csv'
        text = self.load_page()
        self.parse_page(text=text)
        logger.info(
            f'Got {len(self.music)} tracks'
        )
        self.save(path=path)


if __name__ == '__main__':
    parser = Main()
    parser.run()