from flask import Flask, jsonify, request, send_from_directory, send_file,  Response, abort
import json
import os
from scrape_radio_italy import scrape_radio
from scrape_shazam_italy_chartmetric import scrape_shazam
from scrape_spotify_italy_chartmetric import scrape_spotify
from scrape_tiktok_italy_chartmetric import scrape_tiktok
from scrape_youtube_italy_chartmetric import scrape_youtube
from custom_utils import convert_date, get_next_date, zip_files_with_condition
from unified_chart import generate_unified_chart
app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), filename)

@app.post('/api')
def handle_request():
    print("AAA")
    # Handle API endpoint
    content_length = int(request.headers['Content-Length'])
    request_body = request.get_data(as_text=True)
    # Process the request body as needed
    data = json.loads(request_body)

    if 'end_date' in data:
        pass
    else:
        data["end_date"] = None

    try:
        start_date = convert_date(data["start_date"])
        end_date = get_next_date(data["start_date"]) if data["end_date"] is None else get_next_date(data["end_date"])
        start_date_fmt = start_date.strftime("%Y-%m-%d")
        # if data["data"]["radio"] > 0:
        #     scrape_radio(start_date_fmt, end_date)
        
        if data["data"]["shazam"] > 0:
            scrape_shazam(start_date_fmt, end_date)
        
        if data["data"]["spotify"] > 0:
            scrape_spotify(start_date_fmt, end_date)
        
        if data["data"]["tiktok"] > 0:
            scrape_tiktok(start_date_fmt, end_date)
        
        if data["data"]["youtube"] > 0:
            scrape_youtube(start_date_fmt, end_date)

        generate_unified_chart(start_date, end_date, data["data"])
        file_path = f'{os.path.dirname(os.path.abspath(__file__))}/result.zip'
        zip_files_with_condition(f'{os.path.dirname(os.path.abspath(__file__))}/output', file_path, start_date, end_date, ["sorted_music_tracks.csv", "top_music_tracks.csv"])
        
    except Exception as e:
        # Handle the error here
        error_message = str(e)
        print("An error occurred:", error_message)
        # Return the error message as a response if needed
        return jsonify(error=error_message), 500

    try:
        with open(file_path, 'r') as file:
            # Read the contents of the file
            return send_file(
                file_path,
                mimetype="application/zip",
                as_attachment=True
            )
                # headers={"Content-disposition":
                #         "attachment; filename=top_tracks.csv"})
    except:
        return abort(404)

    return send_file(file_path, as_attachment=True)

@app.errorhandler(500)  # Error handler for 500 Internal Server Error
def internal_server_error(error):
    print("WWWWWW", error)
    print(str(error))
    return jsonify(str(error)), 500
 
if __name__ == '__main__':
    app.run('localhost', 8000)