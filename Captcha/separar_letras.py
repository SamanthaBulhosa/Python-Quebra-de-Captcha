# SEPARAR LETRAS
import cv2
import os
import glob


arquivos = glob.glob('tratado/*')
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
    if len(regiao_letras) != 5:  # Se o tamanho(len) da região(imagem) das letras_separadas for diferente de 5 (no captcha de cada imagem tem 5 letras_separadas) faça:
        continue  # Ele pula para o próximo item(imagem) do for. (obs: ele não encerra o for, mas sim pula para o próximo item que é a imagem)

    # Desenhar os contornos e separar as letras_separadas em arquivos individuais.
    imagem_final = cv2.merge([imagem] * 3)

    i = 0
    for retangulo in regiao_letras:  # A parti desse ponto só ladeira abaixo para entender esse trem... :(
        x, y, largura, altura = retangulo
        imagem_letra = imagem[y-2:y+altura+2, x-2:x+largura+2]  # esse número 2 é para dar 2 píxel de espaço para não ficar grudado
        i += 1
        nome_arquivo = os.path.basename(arquivo).replace('.png', f'letra{i}.png')  # nome original do arquivo /
        # O replace eu estou trocando o nome a onde tem .png na pasta original vai passar a ser letra.png / o {i} é de índice.
        cv2.imwrite(f'letras/{nome_arquivo}', imagem_letra)  # local / nome do arquivo / qual arquivo vou salvar
        cv2.rectangle(imagem_final, (x-2, y-2), (x+largura+2, y+altura+2), (153, 50, 204), 1)  # Criar traçar um retângulo verde em volta das letras_separadas.

    nome_arquivo = os.path.basename(arquivo)
    cv2.imwrite(f"identificado/{nome_arquivo}", imagem_final)
    # Retângulo      |rectangle
    # imagem_final   |imagem tratada que vai para pasta 'letra' do código acima.
    # ponto_inicial  |(x-2, y-2)
    # ponto_final    |(x+largura+2, y+altura+2)
    # cor            |(153, 50, 204) coloquei a cor roxa
    # espessura_linha|1 é a espessura do traço em volta de cada letra.
