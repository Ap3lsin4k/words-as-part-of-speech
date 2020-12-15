### Опис алгоритму
Програма має 4 use case.
1. Класифікувати слово
2. Показати приклади слів для назви характеристики
3. Редагувати слово в словнику (наприклад, коли змінюється правопис "індик" -> "индик")
4. Додавання нових слів, характеристик, частин мови.
5. Показ підказок користувачу, якщо він ввів слово неправильно. ("місцо" запропонує виправлення ["місто", "місце"]
```
class UkrainianLanguageInteractor():
    def __init__(self, nested_dictionary):
        self.__dictionary = LanguageEntity(nested_dictionary)
        self.__classifier = WordClassifierRepository(self.__dictionary)
        self.__words_same_category = WordsOfSameCategoryRepository(self.__dictionary)

    # WORD CLASSIFIER
    def classify(self, input_word):
        self.__classifier.for_each_part_of_speech(self.__classifier.make_response_model, input_word)
        return self.__classifier.result

    # SHOW EXAMPLES OF WORDS FOR GIVEN PROPERTY, SHOW CLASS OF WORDS WITH SAME PROPERTY
    def get_examples(self, property_name):
        self.__words_same_category.for_each_part_of_speech(self.__words_same_category.find_words_in_category_of_properties, property_name)
        res = [self.__words_same_category.result, self.__words_same_category.bm]
        return res

    def modify(self, bookmark, old_word, new_word):
        modifiable = list(self.__dictionary.get_words_for_property(bookmark))
        index = modifiable.index(old_word)
        modifiable[index] = new_word
        self.__dictionary[bookmark.get_part_of_speech()][bookmark.category_name][bookmark.property_name] = tuple(modifiable)

    def update(self, param):
        self.__dictionary.update(param)

    def construct_close_matches(self, typo):
        suggestion = set()
        CorrectTypo().get_close_matches(suggestion, self.__dictionary, typo)
        return suggestion
```
### Висновок
З нового я вивчив як працює наслідування атрибутів. Потрібно викликати __init__ для батьківського класу, після цього ми маємо доступ до атрибутів через self.<батьківський атрибут> з дочірнього класу.С
