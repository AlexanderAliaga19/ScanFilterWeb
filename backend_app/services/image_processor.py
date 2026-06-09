# /**
#  * @author: Alexander Auden Aliaga Ocampo
#  * codigo:U202417693
#  */

import base64
from io import BytesIO

import cv2
import numpy as np
from PIL import Image


def load_uploaded_image(uploaded_file, use_color: bool):
    """
    Convierte una imagen subida desde Django a una matriz de NumPy.

    Si use_color es True, la imagen se trabaja en RGB.
    Si use_color es False, se trabaja en escala de grises.
    """
    image = Image.open(uploaded_file)

    if use_color:
        image = image.convert("RGB")
        return np.array(image)

    image = image.convert("L")
    return np.array(image)


def crop_image(image, mode: str, x: int = 0, y: int = 0):
    """
    Devuelve la imagen completa o un recorte 15x15 según el modo seleccionado.
    """
    if mode == "full":
        return image

    height, width = image.shape[:2]

    if x < 0 or y < 0:
        raise ValueError("Las coordenadas no pueden ser negativas.")

    if x + 15 > width or y + 15 > height:
        raise ValueError("El recorte 15x15 se sale de los límites de la imagen.")

    return image[y:y + 15, x:x + 15]


def apply_filter(image, filter_name: str):
    """
    Aplica un filtro digital a la imagen recibida.
    """
    if filter_name == "mean":
        return cv2.blur(image, (3, 3))

    if filter_name == "median":
        return cv2.medianBlur(image, 3)

    if filter_name == "laplacian":
        return cv2.Laplacian(image, cv2.CV_64F)

    if filter_name == "sobel":
        sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        return np.sqrt(sobel_x ** 2 + sobel_y ** 2)

    raise ValueError("Filtro no válido.")


def normalize_image(image):
    """
    Normaliza la imagen entre 0 y 255 para poder visualizarla.
    """
    return cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def image_to_base64(image):
    """
    Convierte una matriz de imagen a base64 para enviarla al frontend.
    """
    if len(image.shape) == 2:
        pil_image = Image.fromarray(image)
    else:
        pil_image = Image.fromarray(image.astype(np.uint8))

    buffer = BytesIO()
    pil_image.save(buffer, format="PNG")

    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded_image}"


def matrix_preview(image, limit: int = 15):
    """
    Devuelve una matriz pequeña para mostrarla en el frontend.

    Si la imagen es muy grande, solo muestra una vista previa 15x15.
    Si es a color, convierte cada píxel RGB en una lista [R, G, B].
    """
    preview = image[:limit, :limit]

    if len(preview.shape) == 3:
        return preview.astype(int).tolist()

    return preview.astype(int).tolist()