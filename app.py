from flask import request,jsonify, Blueprint
from flask_api import status,FlaskAPI
from Validator import Validator

app = FlaskAPI(__name__)
#in-memory used
data = []


@app.route('/ajiranet/process/devices',methods = ['POST','GET'])
def Create_device():
    if request.method == 'POST':
        data_device = Validator().Add_device(data,request.data)
        if data_device['status']:
            return jsonify({'msg':data_device['message']}),status.HTTP_200_OK
        else:
            return jsonify({'msg':data_device['message']}),status.HTTP_400_BAD_REQUEST

    if request.method == 'GET':
        return jsonify({'msg': Validator().Display_device(data)}),status.HTTP_200_OK


@app.route('/ajiranet/process/devices/<source>/<strength>', methods=['POST'])
def Update_devices(source,strength):
    if request.method == 'POST':
        result = Validator().Update_device(data,source,request.data)

        if result['status']:
            return jsonify({'msg':result['message']}), status.HTTP_200_OK,
        return jsonify({'msg':result['message']}), status.HTTP_200_OK,


@app.route('/ajiranet/process/connections',methods = ['POST'])
def Create_connections():
    if request.method == 'POST':
        result = Validator().Connector(data,request.data)
        if result['status']:
            return jsonify({'msg':result['message']}), status.HTTP_200_OK,
        else:
            return jsonify({'msg':result['message']}), status.HTTP_400_BAD_REQUEST,


@app.route('/ajiranet/process/info-routes',methods = ['POST'])
def Does_path_exist():
    if request.method == 'POST':
        result = Validator().Check_path(data, request.args.get('from'), request.args.get('to'))
        print(result)
        if result['status']:
            return jsonify({'msg':result['message']}), status.HTTP_200_OK
        else:
            return jsonify({'msg':result['message']}),status.HTTP_400_BAD_REQUEST


if __name__ == '__main__':
    app.run(debug=True, port=8080)
