# coding: utf-8


from .exceptions import ParseError
from .helpers import escape


class ParsedLine(object):
    def __init__(self, parts):
        self.parts = parts
        self.group = None
        self.key = ""
        self.args = []
        self.kwargs = {}
        self.values = []

        self._initialize()

    def _initialize(self):
        for part in self.parts:
            if isinstance(part, Key):
                self.set_key(str(part))
            elif isinstance(part, Attribute):
                self.add_attribute(str(part))
            else:
                self.add_value(part)

    def set_key(self, key):
        if "." not in key:
            self.key = key
            return

        try:
            self.group, self.key = key.split(".")
        except ValueError:
            raise ParseError("Invalid Group Name: %s" % (key,))

    def add_attribute(self, arg):
        if "=" not in arg:
            self.args.append(arg.strip())
            return

        key, value = arg.split("=", 1)
        self.kwargs[key.strip()] = value.strip()

    def add_value(self, value):
        self.values.append(value)

    def __unicode__(self):
        key = self.key
        if self.group:
            key = escape(u"%s.%s" % (self.group, key))

        args = self.args[:]
        for item in self.kwargs.iteritems():
            args.append(escape(u"%s=%s" % item))
        args.insert(0, u"")

        values = []
        for value in self.values:
            escaped = u",".join(escape(v) for v in value)
            values.append(escaped)

        return u"%s%s:%s" % (key, ";".join(args), ";".join(values))

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __repr__(self):
        return "<ParsedLine %s>" % (self,)


class Key(str):
    def __repr__(self):
        return "Key(%s)" % (self,)


class Attribute(str):
    def __repr__(self):
        return "Attr(%s)" % (self,)


class Values(list):
    def __repr__(self):
        return "Value(%s)" % (", ".join(self))


def _flush_part(parts, part, state):
    part = state("".join(part).strip())
    if part:
        parts.append(part)
    return []


def parse_line(line):
    if not line:
        raise ParseError("Empty line")

    parts = []
    part = []
    state = Key
    for char in line.strip():
        if part and part[-1] == "\\":
            part[-1] = char
            continue

        elif state in (Key, Attribute):
            if char == ":":
                part = _flush_part(parts, part, state)
                state = Values
                parts.append(Values())
                continue

            if char == ";":
                part = _flush_part(parts, part, state)
                state = Attribute
                continue

        else:  # Value
            if char == ";":
                part = _flush_part(parts[-1], part, str)
                parts.append(Values())
                continue

            if char == ",":
                parts[-1].append("".join(part))
                part = []
                continue

        part.append(char)

    _flush_part(parts[-1], part, str)

    parsed = ParsedLine(parts)

    if not parsed.key:
        raise ParseError("Empty Key Part")

    return parsed
