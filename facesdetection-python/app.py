import numpy as np
from urllib.request import urlopen
import cv2
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

def detect_faces(image_url):

    print('hola la url es:')
    print(image_url)
    # Load the cascade Classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Read the input image
    resp = urlopen(image_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(image, cv2.IMREAD_COLOR) # The image object

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Combina las listas de cuadros delimitadores para cada objeto en una sola lista
    all_boxes = []
    for box in faces:
        all_boxes.append(box)


    # Dibuja los cuadros delimitadores en la imagen original
    for box in all_boxes:
        x, y, w, h = box
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    _, encoded_img = cv2.imencode('.png', img)  # Works for '.jpg' as well
    base64_img = base64.b64encode(encoded_img).decode("utf-8")  
    return base64_img  

@app.route('/function/facesdetection-python', methods=['POST'])
def handle_request():
    image_url = request.get_data(as_text=True).strip()
    if not image_url:
        return jsonify({'error': 'No URL provided'}), 400
    try:
        base64_image = detect_faces(image_url)
        return jsonify({'image': base64_image})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)