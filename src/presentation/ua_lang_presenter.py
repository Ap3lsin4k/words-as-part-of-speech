class UkrainianLanguagePresenter:
    error_messages = []

    def __init__(self):
        print('Введіть "help", щоб подивитися більше інформації')

    def print_properties(self, result):
        print('Частина мови — {};'.format(tuple(result.keys())[0]))

        for category_of_property in result.values():
            for property, property_name in category_of_property.items():
                print('{:>10} — {};'.format(property, property_name))

    def print_words_as_examples(self, words, bookmark):
        print('Частина мови — {};'.format(bookmark.get_part_of_speech()))

        print('Слова, що відповідають характеристиці {} — {}:'.format(bookmark.category_name, bookmark.property_name))
        print("\t\t".join(words))

    def print_error(self):
        for msg in self.error_messages:
            print(msg)
        self.error_messages.clear()