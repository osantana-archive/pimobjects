# coding: utf-8


class VCardError(Exception):
    pass


class InvalidCodificationError(VCardError):
    pass


class ParseError(VCardError):
    pass


class UnknownPropertyError(VCardError):
    pass
