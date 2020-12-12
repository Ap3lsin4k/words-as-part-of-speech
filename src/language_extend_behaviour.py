from copy import deepcopy


class LanguageExtendBehaviour(dict):

        # like in Linux do suggestions if command is wrong
        # def __getattribute__(self, attribute):
        # hasattr(self, attribute)
        # pass

    def update(self, E=None, **F):  # known special case of dict.update
        if hasattr(E, "keys"):
            for part_of_speech in E.keys():
                self.__initialize_part_of_speech(E, part_of_speech)
        else:
            raise NotImplementedError

    def __initialize_part_of_speech(self, in_first_lvl_dict, part_of_speech):
        self.__assign_if_key_does_not_exist(self, part_of_speech)
        self.__try_update_each_category(self[part_of_speech], in_first_lvl_dict[part_of_speech])

    def __try_update_each_category(self, dictionary_set_by_reference, in_categories_dict):
        if hasattr(in_categories_dict, "keys"):
            self.__update_each_category(dictionary_set_by_reference, in_categories_dict)
        else:
            raise TypeError("Expected to get dictionary with category properties as keys, but got {}"
                            .format(type(in_categories_dict)))

    def __update_each_category(self, dictionary_set_by_reference, second_lvl_dict):
        for category in second_lvl_dict.keys():
            self.__assign_if_key_does_not_exist(dictionary_set_by_reference, category)
            self.__try_update_each_property(dictionary_set_by_reference[category], second_lvl_dict[category])

    def __try_update_each_property(self, dict_reference, in_dictionary):
        if not isinstance(in_dictionary, dict):
            raise TypeError("Expected to get dictionary, but got {}"
                            .format(type(in_dictionary)))

        self.__update_each_property(dict_reference, in_dictionary)

    def __update_each_property(self, dict_reference, in_dictionary):
        for property_name in in_dictionary:
            self.__push_back_words_to_property(dict_reference, property_name, in_dictionary[property_name])

    def __push_back_words_to_property(self, dict_reference, property_key, new_words):
        self.__assign_if_key_does_not_exist(dict_reference, property_key, default_value=tuple())
        dict_reference[property_key] = dict_reference[property_key] + new_words

    def __assign_if_key_does_not_exist(self, dict_ref, key, default_value=None):
        if default_value is None:
            default_value = dict()

        if not isinstance(dict_ref, dict):
            raise TypeError("Expected to get dictionary, but got {}".format(type(dict_ref)))

        if key not in dict_ref:
            dict_ref[key] = default_value

# TODO ability to save information to file and clean it. It is not a business logic but a detail, so de we really need it? not now
