import fnmatch
from os import listdir, path
from os.path import isfile, join
from openformats.utils.tests import translate_stringset


class CommonFormatTestCase(object):
    """
    Define a set of tests to be run by every file format.

    Required class variables and examples for them:

        FORMAT_EXTENSION = "txt"
        HANDLER_CLASS = PlaintextHandler
        TESTFILE_BASE = "openformats/tests/plaintext/files"
    """

    def __init__(self, *args, **kwargs):
        self.data = {}
        super(CommonFormatTestCase, self).__init__(*args, **kwargs)

    def read_files(self, ftypes=('en', 'el', 'tpl')):
        """
        Read test data files into variables.

        Example: 1_en.txt stored into self.data["1_en"]
        """

        # Find source files to use as a base to read all others
        en_files = []
        for f in listdir(self.TESTFILE_BASE):
            if (isfile(join(self.TESTFILE_BASE, f)) and
                    fnmatch.fnmatch(f, '*_en.*')):
                en_files.append(f)

        file_nums = set([f.split("_")[0] for f in en_files])
        for num in file_nums:
            for ftype in ftypes:
                name = "%s_%s" % (num, ftype)  # 1_en, 1_fr etc.
                filepath = path.join(self.TESTFILE_BASE, "%s.%s" % (
                    name, self.FORMAT_EXTENSION))
                if not isfile(filepath):
                    self.fail("Bad test files: Expected to find %s" % filepath)
                with open(filepath, "r") as myfile:
                    self.data[name] = myfile.read()

    def setUp(self):
        self.handler = self.HANDLER_CLASS()
        self.read_files()
        self.tmpl, self.strset = self.handler.parse(self.data["1_en"])
        super(CommonFormatTestCase, self).setUp()


    def test_template(self):
        """Test that the template created is the same as static one."""
        # FIXME: Test descriptions should have the handler's name prefixed to
        # be able to differentiate between them.
        self.assertEquals(self.tmpl, self.data["1_tpl"])

    def test_no_empty_strings_in_handler_stringset(self):
        for s in self.strset:
            self.assertFalse(s.string == '')

    def test_compile(self):
        """Test that import-export is the same as the original file."""
        remade_orig_content = self.handler.compile(self.tmpl, self.strset)
        self.assertEquals(remade_orig_content, self.data["1_en"])

    def test_translate(self):
        """Test that translate + export is the same as the precompiled file."""
        translated_strset = translate_stringset(self.strset)
        translated_content = self.handler.compile(self.tmpl, translated_strset)
        self.assertEquals(translated_content, self.data["1_el"])
