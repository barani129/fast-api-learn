#!/usr/bin/python3

import time
from subprocess import Popen, PIPE
import os
from typing import Union
from io import StringIO
import pandas
from fastapi import FastAPI
from enum import Enum

class ModelName(str, Enum):
  alexnet = "alexnet"
  resnet = "resnet"
  lenet = "lenet"

app = FastAPI()

@app.get("/")
async def root():
   return {"mesage": "this is the root page"}

#with path parameter
@app.get("/items/{item_id}")
async def read_item(item_id):
      return {"message": item_id}

#with path parameter type, other possible values str, float, bool
@app.get("/newitems/{item_id}")
async def read_item2(item_id: int):
      return {"item_id": item_id}

##ordering
@app.get("/users/me")
async def user_me():
   return {"Hi this is the current user"}

@app.get("/users/{user_id}")
async def users_id(user_id):
  return {"info for the user": user_id}

#example with enum
@app.get("/model/{model_name}")
async def model(model_name):
  if model_name == ModelName.alexnet:
    return {"model_name": model_name, "message": "this is alex"}
  elif model_name == ModelName.resnet:
    return {"model_name": model_name, "message": "this is res"}
  else:
    return {"Message": "Doesn't exist"}

#Retrieve namespaced events

def namespace_event(namespace, limit):
    args = f'/app/oc get events -n {namespace} --sort-by=.metadata.creationTimestamp'
    args2 = f'head -{limit}'
    cmd = Popen([args], shell=True, stdout=PIPE)
    cmd2 = Popen([args2], shell=True, stdin=cmd.stdout, stdout=PIPE)
    out, err = cmd2.communicate()
    out = out.decode("utf-8")
    data = StringIO(out)
    new_data = pandas.read_table(data)
    return new_data

@app.get("/namespace_events/{item_id}")
async def namspace_events(item_id, limit: Union[int, None] = None):
     if limit:
       return namespace_event(item_id, limit)
     else:
       return namespace_event(item_id, 20)

