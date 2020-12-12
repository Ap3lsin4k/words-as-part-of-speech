from language_entity import LanguageEntity


class DictionarySurferRepository:

    def __init__(self, dictionary_entity: LanguageEntity):
        self.dictionary = dictionary_entity
        self.result = None

    def for_each_part_of_speech(self, handle_func, input_word_or_property):
        if input_word_or_property is None or input_word_or_property == "":
            raise ValueError("Помилка: рядок не може бути пустий")

        self.result = None
        for part_of_speech, categories_of_properties_dict in self.dictionary.items():
            handle_func(part_of_speech, input_word_or_property)

            if self.result is not None:
                return
        if self.result is None:
            raise KeyError("Помилка: слово не знайдено у словнику.")

    def for_each_category_of_property(self, handle_func, part_of_speech, property_name):
        for category_of_property, properties in self.dictionary[part_of_speech].items():
            handle_func(properties, property_name)