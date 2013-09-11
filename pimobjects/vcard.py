# coding: utf-8


from .exceptions import InvalidCodificationError


class VCard(object):
    def __init__(self):
        self.raw = ""
        self.properties = {
            "version": "3.0",
        }
        self.lines = []
        self._begin = False
        self._end = False

    def _safe_decode(self, raw):
        if isinstance(raw, unicode):
            return raw

        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            raise InvalidCodificationError("vCard must be encoded as UTF-8 string")

    def parse(self, raw):
        self.raw = self._safe_decode(raw)

        for line in self.raw.splitlines():
            if "END:VCARD" in line:
                self._end = True
            if "BEGIN:VCARD" in line:
                self._begin = True
            if line.startswith(" "):
                self.lines[-1] += line
            else:
                self.lines.append(line)

    @property
    def valid(self):
        return self._begin and self._end
