# TRATAMENTO CAPTCHO
# Aqui vou criar um código para rodar todas as imagens de captcha já tratados.

import cv2
import os  # Ler arquivo dentro de pasta, manipular arquivos é uma das tarefas mais comuns
import glob  # Manipulação de arquivos e diretórios, busca por padrões de nome, busca recursiva em subdiretórios e manipulação de caminhos de arquivo
from PIL import Image


def tratar_imagem(pasta_origem, pasta_destino='tratado'):
    # ler na pasta origem(bdcaptcha) e depois salva na pasta destino(tratado).
    arquivos = glob.glob(f'{pasta_origem}/*')
    # vai mostrar o local e o nome do arquivo de tudo que passar por esse comando (*/ significar ler tudo)
    for arquivo in arquivos:  # para cada arquivo em arquivos
        imagem = cv2.imread(arquivo)  # Leia o arquivo

        # transformar a imagem em escala de cinza abaixo:
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

        _, imagem_tratada = cv2.threshold(imagem_cinza, 127, 255, cv2.THRESH_TRUNC or cv2.THRESH_OTSU)
        nome_arquivo = os.path.basename(arquivo)  # ler o nome do arquivo com a extensão do arquivo e com isso faço
        # o código abaixo quando tratado a imagem salvar com o mesmo nome que estava na pasta origem
        cv2.imwrite(f'{pasta_destino}/{nome_arquivo}', imagem_tratada)

    arquivos = glob.glob(f'{pasta_destino}/*')
    for arquivo in arquivos:
        imagem = Image.open(arquivo)
        imagem = imagem.convert('P')
        imagem2 = Image.new('P', imagem.size, (255, 255, 255))  # faz a copia da imagem / 255 cor branca

        for pixel_largura in range(imagem.size[1]):
            for pixel_altura in range(imagem.size[0]):
                cor_pixel = imagem.getpixel((pixel_altura, pixel_largura))
                if cor_pixel < 115:  # Se a cor do píxel for menor que X faça:
                    imagem2.putpixel((pixel_altura, pixel_largura), (0, 0, 0))  # valor 0 é cor preta
        nome_arquivo = os.path.basename(arquivo)
        imagem2.save(f'{pasta_destino}/{nome_arquivo}')


if __name__ == '__main__':  # se voce estiver exportando esse aquivo de outro lugar ele não vai executar dentro desse if
    tratar_imagem('bdcaptcha')
