from part_of_speech import UkrainianLanguageInteractor
import pytest


@pytest.fixture
def use_cases() -> UkrainianLanguageInteractor:
    return UkrainianLanguageInteractor()


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
# ability to save information to file and clean it
