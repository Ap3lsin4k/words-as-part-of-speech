class PartOfSpeech(dict):

    # like in Linux do suggestions if command is wrong
    # def __getattribute__(self, attribute):
    # hasattr(self, attribute)
    #    pass

    def __init__(self):
        super().__init__()

        # згенерувати список з ключами - українські літери, значення - пусті словники
        # for i in range(1072, 1072 + 33):
        #    self.update({chr(i): dict()})

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
                        ('хлопець', "дівчина", "життя", "почуття", "право","місто", "місце", "прислів'я", "потяг"),
                    'множина':
                        ("потяги", "двері","штани","ножиці")
                }
            },
            'числівник': {
                'за значенням': {
                    "кількісний":
                        ("п'ять", "двісті двадцять", "шість","тридцять три", "сорок вісім"),
                    "порядковий":
                        ("четвертий", "сьомий", "десятий", "сто двадцять перший")
                }
            }

        })

    def characterize(self, word):
        for part_of_speech, categories_of_properties in self.items():
            result = {part_of_speech:{}}

            for category_of_property, properties in categories_of_properties.items():
                for property_name, property_word_examples in properties.items():
                    if word in property_word_examples:
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