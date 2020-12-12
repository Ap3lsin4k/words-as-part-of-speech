from part_of_speech import UkrainianLanguageInteractor
import pytest

ua = UkrainianLanguageInteractor()


def test_000_characterize_noun():
    # assert dict() == p
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
