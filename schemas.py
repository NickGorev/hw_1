import decimal
from pydantic import BaseModel
import uuid


class DishBase(BaseModel):
    title: str
    description: str
    price: decimal.Decimal


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    pass


class Dish(DishBase):
    id: uuid.UUID
    submenu_id: uuid.UUID

    class Config:
        orm_mode = True


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuCreate(SubMenuBase):
    pass


class SubMenuUpdate(SubMenuBase):
    pass


class SubMenu(SubMenuBase):
    id: uuid.UUID
    menu_id: uuid.UUID
    dishes: list[Dish] = []
    dishes_count: int = 0

    class Config:
        orm_mode = True


class MenuBase(BaseModel):
    title: str
    description: str


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class Menu(MenuBase):
    id: uuid.UUID
    submenus: list[SubMenu] = []
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        orm_mode = True
