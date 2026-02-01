from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# Import directly from the files to break the circular dependency loop
# Instead of: from app.routers import budget_routers
# Use direct imports to avoid the __init__ error:

from app.routers.auth_routes import router as auth_router
from app.routers.admin_routes import router as admin_router
from app.routers.category_routers import router as category_router
from app.routers.expense_routes import router as expense_router
from app.routers.report_routes import router as report_router
from app.routers.budget_routers import router as budget_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Include Routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(category_router)
app.include_router(expense_router)
app.include_router(report_router)
app.include_router(budget_router)

# 2. Swagger Security Config
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Finance API",
        version="1.0.0",
        description="Expense Tracker API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi