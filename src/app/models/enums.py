from sqlalchemy.dialects.postgresql import ENUM

from src.app.models import db


payment_type = ENUM(
    "visa",
    "mastercard",
    "rbc",
    "tangerine",
    "saving",
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
