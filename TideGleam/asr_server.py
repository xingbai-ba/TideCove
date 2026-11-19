# -*- coding: utf-8 -*-
"""常驻的语音转写服务：模型只加载一次，之后每次转写几秒

启动：
    python asr_server.py            # 默认 127.0.0.1:9881
    python asr_server.py 9882

接口：
    POST /asr   {"path": "C:\\...\\a.webm"}   → {"text": "..."}
    GET  /ping  → {"ok": true}
"""
import sys
import json
import os
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import asr  # 同目录的 asr.py

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9881


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        data = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith('/ping'):
            return self._send(200, {'ok': True, 'model': asr.MODEL_DIR})
        self._send(404, {'error': 'not found'})

    def do_POST(self):
        if not self.path.startswith('/asr'):
            return self._send(404, {'error': 'not found'})
        try:
            n = int(self.headers.get('Content-Length') or 0)
            body = json.loads(self.rfile.read(n).decode('utf-8') or '{}')
            p = body.get('path') or ''
            if not p or not os.path.exists(p):
                return self._send(400, {'error': '音频不存在: %s' % p})
            text = asr.transcribe(p)
            return self._send(200, {'text': text})
        except Exception as e:
            return self._send(500, {'error': str(e), 'trace': traceback.format_exc()[-400:]})

    def log_message(self, fmt, *args):
        pass


if __name__ == '__main__':
    print('ASR 服务启动，端口 %d（首次请求会加载模型，约 10 秒）' % PORT, flush=True)
    HTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
