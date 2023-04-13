from board import BoardSudoku
import pygame
import os

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
DARKBROWN = (77, 54, 32)

TELA_LARGURA = 1280
TELA_ALTURA = 720

pygame.init()
screen = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))

img_background = pygame.image.load(os.path.join('imgs', 'background.png'))

CELL_SIZE = 60

# Desenhando o tabuleiro do SUDOKU

# -> variáveis para as dimensões das telas
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# -> Definindo as constantes para a grade
SQUARE_SIZE = 65
LINE_WIDTH = 5
NUM_SQUARES = 9

# -> Variáveis para calcular a posição da grade no centro da tela
grid_width = NUM_SQUARES * SQUARE_SIZE
grid_height = NUM_SQUARES * SQUARE_SIZE
grid_x = (SCREEN_WIDTH - grid_width) // 2
grid_y = (SCREEN_HEIGHT - grid_height) // 2


def show_board(board, tela, cursor_pos):
    tela.blit(img_background, (0, 0))

    square_positions = [(i * SQUARE_SIZE + grid_x, j * SQUARE_SIZE + grid_y) for i in range(NUM_SQUARES) for j in range(
        NUM_SQUARES)]

    for i, position in enumerate(square_positions):
        pygame.draw.rect(tela, DARKBROWN, (position[0], position[1], SQUARE_SIZE, SQUARE_SIZE), LINE_WIDTH)
    # Desenha linhas grossas para dividir o tabuleiro em subgrids
    for k in range(3):
        pygame.draw.line(tela, BLACK, (grid_x + k * 3 * SQUARE_SIZE, grid_y),
                         (grid_x + k * 3 * SQUARE_SIZE, grid_y + grid_height), LINE_WIDTH)
        pygame.draw.line(tela, BLACK, (grid_x, grid_y + k * 3 * SQUARE_SIZE),
                         (grid_x + grid_width, grid_y + k * 3 * SQUARE_SIZE), LINE_WIDTH)

    # Desenha as linhas de baixo
    pygame.draw.line(tela, BLACK, (grid_x, grid_y + grid_height), (grid_x + grid_width, grid_y + grid_height),
                     LINE_WIDTH)

    # Desenha as linhas da direita
    pygame.draw.line(tela, BLACK, (grid_x + grid_width, grid_y), (grid_x + grid_width, grid_y + grid_height),
                     LINE_WIDTH)

    font = pygame.font.Font(None, 60)
    for j in range(NUM_SQUARES):
        for i in range(NUM_SQUARES):
            if board.get_status(i, j) != 0:
                if board.vetor.__contains__((i, j)):
                    number = font.render(str(board.get_status(i, j)), True, RED)
                else:
                    number = font.render(str(board.get_status(i, j)), True, BLACK)
                number_rect = number.get_rect(
                    center=(j * SQUARE_SIZE + SQUARE_SIZE // 2 + grid_x, i * SQUARE_SIZE + SQUARE_SIZE // 2 + grid_y))
                if cursor_pos == (i, j):
                    pygame.draw.rect(tela, GREEN, number_rect, 2)
                    number = font.render(str(board.get_status(i, j)), True, GREEN)
                tela.blit(number, number_rect)


def jogo(nome_arq, tela):
    tabuleiro = BoardSudoku()
    tabuleiro.upload_arq(nome_arq)
    controller = True

    # Definindo um objeto Rect para cada retângulo do jogo
    rects = []
    for i in range(9):
        for j in range(9):
            rect = pygame.Rect(i * SQUARE_SIZE + grid_x, j * SQUARE_SIZE + grid_y, SQUARE_SIZE, SQUARE_SIZE)
            rects.append(rect)

    cursor_pos = None

    while controller:
        show_board(tabuleiro, tela, cursor_pos)
        # Botão para verificar se a resposta esta correta
        font2 = pygame.font.Font(None, 24)

        text2 = font2.render("Check", True, BLACK)

        button_verificar = pygame.Rect(TELA_LARGURA - 40 - 100, 660, 100, 50)

        # Desenhando o botão na tela
        pygame.draw.rect(tela, WHITE, button_verificar)

        tela.blit(text2, (TELA_LARGURA - 40 - 100 + 25, 680))

        # Botão para voltar a home
        text3 = font2.render("Back", True, BLACK)

        button = pygame.Rect(40, 660, 85, 50)

        # Desenhando o botão na tela
        pygame.draw.rect(tela, WHITE, button)

        tela.blit(text3, (60, 680))

        pygame.display.update()
        for action in pygame.event.get():
            if action.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif action.type == pygame.KEYDOWN:
                if action.key == pygame.K_ESCAPE:
                    controller = False
            elif action.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos2 = pygame.mouse.get_pos()
                cursor_pos = (mouse_pos2[1] - grid_y) // SQUARE_SIZE, (mouse_pos2[0] - grid_x) // SQUARE_SIZE
                if button.collidepoint(mouse_pos2):
                    controller = False
                elif button_verificar.collidepoint(mouse_pos2):
                    if not tabuleiro.check():
                        rodando = True
                        while rodando:

                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                elif e.type == pygame.KEYDOWN:
                                    if e.key == pygame.K_ESCAPE:
                                        rodando = False
                                elif e.type == pygame.MOUSEBUTTONDOWN:
                                    rodando = False

                            font = pygame.font.Font(None, 100)
                            header_surface = font.render("Errado!", True, BLACK)

                            # Definindo a posição central do texto
                            header_x = (1280 - header_surface.get_width()) // 2
                            header_y = TELA_ALTURA / 2

                            # Obtendo as dimensões da superfície do texto
                            text_rect = header_surface.get_rect()

                            # Criando um retângulo centrado na tela que tem as mesmas dimensões da superfície do texto
                            rect_x = header_x - 10  # subtraindo 10 para criar um espaço entre o texto e o retângulo
                            rect_y = header_y - 10
                            rect_width = text_rect.width + 20  # adicionando 20 para criar espaço em todos os lados do texto
                            rect_height = text_rect.height + 20
                            rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

                            # Desenhando o retângulo branco em volta do texto
                            pygame.draw.rect(screen, WHITE, rect, 1000)

                            # Desenhando a superfície do texto na tela
                            screen.blit(header_surface, (header_x, header_y))

                            pygame.display.update()

                        print("ERRADO")
                        # Imprimir uma mensagem
                    else:
                        rodando = True
                        while rodando:

                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                elif e.type == pygame.KEYDOWN:
                                    if e.key == pygame.K_ESCAPE:
                                        rodando = False
                                elif e.type == pygame.MOUSEBUTTONDOWN:
                                    rodando = False

                            font = pygame.font.Font(None, 100)

                            header_surface = font.render("Parabéns!", True, BLACK)

                            # Defininfo a posição
                            header_x = (1280 - header_surface.get_width()) // 2
                            header_y = TELA_ALTURA / 2

                            # Desenhar o retângulo branco
                            text_rect = header_surface.get_rect()
                            pygame.draw.rect(screen, WHITE, text_rect, 10)

                            # Desenhar a superfície do texto em cima do retângulo
                            screen.blit(header_surface, (header_x, header_y))

                            # Desenhando a superfície na tela
                            screen.blit(header_surface, (header_x, header_y))

                            pygame.display.update()

                        print("ACERTOU")
                        # Imprimir uma mensagem
                else:
                    show_board(tabuleiro, tela, cursor_pos)

                    # Desenhando o botão na tela
                    pygame.draw.rect(tela, WHITE, button)

                    tela.blit(text3, (60, 680))
                    pygame.display.update()
                    for o in range(9):
                        for p in range(9):
                            if rects[o * 9 + p].collidepoint(action.pos):
                                # Quadrado clicado
                                x = p
                                y = o
                                # Aqui você pode abrir uma caixa de diálogo para o usuário inserir o número
                                # e inserir na posição (x, y) com o comando abaixo:
                                # board.insert(x, y, numero_inserido)
                                loop = True
                                while loop:
                                    for ac in pygame.event.get():
                                        if ac.type == pygame.QUIT:
                                            pygame.quit()
                                            exit()
                                        elif ac.type == pygame.KEYDOWN:
                                            if ac.key == pygame.K_ESCAPE:
                                                loop = False
                                            elif ac.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                                            pygame.K_5,
                                                            pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
                                                            pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4,
                                                            pygame.K_KP5,
                                                            pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9]:
                                                numero_inserido = int(ac.unicode)
                                                if tabuleiro.insert(x, y, numero_inserido) == 1:
                                                    # Número inserido com sucesso, atualiza a tela
                                                    show_board(tabuleiro, tela, cursor_pos)
                                                    pygame.display.update()
                                                    loop = False
                                            elif ac.key == pygame.K_BACKSPACE:
                                                tabuleiro.erase(x, y)
                                                show_board(tabuleiro, tela, cursor_pos)
                                                pygame.display.update()
                                                loop = False
                                            else:
                                                print("Valor invalido")


def main():
    # Iniciando o looping
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Definindo o botão para jogar

        # -> Defininfo a posição do botão
        button_x = (TELA_LARGURA / 2) - (200 / 2)
        button_y = (TELA_ALTURA / 2) - (50 / 2)

        # -> Definindo o retângulo do botão
        button_rect = pygame.Rect(button_x, button_y, 200, 50)

        # -> Criando o texto do botão
        font = pygame.font.Font(None, 36)
        text = font.render("Jogar", True, BLACK)

        # Defininfo o botão para ver respostas

        # -> Definindo a posição do botão
        button_x1 = button_x
        button_y1 = (1000 / 2) - (50 / 2)

        # -> Defininfo o retãngulo do botão
        button_rect_resp = pygame.Rect(button_x1, button_y1, 200, 50)

        # -> Criando o texto do botão
        text1 = font.render("Resposta", True, BLACK)

        # Desenando o plano de fundo
        screen.blit(img_background, (0, 0))

        # Desenhando a tela inicial

        font = pygame.font.Font(None, 100)

        header_surface = font.render("SUDOKU", True, BLACK)

        # Defininfo a posição
        header_x = (1280 - header_surface.get_width()) // 2
        header_y = 60

        pygame.draw.rect(screen, WHITE, (button_x - 52, button_y - 52, 304, 304))

        pygame.draw.rect(screen, BLACK, (button_x - 50, button_y - 50, 300, 300))

        # Desenhando a superfície na tela
        screen.blit(header_surface, (header_x, header_y))

        # Desenhando o botão na tela
        pygame.draw.rect(screen, WHITE, button_rect)
        screen.blit(text, (button_x + 60, button_y + 10))

        # Desenhando o botão na tela
        pygame.draw.rect(screen, WHITE, button_rect_resp)
        screen.blit(text1, (button_x1 + 40, button_y1 + 10))

        # Verificando se o botão do mouse foi pressionado
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                # interface para escolher qual tabuleiro quer jogar
                run = True
                while run:

                    font = pygame.font.Font(None, 100)

                    header_surface = font.render("Board", True, BLACK)

                    # Definindo a posição
                    header_x = (1280 - header_surface.get_width()) // 2
                    header_y = 60

                    # Desenando o plano de fundo
                    screen.blit(img_background, (0, 0))

                    # Desenhando a superfície na tela
                    screen.blit(header_surface, (header_x, header_y))

                    # Definindo a largura e altura dos botões
                    BUTTON_WIDTH = 125
                    BUTTON_HEIGHT = 50

                    # Definindo o número de colunas e linhas de botões
                    NUM_COLUMNS = 5
                    NUM_ROWS = 2

                    # Definindo o espaçamento entre os botões
                    SPACING_X = (TELA_LARGURA - (NUM_COLUMNS * BUTTON_WIDTH)) / (NUM_COLUMNS + 1)
                    SPACING_Y = (TELA_ALTURA - (NUM_ROWS * BUTTON_HEIGHT)) / (NUM_ROWS + 1)

                    # Cria uma lista para armazenar os retângulos dos botões
                    button_rects1 = []

                    # Loop para criar os botões
                    for i in range(NUM_COLUMNS):
                        for j in range(NUM_ROWS):
                            # Calculando a posição x e y do botão
                            button_x = SPACING_X * (i + 1) + BUTTON_WIDTH * i
                            button_y = SPACING_Y * (j + 1) + BUTTON_HEIGHT * j

                            # Criando o retângulo do botão
                            button_rect1 = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

                            # Adicionando o retângulo à lista de retângulos dos botões
                            button_rects1.append(button_rect1)

                            # Criando o texto do botão
                            font = pygame.font.Font(None, 36)
                            text = font.render("Board {}".format(i * NUM_ROWS + j + 1), True, BLACK)

                            # Desenhando o botão na tela
                            pygame.draw.rect(screen, WHITE, button_rect1)
                            screen.blit(text, (button_x + 10, button_y + 15))

                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif evento.type == pygame.KEYDOWN:
                            if evento.key == pygame.K_ESCAPE:
                                run = False
                        elif evento.type == pygame.MOUSEBUTTONDOWN:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            # Verificando em qual botão foi clicado
                            for i in range(NUM_COLUMNS * NUM_ROWS):
                                if button_rects1[i].collidepoint(mouse_x, mouse_y):
                                    # O clique do mouse colidiu com o botão i
                                    print("Clicou no botão {}".format(i + 1))
                                    jogo(f"puzzle_board/board{i + 1}.txt", screen)
                                    pygame.display.update()
                    pygame.display.update()

            elif button_rect_resp.collidepoint(mouse_pos):
                # interface para os resultados
                run = True
                while run:

                    font = pygame.font.Font(None, 100)

                    header_surface = font.render("Resposta", True, BLACK)

                    # Definindo a posição
                    header_x = (1280 - header_surface.get_width()) // 2
                    header_y = 60

                    # Desenando o plano de fundo
                    screen.blit(img_background, (0, 0))

                    # Desenhando a superfície na tela
                    screen.blit(header_surface, (header_x, header_y))

                    # Definindo a largura e altura dos botões
                    BUTTON_WIDTH = 125
                    BUTTON_HEIGHT = 50

                    # Definindo o número de colunas e linhas de botões
                    NUM_COLUMNS = 5
                    NUM_ROWS = 2

                    # Definindo o espaçamento entre os botões
                    SPACING_X = (TELA_LARGURA - (NUM_COLUMNS * BUTTON_WIDTH)) / (NUM_COLUMNS + 1)
                    SPACING_Y = (TELA_ALTURA - (NUM_ROWS * BUTTON_HEIGHT)) / (NUM_ROWS + 1)

                    # Cria uma lista para armazenar os retângulos dos botões
                    button_rects = []

                    # Loop para criar os botões
                    for i in range(NUM_COLUMNS):
                        for j in range(NUM_ROWS):
                            # Calculando a posição x e y do botão
                            button_x = SPACING_X * (i + 1) + BUTTON_WIDTH * i
                            button_y = SPACING_Y * (j + 1) + BUTTON_HEIGHT * j

                            # Criando o retângulo do botão
                            button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

                            # Adicionando o retângulo à lista de retângulos dos botões
                            button_rects.append(button_rect)

                            # Criando o texto do botão
                            font = pygame.font.Font(None, 36)
                            text = font.render("Board {}".format(i * NUM_ROWS + j + 1), True, BLACK)

                            # Desenhando o botão na tela
                            pygame.draw.rect(screen, WHITE, button_rect)
                            screen.blit(text, (button_x + 10, button_y + 15))

                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif evento.type == pygame.KEYDOWN:
                            if evento.key == pygame.K_ESCAPE:
                                run = False
                        elif evento.type == pygame.MOUSEBUTTONDOWN:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            # Verificando em qual botão foi clicado
                            for i in range(NUM_COLUMNS * NUM_ROWS):
                                if button_rects[i].collidepoint(mouse_x, mouse_y):
                                    # O clique do mouse colidiu com o botão i
                                    running = True
                                    while running:
                                        for evet in pygame.event.get():
                                            if evet.type == pygame.QUIT:
                                                pygame.quit()
                                                exit()
                                            elif evet.type == pygame.MOUSEBUTTONDOWN:
                                                continue
                                            elif evet.type == pygame.KEYDOWN:
                                                if evet.key == pygame.K_ESCAPE:
                                                    running = False

                                        font = pygame.font.Font(None, 100)

                                        header_surface = font.render(f"Board {i + 1}", True, BLACK)

                                        # Defininfo a posição
                                        header_x = (1280 - header_surface.get_width()) // 2
                                        header_y = 60

                                        # Desenando o plano de fundo
                                        screen.blit(img_background, (0, 0))

                                        # Desenhando a superfície na tela
                                        screen.blit(header_surface, (header_x, header_y))

                                        # Abrindo arquivo com as repostas
                                        board = BoardSudoku()
                                        board.upload_answer(f'puzzle_board_answer/board{i + 1}_answer.txt')
                                        cursor = None
                                        show_board(board, screen, cursor)

                                        # Atualizando a tela
                                        pygame.display.update()

                    # Atualizando a tela
                    pygame.display.update()

        # Atualizando a tela
        pygame.display.update()


if __name__ == '__main__':
    main()
