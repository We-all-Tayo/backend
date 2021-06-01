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
                print('!!! No input data')
                return jsonify({'error': 'No input data'})

            image_path = 'bus.jpg'
            image_data = base64.b64decode(image_bytes)
            with open(image_path, 'wb') as f:
                f.write(image_data)
            
            bus_dict = services.bus_arrive.get_bus_dict(bus_station)
            if target_bus not in bus_dict:
                print('Target bus is not comming')
                return jsonify({'error': 'Target bus is not comming'})

            target_color, plain_no = bus_dict[target_bus]
            same_color, diff_color = services.utils.count_bus(bus_dict, target_color)
            
            bus_leftup, bus_rightdown, door_dict, route_number_leftup, route_number_rightdown, bus_number_leftup, bus_number_rightdown = services.yolo.yolo(infer, image_path)

            if diff_color > 0:
                detected_color = services.color_detection.detect_color(image_path, leftup=bus_leftup, rightdown=bus_rightdown)
                if detected_color is not target_color:
                    print('Unexpected color')
                    return jsonify({'error': 'Unexpected color'})
            
            plain_no = plain_no[-4:]
            if same_color > 1 and (services.number_detection.detect_number(image_path, plain_no, bus_number_leftup, bus_number_rightdown) == False \
                    and services.route_number_detection.detect_routenumber(image_path, target_bus,route_number_leftup, route_number_rightdown) == False):
                print('Unexpected number')
                return jsonify({'error': 'Unexpected number'})
            
            door = services.door_detection.detect_door(image_path, bus_leftup, bus_rightdown)
            radian = services.angle_detection.detect_angle(image_path, bus_leftup, bus_rightdown)

            door_union = {}
            door_union["x"] = min(door['x'], door_dict['x'])
            door_union["y"] = min(door['y'], door_dict['y'])
            door_union["right_x"] = max(door['x'] + door['w'], door_dict['x'] + door_dict['w'])
            door_union["down_y"] = max(door['y'] + door['h'], door_dict['y'] + door_dict['h'])
            door_union["w"] = door_union["right_x"] - door_union["x"]
            door_union["h"] = door_union["down_y"] - door_union["y"]

            door_intersect = {}
            door_intersect["x"] = max(door['x'], door_dict['x'])
            door_intersect["y"] = max(door['y'], door_dict['y'])
            door_intersect["right_x"] = min(door['x'] + door['w'], door_dict['x'] + door_dict['w'])
            door_intersect["down_y"] = min(door['y'] + door['h'], door_dict['y'] + door_dict['h'])
            door_intersect["w"] = door_intersect["right_x"] - door_intersect["x"]
            door_intersect["h"] = door_intersect["down_y"] - door_intersect["y"]

            # Calculation
            distance1, angle1 = services.calculator.calculate_distance_angle(door, radian)  # opencv
            distance2, angle2 = services.calculator.calculate_distance_angle(door_dict, radian)  # yolo
            distance3, angle3 = services.calculator.calculate_distance_angle(door_union, radian)  # opencv + yolo union
            distance4, angle4 = services.calculator.calculate_distance_angle(door_intersect, radian)  # opencv + yolo intersect

            print(str(round(distance1 / 1000, 2)) + " meter")
            print(str(round(angle1 * 180 / np.pi)) + " 도")
            print(str(round(distance2 / 1000, 2)) + " meter")
            print(str(round(angle2 * 180 / np.pi)) + " 도")
            print(str(round(distance3 / 1000, 2)) + " meter")
            print(str(round(angle3 * 180 / np.pi)) + " 도")
            print(str(round(distance4 / 1000, 2)) + " meter")
            print(str(round(angle4 * 180 / np.pi)) + " 도")

            print('it\'s work ― distance:', str(round(distance1/1000, 2)), ', angle:', str(round(angle1 * 100 / np.pi)))
            return jsonify({
                'distance': str(round(distance1/1000, 2)),
                'angle': str(round(angle1 * 100 / np.pi))
            })            
        except Exception as e:
            print(str(e))
            return jsonify({'error': str(e)})
