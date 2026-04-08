from http.server import BaseHTTPRequestHandler
import urllib.request
import json
import os

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        api_key = os.environ.get('REMOVE_BG_API_KEY', '')
        if not api_key:
            self._json(500, {'error': 'API 키 없음'})
            return

        try:
            req = urllib.request.Request(
                'https://api.remove.bg/v1.0/account',
                headers={'X-Api-Key': api_key}
            )
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read())
            attrs = data.get('data', {}).get('attributes', {})
            credits = attrs.get('credits', {}).get('total', 0)
            self._json(200, {'credits': credits})
        except Exception as e:
            self._json(500, {'error': str(e)})

    def _json(self, code, obj):
        body = json.dumps(obj).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass
