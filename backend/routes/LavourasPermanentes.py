from fastapi import APIRouter
from services import LavourasPermanentesService as lp

router = APIRouter()

@router.get("/permanentesEstado/permanentes")
def getLavourasPermanentesPorEstado():
    return lp.get_lavouras_permanentes_por_estado()
