from part_of_speech import UkrainianLanguageRepository
import pytest


def test_default_dictionary():
    p = UkrainianLanguageRepository()
    #assert dict() == p
    result = p.characterize("хлопець")
    # assert ('іменник' in result)
    assert result['іменник'] == {'рід': 'чоловічий', 'число': "однина"}

    result = p.characterize('дівчина')
    assert result == {'іменник': {'рід': 'жіночий', 'число': 'однина'}}
    result = p.characterize("п'ять")
    assert result == {'числівник': {'за значенням': 'кількісний'}}
    # p.what_can_we_say("хлопець")
    # "іменник" -> example of nouns
    # "число" -> example of singular and plural words
    # "жіночий" -> example of words
    # append new words
    # edit words?
    # throw exception if word is not found


def test_property_example():
    p = UkrainianLanguageRepository()

    examples = p.give_examples("середній")

    assert examples[0] == 'життя'
    assert examples[1] == 'почуття'
    assert examples[2] == 'право'

    examples = p.give_examples('однина')
    assert len(examples) > 6


def test_extend_with_new_words():
    use_cases = UkrainianLanguageRepository()
    assert use_cases.characterize("веселий") is None
    with pytest.raises(TypeError):
        use_cases.update({"прикметник": {"рід": ("чоловічий")}})



