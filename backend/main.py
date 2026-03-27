import os
from pathlib import Path
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import backend.models as models
import backend.schemas as schemas
import backend.crud as crud
from backend.database import SessionLocal, engine

# Убедимся, что таблицы созданы
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="UniChance API")

# Настройки путей к фронтенду
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR / "static"

# Разрешаем CORS (чтобы фронтенд мог обращаться к API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем статические файлы (CSS, JS, картинки)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Зависимость для БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================
# API ЭНДПОИНТЫ
# ============================

@app.post("/calculate", response_model=dict)
def calculate(user_data: schemas.UserRequest, db: Session = Depends(get_db)):
    """Рассчитать шансы на основе данных пользователя"""
    results = crud.get_calculated_programs(db, user_data)
    return {"results": results}

@app.get("/majors", response_model=List[str])
def get_all_majors(db: Session = Depends(get_db)):
    """Получить список всех специальностей для выпадающего списка"""
    majors = db.query(models.Program.name).distinct().all()
    return sorted([m[0] for m in majors if m[0]])

@app.get("/api/universities/{uni_id}", response_model=schemas.UniversityBase)
def get_university(uni_id: int, db: Session = Depends(get_db)):
    """Получить данные об университете по ID"""
    uni = crud.get_university_details(db, uni_id)
    if not uni:
        raise HTTPException(status_code=404, detail="University not found")
    return uni

# ============================
# РАЗДАЧА HTML СТРАНИЦ
# ============================

@app.get("/")
def read_index():
    path = FRONTEND_DIR / "index.html"
    if path.exists():
        return FileResponse(path)
    raise HTTPException(status_code=404, detail="Файл index.html не найден. Поместите его в папку frontend.")

@app.get("/{page_name}.html")
def serve_html(page_name: str):
    path = FRONTEND_DIR / f"{page_name}.html"
    if path.exists():
        return FileResponse(path)
    raise HTTPException(status_code=404, detail=f"Страница {page_name}.html не найдена")

# ... (жоғарыдағы кодтар сол күйінде қалады) ...

@app.get("/{page_name}.html")
def serve_html(page_name: str):
    # Файлды бірнеше ықтимал папкалардан іздеу
    paths_to_check = [
        FRONTEND_DIR / f"{page_name}.html",
        BASE_DIR / "frontend" / f"{page_name}.html",
        BASE_DIR / f"{page_name}.html"
    ]
    
    for path in paths_to_check:
        if path.exists():
            return FileResponse(path)
            
    # Егер файл ешқайсысынан табылмаса:
    raise HTTPException(status_code=404, detail=f"Қате: {page_name}.html файлы frontend папкасының ішінен табылмады!")