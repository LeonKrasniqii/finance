from fastapi import FastAPI
from app.routers import add_expense, dashboard, login, register, reports
from app.utils.error_handler import validation_exception_handler
from fastapi.exceptions import RequestValidationError

app = FastAPI()

app.include_router(add_expense.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(login.router, prefix="/api")
app.include_router(register.router, prefix="/api")
app.include_router(reports.router, prefix="/api")

app.add_exception_handler(RequestValidationError, validation_exception_handler)
