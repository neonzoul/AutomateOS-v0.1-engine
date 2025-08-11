from fastapi import FastAPI

# initialized opject that can call.
# object is what FastAPI uses to define your API endpoints and configurations 
workflow = FastAPI()

# [[ The use of decorators in FastAPI (like @app.get("/")) ]]
# [[ to define API endpoints is an example of the project's declarative and data-oriented programming style ]]
@workflow.get('/')

def read_workflow():
    return {
            "name":"Alice",
            "message": "Hi, I'm worker.",
            }