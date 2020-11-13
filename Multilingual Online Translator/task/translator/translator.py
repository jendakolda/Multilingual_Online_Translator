import requests
from bs4 import BeautifulSoup
import sys


class Translator(object):
    langs = dict(enumerate(['Arabic', 'German', 'English', 'Spanish', 'French',
                            'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish'],
                           start=1))
    user_agent = 'Mozilla/5.0'

    def __init__(self):
        args = sys.argv
        try:
            self.src_lang, self.tran_lang, self.word = args[1:]
            if self.tran_lang == 'all':
                self.tran_lang = list(v for v in Translator.langs.values())
                self.length = 1
            else:
                self.tran_lang = [self.tran_lang]
                self.length = 5
                
        except ValueError:
            print('Hello, you\'re welcome to the translator. Translator supports: ')
            print(*[str(k) + '. ' + v for k, v in Translator.langs.items()], sep='\n')
            # print(f'You chose "{self.language}" as a language to translate "{self.word}".')
            while True:
                try:
                    self.src_lang = Translator.langs[int(input('Type the number of your language:\n '))]
                    break
                except KeyError:
                    print('Inserted value has to be 1-13.')

            while True:
                lang_num = int(input('Type the number of a language you want to translate to or \'0\''
                                     ' to translate to all languages:\n'))
                if lang_num == 0:
                    self.length = 1
                    self.tran_lang = list(v for v in Translator.langs.values())
                    # print(self.tran_lang)
                    break
                elif 1 <= lang_num <= 13:
                    self.tran_lang = [Translator.langs[lang_num]]
                    self.length = 5
                    break
                else:
                    print('Inserted value has to be 0-13.')

            self.word = input('Type the word you want to translate:\n')
        self.output_file = open(f'{self.word}.txt', 'w', encoding='utf-8')

    def form_request(self, lang):
        return f'https://context.reverso.net/translation/{self.src_lang.lower()}-{lang.lower()}/{self.word}'

    def main(self):
        self.output_file = open(f'{self.word}.txt', 'w', encoding='utf-8')
        for lang in self.tran_lang:
            self.get_translation(lang)
        self.output_file.close()

    def get_translation(self, lang):
        if self.src_lang.lower() == lang.lower():
            return
        response = requests.get(Translator.form_request(self, lang), headers={'User-Agent': Translator.user_agent})
        web_data = BeautifulSoup(response.content, 'lxml')
        words = web_data.find('div', attrs={'id': 'translations-content'})
        translations = words.find_all('a')
        synonyms = [translation.text.strip() for translation in translations]

        src_phrases = web_data.find_all("div", {"class": "src ltr"})
        tran_phrases = web_data.find_all("div", {"class": "trg ltr"})

        lst_src_phrases = [phrase.text.strip() for phrase in src_phrases]
        lst_tran_phrases = [phrase.text.strip() for phrase in tran_phrases]

        print(response.status_code, 'OK\n' if response else 'Denied')
        print(f'Context examples:\n\n{lang.capitalize()} Translations:')
        self.output_file.write(f'\n\n{lang.capitalize()} Translations:\n')
        print(*synonyms[:self.length], sep='\n')
        # self.output_file.writelines(*synonyms[:self.length])
        for i in range(self.length):
            self.output_file.write(synonyms[i] + '\n')

        print(f'\n{lang.capitalize()} Examples:\n')
        self.output_file.write(f'\n\n{lang.capitalize()} Example:\n')
        if tran_phrases:
            print(*[lst_src_phrases[i] + '\n' + lst_tran_phrases[i] + '\n' for i in range(self.length)], sep='\n')
            for i in range(self.length):
                self.output_file.write(lst_src_phrases[i] + '\n')
                self.output_file.write(lst_tran_phrases[i] + '\n')


Translator().main()
