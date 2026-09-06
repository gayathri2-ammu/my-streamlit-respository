from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import auth
from backend.routes import customers
from backend.routes import rooms
from backend.routes import bookings
from backend.routes import payments
from backend.routes import services
from backend.routes import booking_services
from backend.routes import reports


app = FastAPI(
    title="Hotel Management System API",
    description="REST API for Hotel Management System",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(payments.router)
app.include_router(services.router)
app.include_router(booking_services.router)
app.include_router(reports.router)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Hotel Management System API",
        "status": "running",
        "docs": "/docs"
    }