import uuid

from datetime import datetime
from typing import Optional, TypedDict


class SectionItem(TypedDict):
    item_amount: float
    item_label: Optional[str]
    item_id: uuid.UUID
    item_date: Optional[datetime]
    item_extra: Optional[float]
