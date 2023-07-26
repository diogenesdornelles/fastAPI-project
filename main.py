"""
Main module
"""
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes import orders_router, products_router, clients_router, tokens_router, users_router, uploads_router
from fastapi.staticfiles import StaticFiles

# create app
app = FastAPI()

# Include routes to app
app.include_router(clients_router)
# app.include_router(products_router)
# app.include_router(orders_router)
# app.include_router(users_router)
# app.include_router(tokens_router)
# app.include_router(uploads_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"error": str(exc.detail)}
