# Treinar modelo para aprender a identificar cada letra.

import cv2
import os
import numpy as np
import pickle
from imutils import paths
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from helpers import resize_to_fit

dados = []  # São os dados dentro da pasta que nesse caso é a imagem.
rotulos = []  # São as letras das pastas
pasta_base_imagens = "base_letras"
# O paths olha dentro das pastas e lista, ex: na pasta A ele olha o que tem dentro e classifica com \\A\\
imagens = paths.list_images(pasta_base_imagens)

for arquivo in imagens:
    # Separador dos caminhos - os.path.sep - caminho é assim: ['base_letras', 'A', "telanova1150003.png"]
    # O [-2] é para pegar a pasta e o arquivo, se tivesse 2 pasta e o arquivo colocaria -3.
    rotulo = arquivo.split(os.path.sep)[-2]
    imagem = cv2.imread(arquivo)
    # converto a imagem para a escala de cinza, (aqui eu já tenho 2 dimensões).
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Trata a imagem para ficar em 20x20 píxel devido à biblioteca usada.
    imagem = resize_to_fit(imagem, 20, 20)

    # Adicionar uma dimensão para o Keras ler a imagem
    # (dependendo do método preciso adicionar mais de uma dimensão).
    imagem = np.expand_dims(imagem, axis=2)

    # adicionar ás listas de dados e rótulos.
    rotulos.append(rotulo)
    dados.append(imagem)

dados = np.array(dados, dtype="float") / 255
rotulos = np.array(rotulos)

# Separação em dados de treino (75%) e dados de teste (25%).
# X é os dados: informações que me ajudam a chegar na resposta / Y são os rótulos: respostas
# O test_size é porcentagem de teste, random_state é para padronizar a forma que os dados vão ser separados.
(X_train, X_test, Y_train, Y_test) = train_test_split(dados, rotulos, test_size=0.25, random_state=0)

# Converter com one-hot encoding nos rótulos para que as letras fiquem como número
# e a "inteligencia artificial" identifique.

lb = LabelBinarizer().fit(Y_train)
Y_train = lb.transform(Y_train)
Y_test = lb.transform(Y_test)

# Salvando o tratamento feito acima de labelbinarizer em um arquivo com pickle.
with open('rotulos_modelo.dat', 'wb') as arquivo_pickle:
    pickle.dump(lb, arquivo_pickle)

# Passos de como criar e treinar uma inteligência artificial.

# Criar uma rede neural por sequências
modelo = Sequential()

# Criar as camadas da rede neural (ConvolutionalNetwork)
modelo.add(Conv2D(20, (5, 5), padding="same", input_shape=(20, 20, 1), activation="relu"))
modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# Criando a 2º camada
modelo.add(Conv2D(50, (5, 5), padding="same", activation="relu"))
modelo.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# Criando a 3° camada para conectar tudo (utilizando o Flatten e o Dense)
modelo.add(Flatten())
modelo.add(Dense(500, activation="relu"))

# Camada de saída com 26 neurônios (uma para cada letra do alfabeto)
modelo.add(Dense(26, activation="softmax"))  # 26 respostas

# Compilação do modelo
modelo.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

# Treinar a inteligência artificial
modelo.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=26, epochs=10, verbose=1)

# Treina e valida com o teste X e Y
# Verbose = progresso da nossa IA, para saber em qual velocidade está sendo feita os reconhecimentos.
# Epochs = quantas interações estão sendo feitas, no caso quero 10 interações para que a IA aprenda.

# Salvar o modelo em um arquivo
modelo.save("modelo_treinado.keras")

