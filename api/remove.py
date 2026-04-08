from http.server import BaseHTTPRequestHandler
import cgi
import urllib.request
import os

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_type = self.headers.get('Content-Type', '')
        if 'multipart/form-data' not in content_type:
            self._error(400, '이미지를 multipart/form-data로 보내주세요')
            return

        try:
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    'REQUEST_METHOD': 'POST',
                    'CONTENT_TYPE': content_type,
                }
            )

            if 'image' not in form:
                self._error(400, 'image 필드가 없습니다')
                return

            image_data = form['image'].file.read()

            api_key = os.environ.get('REMOVE_BG_API_KEY', '')
            if not api_key:
                self._error(500, 'API 키가 설정되지 않았습니다')
                return

            body = (
                b'------FormBoundary\r\n'
                b'Content-Disposition: form-data; name="image_file"; filename="image.png"\r\n'
                b'Content-Type: image/png\r\n\r\n' +
                image_data +
                b'\r\n------FormBoundary\r\n'
                b'Content-Disposition: form-data; name="size"\r\n\r\nauto\r\n'
                b'------FormBoundary--\r\n'
            )

            req = urllib.request.Request(
                'https://api.remove.bg/v1.0/removebg',
                data=body,
                headers={
                    'X-Api-Key': api_key,
                    'Content-Type': 'multipart/form-data; boundary=----FormBoundary',
                }
            )

            with urllib.request.urlopen(req) as resp:
                result = resp.read()

            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.send_header('Content-Length', str(len(result)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(result)

        except Exception as e:
            self._error(500, f'오류: {str(e)}')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _error(self, code, message):
        import json
        body = json.dumps({'error': message}).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass
