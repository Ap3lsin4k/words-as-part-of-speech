from bookmark_entity import Bookmark
from dictionary_entity import DictionaryEntity


class DictionarySurferRepository:
    def __init__(self, dictionary_entity: DictionaryEntity):
        self.dictionary = dictionary_entity

    def for_each_part_of_speech(self, handle_func, input_word_or_property):
        if input_word_or_property is None or input_word_or_property == "":
            raise ValueError("Помилка: рядок не може бути пустий")

        self.setResult(None)
        for part_of_speech, categories_of_properties_dict in self.dictionary.items():
            handle_func(part_of_speech, input_word_or_property)

            if self.getResult() is not None:
                return
        if self.getResult() is None:
            raise KeyError("Помилка: слово не знайдено у словнику.")

    def for_each_category_of_property(self, handle_func, part_of_speech, property_name):
        for category_of_property, properties in self.dictionary[part_of_speech].items():
            handle_func(properties, property_name)

    def setResult(self, result):
        self._result = result

    def getResult(self):
        return self._result


class WordClassificatorRepository(DictionarySurferRepository):

    def setResult(self, result):
        self.result = result

    def getResult(self):
        return self.result

    def make_response_model(self, part_of_speech, input_word):
        self.result = {part_of_speech: {}}

        for category_of_property, properties in self.dictionary[part_of_speech].items():
            bookmark = Bookmark(part_of_speech, category_of_property)
            self.__classify_word_by_property(bookmark, input_word)

        if len(self.result[part_of_speech]) == 0:
            self.result = None

    def __save_property_of_word_to_presentable_format(self, bookmark):
        self.result[bookmark.get_part_of_speech()].update({bookmark.category_name: bookmark.property_name})

    def __classify_word_by_property(self, bookmark, input_word):
        for bookmark.property_name in self.dictionary.get_properties(bookmark):
            words_tuple = self.dictionary.get_words_for_property(bookmark)
            if input_word in words_tuple:
                self.__save_property_of_word_to_presentable_format(bookmark)


class WordsOfSameCategoryRepository(DictionarySurferRepository):
    def setResult(self, result):
        self.result = result

    def getResult(self):
        return self.result

    def __save_examples_for_given_property(self, properties, property_name):
        if property_name in properties:
            self.result = properties[property_name]

    def find_words_in_category_of_properties(self, part_of_speech, property_name):
        self.for_each_category_of_property(self.__save_examples_for_given_property, part_of_speech, property_name)


class UkrainianLanguageInteractor(WordClassificatorRepository, WordsOfSameCategoryRepository):
    def __init__(self, nested_dictionary):
        #super().__init__(nested_dictionary)

        self.dictionary = DictionaryEntity(nested_dictionary)
        self.classifier = WordClassificatorRepository(self.dictionary)
        self.words_same_category = WordsOfSameCategoryRepository(self.dictionary)
        super().__init__(self.dictionary)
    # like in Linux do suggestions if command is wrong
    # def __getattribute__(self, attribute):
    # hasattr(self, attribute)
# reason: not tested with unit testing
#    def find(self, command):
#        res = self.get_examples(command)
#        if len(res) == 0:
#            res = self.classify(command)

#        raise KeyError("Помилка: не вдалося знайти {} в словнику".format(command))

    # WORD CLASSIFICATOR
    def classify(self, input_word):
        self.classifier.for_each_part_of_speech(self.classifier.make_response_model, input_word)
        return self.classifier.result

    # TODO use difflib.getclose_matches_for_command

    # SHOW EXAMPLES OF WORDS FOR GIVEN PROPERTY, SHOW CLASS OF WORDS WITH SAME PROPERTY
    def get_examples(self, property_name):
        self.words_same_category.for_each_part_of_speech(self.words_same_category.find_words_in_category_of_properties, property_name)
        return self.words_same_category.result

    def modify(self, bookmark, old_word, new_word):
        modifiable = list(self.dictionary.get_words_for_property(bookmark))
        index = modifiable.index(old_word)
        modifiable[index] = new_word
        self.dictionary[bookmark.get_part_of_speech()][bookmark.category_name][bookmark.property_name] = tuple(modifiable)

    def update(self, param):
        self.dictionary.update(param)



