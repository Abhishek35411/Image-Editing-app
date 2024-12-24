from flask import Flask, render_template, jsonify, request
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from cloudinary import CloudinaryImage
import requests
import secret as s

app = Flask(__name__)

# Configuration       
cloudinary.config(
    cloud_name = s.cloud_name, 
    api_key = s.api_key,
    api_secret = s.api_secret,
    secure=True
)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/playground')
def playground():
    return render_template('playground.html')

# Upload route
@app.route('/upload', methods=['POST'])
def upload_image():
    file_to_upload = request.files['file']
    if file_to_upload:
        upload_result = cloudinary.uploader.upload(file_to_upload)
        return jsonify({
            'url': upload_result['secure_url'],
            'public_id': upload_result['public_id']
        })
    return jsonify({'error': 'No file uploaded'})

# Process image route (testing by showing the same image)
@app.route('/process', methods=['POST'])
def process_image():
    data = request.get_json()
    public_id = data.get('public_id')
    action = data.get('action')
    global url
    global id
    if(action == "enhance"):
        img_tag = CloudinaryImage("me/underexposed-1.jpg").image(effect="enhance")
        # Find the position of the 'src' attribute
        start_pos = img_tag.find('src="') + len('src="')

        # Find the position of the closing double quote after the URL
        end_pos = img_tag.find('"', start_pos)

        # Extract the URL
        img_url = img_tag[start_pos:end_pos]
        url=img_url
        id=public_id
        return jsonify({
            'processed_url': img_url
        })

    elif (action == "resize"):
        img_tag = CloudinaryImage(public_id).image(gravity="auto", height=940, width=880, crop="auto")
        # Find the position of the 'src' attribute
        start_pos = img_tag.find('src="') + len('src="')

        # Find the position of the closing double quote after the URL
        end_pos = img_tag.find('"', start_pos)

        # Extract the URL
        img_url = img_tag[start_pos:end_pos]
        url=img_url
        return jsonify({
            'processed_url': img_url
        })
    
def downloader(url):
    img = requests.get(url).content
    with open("image.jpg", "wb") as f:
        f.write(img)
        
@app.route('/download',methods=['GET'])
def download():
    downloader(url)
    return jsonify({'message': 'Image downloaded successfully'})

app.run(debug=True)