import re

class Validator:
    def __init__(self):
        self.route = ''

    def Connector(self,data, data_recieved):
        return_data = {"status": True, "message": ""}
        try:
            device_names = []
            for devices in data:
                device_names.append(devices['name'])
            if data_recieved['source'] not in device_names:
                return_data['status'] = False
                return_data['message'] = "Node " + data_recieved['source'] + " not found"
                return return_data

            for targets in data_recieved['targets']:
                if targets not in device_names:
                    return_data['status'] = False
                    return_data['message'] = "Node " + targets + " not found"
                    return return_data
        except:
            return_data['status'] = False
            return_data['message'] = "Invalid command syntax"
            return return_data

        for targets in data_recieved['targets']:
            if data_recieved['source'] == targets:
                return_data['status'] = False
                return_data['message'] = "Cannot connect device to itself"
                return return_data

        for device in data:
            if device['name'] == data_recieved['source']:
                if len(device['targets']) == 0:
                    device['targets'] = data_recieved['targets']

                    for i in data_recieved['targets']:
                        for device1 in data:
                            if device1['name'] == i:
                                device1['targets'] = device1['targets']+[data_recieved['source']]

                    return_data['status'] = True
                    return_data['message'] = "Successfully connected"
                    return return_data
                for i in data_recieved['targets']:
                    if i in device['targets']:
                        return_data['status'] = False
                        return_data['message'] = "Devices are already connected"
                        return return_data

                for i in data_recieved['targets']:
                    for device1 in data:
                        if device1['name'] == i:
                            device1['targets'] = device1['targets'] + [data_recieved['source']]

                device['targets'] = device['targets'] + data_recieved['targets']
                return_data['status'] = True
                return_data['message'] = "Successfully connected"
                return return_data

    def Update_device(self,data,device_to_be_updated,data_recieved):
        return_data = {"status": True, "message": ""}
        for device in data:
            if device['name'] == device_to_be_updated :
                if device['type'] == 'COMPUTER':
                    try:
                        data_recieved['value'] = int(data_recieved['value'])
                    except:
                        return_data['status'] = False
                        return_data['message'] = "value should be an integer"
                        return return_data

                    if int(data_recieved['value']) > -1:
                        device['strength'] = data_recieved['value']
                        return_data['status'] = True
                        return_data['message'] = "Successfully defined strength"
                        return return_data

                else:
                    return_data['status'] = False
                    return_data['message'] = "Device should be a computer"
                    return return_data


        return_data['status'] = False
        return_data['message'] = "Device Not Found."
        return return_data

    def Display_device(self,data):
        device_names = []
        for devices in data:
            device_details = {'name':devices['name'],'type':devices['type']}
            device_names.append(device_details)
        return device_names
    
    def Add_device(self,data,data_recieved):
        return_data = {"status" : True,"message" : ""}
        try:
            if data_recieved['type'] == 'COMPUTER' :
                if len(data_recieved['name'])>0:
                    device_detail = {'type': data_recieved['type'], 'name': data_recieved['name'],
                                     'targets': [], 'strength': 5}
                else:
                    return_data['status'] = False
                    return_data['message'] = "Invalid Command."
                    return return_data
            elif data_recieved['type'] == 'REPEATER':
                if len(data_recieved['name'])>0:
                    device_detail = {'type': data_recieved['type'], 'name': data_recieved['name'],
                                     'targets': [], 'strength': 0}
                else:
                    return_data['status'] = False
                    return_data['message'] = 'Invalid Command.'
                    return return_data

            else:
                return_data['status'] = False
                return_data['message'] = 'type '+data_recieved['type']+' is not supported'
                return return_data
        except:
            return_data['status'] = False
            return_data['message'] = 'Data missing'
            return return_data

        if len(data) < 1:
            data.insert(0, device_detail)
            return_data['status'] = True
            return_data['message'] = 'Successfully added '+ data_recieved['name']
            return return_data

        else:
            if any(device['name'] == data_recieved['name'] for device in data):
                return_data['status'] = False
                return_data['message'] = 'Device '+data_recieved['name']+' already exist'
                return return_data

            else:
                data.append(device_detail)
                return_data['status'] = True
                return_data['message'] = 'Successfully added '+ data_recieved['name']
                return return_data


    def Check_path(self, data, source, destination):
        return_data = {}
        if source == None or destination == None:
            return_data['status'] = False
            return_data['message'] = 'Invalid Request'
            return return_data

        device_names = []
        for devices in data:
            device_names.append(devices['name'])
        if source not in device_names:
            return_data['status'] = False
            return_data['message'] = "Node " + source + " not found"
            return return_data

        if destination not in device_names:
            return_data['status'] = False
            return_data['message'] = "Node " + destination + " not found"
            return return_data

        if source == destination:
            return_data['status'] = True
            return_data['message'] = 'Route '+ source + ' -> '+destination
            return return_data
        else:
            source_flag = False
            destination_flag = False
            for device in data:
                if device['name'] == source and device['type'] == 'COMPUTER':
                    source_flag = True
                if device['name'] == destination and device['type'] == 'COMPUTER':
                    destination_flag = True
            if source_flag == True and destination_flag == True:
                for device in data:

                    if device['name'] == source:
                        if destination in device['targets']:
                            return_data['status'] = True
                            return_data['message'] = 'The route is '+source+' -> '+destination
                            return return_data
                        route_map = [source]
                        self.route = source

                        for targets in device['targets']:
                            self.route = self.route + ' -> ' + targets
                            route_map.append(targets)
                            recursive_function_result = self.recursive_function(data, len(data)-1, targets,
                                                                                device['strength']-1,
                                                                                destination, route_map)
                            print(recursive_function_result)
                            if recursive_function_result:
                                return_data['status'] = True
                                return_data['message'] = 'Route is '+ self.route
                                return return_data
                            self.route = self.route.replace(' -> ' + targets, '')
                            remove = (4 + len(targets)) * -1
                            self.route = self.route[:remove]
                            route_map.remove(targets)


                        return_data['status'] = False
                        return_data['message'] = 'Route not found'
                        return return_data
            else:
                return_data['status'] = False
                return_data['message'] = 'Route cannot be calculated for repeater'
                return return_data

    def recursive_function(self, data, length_of_the_graph, current_device, strength, destination,route_map):
        if strength > 0 and length_of_the_graph > 0:
            for device in data:
                if device['name'] == current_device:
                    if destination in device['targets']:
                        self.route = self.route + ' -> ' + destination
                        return True
                    if device['type'] == 'REPEATER':
                        strength = strength * 2
                    else:
                        strength = strength - 1
                    for targets in device['targets']:
                        if targets not in route_map:
                            self.route = self.route + ' -> ' + targets

                            route_map.append(targets)
                            if self.recursive_function(data, length_of_the_graph - 1, targets, strength, destination,route_map):
                                return True
                            remove = (4 + len(targets))*-1
                            self.route = self.route[:remove]
                            route_map.remove(targets)
                    return False
        else:
            return False








