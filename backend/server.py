from flask import Flask, request, jsonify
from flask_cors import CORS

import gzip
import xml.etree.ElementTree as ET
import xmltodict, json

app = Flask(__name__)
CORS(app)

print("yallo")
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return "No selected file", 400

    if file:
        # Read the uploaded file
        xml_content = file.read()

        # Decompress the gzip file
        decompressed_content = gzip.decompress(xml_content)
        json_obj = xmltodict.parse(decompressed_content)
        json_str = json.dumps(json_obj)
        # Now you can process the XML data as needed
        return json_str, 200, {'Content-Type': 'application/json'}
    return "Error processing file", 500

if __name__ == '__main__':
    app.run(debug=True)
