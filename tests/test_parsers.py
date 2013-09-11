# coding: utf-8


from unittest import TestCase

from pimobjects.exceptions import ParseError
from pimobjects.parsers import parse_line, Key, Attribute, Values


class ParsersTest(TestCase):
    def _get_line(self, line, test_serialization=True):
        parsed = parse_line(line)
        if test_serialization:
            self.assertEquals(str(parsed), line)
        return parsed

    def test_parse_line(self):
        line = self._get_line("BEGIN:VCARD")
        self.assertEquals(line.group, None)
        self.assertEquals(line.key, "BEGIN")
        self.assertEquals(line.values[0][0], "VCARD")

    def test_strip_whitespaces(self):
        line = self._get_line("   N: Foo; Bar; Baz ;  ;", test_serialization=False)
        self.assertEquals(line.key, "N")
        self.assertEquals(len(line.values), 5)
        self.assertEquals(line.values[0][0], "Foo")
        self.assertEquals(line.values[1][0], "Bar")
        self.assertEquals(line.values[2][0], "Baz")
        self.assertListEqual(line.values[3], [])
        self.assertListEqual(line.values[4], [])

    def test_parse_empty_values(self):
        line = self._get_line("FN:")
        self.assertEquals(len(line.values), 1)

    def test_escaping(self):
        line = self._get_line("g\,\;\:.FN\::\:\;\,Foo\,Bar\;Baz\:Fux")
        self.assertEquals(line.group, u"g,;:")
        self.assertEquals(line.key, u"FN:")
        self.assertEquals(line.group, u"g,;:")
        self.assertEquals(line.values[0][0], u':;,Foo,Bar;Baz:Fux')

    def test_fail_empty_line(self):
        self.assertRaises(ParseError, parse_line, "")

    def test_fail_empty_key(self):
        self.assertRaises(ParseError, parse_line, "  :Error")

    def test_value_duplicated_separators(self):
        line = self._get_line("FN:Foo:Bar", test_serialization=False)
        self.assertEquals(line.key, u"FN")
        self.assertEquals(line.values[0][0], u"Foo:Bar")

    def test_parse_group(self):
        line = self._get_line("g.FN:Foo")
        self.assertEquals(line.group, u"g")
        self.assertEquals(line.key, u"FN")
        self.assertEquals(line.values[0][0], u"Foo")

    def test_fail_invalid_group_name(self):
        self.assertRaises(ParseError, parse_line, "group.error.FN:Foo")

    def test_parse_args_and_kwargs(self):
        line = self._get_line("FN;FOO;BLA = BLE;BAR=BAZ;D===;  ;;:Name", test_serialization=False)
        self.assertEquals(len(line.args), 1)
        self.assertEquals(line.args[0], u"FOO")

        self.assertEquals(len(line.kwargs), 3)
        self.assertEquals(line.kwargs["BAR"], u"BAZ")
        self.assertEquals(line.kwargs["D"], u"==")
        self.assertEquals(line.kwargs["BLA"], u"BLE")

        self.assertEquals(line.values[0][0], u"Name")

    def test_comma_in_value(self):
        line = self._get_line("FN:First\,Name,Second\,Name;Third\,Name,Fourth\,Name;,,Fifth\,Name")
        self.assertEquals(line.values[0][0], u"First,Name")
        self.assertEquals(line.values[0][1], u"Second,Name")
        self.assertEquals(line.values[1][0], u"Third,Name")
        self.assertEquals(line.values[1][1], u"Fourth,Name")
        self.assertEquals(line.values[2][2], u"Fifth,Name")

    def test_serialize(self):
        line = u"g.ADR;ARG;TYPE=WORK:222;Qualquer;Rua Bla\, 910 - ap.101;Alguma,Rua;Sem estado;101 10-990;Smurfs Village"
        line = line.encode("utf-8")
        parsed_line = self._get_line(line)
        self.assertEquals(str(parsed_line), line)

    def test_representation(self):
        line = u"g.ADR;ARG;TYPE=WORK:222;Qualquer;Rua Bla\, 910 - ap.101;Alguma,Rua;Sem estado;101 10-990;Smurfs Village"
        line = line.encode("utf-8")
        parsed_line = self._get_line(line)
        self.assertEquals(repr(parsed_line), "<ParsedLine %s>" % (line,))

    def test_representations(self):
        self.assertEquals(repr(Key("key")), "Key(key)")
        self.assertEquals(repr(Attribute("attr")), "Attr(attr)")
        self.assertEquals(repr(Values(["a", "b"])), "Value(a, b)")
