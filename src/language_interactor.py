from dictionary_entity import DictionaryEntity
from word_classifier_repository import WordClassifierRepository
from word_of_same_category_repository import WordsOfSameCategoryRepository


class UkrainianLanguageInteractor(WordClassifierRepository, WordsOfSameCategoryRepository):
    def __init__(self, nested_dictionary):
        self.dictionary = DictionaryEntity(nested_dictionary)
        self.classifier = WordClassifierRepository(self.dictionary)
        self.words_same_category = WordsOfSameCategoryRepository(self.dictionary)
        super().__init__(self.dictionary)

    # WORD CLASSIFIER
    def classify(self, input_word):
        self.classifier.for_each_part_of_speech(self.classifier.make_response_model, input_word)
        return self.classifier.result

    # TODO use difflib.getclose_matches_for_command like in Linux

    # SHOW EXAMPLES OF WORDS FOR GIVEN PROPERTY, SHOW CLASS OF WORDS WITH SAME PROPERTY
    def get_examples(self, property_name):
        self.words_same_category.for_each_part_of_speech(self.words_same_category.find_words_in_category_of_properties, property_name)
        return self.words_same_category.result

    def modify(self, bookmark, old_word, new_word):
        modifiable = list(self.dictionary.get_words_for_property(bookmark))
        index = modifiable.index(old_word)
        modifiable[index] = new_word
        self.dictionary[bookmark.get_part_of_speech()][bookmark.category_name][bookmark.property_name] = tuple(modifiable)

    def update(self, param):
        self.dictionary.update(param)



