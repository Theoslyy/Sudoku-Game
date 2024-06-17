
class SelecionarNumero:
    def __init__(self, pygame, fonte):
        self.pygame = pygame

        self.numero_selecionado = 0
        self.botao_larg = 40 #largura do botao
        self.botao_alt = 40 # altura do botao
        self.botao_fonte = fonte
        self.cor_selecionado = (0,255, 0)
        self.cor_basico = (200,200,200)
        self.botao_posicoes = [(475, 25), (525, 25), (475, 75), (525, 75), 
                               (475, 125), (525, 125), (475, 175), (525, 175), (475, 225),(525, 225)]
        
    def desenhar(self, pygame, tela):
        for index, pos in enumerate(self.botao_posicoes):
            pygame.draw.rect(tela, self.cor_basico, [pos[0], pos[1], self.botao_larg, self.botao_alt], 
                                width=3, border_radius=10)
            if self.hover_botao(pos):
                 pygame.draw.rect(tela, self.cor_selecionado, [pos[0], pos[1], self.botao_larg, self.botao_alt], 
                                width=3, border_radius=10)
                 texto_numeros = self.botao_fonte.render(str(index), False, (0, 255, 0))
            else:
                 texto_numeros = self.botao_fonte.render(str(index), False, self.cor_basico)

            if self.numero_selecionado > 0: 
                if self.numero_selecionado == index:
                    pygame.draw.rect(tela, self.cor_selecionado, [pos[0], pos[1], self.botao_larg, self.botao_alt], 
                                width=3, border_radius=10)
                    texto_numeros = self.botao_fonte.render(str(index), False, self.cor_selecionado)
                    

            tela.blit(texto_numeros, (pos[0] + 13, pos[1]))

    def click_botao(self, mouse_x: int, mouse_y: int) -> None:
        for index, pos in enumerate(self.botao_posicoes):
            if self.esta_no_botao(mouse_x,mouse_y, pos):
                self.numero_selecionado = index
            
    def hover_botao(self, pos: tuple) -> bool|None:
        mouse_pos = self.pygame.mouse.get_pos()
        if self.esta_no_botao(mouse_pos[0], mouse_pos[1], pos):
            return True
        
    def esta_no_botao(self, mouse_x: int, mouse_y: int, pos: tuple) -> bool:
        if pos[0] < mouse_x < pos[0] + self.botao_larg: #checa se o mouse está entre o começo e o fim da largura do botao
            if pos[1] < mouse_y < pos[1] + self.botao_alt: #checa se o mouse esta entre o começo e o fim da altura do botao
                return True
        return False
