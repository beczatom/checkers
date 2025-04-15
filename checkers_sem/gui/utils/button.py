import pygame

class Button:
    def __init__(self, screen, rect : pygame.Rect, text : str, background_color : tuple[int, int, int],
                 border_radius : int = 0):
        self.screen = screen
        self.rect = rect
        self.text = text
        self.color = background_color
        self.border_radius = border_radius

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=self.border_radius)
        text = pygame.font.SysFont(None, 24).render(self.text, True, (255,255,255))
        text_rect = text.get_rect(center = self.rect.center)
        self.screen.blit(text, text_rect)

    def clicked(self, mouse_pos : tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)
