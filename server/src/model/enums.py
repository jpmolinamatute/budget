from enum import Enum

from sqlalchemy.dialects.postgresql import ENUM

from src.model import db


class PaymentType(Enum):
    visa = "visa"
    mastercard = "mastercard"
    rbc = "rbc"
    tangerine = "tangerine"
    saving = "saving"


class IncomeType(Enum):
    salary = "salary"
    bonus = "bonus"
    other = "other"


income_type_enum = ENUM(
    IncomeType.salary.value,
    IncomeType.bonus.value,
    IncomeType.other.value,
    name="income_type",
    metadata=db.metadata,
)

payment_type = ENUM(
    PaymentType.visa.value,
    PaymentType.mastercard.value,
    PaymentType.rbc.value,
    PaymentType.tangerine.value,
    PaymentType.saving.value,
    name="payment_type",
    metadata=db.metadata,
)
provider_type = ENUM(
    "city_of_ottawa",
    "enbridge",
    "bell",
    "hiydro_ottawa",
    "netflix",
    "copilot",
    "disney+",
    "google_one",
    "spotify",
    "cc",
    "mortgage",
    "condominio",
    "fit4less",
    "tia",
    "seguro",
    "line_of_credit",
    "everyday",
    "saving",
    name="provider_type",
    metadata=db.metadata,
)
