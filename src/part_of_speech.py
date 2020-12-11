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
                if hasattr(E[part_of_speech], "keys"):
                    for category in E[part_of_speech].keys():
                        for property in E[part_of_speech][category]:
                            self.__initialize_if_key_not_exist(self, part_of_speech)
                            self.__initialize_empty_dict_if_key_not_exist(self[part_of_speech], category)
                            if property not in self[part_of_speech][category]:
                                # new property "чоловічий
                                self[part_of_speech][category][property] = E[part_of_speech][category][property]
                            else:
                                # append to existing property
                                self[part_of_speech][category][property] = self[part_of_speech][category][property] \
                                                                           + E[part_of_speech][category][property]
                else:
                    raise TypeError("Expected to get dictionary with category properties as keys, but got {}"
                                    .format(type(E[part_of_speech])))
        else:
            raise NotImplementedError

    def __initialize_if_key_not_exist(self, dictionary_ref, key, default_value=None):
        if default_value is None:
            default_value = dict()
        if key not in dictionary_ref:
            dictionary_ref[key] = dict()

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
