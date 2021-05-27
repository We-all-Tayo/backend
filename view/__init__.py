import numpy as np
import base64
from service import bus_arrive, number_detection
from flask import request, jsonify
import tensorflow as tf

def create_endpoints(app, services, infer):
    @app.route('/')
    def index():
        return 'It\'s work!'

    @app.route('/task', methods=['POST'])
    def task():
        try:
            payload = request.json
            target_bus = payload['bus']
            bus_station = payload['station']
            image_bytes = payload['image']
            if (target_bus == '' or bus_station == '' or image_bytes == ''):
                return jsonify({'error': 'No input data'})

            image_path = 'bus.jpg'
            image_data = base64.b64decode(image_bytes)
            with open(image_path, 'wb') as f:
                f.write(image_data)
            
            bus_dict = services.bus_arrive.get_bus_dict(bus_station)
            if target_bus not in bus_dict:
                return jsonify({'error': 'Target bus is not comming'})

            target_color = bus_dict[target_bus]
            same_color, diff_color = services.utils.count_bus(bus_dict, target_color)
            
            leftup, rightdown = services.yolo.yolo(infer, image_path)

            if diff_color > 0:
                detected_color = services.color_detection.detect_color(image_path, leftup=leftup, rightdown=rightdown)
                if detected_color is not target_color:
                    return jsonify({'error': 'Unexpected color'})
            
            if (same_color > 1 and services.number_detection.detect_number(image_path, target_bus, leftup, rightdown) == False):
                return jsonify({'error': 'Unexpected number'})
            
            door = services.door_detection.detect_door(image_path, leftup, rightdown)
            radian = services.angle_detection.detect_angle(image_path)

            distance, angle = services.calculator.calculate_distance_angle(door, radian)

            return jsonify({
                'distance': str(round(distance/1000, 2)),
                'angle': str(round(angle * 100 / np.pi))
            })            
        except Exception as e:
            return jsonify({'error': str(e)})
