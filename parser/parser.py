import bs4
import requests
import logging
import collections

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('parser')

ParseMusic = collections.namedtuple(
    'ParseMusic',
    (
        'title',
        'music_obj',
    ),
)

MUSIC_HOST = 'https://audio.super.kg/media/audio/'


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

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        items = soup.select('div.audio-block')
        # print(items)
        # print(container)
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
        # logger.info(block)
        # logger.info('=' * 100)

        audio_block = item.select('div.audio-item')
        # print(audio_block)
        if not audio_block:
            logger.error('no audio-item')
            return

        title = audio_block.select_one('div.audio-item-title')
        print(title)
        if not title:
            logger.error('no title')
            return


        # title = title.get_text()
        # title = title.replace('/', '|').strip()

        # logger.info('%s', title)
        logger.info('=' * 100)

    def run(self):
        text = self.load_page()
        self.parse_page(text=text)


if __name__ == '__main__':
    parser = Main()
    parser.run()