# coding: utf-8


from pimobjects.exceptions import InvalidCodificationError


def utf8_decode(raw):
    if isinstance(raw, unicode):
        return raw

    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        raise InvalidCodificationError("vCard must be encoded as UTF-8 string")


def escape(string):
    return string.replace(u";", ur"\;").replace(u",", ur"\,").replace(u":", ur"\:")
