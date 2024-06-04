from dataclasses import dataclass


@dataclass
class ConditionType:
    AND = "And"
    OR = "Or"


@dataclass
class FileType:
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    MISSING = "Missing"


@dataclass
class Order:
    ASCENDING = "Ascending"
    DESCENDING = "Descending"
    EXPLICIT = "Explicit"


@dataclass
class GroupType:
    ANY = "SelectAny"
    ALL = "SelectAll"
    ATLEASTONE = "SelectAtLeastOne"
    ATMOSTONE = "SelectAtMostOne"
    EXACTLYONE = "SelectExactlyOne"


@dataclass
class OptionType:
    OPTIONAL = "Optional"
    REQUIRED = "Required"
    RECOMMENDED = "Recommended"
    NOTUSABLE = "NotUsable"
    COULDBEUSABLE = "CouldBeUsable"
