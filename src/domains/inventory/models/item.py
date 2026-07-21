from pydantic import BaseModel

class Item(BaseModel):

    name: str
    category_id: int
    default_unit: str
    perishable: bool
    