class Translator(object):

    def __init__(self):
        self.language = input('Type "en" if you want to translate from French into English,'
                              ' or "fr" if you want to translate from English into French:')
        self.word = input('Type the word you want to translate:')
        print(f'You chose "{self.language}" as the language to translate "{self.word}" to.')


Translator()
