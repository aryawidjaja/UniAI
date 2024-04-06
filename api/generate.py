from http.server import BaseHTTPRequestHandler
import sys
import os
import json

# Add the project root to sys.path to import script.py
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from script import generate_vocab

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        # Extract input data from the POST request
        subject = data.get('language')
        grade = data.get('grade')
        level = data.get('level')
        topic = data.get('topic')
        amount = data.get('amount')

        # Call the generate_vocab function from script.py
        try:
            results = generate_vocab(subject, grade, level, topic, amount)
            self._send_response(200, json.dumps({"result_html": results}))
        except Exception as e:
            self._send_response(500, json.dumps({"error_message": str(e)}))

    def _send_response(self, status_code, body):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(body.encode())
