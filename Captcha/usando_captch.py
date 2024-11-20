# Escolha qualquer imagem de captcha para ser resolvido/quebrado.
# Coloque a imagem na pasta "resolver_captcha"
from resolver_captcha import quebrar_captcha

texto_captcha = quebrar_captcha()
print(f"Texto do CAPTCHA: {texto_captcha}")

# OBS: esse projeto tem uma margem de erro, podendo errar algumas letras,
# exemplo de 10 imagem de captcha 2 imagem pode conter letra errada como G com C.

'''
Crédito:
Canal do YouTube - Hashtag Programação
Professor - Lira
Projeto CAPTCHA
'''
