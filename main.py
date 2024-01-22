from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import uuid

import crud
import models
import schemas

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/menus", response_model=list[schemas.Menu])
async def read_menus(db: Session = Depends(get_db)):
    menus = crud.get_menus(db)
    return menus


@app.get("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
async def read_target_menu(menu_id: uuid.UUID, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_menu


@app.post("/api/v1/menus", response_model=schemas.Menu, status_code=201)
async def create_menu(menu: schemas.MenuCreate,
                      db: Session = Depends(get_db)):
    return crud.create_menu(db=db, menu=menu)


@app.patch("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
async def update_menu(menu_id: uuid.UUID,
                      menu: schemas.MenuUpdate,
                      db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return crud.update_menu(db=db, menu_id=menu_id, menu=menu)


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: uuid.UUID, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")

    crud.delete_menu(db=db, menu_id=menu_id)
    return {
        "status": True,
        "message": "The menu has been deleted"
    }


@app.get("/api/v1/menus/{menu_id}/submenus", response_model=list[schemas.SubMenu])
async def read_submenus(menu_id: uuid.UUID, db: Session = Depends(get_db)):
    submenus = crud.get_submenus(db, menu_id)
    return submenus


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenu)
async def read_target_menu(menu_id: uuid.UUID,
                           submenu_id: uuid.UUID,
                           db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return db_submenu


@app.post("/api/v1/menus/{menu_id}/submenus", response_model=schemas.SubMenu, status_code=201)
async def create_submenu(menu_id: uuid.UUID,
                         submenu: schemas.SubMenuCreate,
                         db: Session = Depends(get_db)):
    return crud.create_submenu(db=db, menu_id=menu_id, submenu=submenu)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenu)
async def update_submenu(menu_id: uuid.UUID,
                         submenu_id: uuid.UUID,
                         submenu: schemas.SubMenuUpdate,
                         db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return crud.update_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id, submenu=submenu)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: uuid.UUID,
                   submenu_id: uuid.UUID,
                   db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")

    crud.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    return {
        "status": True,
        "message": "The submenu has been deleted"
    }


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
         response_model=list[schemas.Dish])
async def read_dishes(submenu_id: uuid.UUID,
                      db: Session = Depends(get_db)):
    submenus = crud.get_dishes(db, submenu_id)
    return submenus


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
         response_model=schemas.Dish)
async def read_target_dish(submenu_id: uuid.UUID,
                           dish_id: uuid.UUID,
                           db: Session = Depends(get_db)):
    db_dish = crud.get_dish(db, submenu_id=submenu_id, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
          response_model=schemas.Dish, status_code=201)
async def create_dish(submenu_id: uuid.UUID,
                      dish: schemas.DishCreate,
                      db: Session = Depends(get_db)):
    return crud.create_dish(db=db, submenu_id=submenu_id, dish=dish)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
           response_model=schemas.Dish)
async def update_dish(submenu_id: uuid.UUID,
                      dish_id: uuid.UUID,
                      dish: schemas.DishUpdate,
                      db: Session = Depends(get_db)):
    db_dish = crud.get_dish(db, submenu_id=submenu_id, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return crud.update_dish(db=db,
                            submenu_id=submenu_id,
                            dish_id=dish_id,
                            dish=dish)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(submenu_id: uuid.UUID,
                dish_id: uuid.UUID,
                db: Session = Depends(get_db)):
    db_dish = crud.get_dish(db, submenu_id=submenu_id, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    crud.delete_dish(db=db, submenu_id=submenu_id, dish_id=dish_id)
    return {
        "status": True,
        "message": "The dish has been deleted"
    }
