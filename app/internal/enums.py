from enum import Enum


class Roles(Enum):
    admin = 'ADMIN'
    staff = 'STAFF'
    user = 'USER'
    visitor = 'VISITOR'


class AssetStatus(Enum):
    active = "ACTIVE"
    deactive = "DEACTIVE"


class SymbolStatus(Enum):
    trading = "TRADING"
    stopped = "STOPPED"
