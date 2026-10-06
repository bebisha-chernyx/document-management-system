from fastapi import FastAPI
from app.router.api.document_routes import router
from app.infrastructure.database.sqlite import initialize_database


app = FastAPI(
    title="Document Management System"
)


# Create storage/database resources
initialize_database()


# Register API routes
app.include_router(router)