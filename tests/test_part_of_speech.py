from part_of_speech import UkrainianLanguageRepository
import pytest

p = UkrainianLanguageRepository()


@pytest.fixture
def use_cases() -> UkrainianLanguageRepository:
    return UkrainianLanguageRepository()

def test_000_characterize_noun():
    # assert dict() == p
    result = p.classify("хлопець")
    # assert ('іменник' in result)
    assert result['іменник'] == {'рід': 'чоловічий', 'число': "однина"}

    result = p.classify('дівчина')
    assert result == {'іменник': {'рід': 'жіночий', 'число': 'однина'}}


def test_001_characterize_numbers():
    result = p.classify("п'ять")
    assert result == {'числівник': {'за значенням': 'кількісний'}}


def test_property_example():
    p = UkrainianLanguageRepository()

    examples = p.give_examples("середній")

    assert examples[0] == 'життя'
    assert examples[1] == 'почуття'
    assert examples[2] == 'право'

    examples = p.give_examples('однина')
    assert len(examples) > 6


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


def test_should_raise_error_for_empty_input(use_cases):
    with pytest.raises(ValueError):
        use_cases.classify("")
        use_cases.classify(None)

def test_2_newly_added_words(use_cases):
    with pytest.raises(KeyError):
        use_cases.classify("гартувати")

# ability to save information to file and clean it