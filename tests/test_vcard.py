# coding: utf-8


from unittest import TestCase
import unittest
from pimobjects.exceptions import InvalidCodificationError

from pimobjects.vcards import VCard


IMAGE = ur"""/9j/4AAQSkZJRgABAQEASABIAAD//gATQ3JlYXRlZCB3aXRoIEdJTVD/2wBDAP//
  ///////////////////////////////////////////////////////////////////////////
  /////////2wBDAf////////////////////////////////////////////////////////////
  //////////////////////////wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAA
  AAAAAP/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFAEBAAAAAAAAAAAAAAAAAAAAAP/EABQRAQAA
  AAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/AKAA/9k="""

ENCODED_AVATAR = ur"""PHOTO;X-ABCROP-RECTANGLE=ABClipRect_1&0&0&512&512&iUti9FPltdD+JZ8iJ5V7Lw==;ENCODING=b;TYPE=JPEG:
 {}""".format(IMAGE)

VCARDS = {

    "basic": ur"""
BEGIN:VCARD
VERSION:3.0
FN:Sr José Antonio Oliveira Silva Neto
N:Silva;José Antonio;Oliveira;Sr;Neto
NICKNAME:Cara
X-GTALK:jose
X-MSN:jose@casa.com.br
X-ICQ:1234567890
TEL;TYPE=WORK:21999991234
TEL;TYPE=CELL:2112345678
ADR;TYPE=WORK:222;Qualquer;Rua Bla\, 910 - apto.101;Alguma;Sem estado;101
 10-990;Smurfs Village
ORG:Bar do José & Amigos
TITLE:Manager
BDAY:2000-01-11
URL;TYPE=WORK:http://www.bardojose.com.br/
item2.URL:http://www.jose.com
item2.X-ABLabel:PROFILE
NOTE:Isso é uma nota
  multilinha
{avatar}
END:VCARD
""".format(avatar=ENCODED_AVATAR).lstrip(),

    "basic_str": """
BEGIN:VCARD
VERSION:3.0
FN:Sr José Antonio Oliveira Silva Neto
N:Silva;José Antonio;Oliveira;Sr;Neto
END:VCARD
""".lstrip(),

    "basic_str_latin1": u"""
BEGIN:VCARD
VERSION:3.0
FN:Sr José Antonio Oliveira Silva Neto
N:Silva;José Antonio;Oliveira;Sr;Neto
END:VCARD
""".lstrip().encode("latin1"),

    "empty": u"""
BEGIN:VCARD
VERSION:3.0
FN:
N:;;;;
END:VCARD
""".lstrip(),
}


@unittest.skip
class BasicVCardTest(TestCase):
    def test_preserve_raw(self):
        vcard = VCard()
        vcard.parse(VCARDS["basic"])
        self.assertEquals(VCARDS["basic"], vcard.raw)
        self.assertIsInstance(vcard.raw, unicode)

    def test_raw_vcard_decoding(self):
        vcard = VCard()
        vcard.parse(VCARDS["basic_str"])
        self.assertIsInstance(vcard.raw, unicode)

    def test_fail_vcard_encoding(self):
        vcard = VCard()
        self.assertRaises(InvalidCodificationError, vcard.parse, VCARDS["basic_str_latin1"])

    def test_split_lines(self):
        vcard = VCard()
        vcard.parse(VCARDS["basic"])
        self.assertEquals(20, len(vcard.lines))

    def test_empty_vcard_properties(self):
        vcard = VCard()
        vcard.parse(VCARDS["empty"])
        self.assertEquals("3.0", vcard.properties["version"])

    def test_valid_empty_card(self):
        vcard = VCard()
        vcard.parse(VCARDS["empty"])
        self.assertTrue(vcard.valid)

    def test_broken_vcard_missing_begin(self):
        vcard = VCard()
        vcard.parse("VERSION:3.0\nEND:VCARD\n")
        self.assertFalse(vcard.valid)

    def test_broken_vcard_missing_end(self):
        vcard = VCard()
        vcard.parse("BEGIN:VCARD\nVERSION:3.0\n")
        self.assertFalse(vcard.valid)
