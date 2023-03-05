import http.server
import socketserver
import json
import xml.etree.ElementTree as ET
import xmltodict
from xml.dom import minidom

# with open("customers.xml") as xml_file:
#     data_dict = xmltodict.parse(xml_file.read())
#     json_data = json.dumps(data_dict)
#     print(data_dict['Customers']['Customer'][1])
#     print(len(data_dict['Customers']['Customer']))
#     for key in data_dict['Customers']['Customer'][1].keys():
#         print(data_dict['Customers']['Customer'][1]['@id'])
#     tree = ET.parse('customers.xml')
#     root = tree.getroot()
#     for names in root.iter('CustomerName'):
#         print(",,",names.text)


class MyHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        path_parts = self.path.split("/")
        print(len(path_parts))
        if self.path == '/customers':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            data = ""
            tree = ET.parse('customers.xml')
            root = tree.getroot()
            for names in root.iter('CustomerName'):
                data += names.text + ','
            data = data[0:-1]
            message = {'data': data}
            self.wfile.write(bytes(json.dumps(message), "utf8"))
        elif path_parts[1] == 'customers' and len(path_parts) == 3:
            customer_id = path_parts[2]
            print(customer_id)
            print(path_parts)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            data = ""
            tree = ET.parse('customers.xml')
            root = tree.getroot()
            for customer in root.iter('Customer'):
                if customer.get("id") == customer_id:
                    data = customer.find("CustomerName").text
            if data != "":
                message = {'data': data}
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Customer not found"}).encode("utf-8"))

            self.wfile.write(bytes(json.dumps(message), "utf8"))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

    def do_POST(self):
        path_parts = self.path.split("/")
        if self.path == '/customers':
            content_length = int(self.headers['Content-Length'])
            print(content_length)
            body = self.rfile.read(content_length)
            data = body.decode()
            print(data)
            tree = ET.parse('customers.xml')
            root = tree.getroot()
            for customer in root.iter('Customer'):
                len_ids = customer.get("id")
            len_ids = int(len_ids)
            len_ids += 1
            new = root.find("Customers")
            new_elem = ET.Element('Customer')
            new_elem.set('id', str(len_ids))
            ET.dump(new_elem)
            new_elem_name = ET.SubElement(new_elem, 'CustomerName')
            new_elem_name.text = str(data)
            #ET.dump(new_elem_name)

            #dom = minidom.parseString(ET.tostring(new_elem))
            #dom.toprettyxml(indent='\t')
            root.append(new_elem)
            ##ET.tostring(root, encoding='utf8').decode('utf8')
            print("wtf")

            tree.write('customers.xml')

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.send_header('Location', 'http://localhost:8000/customers/' + str(len_ids))
            self.end_headers()

            response = {'message': 'Data received successfully', 'data': data}
            self.wfile.write(bytes(json.dumps(response), "utf8"))
        elif path_parts[1] == 'customers' and len(path_parts) == 3:
            customer_id = path_parts[2]
            content_length = int(self.headers['Content-Length'])
            print(content_length)
            body = self.rfile.read(content_length)
            data = body.decode()
            print(data)
            tree = ET.parse('customers.xml')
            root = tree.getroot()
            found = 0
            for customer in root.iter('Customer'):
                if customer.get("id") == customer_id:
                    self.send_response(409)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'message': 'Id already exists'}
                    self.wfile.write(bytes(json.dumps(response), "utf8"))
                    found = 1
            if found == 0:
                new = root.find("Customers")
                new_elem = ET.Element('Customer')
                new_elem.set('id', str(customer_id))
                ET.dump(new_elem)
                new_elem_name = ET.SubElement(new_elem, 'CustomerName')
                new_elem_name.text = str(data)
                root.append(new_elem)
                tree.write('customers.xml')
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.send_header('Location', 'http://localhost:8000/customers/' + str(customer_id))
                self.end_headers()
                response = {'message': 'Data received successfully', 'data': data}
                self.wfile.write(bytes(json.dumps(response), "utf8"))

    def do_PUT(self):
        path_parts = self.path.split("/")
        if self.path == '/customers':
            self.send_response(405)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
        elif path_parts[1] == 'customers' and len(path_parts) == 3:
            customer_id = path_parts[2]
            print(customer_id)
            tree = ET.parse('customers.xml')
            root = tree.getroot()
            found = 0
            for customer in root.iter('Customer'):
                if customer.get("id") == customer_id:
                    found = 1
                    print(customer_id)
                    content_length = int(self.headers['Content-Length'])
                    if content_length == 0:
                        self.send_response(204)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                    else:
                        body = self.rfile.read(content_length)
                        data = body.decode()
                        customer.find("CustomerName").text = str(data)
                        tree.write('customers.xml')
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = {'message': 'Data received successfully', 'data': data}
                        self.wfile.write(bytes(json.dumps(response), "utf8"))
                    break
            if found == 0:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
    def do_DELETE(self):
        path_parts = self.path.split("/")
        if self.path == '/customers':
            self.send_response(405)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
        elif path_parts[1] == 'customers' and len(path_parts) == 3:
            customer_id = path_parts[2]
            print(customer_id)
            tree = ET.parse('customers.xml')
            root = tree.getroot()
            found = 0
            for customer in root.iter('Customer'):
                if customer.get("id") == customer_id:
                    found = 1
                    print(customer_id)
                    root.remove(customer)
                    tree.write('customers.xml')
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'message': 'Data deleted successfully', 'data': customer_id}
                    self.wfile.write(bytes(json.dumps(response), "utf8"))
                    break
            if found == 0:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()


PORT = 8000
handler = MyHandler
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("Server started at localhost:" + str(PORT))
    httpd.serve_forever()

