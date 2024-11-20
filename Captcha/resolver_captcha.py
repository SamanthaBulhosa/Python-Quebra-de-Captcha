from tensorflow.keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
import numpy as np
import pickle
import cv2
from tratamento_captcha import tratar_imagem


def quebrar_captcha():
    # importa o modelo que foi treinado e importa o tradutor
    with open("rotulos_modelo.dat", "rb") as arquivo_tradutor:
        lb = pickle.loads(arquivo_tradutor.read())

    modelo = load_model("modelo_treinado.keras")

    # Usar o modelo para resolver os captchas
    tratar_imagem("resolver", pasta_destino="resolver")

    # Ctrl+C e Ctrl+V esse trecho de código é da pasta separar_letras que fiz pequenas alterações
    arquivos = list(paths.list_images("resolver"))
    for arquivo in arquivos:
        imagem = cv2.imread(arquivo)  # leu a imagem
        imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)  # converte para a escala de preto preto e branco
        _, nova_imagem = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY_INV)
        # esse método dar 2 retorno uma que vou ignorar utilizando _, o THRESH_BINARY_INV inverte
        # a cor onde for preto vai ficar branco e onde for branco vai ser preto.

        # encontrar o contornos de cada letra
        contornos, _ = cv2.findContours(nova_imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # gerar 2 retorno = faz o contorno(imagem, o píxel de fora para dentro)

        regiao_letras = []

        # Filtrando os contornos que são realmente letras_separadas
        for contorno in contornos:
            (x, y, largura, altura) = cv2.boundingRect(contorno)  # o meu contorno vai ser feito nessas médidas
            area = cv2.contourArea(contorno)  # area do retângulo já contornada
            if area > 115:  # Se a area do retângulo feita acima for mais que 115 ele vai desenhar e reconhecer como sendo uma letra.
                regiao_letras.append((x, y, largura, altura))
        regiao_letras = sorted(regiao_letras, key=lambda x: x[0])
        # Desenhar os contornos e separar as letras_separadas em arquivos individuais.
        imagem_final = cv2.merge([imagem] * 3)
        previsao = []

        i = 0
        for retangulo in regiao_letras:  # A parti desse ponto só ladeira abaixo para entender esse trem... :(
            x, y, largura, altura = retangulo
            imagem_letra = imagem[y - 2:y + altura + 2, x - 2:x + largura + 2]  # esse número 2 é para dar 2 píxel de espaço para não ficar grudado

            # Entrega a letra para a IA e ela descobre que letra é essa, mas no tamanho passado de 20x20.
            imagem_letra = resize_to_fit(imagem_letra, 20, 20)

            # Expandir dimensões - tratamento para o Keres funcionar
            imagem_letra = np.expand_dims(imagem_letra, axis=2)
            imagem_letra = np.expand_dims(imagem_letra, axis=0)

            # Previsão da letra por IA (número)
            letra_prevista = modelo.predict(imagem_letra)
            letra_prevista = lb.inverse_transform(letra_prevista)[0]
            previsao.append((letra_prevista))

        texto_previsao = "".join(previsao)
        print(texto_previsao)
        return texto_previsao

if __name__ == "__main__":
    quebrar_captcha()
