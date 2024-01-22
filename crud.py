from sqlalchemy.orm import Session
import uuid

import models
import schemas


def get_menus(db: Session):
    return db.query(models.Menu).all()


def get_menu(db: Session, menu_id: uuid.UUID):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if menu is not None:
        menu.submenus_count = len(menu.submenus)
        menu.dishes_count = sum(len(s.dishes) for s in menu.submenus)
    return menu


def create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(title=menu.title, description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def update_menu(db: Session, menu_id: uuid.UUID, menu: schemas.MenuUpdate):
    device = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    setattr(device, 'title', menu.title)
    setattr(device, 'description', menu.description)
    db.commit()

    return device


def delete_menu(db: Session, menu_id: uuid.UUID):
    db.query(models.Menu).filter(models.Menu.id == menu_id).delete()
    db.commit()


def get_submenus(db: Session, menu_id: uuid.UUID):
    return db.query(models.SubMenu).filter(models.SubMenu.menu_id == menu_id).all()


def get_submenu(db: Session, menu_id: uuid.UUID, submenu_id: uuid.UUID):
    submenu = db.query(models.SubMenu).filter(models.SubMenu.menu_id == menu_id,
                                              models.SubMenu.id == submenu_id
                                              ).first()
    if submenu is not None:
        submenu.dishes_count = len(submenu.dishes)
    return submenu


def create_submenu(db: Session, menu_id: uuid.UUID, submenu: schemas.SubMenuCreate):
    db_submenu = models.SubMenu(title=submenu.title,
                                description=submenu.description,
                                menu_id=menu_id
                                )
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def update_submenu(db: Session,
                   menu_id: uuid.UUID,
                   submenu_id: uuid.UUID,
                   submenu: schemas.SubMenuUpdate):
    device = db.query(models.SubMenu).filter(models.SubMenu.menu_id == menu_id,
                                             models.SubMenu.id == submenu_id
                                             ).first()
    setattr(device, 'title', submenu.title)
    setattr(device, 'description', submenu.description)
    db.commit()

    return device


def delete_submenu(db: Session, menu_id: uuid.UUID, submenu_id: uuid.UUID):
    db.query(models.SubMenu).filter(models.SubMenu.id == submenu_id,
                                    models.SubMenu.menu_id == menu_id
                                    ).delete()
    db.commit()

    return


def get_dishes(db: Session, submenu_id: uuid.UUID):
    return db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).all()


def get_dish(db: Session, submenu_id: uuid.UUID, dish_id: uuid.UUID):
    return db.query(models.Dish).filter(models.Dish.id == dish_id,
                                        models.SubMenu.id == submenu_id
                                        ).first()


def create_dish(db: Session, submenu_id: uuid.UUID, dish: schemas.DishCreate):
    db_dish = models.Dish(title=dish.title,
                          description=dish.description,
                          price=dish.price,
                          submenu_id=submenu_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def update_dish(db: Session,
                submenu_id: uuid.UUID,
                dish_id: uuid.UUID,
                dish: schemas.DishUpdate):
    device = db.query(models.Dish).filter(models.Dish.id == dish_id,
                                          models.Dish.submenu_id == submenu_id
                                          ).first()
    setattr(device, 'title', dish.title)
    setattr(device, 'description', dish.description)
    setattr(device, 'price', dish.price)
    db.commit()

    return device


def delete_dish(db: Session, submenu_id: uuid.UUID, dish_id: uuid.UUID):
    db.query(models.Dish).filter(models.Dish.id == dish_id,
                                 models.Dish.submenu_id == submenu_id
                                 ).delete()
    db.commit()
