# Import the FastAPI class
from fastapi import FastAPI
# Import the models module
from app import models

# Import the engine object from the database module
from app.database import engine
# Import the blog, user, and authentication routers
from app.routers import blog, user, authentication

# Create a new FastAPI instance
app = FastAPI()

# Create all the tables in the database
models.Base.metadata.create_all(engine)

# Include the authentication router
app.include_router(authentication.router)
# Include the blog router
app.include_router(blog.router)
# Include the user router

app.include_router(user.router)
