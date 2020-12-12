from dictionary_entity import DictionaryEntity
from dictionary_surfer_common import DictionarySurferRepository


class WordsOfSameCategoryRepository(DictionarySurferRepository):

    def __init__(self, dictionary_entity: DictionaryEntity):
        super().__init__(dictionary_entity)
        self.result = None

    def __save_examples_for_given_property(self, properties, property_name):
        if property_name in properties:
            self.result = properties[property_name]

    def find_words_in_category_of_properties(self, part_of_speech, property_name):
        self.for_each_category_of_property(self.__save_examples_for_given_property, part_of_speech, property_name)