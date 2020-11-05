import requests
from bs4 import BeautifulSoup


class Translator(object):
    langs = dict(enumerate(['Arabic', 'German', 'English', 'Spanish', 'French',
                            'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish'],
                           start=1))
    user_agent = 'Mozilla/5.0'

    def __init__(self):
        print('Hello, you\'re welcome to the translator. Translator supports: ')
        print(*[str(k) + '. ' + v for k, v in Translator.langs.items()], sep='\n')
        # print(f'You chose "{self.language}" as a language to translate "{self.word}".')
        self.src_lang = Translator.langs[int(input('Type the number of your language:\n '))]
        self.tran_lang = Translator.langs[int(input('Type the number of language you want to translate to: \n'))]
        self.word = input('Type the word you want to translate:\n')

    def form_request(self):
        return f'https://context.reverso.net/translation/{self.src_lang.lower()}-{self.tran_lang.lower()}/{self.word}'

    def main(self):
        response = requests.get(Translator.form_request(self), headers={'User-Agent': Translator.user_agent})
        web_data = BeautifulSoup(response.content, 'lxml')
        words = web_data.find('div', attrs={'id': 'translations-content'})
        translations = words.find_all('a')
        synonyms = list()
        for word in translations:
            synonyms.append(word.text.strip())

        src_phrases = web_data.find_all("div", {"class": "src ltr"})
        tran_phrases = web_data.find_all("div", {"class": "trg ltr"})

        lst_src_phrases = [phrase.text.strip() for phrase in src_phrases]
        lst_tran_phrases = [phrase.text.strip() for phrase in tran_phrases]

        print(response.status_code, 'OK\n' if response else 'Denied')
        print(f'Context examples:\n\n{self.tran_lang} Translations:')
        print(*synonyms[:5], sep='\n')

        print(f'\n{self.tran_lang} Examples:\n')
        print(*[lst_src_phrases[i] + '\n' + lst_tran_phrases[i] + '\n' for i in range(5)], sep='\n')


Translator().main()
