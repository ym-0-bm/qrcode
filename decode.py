import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image
import io
import base64
import json
import zlib


def decompress_image(compressed_image_data, original_size):
    # Decode the Base64-encoded compressed string
    compressed_data = base64.b64decode(compressed_image_data)

    # Decompress the zlib-compressed data
    decompressed_data = zlib.decompress(compressed_data)

    # Decode the final Base64 to get the original image bytes
    image_data = base64.b64decode(decompressed_data)

    image = Image.open(io.BytesIO(image_data))
    decompressed_image = image.resize(original_size, Image.LANCZOS)
    return decompressed_image


def decode_qr_code(image):
    decoded_objects = decode(image)
    if decoded_objects:
        data = decoded_objects[0].data.decode('utf-8')
        return data
    return None


def save_and_display_image(base64_image, original_size):
    try:
        decompressed_image = decompress_image(base64_image, original_size)
        st.image(decompressed_image, caption="Image décodée et décompressée", use_column_width=True)
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde ou de l'affichage de l'image : {e}")


def display_data(data):
    try:
        data = json.loads(data)
        name = data.get("name", "No name")
        image_base64 = data.get("image", "")
        original_size = tuple(data.get("original_size", (100, 100)))

        st.write(f"Nom: {name}")

        if image_base64:
            save_and_display_image(image_base64, original_size)
        else:
            st.warning("Aucune image encodée trouvée dans les données.")
    except Exception as e:
        st.error(f"Erreur lors du traitement des données : {e}")


st.title("Décodeur de QR Code")

uploaded_file = st.file_uploader("Téléchargez un QR Code", type=["png", "jpg", "jpeg"])

if st.button("Décoder le QR Code"):
    if uploaded_file:
        image = Image.open(uploaded_file)
        data = decode_qr_code(image)

        if data:
            display_data(data)
        else:
            st.error("Aucun QR code détecté ou impossible de décoder le QR code.")
    else:
        st.error("Veuillez télécharger une image de QR Code.")
