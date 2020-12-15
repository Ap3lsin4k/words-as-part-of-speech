### Опис
Програма має 5 use cases. Відповідно кожний має свій клас
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
З нового я вивчив як працює наслідування атрибутів. Потрібно викликати __init__ для батьківського класу, після цього ми маємо доступ до атрибутів через self.<батьківський атрибут> з дочірнього класу.

### Документація по використанню коду від програміста до програмістів

https://github.com/Ap3lsin4k/words-as-part-of-speech/blob/master/tests/test_suggest_most_similiar_word.py


### 20 UNIT тестів які покривають всі можливі

```from language_interactor import UkrainianLanguageInteractor
import pytest

ua = UkrainianLanguageInteractor({
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


def test_000_characterize_noun():
    result = ua.classify("хлопець")
    assert ('іменник' in result)
    assert result['іменник'] == {'рід': 'чоловічий', 'число': "однина"}

    result = ua.classify('дівчина')
    assert result == {'іменник': {'рід': 'жіночий', 'число': 'однина'}}


def test_001_characterize_numbers():
    result = ua.classify("п'ять")
    assert result == {'числівник': {'за значенням': 'кількісний'}}


def test_should_raise_error_for_empty_input():
    with pytest.raises(ValueError):
        ua.classify("")
        ua.classify(None)
```

```import pytest
from language_interactor import UkrainianLanguageInteractor

ua = UkrainianLanguageInteractor({
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

        })


def test_property_example():
    examples, bm = ua.get_examples("середній")

    assert examples[0] == 'життя'
    assert examples[1] == 'почуття'
    assert examples[2] == 'право'
    assert bm.get_part_of_speech() == 'іменник'
    assert bm.category_name == 'рід'
    assert bm.property_name == 'середній'

    examples = ua.get_examples('однина')[0]
    assert len(examples) > 6
```

```from bookmark_entity import Bookmark
from language_interactor import UkrainianLanguageInteractor
import pytest


@pytest.fixture
def use_cases() -> UkrainianLanguageInteractor:
    return UkrainianLanguageInteractor({
        'іменник': {
            'рід': {
                'середній':
                    ("почуття",)
            },
        },
    })


def test_extend_with_new_words(use_cases):
    with pytest.raises(KeyError):
        use_cases.classify("добрий")


def test_extend_should_fail(use_cases):
    with pytest.raises(TypeError):
        use_cases.update({"прикметник": {"рід": ("чоловічий",)}})


def test_002_extend_should_fail(use_cases):
    with pytest.raises(TypeError):
        use_cases.update({"прикметник": ("рід",)})


def test_newly_added_piece_of_information(use_cases):
    with pytest.raises(KeyError):
        use_cases.classify("веселий")
    use_cases.update({"прикметник": {"рід": {"чоловічий": ("веселий",)}}})
    result = use_cases.classify("веселий")
    assert result is not None
    assert result == {'прикметник': {'рід': 'чоловічий'}}


def test_2_newly_added_words_at_the_same_time(use_cases):
    with pytest.raises(KeyError):
        use_cases.classify("гартувати")
    with pytest.raises(KeyError):
        use_cases.classify("думати")
    use_cases.update({"дієслово": {"час": {"теперішній": ("гартувати", "думати")}}})
    result = use_cases.classify("гартувати")
    assert result is not None
    assert result == {"дієслово": {"час": "теперішній"}}
    result = use_cases.classify("думати")
    assert result is not None


def test_extend_for_two_words_but_with_different_property(use_cases):
    with pytest.raises(KeyError):
        use_cases.classify("гартувати")
    with pytest.raises(KeyError):
        use_cases.classify("думав")
    use_cases.update({"дієслово": {"час": {"теперішній": ("гартувати",), "минулий": ("думав",)}}})

    result = use_cases.classify("гартувати")
    assert result is not None
    assert result == {"дієслово": {"час": "теперішній"}}
    result = use_cases.classify("думав")
    assert result == {"дієслово": {"час": "минулий"}}


def test_extend_two_parts_of_speech_at_the_same_time(use_cases):
    use_cases.update({"прикметник": {"рід": {"чоловічий": ("веселий",)}},
                      "дієслово": {"час": {"минулий": ("думав",)}}})
    result = use_cases.classify("думав")
    assert result is not None
    result = use_cases.classify("веселий")
    assert result is not None


def test_show_property_when_extended(use_cases):
    with pytest.raises(KeyError):
        result_none = use_cases.get_examples("минулий")
    use_cases.update({"дієслово": {"час": {"минулий": ("думав",)}}})
    result = use_cases.get_examples("минулий")[0]
    assert len(result) == 1
    assert result[0] == "думав"


def test_update_should_not_clean_dict(use_cases):
    result_before_update = use_cases.classify("почуття")
    with pytest.raises(KeyError):
        result_none = use_cases.classify("село")
    use_cases.update({'іменник': {'рід': {'середній': ('село',)}}})
    result = use_cases.classify('село')

    assert 'рід' in result_before_update['іменник']
    assert 'середній' == result_before_update['іменник']['рід']
    assert result == {'іменник': {'рід': 'середній'}}


def test_should_fail_edit_if_key_does_not_exist():
    interactor = UkrainianLanguageInteractor({'noun': {'grammatical number': {'plural': ("travellers",)}}})
    bm = Bookmark('noun', 'grammaticalnumber', 'plural')
    with pytest.raises(KeyError):
        interactor.modify(bm, 'travellers', 'travelers')

    bm = Bookmark('noun', 'grammatical number', 'plural')
    with pytest.raises(ValueError):
        interactor.modify(bm, 'doed', 'did')


# advanced modification
def test_edit_newly_added_word_in_tuple():
    interactor = UkrainianLanguageInteractor({'noun': {'grammatical number': {'plural': ("travellers",)}}})
    result_before_update = interactor.get_examples("plural")[0]
    assert result_before_update == ('travellers',)

    bm = Bookmark('noun', 'grammatical number', 'plural')
    interactor.modify(bm, 'travellers', 'travelers')
    result = interactor.get_examples("plural")[0]
    assert result == ('travelers',)

    interactor.update({'verb': {'tense': {'past': ("doed",)}}})
    result_before_modification = interactor.get_examples("past")[0]
    assert result_before_modification == ("doed",)

    interactor.modify(Bookmark('verb', 'tense', 'past'),
                      'doed', 'did')

    result = interactor.get_examples('past')[0]
    assert result == ('did',)
```

```
from bookmark_entity import Bookmark
from language_interactor import UkrainianLanguageInteractor
import pytest


@pytest.fixture
def use_cases() -> UkrainianLanguageInteractor:
    return UkrainianLanguageInteractor({
        'іменник': {
            'рід': {
                'середній':
                    ("почуття",)
            },
        },
    })


def test_extend_with_new_words(use_cases):
    with pytest.raises(KeyError):
        use_cases.classify("добрий")


def test_extend_should_fail(use_cases):
    with pytest.raises(TypeError):
        use_cases.update({"прикметник": {"рід": ("чоловічий",)}})


def test_002_extend_should_fail(use_cases):
    with pytest.raises(TypeError):
        use_cases.update({"прикметник": ("рід",)})


def test_newly_added_piece_of_information(use_cases):
    with pytest.raises(KeyError):
        use_cases.classify("веселий")
    use_cases.update({"прикметник": {"рід": {"чоловічий": ("веселий",)}}})
    result = use_cases.classify("веселий")
    assert result is not None
    assert result == {'прикметник': {'рід': 'чоловічий'}}


def test_2_newly_added_words_at_the_same_time(use_cases):
    with pytest.raises(KeyError):
        use_cases.classify("гартувати")
    with pytest.raises(KeyError):
        use_cases.classify("думати")
    use_cases.update({"дієслово": {"час": {"теперішній": ("гартувати", "думати")}}})
    result = use_cases.classify("гартувати")
    assert result is not None
    assert result == {"дієслово": {"час": "теперішній"}}
    result = use_cases.classify("думати")
    assert result is not None


def test_extend_for_two_words_but_with_different_property(use_cases):
    with pytest.raises(KeyError):
        use_cases.classify("гартувати")
    with pytest.raises(KeyError):
        use_cases.classify("думав")
    use_cases.update({"дієслово": {"час": {"теперішній": ("гартувати",), "минулий": ("думав",)}}})

    result = use_cases.classify("гартувати")
    assert result is not None
    assert result == {"дієслово": {"час": "теперішній"}}
    result = use_cases.classify("думав")
    assert result == {"дієслово": {"час": "минулий"}}


def test_extend_two_parts_of_speech_at_the_same_time(use_cases):
    use_cases.update({"прикметник": {"рід": {"чоловічий": ("веселий",)}},
                      "дієслово": {"час": {"минулий": ("думав",)}}})
    result = use_cases.classify("думав")
    assert result is not None
    result = use_cases.classify("веселий")
    assert result is not None


def test_show_property_when_extended(use_cases):
    with pytest.raises(KeyError):
        result_none = use_cases.get_examples("минулий")
    use_cases.update({"дієслово": {"час": {"минулий": ("думав",)}}})
    result = use_cases.get_examples("минулий")[0]
    assert len(result) == 1
    assert result[0] == "думав"


def test_update_should_not_clean_dict(use_cases):
    result_before_update = use_cases.classify("почуття")
    with pytest.raises(KeyError):
        result_none = use_cases.classify("село")
    use_cases.update({'іменник': {'рід': {'середній': ('село',)}}})
    result = use_cases.classify('село')

    assert 'рід' in result_before_update['іменник']
    assert 'середній' == result_before_update['іменник']['рід']
    assert result == {'іменник': {'рід': 'середній'}}


def test_should_fail_edit_if_key_does_not_exist():
    interactor = UkrainianLanguageInteractor({'noun': {'grammatical number': {'plural': ("travellers",)}}})
    bm = Bookmark('noun', 'grammaticalnumber', 'plural')
    with pytest.raises(KeyError):
        interactor.modify(bm, 'travellers', 'travelers')

    bm = Bookmark('noun', 'grammatical number', 'plural')
    with pytest.raises(ValueError):
        interactor.modify(bm, 'doed', 'did')


# advanced modification
def test_edit_newly_added_word_in_tuple():
    interactor = UkrainianLanguageInteractor({'noun': {'grammatical number': {'plural': ("travellers",)}}})
    result_before_update = interactor.get_examples("plural")[0]
    assert result_before_update == ('travellers',)

    bm = Bookmark('noun', 'grammatical number', 'plural')
    interactor.modify(bm, 'travellers', 'travelers')
    result = interactor.get_examples("plural")[0]
    assert result == ('travelers',)

    interactor.update({'verb': {'tense': {'past': ("doed",)}}})
    result_before_modification = interactor.get_examples("past")[0]
    assert result_before_modification == ("doed",)

    interactor.modify(Bookmark('verb', 'tense', 'past'),
                      'doed', 'did')

    result = interactor.get_examples('past')[0]
    assert result == ('did',)
```
