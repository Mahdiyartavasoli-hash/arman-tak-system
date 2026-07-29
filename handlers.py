
from fastapi import Request  
from fastapi.responses import JSONResponse
from exceptions import AppException,DuplicateEntityError, EntityNotFoundError



async def duplicate_entity_exception_handler(request: Request, exc: DuplicateEntityError):
    return JSONResponse(
    status_code=400,
    content={"detail": exc.message}
    )

async def entity_not_found_exception_handler(request: Request, exc: EntityNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message}
        )