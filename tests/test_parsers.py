# coding: utf-8


from unittest import TestCase
from pimobjects.exceptions import ParseError, InvalidCodificationError
from pimobjects.parsers import parse_line


class ParsersTest(TestCase):
    def test_parse_line(self):
        line = parse_line("BEGIN:VCARD")
        self.assertEquals(line.group, None)
        self.assertEquals(line.key, "BEGIN")
        self.assertEquals(line.values[0][0], "VCARD")

    def test_strip_whitespaces(self):
        line = parse_line("   N: Foo; Bar; Baz ;  ;")
        self.assertEquals(line.key, "N")
        self.assertEquals(len(line.values), 4)
        self.assertEquals(line.values[0][0], "Foo")
        self.assertEquals(line.values[1][0], "Bar")
        self.assertEquals(line.values[2][0], "Baz")
        self.assertEquals(line.values[3][0], "")

    def test_parse_empty_values(self):
        line = parse_line("FN:")
        self.assertEquals(len(line.values), 0)

    def test_escaping(self):
        line = parse_line("g\,\;\:.FN\::\:\;\,Foo\,Bar\;Baz\:Fux")
        self.assertEquals(line.group, u"g,;:")
        self.assertEquals(line.key, u"FN:")
        self.assertEquals(line.group, u"g,;:")
        self.assertEquals(line.values[0][0], u':;,Foo,Bar;Baz:Fux')

    def test_fail_empty_line(self):
        self.assertRaises(ParseError, parse_line, "")

    def test_fail_invalid_codec(self):
        self.assertRaises(InvalidCodificationError, parse_line, u"FN:José".encode("latin1"))

    def test_fail_empty_key(self):
        self.assertRaises(ParseError, parse_line, "  :Error")

    def test_value_duplicated_separators(self):
        line = parse_line("FN:Foo:Bar")
        self.assertEquals(line.key, u"FN")
        self.assertEquals(line.values[0][0], u"Foo:Bar")

    def test_parse_group(self):
        line = parse_line("g.FN:Foo")
        self.assertEquals(line.group, u"g")
        self.assertEquals(line.key, u"FN")
        self.assertEquals(line.values[0][0], u"Foo")

    def test_fail_invalid_group_name(self):
        self.assertRaises(ParseError, parse_line, "group.error.FN:Foo")

    def test_parse_args_and_kwargs(self):
        line = parse_line("FN;FOO;BAR=BAZ;D===;  ;BLA = BLE;;:Name")

        self.assertEquals(len(line.args), 1)
        self.assertEquals(line.args[0], u"FOO")

        self.assertEquals(len(line.kwargs), 3)
        self.assertEquals(line.kwargs["BAR"], u"BAZ")
        self.assertEquals(line.kwargs["D"], u"==")
        self.assertEquals(line.kwargs["BLA"], u"BLE")

        self.assertEquals(line.values[0][0], u"Name")

    def test_comma_in_value(self):
        line = parse_line("FN:First\,Name,Second\,Name;Third\,Name,Fourth\,Name;,,Fifth\,Name")
        self.assertEquals(line.values[0][0], u"First,Name")
        self.assertEquals(line.values[0][1], u"Second,Name")
        self.assertEquals(line.values[1][0], u"Third,Name")
        self.assertEquals(line.values[1][1], u"Fourth,Name")
        self.assertEquals(line.values[2][0], u"Fifth,Name")

    def test_serialize(self):
        line = u"g.ADR;ARG;TYPE=WORK:222;Qualquer;Rua Bla\, 910 - ap.101;Alguma,Rua;Sem estado;101 10-990;Smurfs Village"
        line = line.encode("utf-8")
        parsed_line = parse_line(line)
        self.assertEquals(str(parsed_line), line)

    def test_representation(self):
        line = u"g.ADR;ARG;TYPE=WORK:222;Qualquer;Rua Bla\, 910 - ap.101;Alguma,Rua;Sem estado;101 10-990;Smurfs Village"
        line = line.encode("utf-8")
        parsed_line = parse_line(line)
        self.assertEquals(repr(parsed_line), "<ParsedLine %s>" % (line,))
