import streamlit as st
from PIL import Image
import io
import base64
import json
import qrcode
import zlibgi


def compress_image(image, max_size=(100, 100), quality=80):
    original_size = image.size
    image.thumbnail(max_size)
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=quality)
    return buffered.getvalue(), original_size

def generate_qr_code(data):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return buffered.getvalue()

st.title("Générateur de QR Code")

name = st.text_input("Entrez votre nom:")
uploaded_file = st.file_uploader("Choisissez une image", type=["png", "jpg", "jpeg"])

if st.button("Générer le QR Code"):
    if uploaded_file and name:
        image = Image.open(uploaded_file)
        compressed_image, original_size = compress_image(image)

        encoded_image = base64.b64encode(compressed_image).decode('utf-8')
        compressed_encoded_image = base64.b64encode(zlib.compress(encoded_image.encode('utf-8'))).decode('utf-8')

        data = {
            "name": name,
            "image": compressed_encoded_image,
            "original_size": original_size
        }
        json_data = json.dumps(data)

        qr_code_image = generate_qr_code(json_data)

        st.success("QR code généré avec succès!")
        st.image(qr_code_image, caption="QR Code", use_column_width=True)

        st.download_button(label="Télécharger le QR Code", data=qr_code_image, file_name="qrcode.png", mime="image/png")
    else:
        st.error("Veuillez entrer un nom et télécharger une image.")
