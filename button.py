import pygame
#创建一个类
class Button():
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width * scale),int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.is_clicked = False

    def draw(self,surface):
        action = False
        pygame.draw.rect(surface,(0,0,0),(self.rect.x,self.rect.y,self.image.get_width(),self.image.get_height()))
        bk = pygame.draw.rect(surface,(255,255,255),(self.rect.x,self.rect.y, self.image.get_width(),self.image.get_height()),3)
        # 获取鼠标的位置
        pos = pygame.mouse.get_pos()
        # 点击事件
        if bk.collidepoint(pos):
            # pygame.mouse.set_cursor(*pygame.cursors.hand)
            # action = True
            if pygame.mouse.get_pressed()[0] == 1 and self.is_clicked == False:
                self.is_clicked = True
                action = True
                pygame.draw.rect(surface, (0, 0, 255),
                                 (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()),3)
        if pygame.mouse.get_pressed()[0] == 0:
            self.is_clicked = False
        #     action = True
        # else:
        #     pygame.mouse.set_cursor(*pygame.cursors.arrow)
        #     self.is_clicked = False
        surface.blit(self.image,(self.rect.x,self.rect.y))
        return action
