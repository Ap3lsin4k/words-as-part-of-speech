from language_entity import LanguageEntity
from dictionary_surfer_common import DictionarySurferRepository


class WordsOfSameCategoryRepository(DictionarySurferRepository):

    def __init__(self, dictionary_entity: LanguageEntity):
        super().__init__(dictionary_entity)
        self.result = None
        self.bm = None

    def find_words_in_category_of_properties(self, part_of_speech, property_name):
        self.for_each_category_of_property(self.__save_examples_for_given_property, part_of_speech, property_name)

    def __save_examples_for_given_property(self, bm, property_name):
        if property_name in self.dictionary.get_properties(bm):
            self.bm = bm
            self.bm.property_name = property_name
            self.result = self.dictionary.get_words_for_property(bm)