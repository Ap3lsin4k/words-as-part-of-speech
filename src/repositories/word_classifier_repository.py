from bookmark_entity import Bookmark
from language_entity import LanguageEntity
from repositories.dictionary_surfer_common import DictionarySurferRepository


class WordClassifierRepository(DictionarySurferRepository):

    def __init__(self, dictionary_entity: LanguageEntity):
        super().__init__(dictionary_entity)

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