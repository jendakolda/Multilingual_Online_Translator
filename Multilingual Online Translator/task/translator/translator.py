import requests
from bs4 import BeautifulSoup


class Translator(object):
    pairs = {'en': 'french-english', 'fr': 'english-french'}
    user_agent = 'Mozilla/5.0'

    def __init__(self):
        # self.language = input('Type "en" if you want to translate from French into English,'
        #                       ' or "fr" if you want to translate from English into French:')
        # self.word = input('Type the word you want to translate:')
        self.language = 'fr'
        self.word = 'hello'
        print(f'You chose "{self.language}" as a language to translate "{self.word}".')

    def form_request(self):
        return f'https://context.reverso.net/translation/{Translator.pairs[self.language]}/{self.word}'

    def main(self):

        response = requests.get(Translator.form_request(self), headers={'User-Agent': Translator.user_agent})
        src = response.content
        web_data = BeautifulSoup(src, 'html.parser')
        translations = []
        words = web_data.find('div', attrs={'id': 'translations-content'})
        translations = [word.text.strip('\n "') for word in words]
        # for word in words:
        #     print(word.text)
        print(words)


        print(response.status_code, 'OK' if response else 'Denied')
        print('Translations')
        # print(translations)


Translator().main()
