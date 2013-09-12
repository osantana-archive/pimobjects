# coding: utf-8


from pimobjects.exceptions import UnknownPropertyError
from pimobjects.helpers import join_values


class Property(object):
    _properties = {}

    @classmethod
    def register(cls, prop):
        cls._properties[prop.name] = prop
        return prop

    @classmethod
    def create(cls, line):
        name = line.key.lower()
        if name.startswith("x-"):
            return ExtendedProperty(line)

        if name not in cls._properties:
            raise UnknownPropertyError("Invalid Property %s" % (line.key,))

        return cls._properties[name](line)

    def __init__(self, line):
        self.line = line
        self.key = self.line.key
        self._value = None

    def _build_value(self):
        return join_values(self.line.values)

    @property
    def value(self):
        if not self._value:
            self._value = self._build_value()
        return self._value


class V21(object):
    pass


class V30(object):
    pass


class V40(object):
    pass

@Property.register
class BeginProperty(Property, V21, V30, V40):
    name = "begin"


@Property.register
class EndProperty(Property, V21, V30, V40):
    name = "end"


@Property.register
class VersionProperty(Property, V21, V30, V40):
    name = "version"


@Property.register
class FormattedNameProperty(Property, V21, V30, V40):
    name = "fn"


@Property.register
class StructuredNameProperty(Property, V21, V30, V40):
    name = "n"


@Property.register
class UIDProperty(Property, V21, V30, V40):
    name = "uid"


@Property.register
class LogoProperty(Property, V21, V30, V40):
    name = "logo"


@Property.register
class PhotoProperty(Property, V21, V30, V40):
    name = "photo"


@Property.register
class TitleProperty(Property, V21, V30, V40):
    name = "title"


@Property.register
class SoundProperty(Property, V21, V30, V40):
    name = "sound"


@Property.register
class TelephoneProperty(Property, V21, V30, V40):
    name = "tel"


@Property.register
class EmailProperty(Property, V21, V30, V40):
    name = "email"


@Property.register
class TimezoneProperty(Property, V21, V30, V40):
    name = "tz"


@Property.register
class GeolocationProperty(Property, V21, V30, V40):
    name = "geo"


@Property.register
class NoteProperty(Property, V21, V30, V40):
    name = "note"


@Property.register
class URLProperty(Property, V21, V30, V40):
    name = "url"


@Property.register
class BirthdayProperty(Property, V21, V30, V40):
    name = "bday"


@Property.register
class RoleProperty(Property, V21, V30, V40):
    name = "role"


@Property.register
class RevisionProperty(Property, V21, V30, V40):
    name = "rev"


@Property.register
class KeyProperty(Property, V21, V30, V40):
    name = "key"

@Property.register
class ExtendedProperty(Property, V21, V30, V40):
    name = "x"


@Property.register
class SourceProperty(Property, V30, V40):
    name = "source"


@Property.register
class NicknameProperty(Property, V30, V40):
    name = "nickname"


@Property.register
class AddressProperty(Property, V30, V40):
    name = "adr"


@Property.register
class IMPPProperty(Property, V30, V40):
    name = "impp"


@Property.register
class OrganizationProperty(Property, V30, V40):
    name = "org"


@Property.register
class MemberProperty(Property, V30, V40):
    name = "member"


@Property.register
class RelatedProperty(Property, V30, V40):
    name = "related"


@Property.register
class CategoriesProperty(Property, V30, V40):
    name = "categories"


@Property.register
class ProductIdProperty(Property, V30, V40):
    name = "prodid"


@Property.register
class FBURLProperty(Property, V30, V40):
    name = "fburl"


@Property.register
class CalendarAddressURIProperty(Property, V30, V40):
    name = "caladruri"


@Property.register
class CalendarURIProperty(Property, V30, V40):
    name = "caluri"


@Property.register
class ProfileProperty(Property, V30, V40):
    name = "profile"


@Property.register
class AgentProperty(Property, V30, V40):
    name = "agent"


@Property.register
class SortStringURIProperty(Property, V30, V40):
    name = "sort-string"


@Property.register
class LabelProperty(Property, V21, V30):
    name = "label"


@Property.register
class MailerProperty(Property, V21, V30):
    name = "mailer"


@Property.register
class NameProperty(Property, V30):
    name = "name"


@Property.register
class ClassProperty(Property, V30):
    name = "class"


@Property.register
class KindProperty(Property, V40):
    name = "kind"


@Property.register
class GenderProperty(Property, V40):
    name = "gender"


@Property.register
class LanguageProperty(Property, V40):
    name = "lang"


@Property.register
class AnniversaryProperty(Property, V40):
    name = "anniversary"


@Property.register
class XMLProperty(Property, V40):
    name = "xml"


@Property.register
class ClientPIDMapProperty(Property, V40):
    name = "clientpidmap"
