from part_of_speech import UkrainianLanguageRepository
import pytest

p = UkrainianLanguageRepository()

def test_000_characterize_noun():
    #assert dict() == p
    result = p.characterize("хлопець")
    # assert ('іменник' in result)
    assert result['іменник'] == {'рід': 'чоловічий', 'число': "однина"}

    result = p.characterize('дівчина')
    assert result == {'іменник': {'рід': 'жіночий', 'число': 'однина'}}


def test_001_characterize_numbers():
    result = p.characterize("п'ять")
    assert result == {'числівник': {'за значенням': 'кількісний'}}


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
    

def test_extend_should_fail():
    use_cases = UkrainianLanguageRepository()
    with pytest.raises(TypeError):
        use_cases.update({"прикметник": {"рід": ("чоловічий",)}})

def test_002_extend_should_fail():
    use_cases = UkrainianLanguageRepository()
    with pytest.raises(TypeError):
        use_cases.update({"прикметник": ("рід",)})


