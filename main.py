from fastapi import FastAPI # imports the FastAPI class from the fastapi library,

# app object is what FastAPI uses to define API endpoints and configurations.
app = FastAPI()

# define API Endpoint
@app.get('/')  # [[decorator that tells FastAPI that the read_root function directly]]
	# [[ below it should be executed when an HTTP GET request is received at the root URL (/) of your API. ]]
	# [[FastAPI is designed to be the API Layer and the Front Door for all incoming HTTP requests, built for speed and responsiveness. ]]

async def read_root(): #Asynchronous functions are used in FastAPI to handle requests efficiently
    # [[, especially for I/O-bound tasks]]
	return {"message": "hello, world"} #  returns a standard Python dictionary 
     # [[ FastAPI automatically converts this into a JSON response when a client requests this endpoint ]]