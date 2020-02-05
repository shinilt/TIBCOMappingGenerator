import xmltodict
import json
from flask import Flask
from flask import request
import json2table
import xml.etree.ElementTree as ET

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    return """
    <i>Service Health - Good</i>
    <br>
    <h1><u> TIBCO Mapping Exporter</u> </h1>
    This application provides below functionality.
     <br>
    The API can be used to export the mapping defined in the TIBCO BW 5.x processes.
    <br>
    The scope is to extract the mapping content of the Map Data activity only. The response can be copied to excel in tabular form.
    <br>
    Basic exposure to xml is required to understand and interpret the mapping exported to the table.
    <br><br><br>
    <u>API Details</u> <br><br>
    API URI- /generatetable
    <br>
    API Method - POST,GET (both work the same for simplicity).
    <br>
    API Input-  TIBCO BW 5.x process definition xml content in full(.process file content).
    <br>
    API Response -  Tabular format  of the mappings defined all the Map Data activities.
    
    <br><br><br><br><br>
    Disclaimer- The data you submit is neither logged nor archived. If you dump trash, you will be returned trash. Developed as a personal project.
    """


@app.route("/generatetable", methods=['GET', 'POST'])
def generatetable():
    #define the functions
    def createTable(xmlinput):
        jsonstring=(json.dumps(xmltodict.parse(xmlinput))) # this create an jsonstring-we can directly use jsonloads operation
        jsonobject=json.loads(jsonstring)
            #set table props
        build_direction = "LEFT_TO_RIGHT"
        table_attributes = {"style": "width:100%", "border": 1, "border-collapse": "collapse"}
        tableout = json2table.convert(jsonobject, build_direction=build_direction, table_attributes=table_attributes)
        return tableout
    # processing start for uri
    try:
        xmlstringdata = request.data #get the xml string content from the request
        # parse the xml
        root = ET.fromstring(xmlstringdata)
        #create dictionary of needed namespaces for use later to parse
        myxmlnamespaces={'pd':'http://xmlns.tibco.com/bw/process/2003'}
        allTableOutput = ""
        #use xpath to filter the mapper activity in groups

        for activity in root.findall("./pd:group/pd:activity[pd:resourceType='ae.activities.MapperActivity']",myxmlnamespaces):

            activityxml=(ET.tostring(activity, encoding='utf8').decode('utf8'))
            allTableOutput=allTableOutput+'<br>'+createTable(activityxml)
        # use xpath to filter the root mapper activities
        for activity in root.findall("./pd:activity[pd:resourceType='ae.activities.MapperActivity']",myxmlnamespaces):

            activityxml=(ET.tostring(activity, encoding='utf8').decode('utf8'))
            allTableOutput=allTableOutput+'<br>'+createTable(activityxml)

        #retun response for the api
        return allTableOutput
    except:
        return('Something is not right.  Please check the input xml,fix it and get back.')



if __name__ == "__main__":
    app.run(debug=True)