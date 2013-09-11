# coding: utf-8


from .exceptions import ParseError, InvalidCodificationError


(
    KEY,
    ARGS,
    VALUE,
) = range(3)


def _escape(string):
    return string.replace(u";", ur"\;").replace(u",", ur"\,").replace(u":", ur"\:")


class ParsedLine(object):
    def __init__(self):
        self.group = None
        self.key = ""
        self.args = []
        self.kwargs = {}
        self._values = []
        self._part = []

    def set_key(self, key):
        if u"." not in key:
            self.key = key
            return
        try:
            self.group, self.key = key.split(".")
        except ValueError:
            raise ParseError("Invalid Group Name: %s" % (key,))

    def add_arg(self, arg):
        if not arg.strip():
            return

        if arg == u";":
            return

        if u"=" not in arg:
            self.args.append(arg.strip())
            return

        key, value = arg.split(u"=", 1)
        self.kwargs[key.strip()] = value.strip()

    @property
    def values(self):
        if self._part:
            self._values.append(self._part)
            self._part = []
        return self._values

    def add_value(self, value):
        value = value.strip()

        if value == u";":
            self._values.append(self._part)
            self._part = []
            return

        if value == u",":
            return

        self._part.append(value)

    def __unicode__(self):
        key = self.key
        if self.group:
            key = _escape(u"%s.%s" % (self.group, key))

        args = self.args[:]
        for item in self.kwargs.iteritems():
            args.append(_escape(u"%s=%s" % item))
        args.insert(0, "")

        values = []
        for value in self.values:
            escaped = u",".join(_escape(v) for v in value)
            values.append(escaped)

        return u"%s%s:%s" % (key, ";".join(args), ";".join(values))

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __repr__(self):
        return "<ParsedLine %s>" % (self,)


def parse_line(line):
    if not line:
        raise ParseError("Empty line")

    if not isinstance(line, unicode):
        try:
            line = line.decode("utf-8")
        except UnicodeDecodeError:
            raise InvalidCodificationError("String must be encoded as UTF-8 string")

    parts = []
    part = []
    for char in line.strip():
        if part and part[-1] == "\\":
            part[-1] = char
            continue

        if char in u":;,":
            if part:
                parts.append(u"".join(part))
                part = []

            parts.append(char)
            continue

        part.append(char)

    if part:
        parts.append(u"".join(part))

    parsed = ParsedLine()
    state = KEY

    for part in parts:
        if part == u";" and state == KEY:
            state = ARGS
            continue

        if part == u":":
            if state == VALUE:
                raise ParseError("Duplicated separator")
            state = VALUE
            continue

        if state == KEY:
            parsed.set_key(part)
        elif state == ARGS:
            parsed.add_arg(part)
        else:  # VALUE
            parsed.add_value(part)

    if not parsed.key:
        raise ParseError("Empty Key Part")

    return parsed
