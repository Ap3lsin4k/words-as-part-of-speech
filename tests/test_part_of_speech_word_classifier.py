from language_interactor import UkrainianLanguageInteractor
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
