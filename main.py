from fastapi import FastAPI
from app.routers import user, auth
from app.db.database import Base, engine

# def create_tables():
#    Base.metadata.create_all(bind=engine)


# create_tables()


app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
