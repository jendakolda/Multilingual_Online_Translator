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
        web_data = BeautifulSoup(response.content, 'lxml')
        print(response.status_code, 'OK' if response else 'Denied')
        print('Translations')
        words = web_data.find('div', attrs={'id': 'translations-content'})
        translations = words.find_all('a')
        # translations = [word.text.replace(' ', '').replace('\n', '') for word in words]
        synonyms = list()
        for word in translations:
            synonyms.append(word.text.strip())
        print(synonyms)
        # examps = web_data.find('section', attrs={'id': 'examples-content'})
        # sentences = examps.find_all('div', attrs={'class': 'example'})
        # examples = list()
        # for sentence in sentences:
        #     examples.append(sentence.text.strip())
        phrases = web_data.find_all('div', {'class': 'src ltr'})
        phrases += web_data.find_all('div', {'class': 'trg ltr'})
        lst_phrases = [phrase.text.strip() for phrase in phrases]
        print(lst_phrases)


Translator().main()
