
"""
Various methods useful for tests and similar operations.
"""

import csv

DICT_FNAME = "openformats/tests/common/dictionary.csv"


class FunkyDictionary(object):
    def __init__(self):
        self.phrase_list = []
        self.phrase_dict = {}
        with open(DICT_FNAME, 'rU') as dict_file:
            dict_reader = csv.DictReader(dict_file)
            for phrase in dict_reader:
                self.phrase_list.append(phrase)
                # We can assume 'en' is going to be used as a source language
                # often, so it makes sense to be able to do quick lookups
                self.phrase_dict[phrase['en']] = phrase

    def translate(self, phrase, to_lang, from_lang="en", debug=False):
        if from_lang == "en":
            try:
                if debug:
                    print('Lookup for "{}" successful'.format(phrase[:20]))
                return self.phrase_dict[phrase][to_lang]
            except KeyError:
                pass
        else:
            for dict_phrase in self.phrase_list:
                if phrase == dict_phrase[from_lang]:
                    return dict_phrase[to_lang]
        # Phrase not found in funky dict
        if debug:
            print('Lookup for "{}" unsuccessful.'.format(phrase[:20]))
        return "{}:{}".format(to_lang, phrase)


funky_dictionary = FunkyDictionary()


def translate_stringset(stringset, from_lang="en", to_lang="el", debug=False):
    for s in stringset:
        for rule, pluralform in s._strings.items():
            s._strings[rule] = funky_dictionary.translate(
                pluralform, to_lang, from_lang, debug
            )
    return stringset
