import pytest
from ukrainian_language_interactor import UkrainianLanguageInteractor

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
    examples = ua.get_examples("середній")

    assert examples[0] == 'життя'
    assert examples[1] == 'почуття'
    assert examples[2] == 'право'

    examples = ua.get_examples('однина')
    assert len(examples) > 6


@pytest.mark.skip("Not implemented")
def test_property():
    examples = ua.get_examples('')

    pass

# todo show that a property is present in noun and adjective
# todo ability to enter part of speech and then property
