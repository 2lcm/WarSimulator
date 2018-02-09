import pygame
import sys
import LinkedList
import numpy as np

MAXFPS = 100
SCREEN_SIZE = 800, 600
UNIT_LENGTH = 101  # must be odd number

unit_img = pygame.image.load("unit (1).png")
unit_img = pygame.transform.scale(unit_img, (UNIT_LENGTH, UNIT_LENGTH))


class WS(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(10, 25)
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.units = LinkedList.LL()
        tmp = Unit()
        tmp.p = (100, 100)
        tmp.img = unit_img
        self.units.insert(tmp)
        self.user = self.units.head.next.val

    def run(self):
        fps_clk = pygame.time.Clock()
        up_act = False
        down_act = False
        left_act = False
        right_act = False

        while True:
            # set maximum fps
            fps_clk.tick(MAXFPS)
            user = self.units.head.next.val

            # draw screen
            self.screen.fill((255, 255, 255))
            draw_screen([self.units], self.screen)
            pygame.display.update()

            # handle events
            for event in pygame.event.get():
                # when click x button on window
                if event.type == pygame.QUIT:
                    sys.exit()
                # when press the keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_w:
                        up_act = True
                    if event.key == pygame.K_a:
                        left_act = True
                    if event.key == pygame.K_d:
                        right_act = True
                    if event.key == pygame.K_s:
                        down_act = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_w:
                        up_act = False
                    if event.key == pygame.K_a:
                        left_act = False
                    if event.key == pygame.K_d:
                        right_act = False
                    if event.key == pygame.K_s:
                        down_act = False

                if up_act:
                    user.move((0, -2))
                if down_act:
                    user.move((0, 2))
                if left_act:
                    user.move((-2, 0))
                if right_act:
                    user.move((2, 0))

            # make user unit look toward mouse position
            xy = np.subtract(np.array(pygame.mouse.get_pos()), np.array(self.user.p))
            if xy[0] == 0:
                if xy[1] / abs(xy[1]) == 1:
                    self.user.direct = 90
                else:
                    self.user.direct = -90
            else:
                self.user.direct = 0 - np.rad2deg(np.arctan(xy[1] / xy[0]))
                if xy[0] < 0:
                    self.user.direct += 180


class Unit(object):
    def __init__(self):
        self.p = [0, 0]
        self.img = None
        self.direct = 0  # deg

    def move(self, d):
        self.p = self.p[0] + d[0], self.p[1] + d[1]


# take pygame.Surface(screen) and list comprised of LinkedList.LL
# draw given Units in LinkedLists on given Surface(screen)
def draw_screen(ls, screen):
    for LL in ls:
        # defensive coding
        if type(LL) != LinkedList.LL or type(screen) != pygame.Surface:
            raise TypeError

        # draw unit image on screen
        cur = LL.head.next
        while cur != LL.tail:
            new_img = pygame.transform.rotate(cur.val.img, cur.val.direct)
            new_p = cur.val.p[0] - int(UNIT_LENGTH / 2), cur.val.p[1] - int(UNIT_LENGTH / 2)
            screen.blit(new_img, new_p)
            cur = cur.next


if __name__ == '__main__':
    ws = WS()
    WS().run()