from fastapi import FastAPI
from views import router as communication_router


app = FastAPI(title="Communication API")
app.include_router(communication_router)


