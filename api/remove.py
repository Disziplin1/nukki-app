from http.server import BaseHTTPRequestHandler
import cgi
import io
from rembg import remove
from PIL import Image


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # Parse multipart form data
        content_type = self.headers.get('Content-Type', '')
        if 'multipart/form-data' not in content_type:
            self._error(400, 'multipart/form-data 형식으로 보내주세요')
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

            file_item = form['image']
            image_data = file_item.file.read()

            if len(image_data) > 20 * 1024 * 1024:
                self._error(413, '20MB 이하 파일만 가능합니다')
                return

            # Open and validate image
            try:
                img = Image.open(io.BytesIO(image_data))
                img.verify()
                img = Image.open(io.BytesIO(image_data))
            except Exception:
                self._error(400, '유효하지 않은 이미지 파일입니다')
                return

            # Remove background using rembg (U2Net model)
            output = remove(image_data)

            # Return PNG with transparent background
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.send_header('Content-Length', str(len(output)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(output)

        except Exception as e:
            self._error(500, f'처리 중 오류가 발생했습니다: {str(e)}')

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
        pass  # suppress default logging
