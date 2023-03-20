import requests
from flask import Flask
from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/get', methods=['POST'])
def get():
   data = request.json
   message = data['message']
   print(message)
   #url = "https://api.openapi.ro/api/companies/23838406"
   #headers={"x-api-key":"gsMQ8ueVTWCPx41sy6P649F4AbR1sn7TTiGsPtYykTUV3M67mQ"}
   #response = requests.get(url, headers=headers)
   response = requests.get(message)
   data = response.json()
   print(str(data))
   return jsonify(data)

@app.route('/post/<int:id>', methods=['POST'])
def post(id):
   data = request.json
   print(data)
   message = data
   print(message)
   print(id)
   #url = "https://api.openapi.ro/api/companies/23838406"
   #headers={"x-api-key":"gsMQ8ueVTWCPx41sy6P649F4AbR1sn7TTiGsPtYykTUV3M67mQ"}
   #response = requests.get(url, headers=headers)
   response = requests.post("http://localhost:8000/customers/"+str(id), data=message)
   data = response.json()
   print(str(data))
   return jsonify(data)

@app.route('/put/<int:id>', methods=['POST'])
def put(id):
   data = request.json
   print(data)
   message = data
   print(message)
   print(id)
   #url = "https://api.openapi.ro/api/companies/23838406"
   #headers={"x-api-key":"gsMQ8ueVTWCPx41sy6P649F4AbR1sn7TTiGsPtYykTUV3M67mQ"}
   #response = requests.get(url, headers=headers)
   response = requests.put("http://localhost:8000/customers/"+str(id), data=message)
   data = response.json()
   print(str(data))
   return jsonify(data)

@app.route('/delete', methods=['POST'])
def delete():
   data = request.json
   message = data['message']
   print(message)
   #url = "https://api.openapi.ro/api/companies/23838406"
   #headers={"x-api-key":"gsMQ8ueVTWCPx41sy6P649F4AbR1sn7TTiGsPtYykTUV3M67mQ"}
   #response = requests.get(url, headers=headers)
   response = requests.delete(message)
   data = response.json()
   print(str(data))
   return jsonify(data)
@app.route('/cif', methods=['POST'])
def cif():
   data = request.json
   message = data['message']
   print(message)
   #url = "https://api.openapi.ro/api/companies/23838406"
   #headers={"x-api-key":"gsMQ8ueVTWCPx41sy6P649F4AbR1sn7TTiGsPtYykTUV3M67mQ"}
   #response = requests.get(url, headers=headers)
   response = requests.get(message)
   data = response.json()
   print(data['data'])
   header = {
      'x-api-key': 'gsMQ8ueVTWCPx41sy6P649F4AbR1sn7TTiGsPtYykTUV3M67mQ'
   }
   responseApi = requests.get('https://api.openapi.ro/api/companies/' + str(data['data']), headers=header)
   dataApi = responseApi.json()
   return jsonify(dataApi)

@app.route('/cnp', methods=['POST'])
def cnp():
   data = request.json
   message = data['message']
   print(message)
   #url = "https://api.openapi.ro/api/companies/23838406"
   #headers={"x-api-key":"gsMQ8ueVTWCPx41sy6P649F4AbR1sn7TTiGsPtYykTUV3M67mQ"}
   #response = requests.get(url, headers=headers)
   response = requests.get(message)
   data = response.json()
   print(data['data'])
   header={
    'x-api-key': 'gsMQ8ueVTWCPx41sy6P649F4AbR1sn7TTiGsPtYykTUV3M67mQ'
   }
   responseApi = requests.get('https://api.openapi.ro/api/validate/cnp/'+str(data['data']), headers=header)
   dataApi = responseApi.json()
   return jsonify(dataApi)
# url = "https://webservicesp.anaf.ro/AsynchWebService/api/v7/ws/tva"
# data = [
#     {
#         "cui": 23838406,
#         "data": "2015-02-14"
#     }
# ]
#
# # send the request
# response = requests.post(url, json=data)
#
# # check the response status code and content
# if response.status_code == 200:
#     print("POST request successful")
#     print(response.content)
# else:
#     print("POST request failed")
# import json
# url = "https://webservicesp.anaf.ro/AsynchWebService/api/v7/ws/tva?id=272a95a7-e44b-4201-9a8d-35432b714a82"
#
# # send the request
# response = requests.get(url)
#
# # check the response status code and content
# if response.status_code == 200:
#     # the response content is usually JSON, so you can parse it with json.loads()
#     data = json.loads(response.content)
#     print("GET request successful")
#     print(data)
# else:
#     print("GET request failed")
if __name__ == '__main__':
   app.run()

