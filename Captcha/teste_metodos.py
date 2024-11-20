# TESTE METODOS
# Aqui vou fazer o tratamento da imagem com teste para ver qual será o melhor resultado para poder
# aplicar nas demais imagens.

import cv2
from PIL import Image

# faz 5 tratamentos de imagem e escolhemos o que tem melhor resultado
metodos_tratamento = [
    cv2.THRESH_BINARY,
    cv2.THRESH_BINARY_INV,
    cv2.THRESH_TRUNC,
    cv2.THRESH_TOZERO,
    cv2.THRESH_TOZERO_INV,]

imagem = cv2.imread("bdcaptcha/telanova108.png")  # ler a imagem, coloquei a pasta e o nome do arquivo
# transformar a imagem em escala de cinza abaixo:

imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)
i = 0
for metodo in metodos_tratamento:
    i += 1
    _, imagem_tratada = cv2.threshold(imagem_cinza, 127, 255, metodo or cv2.THRESH_OTSU)
    # essa função(threshold) analisa o píxel e vai pintar o captcha de uma determinada cor.

    # Gera 2 resultado, um é a variável e o outro o resultado do tratamento da imagem.
    # _, antes da minha variável, indica que não vou utilizar para o restante do código
    # porque se trata de uma imagem que vai gerar um resultado vizual e não utilizo depois a variável.

    cv2.imwrite(f'teste_tratamento/imagem_tratada_{i}.png', imagem_tratada)
    # local é a pasta onde quero salvar a imagem tratada, o nome da imagem e coloquei o 'i' porque é de índice,
    # As próximas imagens que vai ser salvas na pasta vai começar (índice) do 1 até a quantidade de arquivo que salvar.

imagem = Image.open('teste_tratamento/imagem_tratada_3.png')
imagem = imagem.convert('P')  # Converte cada píxel da imagem da cor 'branca/cinza' para 'preto', e a onde for 'preto' ele pinta o píxel de 'branco'.
imagem2 = Image.new('P', imagem.size, (255, 255, 255))  # faz a copia da imagem / 255 cor branca
for pixel_largura in range(imagem.size[1]):
    for pixel_altura in range(imagem.size[0]):
        cor_pixel = imagem.getpixel((pixel_altura, pixel_largura))
        if cor_pixel < 115:  # Se a cor do píxel for menor que X faça:
            imagem2.putpixel((pixel_altura, pixel_largura), (0, 0, 0))  # valor 0 é cor preta
imagem2.save('tratado/imagemfinal.png')