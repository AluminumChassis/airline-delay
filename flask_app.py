from flask import Flask
from flask import request
from typing import Dict

import sys
from flask_cors import CORS
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

def predict_tabular_regression_sample(
    project: str,
    endpoint_id: str,
    instance_dict: Dict,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # Google sample code
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient.from_service_account_file("/home/bkciccar/mysite/service.json", client_options=client_options)

    # for more info on the instance schema, please use get_model_sample.py
    # and look at the yaml found in instance_schema_uri
    instance = json_format.ParseDict(instance_dict, Value())
    instances = [instance]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())

    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    print("response")
    print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/tables_regression.yaml for the format of the predictions.
    predictions = response.predictions
    # End Google Sample Code
    for prediction in predictions:
        return(str(dict(prediction)).replace("'",'"'))



app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['POST'])
def hello_world():
    try:
        data = request.json
        return predict_tabular_regression_sample(
                project="234973481309",
                endpoint_id="8447046458900742144",
                location="us-central1",
                instance_dict={"DepTime": data["CRSDepTime"],
                    "CRSDepTime":data["CRSDepTime"],
                    "CRSArrTime":data["CRSArrTime"],
                    "Dest": "TPA",
                    "CRSElapsedTime":data["CRSElapsedTime"],
                    "ArrDelay":"0",
                    "ActualElapsedTime":data["CRSElapsedTime"],
                    "AirTime":"100",
                    "TaxiOut":"10",
                    "NASDelay":"0",
                    "LateAircraftDelay":"20",
                    "CarrierDelay":"2",
                    "TaxiIn":"5",
                    "ArrTime":"1500",
                    "TailNum":"N763SW",
                    "WeatherDelay":"0",
                    "Distance":"1000",
                    "Origin":"JAX",
                    "UniqueCarrier":"WN",
                    "FlightNum":"600",
                    "DayofMonth":data["DayofMonth"],
                    "Month":"1",
                    "DayOfWeek":"4",
                    "SecurityDelay":"0",
                    "Diverted":"0",
                    "CancellationCode":"N",
                    "Cancelled":"0",
                    "Year":"" "2008"
                }
            )
    except:
        return str(sys.exc_info())