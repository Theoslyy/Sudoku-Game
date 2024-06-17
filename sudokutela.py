import pygame
import os
from griddosudoku import Tabuleiro


pygame.init()
pygame.font.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (0, 100) 
tela = pygame.display.set_mode((600, 450))
pygame.display.set_caption("Sudoku")
cor_de_fundo = (21, 52, 72)

game_font = pygame.font.SysFont("arialblack", 25)
game_font2 = pygame.font.SysFont("arialblack", 12)

tabuleiro = Tabuleiro(pygame, game_font)
running = True


while running:
    
    #checa inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not tabuleiro.vence:
            if pygame.mouse.get_pressed()[0]: #checa o botão esquerdo do mouse
                posicao = pygame.mouse.get_pos()
                tabuleiro.get_mouse_click(posicao[0], posicao[1])
                tabuleiro.checa_vitoria
                
    #colore
    tela.fill(cor_de_fundo)

    #desenha o tabuleiro
    tabuleiro.desenhar(pygame, tela)
    
    if tabuleiro.vence: 
        tela_vitoria = game_font.render("Vitória!", False, (0,255,0))
        tela.blit(tela_vitoria, (475, 325))

        tela_espaco = game_font2.render("Espaço para reiniciar", False, (0,255,200))
        tela.blit(tela_espaco, (460, 375))

    #atualiza
    pygame.display.update()
