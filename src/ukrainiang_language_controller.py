from language_interactor import UkrainianLanguageInteractor

ua_lang = UkrainianLanguageInteractor({
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



class PartOfSpeechPresenter:

    def show_properties(self, result):
        print('частина мови: {};'.format(tuple(result.keys())[0]))

        for category_of_property in result.values():
            for property, property_name in category_of_property.items():
                print('{:>15}: {};'.format(property, property_name))


presenter = PartOfSpeechPresenter()
#presenter.show_properties(ua_lang.characterize("хлопець"))

while True:
    command = input("Слово (або команда): ")
    if command == 'new':
        print(
            '"зелений прикметник рід чоловічий" додасть слово "зелений" до частини мови прекметник, та з родом чоловічий')
        l = input().split()

        ua_lang.update({l[1]: {l[2]: {l[3]: (l[0],)}}})

    res = ua_lang.get_examples(command)
    if (res) == None:
        res = ua_lang.classify(command)

    print(
        "Помилка: не вдалося знайти {} в словнику. Введіть new, якщо бажаєте додати слово до словника".format(command))
