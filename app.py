from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            if not video_url:
                 # Start looking for requested formats if 'url' not in info
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

if __name__ == '__main__':
    # Optional: Start ngrok to share with friends
    try:
        from pyngrok import ngrok
        # Open a HTTP tunnel on the default port 5000
        public_url = ngrok.connect(5000).public_url
        print(f" * Public URL to share with friends: {public_url}")
    except ImportError:
        print(" * pyngrok not installed, skipping public URL generation.")
    except Exception as e:
        print(f" * Could not start ngrok: {e}")

    app.run(debug=True, port=5000)
