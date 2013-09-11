# coding: utf-8


from unittest import TestCase

from pimobjects.exceptions import InvalidCodificationError
from pimobjects.helpers import escape, utf8_decode


class HelpersTest(TestCase):
    def test_escape(self):
        self.assertEquals(escape(u"XYZ;:,abc"), r"XYZ\;\:\,abc", )

    def test_utf_decode(self):
        self.assertEquals(utf8_decode(u"á".encode("utf-8")), u"á")

    def test_fail_decode_invalid_codec(self):
        self.assertRaises(InvalidCodificationError, utf8_decode, u"á".encode("latin1"))

    def test_decode_decoded_str(self):
        self.assertEquals(utf8_decode(u"á"), u"á")
