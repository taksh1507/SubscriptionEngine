from app.crud import subscription as crud
from app.schemas.subscription import PlanCreate

def test_create_plan(db):
    plan_in = PlanCreate(
        name="Test Plan",
        price=10.0,
        features="Test feature",
        duration_days=30
    )
    plan = crud.create_plan(db=db, plan=plan_in)
    assert plan.name == "Test Plan"
    assert plan.price == 10.0
    assert plan.duration_days == 30
    assert plan.id is not None

def test_get_plans(db):
    plans, total = crud.get_plans(db=db, skip=0, limit=10)
    assert total > 0
    assert len(plans) > 0
