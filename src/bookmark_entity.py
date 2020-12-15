# bookmark_entity.py
class Bookmark:
    def __init__(self, part_of_speech=None, category_name=None, property_name=None):
        self.__part_of_speech = part_of_speech
        self.category_name = category_name
        self.property_name = property_name

    def get_part_of_speech(self):
        if self.__part_of_speech is not None:
            return self.__part_of_speech
        else:
            raise ValueError("Cannot get Bookmark.part_of_speech key name because it was not set to a value. "
                             "Please specify before using.")
