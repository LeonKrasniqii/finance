# server.py at the root (finance/server.py)
from fastapi import FastAPI
from app.routers import admin_routes  # Make sure this works in step 2
from app.routers import auth_routes, admin_routes
from app.routers import auth_routes, admin_routes, category_routers
from app.routers import auth_routes, admin_routes, category_routers, expense_routes

app = FastAPI(title="Finance App API")

# Include routers
app.include_router(admin_routes.router)
app.include_router(auth_routes.router)
app.include_router(category_routers.router)
app.include_router(expense_routes.router)

@app.get("/")
def root():
    return {"message": "Finance API is running"}
