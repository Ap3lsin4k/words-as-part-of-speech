import pytest
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