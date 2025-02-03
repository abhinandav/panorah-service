from fastapi import FastAPI
from api.views import router as communication_router


app = FastAPI(title="Communication API")
app.include_router(communication_router)


