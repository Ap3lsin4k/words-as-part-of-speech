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
            'відміна': {
                'перша':
                    ("дівчина", "ледащо", "сирота", "нероба", "розбишака", "бідолаха", "староста"),
                'друга':
                    ("хлопець", "потяг", "життя", "почуття", "право", "місто", "місце", "прислів'я", "каменяр"),
                'третя':
                    ("нехворощ", "любов", "мати"),
                'четверта':
                    ("ягня",)
            }
        },

    })


def test_should_suggest_the_word_itself_when_perfect_match(use_cases):
    result = use_cases.get_close_matches('іменник')
    assert 'іменник' in result


def test_should_suggest_if_typo_at_second_level(use_cases):
    result = use_cases.get_close_matches('род')
    assert 'рід' in result
    result = use_cases.get_close_matches('відмінок')
    assert 'відміна' in result


def test_should_suggest_when_multiple_parts_of_speech(use_cases):
    use_cases.update({'числівник': {
        'за значенням': {
            "кількісний":
                ("п'ять", "двісті двадцять", "шість", "тридцять три", "сорок вісім"),
            "порядковий":
                ("четвертий", "сьомий", "десятий", "сто двадцять перший")
        }
    }})

    result = use_cases.get_close_matches('іменик')
    assert 'іменник' in result

    result = use_cases.get_close_matches('числівник')
    assert 'числівник' in result

    result = use_cases.get_close_matches('кількістний')
    assert 'кількісний' in result


def test_should_suggest_multiple_words(use_cases):
    suggested = use_cases.get_close_matches("місцо")

    assert 'місто' in suggested
    assert 'місце' in suggested


def test_should_not_contain_duplicates(use_cases):
    result = use_cases.get_close_matches("почутя")
    assert 'почуття' in result
