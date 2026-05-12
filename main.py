from pygame import *
import sys
init()


def valida_email(email):
    return email[-8:] == '@puc.com'


def possuimaiuscula(palavra):
    for letra in palavra:
        if 'A' <= letra <= 'Z':
            return True
    return False


def possuiminuscula(palavra):
    for letra in palavra:
        if 'a' <= letra <= 'z':
            return True
    return False


def possuinumero(palavra):
    for caracter in palavra:
        if '0' <= caracter <= '9':
            return True
    return False


def valida_senha(senha):
    chek_tamanho = len(senha) >= 8
    chek_maiuscula = possuimaiuscula(senha)
    chek_minuscula = possuiminuscula(senha)
    chek_numero = possuinumero(senha)
    return chek_tamanho and chek_maiuscula and chek_minuscula and chek_numero


def criptografa_senha(senha):
    senha_cripto = ""
    for char in senha:
        if char.isdigit():
            ref = ord('0')
            ascii_char = ord(char)
            pos_alpha = ascii_char - ref
            pos_cesar = pos_alpha + 3
            pos_cesar = pos_cesar % 10
            letra_cesar = chr(ref + pos_cesar)
            senha_cripto += letra_cesar
        elif 'A' <= char <= 'Z':
            ref = ord('A')
            ascii_char = ord(char)
            pos_alpha = ascii_char - ref
            pos_cesar = pos_alpha + 3
            pos_cesar = pos_cesar % 26
            letra_cesar = chr(ref + pos_cesar)
            senha_cripto += letra_cesar
        elif 'a' <= char <= 'z':
            ref = ord('a')
            ascii_char = ord(char)
            pos_alpha = ascii_char - ref
            pos_cesar = pos_alpha + 3
            pos_cesar = pos_cesar % 26
            letra_cesar = chr(ref + pos_cesar)
            senha_cripto += letra_cesar
        else:
            senha_cripto += char
    return senha_cripto

def main():
    mixer.init()
    
    window = display.set_mode((1280, 720))
    display.set_caption("Casinha - Regular Show")
    running = True
    clock = time.Clock()

    # Carregamento de Recursos
    rigbymordecai_img = image.load('rigbymordecai.png')
    rigbymordecai_img = transform.scale(rigbymordecai_img, (225, 200))
    rigbymordecai_font = font.Font('IceCreamPartySolid.ttf', 50)

    som_manha = mixer.Sound('aberturaapenasumshow.mp3')
    som_tarde = mixer.Sound('ISSOÉTRAPmixtape.mp3')
    som_noite = mixer.Sound('noitedarapaziada.mp3')

    # Variáveis Iniciais
    sol_x = 140
    sol_y = 100
    nuvem_x = 850
    velocidade_nuvem = 3

    manha = (209, 245, 255)
    tarde = (219, 112, 104)
    noite = (11, 7, 49)

    while running:
        clock.tick(60)
        
        # Captura de eventos para fechar e sons do mouse
        for ev in event.get():
            if ev.type == QUIT:
                quit()
                sys.exit
            
            if ev.type == MOUSEMOTION:
                sol_x, sol_y = ev.pos

            if ev.type == MOUSEBUTTONDOWN:
                if sol_x < 520:
                    som_manha.play()
                elif sol_x < 760:
                    som_tarde.play()
                else:
                    som_noite.play()

        # Movimentação da Nuvem
        nuvem_x += velocidade_nuvem
        if nuvem_x <= 45 or nuvem_x >= 1025:
            velocidade_nuvem = -velocidade_nuvem

        # Controles de teclado
        dt = clock.get_time() / 1000
        keys = key.get_pressed()

        if keys[K_d] or keys[K_RIGHT]:
            sol_x += 300 * dt
        elif keys[K_a] or keys[K_LEFT]:
            sol_x -= 300 * dt

        # Limites do Sol
        if sol_x <= 110: sol_x = 110
        elif sol_x >= 1170: sol_x = 1170

        # Lógica de cores do céu (Degradê)
        progresso = sol_x / 1280
        if progresso < 0.5:
            fator = progresso * 2
            r = manha[0] + (tarde[0] - manha[0]) * fator
            g = manha[1] + (tarde[1] - manha[1]) * fator
            b = manha[2] + (tarde[2] - manha[2]) * fator
        else:
            fator = (progresso - 0.5) * 2
            r = tarde[0] + (noite[0] - tarde[0]) * fator
            g = tarde[1] + (noite[1] - tarde[1]) * fator
            b = tarde[2] + (noite[2] - tarde[2]) * fator

        cor_fundo = (int(r), int(g), int(b))
        window.fill(cor_fundo)

        # DESENHOS
        draw.rect(window, (159, 212, 101), (0, 600, 1280, 350)) # Grama
        draw.rect(window, (168, 222, 202), (350, 350, 235, 250)) # Casa
        draw.circle(window, (255, 247, 185), (int(sol_x), 100), 55) # Sol
        draw.polygon(window, (118, 139, 126), ((350, 350), (468, 150), (585, 350))) # Telhado

        draw.rect(window, (170, 131, 140), (830, 450, 40, 150)) # Tronco
        draw.circle(window, (156, 204, 86), (850, 400), 100) # Folhas

        # Nuvens
        draw.circle(window, (255, 255, 255), (nuvem_x, 100), 50)
        draw.circle(window, (255, 255, 255), (nuvem_x + 70, 100), 60)
        draw.circle(window, (255, 255, 255), (nuvem_x + 140, 100), 55)
        draw.circle(window, (255, 255, 255), (nuvem_x + 210, 100), 50)

        # Raios de Sol
        draw.line(window, (255, 247, 185), (sol_x, 45), (sol_x, -10), 5)
        draw.line(window, (255, 247, 185), (sol_x, 155), (sol_x, 210), 5)
        draw.line(window, (255, 247, 185), (sol_x - 55, 100), (sol_x - 110, 100), 5)
        draw.line(window, (255, 247, 185), (sol_x + 55, 100), (sol_x + 110, 100), 5)

        # Detalhes da Casa
        draw.rect(window, (255, 255, 255), (480, 460, 80, 140)) # Porta
        draw.circle(window, (184, 191, 174), (490, 535), 5) # Maçaneta
        draw.rect(window, (171, 186, 179), (375, 430, 80, 100)) # Janela

        # Blit de Imagens e Texto
        window.blit(rigbymordecai_img, (50, 410))
        rigbymordecai_text = rigbymordecai_font.render('REGULAR SHOW', True, (0,0,0))
        window.blit(rigbymordecai_text, (500, 0))

        display.update()
        
# CORES
window = display.set_mode((1280, 720))
branco = (255, 255, 255)
preto = (0, 0, 0)
cinza = (180, 180, 180)
azul = (109, 109, 235)
fonte = font.SysFont("Arial", 30)

# INPUTS
tela_atual = "login"
mensagem = ""

texto_email = ""
texto_senha = ""
campo_ativo = None

placeholder = 'Digite seu email aqui'
placeholder1 = 'Digite sua senha aqui (8 caracteres)'

input_rect = Rect(393, 303, 454, 40)
input_rect1 = Rect(393, 403, 454, 40)
bot_rec = Rect(510, 500, 200, 54)

def desenhar():
    window.fill(branco)

    titulo = fonte.render('Faça seu login', True, preto)
    window.blit(titulo, (530, 200))

    # CAIXAS
    draw.rect(window, preto, input_rect, 2)
    draw.rect(window, preto, input_rect1, 2)
    draw.rect(window, azul, bot_rec)
    # EMAIL
    if texto_email == "" and campo_ativo != "email":
        texto_surface = fonte.render(placeholder, True, cinza)
    else:
        texto_surface = fonte.render(texto_email, True, preto)

    window.blit(texto_surface, (input_rect.x + 10, input_rect.y + 5))

    # SENHA (com *)
    if texto_senha == "" and campo_ativo != "senha":
        texto_surface = fonte.render(placeholder1, True, cinza)
    else:
        senha_visivel = "*" * len(texto_senha)
        texto_surface = fonte.render(senha_visivel, True, preto)

    window.blit(texto_surface, (input_rect1.x + 10, input_rect1.y + 5))


    if tela_atual == "login":
        draw.rect(window, (0, 0, 0), bot_rec, 2)

        text_avancar = fonte.render('Avançar', True, branco)
        window.blit(text_avancar, (560, 508))
        if mensagem != "":
            msg_surface = fonte.render(mensagem, True, (255, 0, 0))
            window.blit(msg_surface, (450, 460))

    elif tela_atual == "menu":
        window.fill(branco)
        main()

running = True
while running:
      for ev in event.get():
        if ev.type == QUIT:
            quit()
            sys.exit()

        # CLIQUE
        if ev.type == MOUSEBUTTONDOWN:
            if input_rect.collidepoint(ev.pos):
                campo_ativo = "email"
            elif input_rect1.collidepoint(ev.pos):
                campo_ativo = "senha"
            elif bot_rec.collidepoint(ev.pos):
                if valida_email(texto_email) and valida_senha(texto_senha):
                    tela_atual = "menu"
                    mensagem = ""
                else:
                    mensagem = "Email ou senha inválidos"
            else:
                campo_ativo = None

        # DIGITAÇÃO
        if ev.type == KEYDOWN and campo_ativo:
            if campo_ativo == "email":
                if ev.key == K_BACKSPACE:
                    texto_email = texto_email[:-1]
                else:
                    texto_email += ev.unicode

            elif campo_ativo == "senha":
                if ev.key == K_BACKSPACE:
                    texto_senha = texto_senha[:-1]
                else:
                    texto_senha += ev.unicode

     
      desenhar()
      display.flip()

quit()

 
    