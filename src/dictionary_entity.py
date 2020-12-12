from language_extend_behaviour import LanguageExtendBehaviour


class DictionaryEntity(LanguageExtendBehaviour):

    def __init__(self, nested_dictionary):
        super().__init__()
        self.update(nested_dictionary)

    def get_part_of_speech(self, bookmark):
        return self[bookmark.get_part_of_speech()]

    def get_properties(self, bookmark):
        return self[bookmark.get_part_of_speech()][bookmark.category_name]

    def get_words_for_property(self, bookmark):
        return self[bookmark.get_part_of_speech()][bookmark.category_name][bookmark.property_name]