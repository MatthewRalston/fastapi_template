"""
#   Copyright 2025 Matthew Ralston
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
"""
import anyio
from slowapi import Limiter
from slowapi.util import get_remote_address

from fastapi import FastAPI, Request # , Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# Sqlalchemy
from sqlalchemy.orm import Session

#   My application
from .database.core import Base, engine, SessionLocal
from .api import register_routes

Base.metadata.create_all(bind=engine)

async def startup():
    # AnyIO increase thread limit for performance
    #limiter = anyio.to_thread.current_default_thread_limiter()
    #limiter.total_tokens = 100 # Change if needed
    # slowapi Limiter
    limiter = Limiter(key_func=get_remote_address)
    


#        F a s t   A P I   instantiation
app = FastAPI(on_startup=[startup], default_response_class=ORJSONResponse)
"""
Register all routes from submodule controller.py files from api.py
"""
register_routes(app)

"""
Static files (/assets) and Jinja2 templates
"""
app.mount("/assets", StaticFiles(directory="app/assets/"), name="assets")
templates = Jinja2Templates(directory="app/templates/")

"""
Main routes (TODO: Break off into separate routes categories.
"""


@app.get("/components")
def home(request: Request):
    #return {"message": "First FastAPI app"}
    return templates.TemplateResponse("pages/components_gallery.html", {"request": request})


