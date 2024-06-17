from random import sample
import pygame
from escolhernums import SelecionarNumero

SUB_TABU_TAM = 3
TABU_TAM = SUB_TABU_TAM * SUB_TABU_TAM

#------------------------------------------------------------------------------------------------------#
#classe tabuleiro
class Tabuleiro:
#atributos
    def __init__(self, pygame, fonte):
        self.tamanho_celula = 50
        self.ajuste_x = 17
        self.ajuste_y = 7
        self.coordenadas_linha = self.criar_coordenadas_de_linha(self.tamanho_celula)
        self.tabuleiro = self.criar_tabu(SUB_TABU_TAM)
        self.remove_numeros(self.tabuleiro)
        self.coordenadas_celulas_ocupadas = self.celulas_nao_vazio()
        
        self.vence = False
        self.game_font = fonte
        self.seleciona = SelecionarNumero(pygame, self.game_font)
        
#metodos
    @staticmethod
    def criar_coordenadas_de_linha(tamanho_da_celula: int) -> list[list[tuple]]:
    #ajuda a definir aonde o pygame irá desenhar as linhas do nosso tabuleiro
        pontos = []
        for y in range(1,9):
            temp = []
            temp.append((0, y * tamanho_da_celula))
            # ^ aqui, basicamente, temos que desenhar começando do x = 0 até a borda da primeira celula, depois, desenhamos na borda da segunda célula, e etc., por isso que multiplicamos pela borda da celula ( para ir de célula em célula )
            temp.append((450, y * tamanho_da_celula))
            # ^ alem disso, queremos parar antes do final da tela, por isso adicionamos a parada no 900
            pontos.append(temp)
        for x in range (1, 10):
            temp = []
            temp.append((x * tamanho_da_celula, 0))
            temp.append((x * tamanho_da_celula, 450))
            pontos.append(temp)
        return pontos
    
    def __desenha_linhas(self, pg, tela) -> None:
        #desenha as linhas do tabuleiro
        for index, coordenadas in enumerate(self.coordenadas_linha): # o enumerate retorna tanto indíce quanto o valor
            if index == 2 or index == 5 or index == 10 or index == 13:
                pg.draw.line(tela, (148, 137, 121), coordenadas[0], coordenadas[1])
            else:
                pg.draw.line(tela, (60, 91, 111), coordenadas[0], coordenadas[1])
    
    def __desenha_numeros(self, tela) -> None:
        #desenha os numeros no tabuleiro
        for y in range(len(self.tabuleiro)): #vai de um a nove para pegar as linhas (o tamanho do tabuleiro inteiro é uma lista com 9 posições em que cada posição tem 9 listas dentro, por isso y vai até 9)
            for x in range(len(self.tabuleiro[y])): #vai de um a nove para pegar as colunas (o tamanho de cada tabuleiro[y] é uma lista com 9 posições, logo, 9, por isso x vai até 9)    
                if self.get_valor_coordenada(x,y) != 0:
                    if (y,x) in self.coordenadas_celulas_ocupadas:
                        texto_na_tela = self.game_font.render(str(self.get_valor_coordenada(x,y)), False, (223, 208, 184))
                    elif not self.disponivel(x, y, self.get_valor_coordenada(x,y)):
                        texto_na_tela = self.game_font.render(str(self.get_valor_coordenada(x,y)), False, (255, 0, 0))
                    elif self.disponivel(x,y, self.get_valor_coordenada(x,y)):
                        texto_na_tela = self.game_font.render(str(self.get_valor_coordenada(x,y)), False, (0, 255, 0))
                    tela.blit(texto_na_tela, 
                            (x * self.tamanho_celula + self.ajuste_x, y * self.tamanho_celula + self.ajuste_y))

                
    def desenhar(self, pg, tela) -> None:
        #junta os métodos desenha linhas e desenha numeros pra privar eles e deixar organizado já que né é bom saber organizar as coisas
        self.__desenha_linhas(pg, tela)
        self.__desenha_numeros(tela)
        self.seleciona.desenhar(pg, tela)

    @staticmethod
    def padrao(linha_num: int, col_num: int) -> int:
        return (SUB_TABU_TAM * (linha_num % SUB_TABU_TAM) + linha_num // SUB_TABU_TAM + col_num) % TABU_TAM
    
    @staticmethod
    def embaralho(samp: range) -> list: 
        #é uma máscara para o método sample
        #sample: sample(seq, k): retorna uma lista com k elementos aleatórios de uma sequência, sem repetições. No caso, seq será as possíveis escolhas de número
        return sample(samp, len(samp))
    
    def criar_tabu(self, sub_tabu: int) -> list[list]:
        #cria um tabuleiro aleatorio 
        linha_base = range(sub_tabu)
        linhas = [g * sub_tabu + r for g in self.embaralho(linha_base) for r in self.embaralho(linha_base)]
        colunas = [g * sub_tabu + c for g in self.embaralho(linha_base) for c in self.embaralho(linha_base)]
        numeros = self.embaralho(range(1, sub_tabu * sub_tabu + 1))
        return [[numeros[self.padrao(r,c)] for c in colunas] for r in linhas]

    @staticmethod
    def remove_numeros(tabuleiro: list[list]) -> None:
        #Aleatoriamente muda números do tabuleiro para zero com o intuito de criar o sudoku final
        numero_de_celulas = TABU_TAM * TABU_TAM
        celulas_vazias = numero_de_celulas*3 // 7 # ( o numero que divide numero de celulas vezes 3 é, por padrão, 7 ) 7 é um jogo ok, para jogos mais fáceis aumente o sete
        for i in sample(range(numero_de_celulas), celulas_vazias): # escolhemos dentre as 81 (numero de celulas) células, uma sequência de quantidade predefinida (celulas_vazias) para serem vazias
             tabuleiro[i // TABU_TAM][i % TABU_TAM] = 0 # i // tabu_tam é dado pelo fato de que a posição y da celula 
                            #removida é a parte inteira da divisão por 9 ( temos 9 linhas, cada linha tem 9 elementos, 
                            # vamos somando de nove em nove, se der exato é o primeiro elemento da lista, 
                            # se passar é um dos elementos da lista que não o primeiro, daí que o resto dá a posição x 
                            # ( coluna ) da célula, por isso fazemos i % tabu_tam ) 
                            
    def get_valor_coordenada(self, x: int, y: int) -> int:
        # retorna o valor de uma celula do tabuleiro
        return self.tabuleiro[y][x] # lembrando que y é linha x é coluna
    
    def atualiza_celula(self, x: int, y: int, valor: int) -> None:
        #atualiza o valor de uma celula na coordenada x,y
        self.tabuleiro[y][x] = valor
    
    def celulas_nao_vazio(self) -> list[tuple]:
        # salva os espaços que ja estão preenchidos
        preenchido = []
        for y in range(len(self.tabuleiro)):
            for x in range(len(self.tabuleiro[y])):
                if self.get_valor_coordenada(x,y) != 0:
                    preenchido.append((y, x))
        return preenchido
    
    def is_celula_ocupada(self, x: int, y: int) -> bool:
        #checa se uma celula esta ocupada
        for coords_ocupadas in self.coordenadas_celulas_ocupadas:
            if coords_ocupadas[0] == y and coords_ocupadas[1] == x:
                return True
        return False
    
    def get_mouse_click(self, x: int, y: int) -> None:
        #pega o mouse click
        if x <= 450:
            tabuleiro_x = x // 50
            tabuleiro_y = y // 50 # cada celula tem tamanho 50, logo, a posição x,y será valores por 50
            if not self.is_celula_ocupada(tabuleiro_x, tabuleiro_y):
                self.atualiza_celula(tabuleiro_x, tabuleiro_y, self.seleciona.numero_selecionado)
        self.seleciona.click_botao(x,y)
        if self.checa_vitoria():
            print("Vitoria!")
            self.vence = True

    def disponivel(self, coluna: int, linha: int, num: int) -> bool:
        for col in range(9):
            if col != coluna and self.tabuleiro[linha][col] == num:
                return False
             
        for lin in range(9):
            if lin != linha and self.tabuleiro[lin][coluna] == num:
                return False
 
 
        linhaInicial = linha - linha % 3
        colunaInicial = coluna - coluna % 3
        for i in range(3):
            for j in range(3):
                if i + linhaInicial != linha and j + colunaInicial != coluna and self.tabuleiro[i + linhaInicial][j + colunaInicial] == num:
                    return False
        return True

    def checa_vitoria(self) -> bool| None:
        for y in range(len(self.tabuleiro)):
            for x in range(len(self.tabuleiro[y])):
                if self.tabuleiro[y][x] == 0:
                    return False
                if self.tabuleiro[y][x] > 0:
                    if self.disponivel(x, y, self.get_valor_coordenada(x,y)):
                        pass
                    else:
                        return False
        self.vence = True
        
        
    def mostra(self):
        #mostra o tabuleiro
        for celulas in self.tabuleiro:
            print(celulas)
            
            
if __name__ == "__main__":
    pygame.font.init()
    game_font = pygame.font.SysFont("arialblack", 25)
    tabuleiro = Tabuleiro(pygame, game_font)
    print(len(tabuleiro.tabuleiro))
    print(len(tabuleiro.tabuleiro[8]))
    tabuleiro.mostra()
    print(tabuleiro.disponivel(1,2,3))