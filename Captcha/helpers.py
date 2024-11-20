import cv2

def resize_to_fit(image, width, height):
    """
    Redimensiona uma imagem para um tamanho fixo (width x height), mantendo a proporção.
    """
    # Determina a proporção da imagem
    (h, w) = image.shape[:2]
    if w > h:
        image = cv2.resize(image, (width, int(h * width / w)))
    else:
        image = cv2.resize(image, (int(w * height / h), height))

    # Adiciona preenchimento (padding) para ajustar o tamanho
    padW = int((width - image.shape[1]) / 2.0)
    padH = int((height - image.shape[0]) / 2.0)
    image = cv2.copyMakeBorder(image, padH, padH, padW, padW, cv2.BORDER_REPLICATE)

    return cv2.resize(image, (width, height))
