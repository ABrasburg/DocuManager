import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from db import SessionLocal, engine, Base
import uvicorn

from src.models import comprobante

from src.init_db.init_db import init_db
from src.routes.tipo_comprobante import tipo_comprobante
from src.routes.emisor import emisor
from src.routes.comprobante import comprobante
from src.routes.zeta import zeta

app = FastAPI(
    title="GIO API",
    description="API para gestionar los recursos y funcionalidades de GIO, con documentación interactiva a través de Swagger.",
    version="1.0.0",
)

app.include_router(tipo_comprobante)
app.include_router(emisor)
app.include_router(comprobante)
app.include_router(zeta)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["content-disposition"],
)

Base.metadata.create_all(bind=engine)


def init():
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()


init()


@app.exception_handler(Exception)
def handle_exception(request, exc):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(
        status_code=500, content={"message": f"{base_error_message}, due to: {exc}"}
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 9000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=os.getenv("ENV") == "dev")
