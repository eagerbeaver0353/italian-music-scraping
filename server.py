import http.server
import socketserver
import json

from scrape_radio_italy import scrape_radio
from scrape_shazam_italy import scrape_shazam
from scrape_spotify_italy_daily import scrape_spotify
from scrape_tiktok_italy_daily import scrape_tiktok
from scrape_youtube_italy_chartmetric import scrape_youtube
from custom_utils import convert_date, get_next_date
from unified_chart import generate_unified_chart


PORT = 8000
 # Define the request handler class
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Handle API endpoint
        content_length = int(self.headers['Content-Length'])
        request_body = self.rfile.read(content_length)
        # Process the request body as needed

        data = json.loads(request_body.decode('utf-8'))
        if 'end_date' in data:
            pass
        else:
            data["end_date"] = None
            
        start_date = convert_date(data["start_date"])
        end_date = get_next_date(data["start_date"]) if data["end_date"] is None else get_next_date(data["end_date"])
        
        start_date_fmt = start_date.strftime("%Y-%m-%d")
        
        scrape_radio(start_date_fmt, end_date)
        scrape_shazam(start_date_fmt, end_date)
        scrape_spotify(start_date_fmt, end_date)
        scrape_tiktok(start_date_fmt, end_date)
        scrape_youtube(start_date_fmt, end_date)
        
        self.send_response(200)
        # Set the response headers
        self.send_header('Content-type', 'application/octet-stream')
        self.send_header('Content-Disposition', 'attachment; filename="filename.extension"')
        self.end_headers()
        
        self.wfile.write(generate_unified_chart(start_date, end_date, data["data"]))

    def do_GET(self):
        # Serve static files
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

 # Create an HTTP server with the custom request handler
with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Server started on port {PORT}")
    httpd.serve_forever()