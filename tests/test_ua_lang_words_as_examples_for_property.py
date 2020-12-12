from part_of_speech import UkrainianLanguageInteractor

ua = UkrainianLanguageInteractor()


def test_property_example():
    examples = ua.give_examples("середній")

    assert examples[0] == 'життя'
    assert examples[1] == 'почуття'
    assert examples[2] == 'право'

    examples = ua.give_examples('однина')
    assert len(examples) > 6
