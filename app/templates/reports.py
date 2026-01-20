from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services import analysis_service
from app.database import get_db
from app.auth import get_current_user

router = APIRouter()

@router.get("/reports/summary")
def get_report_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    monthly_spending = analysis_service.monthly_spending(db, current_user.id).to_dict(orient="records")
    spending_by_category = analysis_service.spending_by_category(db, current_user.id).to_dict(orient="records")

    return {
        "monthly_spending": monthly_spending,
        "spending_by_category": spending_by_category
    }
