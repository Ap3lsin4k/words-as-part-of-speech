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
    result = use_cases.get_examples("минулий")
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
    result_before_update = interactor.get_examples("plural")
    assert result_before_update == ('travellers',)

    bm = Bookmark('noun', 'grammatical number', 'plural')
    interactor.modify(bm, 'travellers', 'travelers')
    result = interactor.get_examples("plural")
    assert result == ('travelers',)

    interactor.update({'verb': {'tense': {'past': ("doed",)}}})
    result_before_modification = interactor.get_examples("past")
    assert result_before_modification == ("doed",)

    interactor.modify(Bookmark('verb', 'tense', 'past'),
                      'doed', 'did')

    result = interactor.get_examples('past')
    assert result == ('did',)
