from fastapi import FastAPI
from .database.database import engine
from .models import models
from .api import endpoints

# 创建数据库表 Создание таблиц базы данных
models.Base.metadata.create_all(bind=engine)

# 创建FastAPI应用 Создание приложения FastAPI
app = FastAPI(
    title="Student Management System",
    description="API for managing students and groups",
    version="1.0.0"
)

# 包含路由 Включение маршрутов
app.include_router(endpoints.router)
