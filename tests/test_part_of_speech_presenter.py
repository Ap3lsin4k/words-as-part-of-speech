from part_of_speech_presenter import PartOfSpeechPresenter

import builtins

from tests.view_mock import ViewMock


def test_construction_and_view_initialization():
    viewmock = ViewMock()
    p = PartOfSpeechPresenter(viewmock)
    
    p.show_properties("рід", "чоловічий")
    assert viewmock.get() == "хлопець"
    # будинок