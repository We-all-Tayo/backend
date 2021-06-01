from flask import Flask
from flask_cors import CORS
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants
from view import create_endpoints
from service import AngleDetection, BusArrive, Calculator, ColorDetection, DoorDetection, NumberDetection, RouteNumberDetection, Yolo, Utils

class Services :
    pass

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.update(test_config)
    
    # load model
    saved_model_loaded = tf.saved_model.load(app.config['MODEL_PATH'], tags=[tag_constants.SERVING])
    infer = saved_model_loaded.signatures["serving_default"]

    services = Services()
    services.angle_detection = AngleDetection()
    services.bus_arrive = BusArrive(app.config)
    services.calculator = Calculator()
    services.color_detection = ColorDetection()
    services.door_detection = DoorDetection()
    services.number_detection = NumberDetection()
    services.route_number_detection = RouteNumberDetection()
    services.yolo = Yolo(infer)
    services.utils = Utils()

    create_endpoints(app, services)

    return app
