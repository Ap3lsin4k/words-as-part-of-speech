from ukrainian_lanuage_repository import UkrainianLanguageExtendRepository


class UkrainianLanguageRepository(UkrainianLanguageExtendRepository):
    def __init__(self):
        super().__init__()
        self.update({
            'іменник': {
                'рід': {
                    'чоловічий':
                        ('хлопець', "потяг")
                    ,
                    'жіночий':
                        ('дівчина',),
                    'середній':
                        ("життя", "почуття", "право", "місто", "місце", "прислів'я")

                },

            },
            'числівник': {
                'за значенням': {
                    "кількісний":
                        ("п'ять", "двісті двадцять", "шість", "тридцять три", "сорок вісім"),
                    "порядковий":
                        ("четвертий", "сьомий", "десятий", "сто двадцять перший")
                }
            }

        })

    # like in Linux do suggestions if command is wrong
    # def __getattribute__(self, attribute):
    # hasattr(self, attribute)
    # pass
    def find(self, command):
        res = self.give_examples(command)
        if len(res) == 0:
            res = self.classify(command)

        raise KeyError("Помилка: не вдалося знайти {} в словнику".format(command))

    # WORD CLASSIFICATOR
    def classify(self, input_word):
        self.__for_each_part_of_speech(self.__make_response_model, input_word)
        return self.result

    # TODO use difflib.getclose_matches_for_command

    def __for_each_part_of_speech(self, handle_func, input_word_or_property):
        if input_word_or_property is None or input_word_or_property == "":
            raise ValueError("Помилка: рядок не може бути пустий")

        self.result = None
        for part_of_speech, categories_of_properties_dict in self.items():
            handle_func(part_of_speech, input_word_or_property)

            if self.result is not None:
                return
        if self.result is None:
            raise KeyError("Помилка: слово не знайдено у словнику. Перевірте прав")

    def __make_response_model(self, part_of_speech, input_word):
        self.result = {part_of_speech: {}}

        for category_of_property, properties in self[part_of_speech].items():
            bookmark = self.Bookmark(part_of_speech, category_of_property)
            self.__classify_word_by_property(bookmark, input_word)

        if len(self.result[part_of_speech]) == 0:
            self.result = None

    def __for_each_category_of_property(self, handle_func, part_of_speech, property_name):
        for category_of_property, properties in self[part_of_speech].items():
            handle_func(properties, property_name)

    def __classify_word_by_property(self, bookmark, input_word):
        for bookmark.property_name in self.get_properties(bookmark):
            words_tuple = self.get_words_for_property(bookmark)
            if input_word in words_tuple:
                self.__save_property_of_word_to_presentable_format(bookmark)

    def __save_property_of_word_to_presentable_format(self, bookmark):
        self.result[bookmark.get_part_of_speech()].update({bookmark.category_name: bookmark.property_name})
    # SHOW EXAMPLES OF WORDS FOR GIVEN PROPERTY, SHOW CLASS OF WORDS WITH SAME PROPERTY

    def give_examples(self, property_name):
        self.__for_each_part_of_speech(self.__find_words_in_category_of_properties, property_name)
        return self.result

    def __find_words_in_category_of_properties(self, part_of_speech, property_name):
        self.__for_each_category_of_property(self.__save_examples_for_given_property, part_of_speech, property_name)

    def __save_examples_for_given_property(self, properties, property_name):
        if property_name in properties:
            self.result = properties[property_name]

    class Bookmark:
        def __init__(self, part_of_speech=None, category_name=None, property_name=None):
            self.__part_of_speech = part_of_speech
            self.category_name = category_name
            self.property_name = property_name

        def get_part_of_speech(self):
            if self.__part_of_speech is not None:
                return self.__part_of_speech
            else:
                raise ValueError("Cannot get Bookmark.part_of_speech key name because it was not set to a value. "
                                 "Please specify before using.")

    def get_part_of_speech(self, bookmark):
        return self[bookmark.get_part_of_speech()]

    def get_properties(self, bookmark):
        return self[bookmark.get_part_of_speech()][bookmark.category_name]

    def get_words_for_property(self, bookmark):
        return self[bookmark.get_part_of_speech()][bookmark.category_name][bookmark.property_name]