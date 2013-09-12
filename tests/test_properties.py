# coding: utf-8


from unittest import TestCase

from pimobjects.exceptions import UnknownPropertyError
from pimobjects.parsers import parse_line
from pimobjects.properties import Property


PROPERTIES = {
    "adr": ("ADR:FOO", "ADR", "FOO"),
    "agent": ("AGENT:FOO", "AGENT", "FOO"),
    "anniversary": ("ANNIVERSARY:FOO", "ANNIVERSARY", "FOO"),
    "bday": ("BDAY:FOO", "BDAY", "FOO"),
    "begin": ("BEGIN:FOO", "BEGIN", "FOO"),
    "caladruri": ("CALADRURI:FOO", "CALADRURI", "FOO"),
    "caluri": ("CALURI:FOO", "CALURI", "FOO"),
    "categories": ("CATEGORIES:FOO", "CATEGORIES", "FOO"),
    "class": ("CLASS:FOO", "CLASS", "FOO"),
    "clientpidmap": ("CLIENTPIDMAP:FOO", "CLIENTPIDMAP", "FOO"),
    "email": ("EMAIL:FOO", "EMAIL", "FOO"),
    "end": ("END:FOO", "END", "FOO"),
    "fburl": ("FBURL:FOO", "FBURL", "FOO"),
    "fn": ("FN:FOO", "FN", "FOO"),
    "gender": ("GENDER:FOO", "GENDER", "FOO"),
    "geo": ("GEO:FOO", "GEO", "FOO"),
    "impp": ("IMPP:FOO", "IMPP", "FOO"),
    "key": ("KEY:FOO", "KEY", "FOO"),
    "kind": ("KIND:FOO", "KIND", "FOO"),
    "label": ("LABEL:FOO", "LABEL", "FOO"),
    "lang": ("LANG:FOO", "LANG", "FOO"),
    "logo": ("LOGO:FOO", "LOGO", "FOO"),
    "mailer": ("MAILER:FOO", "MAILER", "FOO"),
    "member": ("MEMBER:FOO", "MEMBER", "FOO"),
    "n": ("N:FOO", "N", "FOO"),
    "name": ("NAME:FOO", "NAME", "FOO"),
    "nickname": ("NICKNAME:FOO", "NICKNAME", "FOO"),
    "note": ("NOTE:FOO", "NOTE", "FOO"),
    "org": ("ORG:FOO", "ORG", "FOO"),
    "photo": ("PHOTO:FOO", "PHOTO", "FOO"),
    "prodid": ("PRODID:FOO", "PRODID", "FOO"),
    "profile": ("PROFILE:FOO", "PROFILE", "FOO"),
    "related": ("RELATED:FOO", "RELATED", "FOO"),
    "rev": ("REV:FOO", "REV", "FOO"),
    "role": ("ROLE:FOO", "ROLE", "FOO"),
    "sort-string": ("SORT-STRING:FOO", "SORT-STRING", "FOO"),
    "sound": ("SOUND:FOO", "SOUND", "FOO"),
    "source": ("SOURCE:FOO", "SOURCE", "FOO"),
    "tel": ("TEL:FOO", "TEL", "FOO"),
    "title": ("TITLE:FOO", "TITLE", "FOO"),
    "tz": ("TZ:FOO", "TZ", "FOO"),
    "uid": ("UID:FOO", "UID", "FOO"),
    "url": ("URL:FOO", "URL", "FOO"),
    "version": ("VERSION:FOO", "VERSION", "FOO"),
    "xml": ("XML:FOO", "XML", "FOO"),
}


class PropertiesTest(TestCase):
    def test_fail_unknown_property(self):
        self.assertRaises(UnknownPropertyError, Property.create, parse_line("FOO:BAR"))

    def test_extended_property(self):
        prop = Property.create(parse_line("X-FOO:BAR"))
        self.assertEquals(prop.key, "X-FOO")
        self.assertEquals(prop.value, "BAR")

    def test_property_begin(self):
        prop = Property.create(parse_line("BEGIN:VCARD"))
        self.assertEquals(prop.key, "BEGIN")
        self.assertEquals(prop.value, "VCARD")

    def test_property_end(self):
        prop = Property.create(parse_line("END:VCARD"))
        self.assertEquals(prop.key, "END")
        self.assertEquals(prop.value, "VCARD")

    def test_all_properties(self):
        for key, test in PROPERTIES.iteritems():
            prop = Property.create(parse_line(test[0]))
            self.assertEquals(prop.key, test[1])
            self.assertEquals(prop.value, test[2])
