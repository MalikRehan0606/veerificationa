import http.server
import socketserver
import subprocess
import logging

PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/verify':
            try:
                # Attempt to start the Tkinter app
                subprocess.Popen(["python", r"C:\Users\imali\OneDrive\Desktop\New folder\project\html\sig.py"])
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"Tkinter app started")
            except Exception as e:
                logging.error("Failed to start Tkinter app", exc_info=True)
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"Failed to start Tkinter app")
        else:
            super().do_GET()

handler = MyHandler

with socketserver.TCPServer(("", PORT), handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
