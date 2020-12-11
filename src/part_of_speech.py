from copy import deepcopy


class UkrainianLanguageRepository(dict):
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
                'число': {
                    'однина':
                        ('хлопець', "дівчина", "життя", "почуття", "право", "місто", "місце", "прислів'я", "потяг"),
                    'множина':
                        ("потяги", "двері", "штани", "ножиці")
                }
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

    def update(self, E=None, **F):  # known special case of dict.update
        if hasattr(E, "keys"):
            for part_of_speech in E.keys():
                self.__assign_if_key_does_not_exist(self, part_of_speech)
                if hasattr(E[part_of_speech], "keys"):
                    self.__update_each_category(self[part_of_speech], E[part_of_speech])
                else:
                    raise TypeError("Expected to get dictionary with category properties as keys, but got {}"
                                    .format(type(E[part_of_speech])))
        else:
            raise NotImplementedError

    def __update_each_category(self, dictionary_set_by_reference, second_lvl_dict):
        for category in second_lvl_dict.keys():
            self.dictionary_slice_reference = dictionary_set_by_reference
            self.__assign_if_key_does_not_exist(dictionary_set_by_reference, category)
            del self.dictionary_slice_reference
            self.__update_each_property(dictionary_set_by_reference[category], second_lvl_dict[category])

    def __update_each_property(self, dict_reference, in_dictionary):
        for property in in_dictionary:
            self.dictionary_slice_reference = dict_reference
            self.__push_back_words_to_property(dict_reference, property, in_dictionary[property])
            del self.dictionary_slice_reference

    def __push_back_words_to_property(self, dict_reference, property_key, new_words):
        self.__assign_if_key_does_not_exist(dict_reference, property_key, default_value=tuple())
        self.dictionary_slice_reference[property_key] = self.dictionary_slice_reference[property_key] + new_words

    def __assign_if_key_does_not_exist(self, dict_ref, key, default_value=None):
        if default_value is None:
            default_value = dict()
        if key not in dict_ref:
            dict_ref[key] = default_value


    def characterize(self, input_word):
        for part_of_speech, categories_of_properties in self.items():
            result = {part_of_speech: {}}
            for category_of_property, properties in categories_of_properties.items():
                for property_name, words_tuple in properties.items():
                    if input_word in words_tuple:
                        result[part_of_speech].update({category_of_property: property_name})

            if len(result[part_of_speech]) > 0:
                return result

    def give_examples(self, property_name):
        for part_of_speech, categories_of_properties in self.items():
            for category_of_property, properties in categories_of_properties.items():
                if property_name in properties:
                    return properties[property_name]

    def find(self, command):
        res = self.give_examples(command)
        if len(res) == 0:
            res = self.characterize(command)

        raise KeyError("Помилка: не вдалося знайти {} в словнику".format(command))
