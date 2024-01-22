from sqlalchemy import Column, ForeignKey, String, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    title = Column(String)
    description = Column(String)

    submenus = relationship("SubMenu",
                            back_populates="main_menu",
                            cascade="all, delete",
                            passive_deletes=True
                            )


class SubMenu(Base):
    __tablename__ = "submenu"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    title = Column(String)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menu.id", ondelete="CASCADE"))

    main_menu = relationship("Menu", back_populates="submenus")

    dishes = relationship("Dish",
                          back_populates="submenu",
                          cascade="all, delete",
                          passive_deletes=True
                          )


class Dish(Base):
    __tablename__ = "dish"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    title = Column(String)
    description = Column(String)
    price = Column(Numeric(10, 2))
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenu.id", ondelete="CASCADE"))

    submenu = relationship("SubMenu", back_populates="dishes")
