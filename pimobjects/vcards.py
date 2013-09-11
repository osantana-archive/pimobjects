# coding: utf-8


from .helpers import utf8_decode
from .parsers import parse_line


class VCard(object):
    def __init__(self):
        self.raw = ""
        self.lines = []

    def parse(self, raw):
        self.raw = utf8_decode(raw)

        for line in self.raw.splitlines():
            parsed_line = parse_line(line)
            self.lines.append(parsed_line)

    @property
    def valid(self):
        return True
