from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.repositories.cafe_repo import CafeRepository
from app.services.cafe import CafeService
from app.utils.dependencies.get_session import get_session


def get_cafe_service(
        session: Session = Depends(get_session)
) -> CafeService:
    repo = CafeRepository(session)
    service = CafeService(product_repo=repo)

    return service
