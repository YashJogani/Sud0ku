from math import ceil
import pygame.gfxdraw

class BouncyAnimation:

    @classmethod
    def initialize(cls, box):
        cls.bouncy_boxes = []
        cls.box = box

    @classmethod
    def animation(cls):
        for i in cls.bouncy_boxes:
            current_change = next(i[0])

            if current_change == -1:
                continue
            elif current_change:
                cls.box[i[1][0]][i[1][1]].w -= current_change
                cls.box[i[1][0]][i[1][1]].h -= current_change
                cls.box[i[1][0]][i[1][1]].x += current_change//2
                cls.box[i[1][0]][i[1][1]].y += current_change//2
            else:
                cls.bouncy_boxes.remove(i)

    def __init__(self, n, collision):
        self.n = n
        self.current_change = self.n//2
        self.easein = False
        BouncyAnimation.bouncy_boxes.append((self, collision))

    def __next__(self):
        if self.current_change != 1 and not self.easein:
            pixels = self.current_change
            self.current_change //= 2
            return pixels

        elif self.easein and self.current_change != self.n:
            pixels = self.current_change
            self.current_change *= 2
            return -pixels

        elif self.current_change == self.n:
            return False

        else:
            self.easein = True
            return -1


class LinearAnimation():
    def __init__(self, length, loops=20):
        self.loops = loops
        # number of pixels to add every loop
        self.n = int(abs(length/self.loops))

        self.n1 = abs(length) - self.n*self.loops
        self.left = self.n1
        self.remaining_n = []

        # number of remaining pixels to add every specific loops
        while self.left:
            self.n1 = ceil(self.loops/self.n1)
            self.remaining_n.append(self.n1)
            self.left -= self.loops//self.n1
            self.n1 = self.left

        self.length = length
        self.i = 1

    def __next__(self):
        self.pixels = self.n
        if len(self.remaining_n) > 0:
            for i in self.remaining_n:
                if self.i % i == 0:
                    self.pixels += 1

        if self.length < 0:
            self.pixels *= -1

        self.i += 1
        return self.pixels


class Switch():
    def __init__(self, screen, rect, x_pos, background_color):
        self.screen = screen
        self.rect = rect
        self.circle_radius = self.rect.h//2 + 1
        self.x_pos = x_pos
        self.background_color = background_color
    
    def toggle(self, darkmode):
        if darkmode:
            color = pygame.Color('dodgerblue')
            border_color = color
        else:
            color = self.background_color
            border_color = (100, 100, 100)

        pygame.gfxdraw.aacircle(self.screen, self.rect.x + self.rect.h//2 - 1, self.rect.y + self.rect.h//2, self.rect.h//2 + 1, border_color)
        pygame.gfxdraw.aacircle(self.screen, self.rect.x + self.rect.w - self.rect.h//2, self.rect.y + self.rect.h//2, self.rect.h//2 + 1, border_color)
        pygame.draw.rect(self.screen, border_color, (self.rect.x - 1 + self.rect.h//2, self.rect.y - 1, self.rect.w + 2 - self.rect.h, self.rect.h + 3))

        pygame.gfxdraw.aacircle(self.screen, self.rect.x + self.rect.h//2 - 1, self.rect.y + self.rect.h//2, self.rect.h//2, color)
        pygame.gfxdraw.aacircle(self.screen, self.rect.x + self.rect.w - self.rect.h//2, self.rect.y + self.rect.h//2, self.rect.h//2, color)
        pygame.gfxdraw.filled_circle(self.screen, self.rect.x + self.rect.h//2 - 1, self.rect.y + self.rect.h//2, self.rect.h//2, color)
        pygame.gfxdraw.filled_circle(self.screen, self.rect.x + self.rect.w - self.rect.h//2, self.rect.y + self.rect.h//2, self.rect.h//2, color)
        pygame.draw.rect(self.screen, color, (self.rect.x + self.rect.h//2, self.rect.y, self.rect.w - self.rect.h, self.rect.h + 1))

        ## changes x of switch so it looks animated
        if darkmode:
            if self.x_pos != 16:
                self.x_pos += 1
        else:
            if self.x_pos != -2:
                self.x_pos -= 1
        
        pygame.gfxdraw.aacircle(self.screen, self.rect.x + self.circle_radius + 1 + self.x_pos, self.rect.y + self.circle_radius - 1, self.circle_radius + 1, border_color)
        pygame.gfxdraw.filled_circle(self.screen, self.rect.x + self.circle_radius + 1 + self.x_pos, self.rect.y + self.circle_radius - 1, self.circle_radius + 1, border_color)
        
        pygame.gfxdraw.aacircle(self.screen, self.rect.x + self.circle_radius + 1 + self.x_pos, self.rect.y + self.circle_radius - 1, self.circle_radius, (255, 255, 255))
        pygame.gfxdraw.filled_circle(self.screen, self.rect.x + self.circle_radius + 1 + self.x_pos, self.rect.y + self.circle_radius - 1, self.circle_radius, (255, 255, 255))


def draw_rounded_rect(surface, color, rect, corner_radius):
    ''' Draw a rectangle with rounded corners.
    Would prefer this:
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
    but this option is not yet supported in my version of pygame so do it ourselves.

    We use anti-aliased circles to make the corners smoother
    '''
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError(f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

    # need to use anti aliasing circle drawing routines to smooth the corners
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    rect_tmp = pygame.Rect(rect)

    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)
