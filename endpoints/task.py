from flask import Blueprint
from flask import request 
from threading import Event, Thread
import httplib
import json
import jsonschema

#local imports 
import globals
 
task_bp = Blueprint('taskEndpoint', __name__)

schema = open("./endpoints/taskSchema.json").read()

@task_bp.route('', methods=['GET', 'POST']) 
def task():
    """Renders the home page.""" 
    if request.json: 
        jsonReq = request.json
        # jsonschema.validate(jsonReq, schema)
        try:
            jsonschema.validate(jsonReq['data'][0], json.loads(schema))
        except jsonschema.ValidationError as e:
            return httplib.BAD_REQUEST, e.message
        except jsonschema.SchemaError as e:
            return httplib.INTERNAL_SERVER_ERROR, e.message
            
        if(globals.FI_SUB_ID in jsonReq and globals.FI_DATA in jsonReq):
            subId =jsonReq[globals.FI_SUB_ID] 
            if(subId in globals.subscriptionDict): 
                globals.taskQueue.put((jsonReq[globals.FI_DATA], globals.subscriptionDict[subId]))
        else:
            # no subscription   
            print "narf"
    else:
        print "no json"
    return "ok", httplib.CREATED
 