from math import ceil

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
    def __init__(self, length, loops):
        self.loops = loops
        # number of pixels to add every loop
        self.n = int(abs(length/self.loops))

        self.n1 = abs(length) - self.n*self.loops
        self.left = self.n1
        self.remaining_n = []

        # number of remaining pixels to add every specific loops
        if self.left != 0:
            while self.loops % self.n1 != 0:
                if self.n1 % 2 != 0:
                    self.n1 -= 1

                self.n1 = ceil(self.loops/self.n1)
                self.remaining_n.append(self.n1)
                self.left -= self.loops//self.n1
                self.n1 = self.left

            self.remaining_n.append(ceil(self.loops/self.n1))

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
