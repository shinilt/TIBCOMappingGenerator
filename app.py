import xmltodict
import json
from flask import Flask
from flask import request
import json2table

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    return "The service is running."


@app.route("/generatetable", methods=['GET', 'POST'])
def generatetable():
    # make sure data is sent to data
    xmldata = '{"Message": "Hi there, we didnt get your message","ResponseStatus": "Waiting"}'
    xmldata = request.data #get the xml content from the request
    #print(xmldata)
    jsonstring=(json.dumps(xmltodict.parse(xmldata))) # this create an jsonstring-we can directly use jsonloads operation
    jsonobject=json.loads(jsonstring)
    build_direction = "LEFT_TO_RIGHT"
    table_attributes = {"style": "width:100%", "border": 1, "border-collapse": "collapse"}
    tableout = json2table.convert(jsonobject, build_direction=build_direction, table_attributes=table_attributes)
    return tableout

if __name__ == "__main__":
    app.run(debug=True)