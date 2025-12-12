from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import yt_dlp
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def get_video_info():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # Prefer mp4 for better compatibility and easier direct downloads
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            # Fallback logic if url is not at top level
            if not video_url:
                for f in info.get('formats', []):
                    if f.get('url'):
                        video_url = f['url']
                        break

            title = info.get('title', 'Pinterest Video')
            thumbnail = info.get('thumbnail')
            
            return jsonify({
                'title': title,
                'video_url': video_url,
                'thumbnail': thumbnail
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_proxy')
def download_proxy():
    video_url = request.args.get('url')
    title = request.args.get('title', 'pinterest_video')
    
    if not video_url:
        return "Missing URL", 400
        
    try:
        # Stream the file from the remote URL to the client
        req = requests.get(video_url, stream=True)
        req.raise_for_status()
        
        # Sanitize title for filename
        safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).strip()
        if not safe_title:
            safe_title = "pinterest_video"
        filename = f"{safe_title}.mp4"

        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': req.headers.get('Content-Type', 'video/mp4')
        }
        
        return Response(stream_with_context(req.iter_content(chunk_size=4096)), headers=headers)
        
    except Exception as e:
        return f"Error downloading file: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
