#TODO use pylint doc string this file
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel


class Course(BaseModel):
    #TODO: need to fill our the rest of the fields of an expected IBM SkillsBuild Course JSON Object
    title: str
    description: str
    learning_hours: str
    course_type: str
    tags: list
    url: str 

@asynccontextmanager
async def lifespan(app: FastAPI):
    #TODO: put code here to clear elastic search and migrate the database data to ekastic saerch engine
    #TODO: put any code here if u need to establish any connection objects to elastic search (if its a global variable make sure 
    #declare it outside this method so its accessible to the entire script)
    #NOTE: add stuff to the csv files if there is any authentication or url stuff for connecting to elastic search
    
    yield
    #NOTE the yeild keyword separate the code
    #Code before yield happends before the server starts
    #Code after yeild happens when the server ends

app = FastAPI(lifespan=lifespan)


@app.post("/{number}")
def search_courses(number: int, course: Course):
    #NOTE number is a path variable (integer) so the request can pass the number of courses they would like returned
    #Remove this if its not possible / irrelevant
    
    #NOTE course is the request body (to learn more about request bodies in FastAPI see https://fastapi.tiangolo.com/tutorial/body/#import-pydantics-basemodel)
    raise NotImplementedError()