import pygame, sys
from pygame.locals import *

largura = 800
altura = 600

#classe do tiro
class tiro(pygame.sprite.Sprite):
    def __init__(self,posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.ImagemTiro =  pygame.image.load('imagens/tiro.png')#imagem
        self.audio_tiro = pygame.mixer.Sound('sons/laser.wav')#som

        #colocando o som e a posicao
        self.rect = self.ImagemTiro.get_rect()
        self.velocidadeTiro = 10
        self.rect.top = posy
        self.rect.left = posx

    def trajetoria(self):
        self.rect.top = self.rect.top - self.velocidadeTiro

    def colocar(self, superficie):
        superficie.blit(self.ImagemTiro, self.rect)

#classes dos inimigos       
class inimigo(pygame.sprite.Sprite):
    def __init__(self,posx, posy):
        pygame.sprite.Sprite.__init__(self)
        self.ImagemInimigo =  pygame.image.load('imagens/nave1.png') #imagens
        self.ImagemInimigo2 =  pygame.image.load('imagens/nave2.png')
        
        self.listaImagens = [self.ImagemInimigo, self.ImagemInimigo2] #lista de imagens
        self.posImagem = 0
        self.imagensInimigos = self.listaImagens[self.posImagem]
        
        self.rect = self.ImagemInimigo.get_rect()
        self.listaDisparo = []
        self.velocidadeTiro = 20
        self.rect.top = posy
        self.rect.left = posx

        self.configTempo = 1

    def comportamento(self, tempo):#funcao para trocar imagens
        if self.configTempo == tempo:
            self.posImagem += 1
            self.configTempo += 1
            if self.posImagem > len(self.listaImagens) - 1:
                self.posImagem = 0

    def colocar(self, superficie):
        self.imagensInimigos = self.listaImagens[self.posImagem]
        superficie.blit(self.ImagemInimigo, self.rect)

#classe da nave    
class nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.ImagemNave =  pygame.image.load('imagens/nave_vermelha.png')#imagem

        #posicao e atributo da nave
        self.rect = self.ImagemNave.get_rect()
        self.rect.centerx = largura/2
        self.rect.centery = altura - 60

        self.listaDisparo = []
        self.vida = True
        self.velocidade = 40
        
    #movimentacao
    def movimento(self):
        if self.vida == True:
            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right > 795:
                self.rect.left = 700

    #disparo
    def disparar(self,x,y):
        meuTiro = tiro(x - 7,y)
        self.listaDisparo.append(meuTiro)
        
    def colocar(self, superficie):
        superficie.blit(self.ImagemNave, self.rect)
    #movimentacao
    def movimentoDireita(self):
        self.rect.right += self.velocidade
        self.__movimento()

    def movimentoEsquerda(self):
        self.rect.left -= self.velocidade
        self.__movimento()

    def __movimento(self):
        if self.vida == True:
            if self.rect.left <= 0:
                self.rect.left = 0
            elif self.rect.right > 800:
                self.rect.left = 800

#classe principal(jogo)
def invasaoEspaco():
    pygame.init()

    tela = pygame.display.set_mode((largura,altura))#tamanho da janela
    pygame.display.set_caption("Invasão do Espaço")#titulo

    jogador = nave() #criando jogador
    imagemFundo = pygame.image.load('imagens/fundo.jpg')#imagem de fundo
    jogando = True #iniciando o jogador

    #ajuste do objetos
    tiroProjetil = tiro(largura / 2, altura - 60) 
    naveInimiga = inimigo(100,100)
    relogio = pygame.time.Clock()

    #enquanto a janela tiver ativa
    while True:
        #relogios pra contar o tempo
        relogio.tick(50)
        tempo = int(pygame.time.get_ticks()/1000)

        
        jogador.movimento()
        tiroProjetil.trajetoria()

        #eventos
        for evento in pygame.event.get():
            if evento.type == QUIT: #evento pra fechar janela
                pygame.quit()
                sys.exit()

            #eventos do teclado
            if evento.type == pygame.KEYDOWN:
                if evento.key == K_LEFT:
                    jogador.movimentoEsquerda()

                elif evento.key == K_RIGHT:
                    jogador.movimentoDireita()

                elif evento.key == K_SPACE:
                    x,y = jogador.rect.center
                    tiroProjetil.audio_tiro.play()
                    jogador.disparar(x,y)
                
        #colocando tudo na tela
        tela.blit(imagemFundo,(0,0))
        jogador.colocar(tela)
        naveInimiga.colocar(tela)
        naveInimiga.comportamento(tempo)
        #ajutando o array de tiros
        if len(jogador.listaDisparo) > 0:
            for x in jogador.listaDisparo:
                x.colocar(tela)
                x.trajetoria()
                if x.rect.top < -10:
                    jogador.listaDisparo.remove(x)
        #atualizando o jogo            
        pygame.display.update()

invasaoEspaco()#chamando a função do jogo
