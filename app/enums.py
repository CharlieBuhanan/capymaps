from enum import Enum

class ActivityEnum(str, Enum):
    studying = "studying"
    eating = "eating"
    onMyPuter = "computer"
    finals = "finals"
    GYM = "GYM"
    umassCapy = "umass capy"
    gameDayCapy = "game day capy"
    bakeSaleCapy = "bake sale capy"

class LocationEnum(str, Enum):
    library = "Library"
    worcesterDC = "Worcester Commons"
    theRec = "Recreation Center"
    LGRT = "Lederle Graduate Research Tower"
    theStu = "Student Union"
    