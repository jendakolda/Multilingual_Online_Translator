import requests
from bs4 import BeautifulSoup


class Translator(object):
    pairs = {'en': 'french-english', 'fr': 'english-french'}
    lang_shorts = {'en': 'English', 'fr': 'French'}
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
        web_data = BeautifulSoup(response.content, 'lxml')
        words = web_data.find('div', attrs={'id': 'translations-content'})
        translations = words.find_all('a')
        # translations = [word.text.replace(' ', '').replace('\n', '') for word in words]
        synonyms = list()
        for word in translations:
            synonyms.append(word.text.strip())


        src_phrases = web_data.find_all("div", {"class": "src ltr"})
        tran_phrases = web_data.find_all("div", {"class": "trg ltr"})

        lst_src_phrases = [phrase.text.strip() for phrase in src_phrases]
        lst_tran_phrases = [phrase.text.strip() for phrase in tran_phrases]

        print(response.status_code, 'OK\n' if response else 'Denied')
        print(f'Context examples:\n\n{Translator.lang_shorts[self.language]} Translations:')
        print(*synonyms[:5], sep='\n')

        print(f'\n{Translator.lang_shorts[self.language]} Examples:\n')
        print(*[lst_src_phrases[i] + '\n' + lst_tran_phrases[i] for i in range(5)], sep='\n')


Translator().main()
