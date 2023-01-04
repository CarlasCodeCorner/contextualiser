import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload_text, search_database, userconf, login


app = FastAPI(title='Contextualiser-1.0', description='NLP-based App', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#include routing for every routing file
app.include_router(login.router)
app.include_router(userconf.router)
app.include_router(upload_text.router)
app.include_router(search_database.router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)