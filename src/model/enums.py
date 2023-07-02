from enum import Enum


class PaymentType(Enum):
    visa = "visa"
    mastercard = "mastercard"
    rbc = "rbc"
    tangerine = "tangerine"
    saving = "saving"
    desjardins = "desjardins"


class IncomeType(Enum):
    salary = "salary"
    bonus = "bonus"
    other = "other"


class ProviderType(Enum):
    city_of_ottawa = "city_of_ottawa"
    enbridge = "enbridge"
    bell = "bell"
    hiydro_ottawa = "hiydro_ottawa"
    netflix = "netflix"
    copilot = "copilot"
    disneyplus = "disneyplus"
    google_one = "google_one"
    spotify = "spotify"
    cc = "cc"
    mortgage = "mortgage"
    condominio = "condominio"
    fit4less = "fit4less"
    tia = "tia"
    seguro = "seguro"
    line_of_credit = "line_of_credit"
    everyday = "everyday"
    saving = "saving"
