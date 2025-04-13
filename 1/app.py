import face_recognition
import base64
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Məlumat bazasında olan üzlər (test üçün 1 nəfərlik nümunə)
known_faces = []
known_names = []

# Sistemdə qeydiyyatda olan bir üzü yükləyək (foto fayl kimi saxlamısansa)
# Şəkli əvvəlcədən "person1.jpg" kimi eyni qovluğa qoy
person_image = face_recognition.load_image_file("person1.jpg")
person_encoding = face_recognition.face_encodings(person_image)[0]
known_faces.append(person_encoding)
known_names.append("Denis")  # Adını özün dəyişə bilərsən

@app.route("/recognize", methods=["POST"])
def recognize():
    data = request.get_json()

    if "image" not in data:
        return jsonify({"message": "Şəkil göndərilməyib"}), 400

    image_data = data["image"].split(',')[1]
    img_bytes = base64.b64decode(image_data)
    img = Image.open(BytesIO(img_bytes))
    img = np.array(img)

    rgb_img = img[:, :, :3]

    face_locations = face_recognition.face_locations(rgb_img)
    face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        if True in matches:
            matched_idx = matches.index(True)
            name = known_names[matched_idx]
            return jsonify({"message": f"Xoş gəldin, {name}!"})

    return jsonify({"message": "Tanımadı"}), 401

if __name__ == "__main__":
    app.run(debug=True)
