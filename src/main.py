from part_of_speech import PartOfSpeech

ua_lang = PartOfSpeech()


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

    res = ua_lang.give_examples(command)
    if (res) == None:
        res = ua_lang.characterize(command)

    print(
        "Помилка: не вдалося знайти {} в словнику. Введіть new, якщо бажаєте додати слово до словника".format(command))
