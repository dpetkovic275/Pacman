from pygame.math import Vector2 as vec
import pygame
import random
import sys

vec = pygame.math.Vector2

ZASLON= SIRINA, VISINA=(610, 670)

FPS = 60
MARGINA = 50
SIRINA_L, VISINA_L = SIRINA - MARGINA, VISINA - MARGINA

REDCI = 30
STUPCI = 28

ZUTA = (255, 255 ,0)
BIJELA = (255, 255, 255)
CRNA = (0, 0, 0)
SIVA = (107, 107, 107)
CRVENA = (255, 0, 0)

IGRAC = (255, 0, 255)

VELICINA_TEKSTA = 18
FONT = 'arial black'



class Player():
    def __init__(self, app, pos):
        self.bodovi = 0
        self.brzina = 2
        self.zivoti = 3
        self.app = app
        self.pocetna_pozicija = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.pozicija_piksela()
        self.smjer = vec(1, 0)
        self.pocetni_smjer = None
        self.moze_se_kretati = True

    def update(self):
        if self.moze_se_kretati:
            self.pix_pos += self.smjer * self.brzina
        if self.vrijeme_za_kretanje():
            if self.pocetni_smjer != None:
                self.smjer = self.pocetni_smjer
            self.moze_se_kretati = self.provjera_zida()

        self.grid_pos[0] = (self.pix_pos[0] - MARGINA +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - MARGINA +
                            self.app.cell_height // 2) // self.app.cell_height + 1
        if self.provjeri_novcic():
            self.pojedi_novcic()

    def provjeri_novcic(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x + MARGINA // 2) % self.app.cell_width == 0:
                if self.smjer == vec(1, 0) or self.smjer == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + MARGINA // 2) % self.app.cell_height == 0:
                if self.smjer == vec(0, 1) or self.smjer == vec(0, -1):
                    return True
        return False

    def pojedi_novcic(self):
        self.app.coins.remove(self.grid_pos)
        self.bodovi += 1

    def kretanje(self, direction):
        self.pocetni_smjer = direction

    def draw(self):

        pygame.draw.rect(self.app.screen, IGRAC,[int(self.pix_pos.x),int(self.pix_pos.y), 15, 15])

        for x in range(self.zivoti):
            pygame.draw.rect(self.app.screen, IGRAC, [30 + 20 * x, VISINA-20, 15, 15])


    def pozicija_piksela(self):
        return vec((self.grid_pos[0] * self.app.cell_width) + MARGINA // 2 + self.app.cell_width // 2,
                   (self.grid_pos[1] * self.app.cell_height) +
                   MARGINA // 2 + self.app.cell_height // 2)

        print(self.grid_pos, self.pix_pos)

    def provjera_zida(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.smjer) == wall:
                return False
        return True


    def vrijeme_za_kretanje(self):
        if int(self.pix_pos.x + MARGINA // 2) % self.app.cell_width == 0:
            if self.smjer == vec(1, 0) or self.smjer == vec(-1, 0) or self.smjer == vec(0, 0):
                return True
        if int(self.pix_pos.y + MARGINA // 2) % self.app.cell_height == 0:
            if self.smjer == vec(0, 1) or self.smjer == vec(0, -1) or self.smjer == vec(0, 0):
                return True


vec = pygame.math.Vector2

class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.pozicija_piksela()
        self.radius = int(self.app.cell_width//2.3)
        self.number = number
        self.colour = self.postavi_boju_neprijatelja()
        self.direction = vec(0, 0)
        self.personality = self.postavi_karakter()
        self.meta = None
        self.speed = self.postavi_brzinu()

    def update(self):
        self.meta = self.postavi_metu()
        if self.meta != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.vrijeme_za_kretanje():
                self.kretanje()

        self.grid_pos[0] = (self.pix_pos[0] - MARGINA +
                            self.app.cell_width // 2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1] - MARGINA +
                            self.app.cell_height // 2)//self.app.cell_height+1

    def postavi_brzinu(self):
        if self.personality in ["brzi", "preplaseni"]:
            speed = 2
        else:
            speed = 1
        return speed

    def postavi_metu(self):
        if self.personality == "brzi" or self.personality == "spori":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > STUPCI//2 and self.app.player.grid_pos[1] > REDCI//2:
                return vec(1, 1)
            if self.app.player.grid_pos[0] > STUPCI//2 and self.app.player.grid_pos[1] < REDCI//2:
                return vec(1, REDCI - 2)
            if self.app.player.grid_pos[0] < STUPCI//2 and self.app.player.grid_pos[1] > REDCI//2:
                return vec(STUPCI - 2, 1)
            else:
                return vec(STUPCI - 2, REDCI - 2)

    def draw(self):
        pygame.draw.circle(self.app.screen, self.colour,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)


    def vrijeme_za_kretanje(self):
        if int(self.pix_pos.x + MARGINA // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + MARGINA // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def kretanje(self):
        if self.personality == "random":
            self.direction = self.random_putanja()
        if self.personality == "spori":
            self.direction = self.putanja(self.meta)
        if self.personality == "brzi":
            self.direction = self.putanja(self.meta)
        if self.personality == "preplaseni":
            self.direction = self.putanja(self.meta)

    def putanja(self,


                target):
        next_cell = self.iduca_celija_u_putanji(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def iduca_celija_u_putanji(self, target):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [
                        int(target[0]), int(target[1])])
        return path[1]


    def random_putanja(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)

    def pozicija_piksela(self):
        return vec((self.grid_pos.x*self.app.cell_width) + MARGINA // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y*self.app.cell_height) + MARGINA // 2 +
                   self.app.cell_height // 2)

    def postavi_boju_neprijatelja(self):
        if self.number == 0:
            return (28, 247, 28)
        if self.number == 1:
            return (28, 43, 247)
        if self.number == 2:
            return (247, 28, 28)
        if self.number == 3:
            return (255, 95, 31)

    def postavi_karakter(self):
        if self.number == 0:
            return "brzi"
        elif self.number == 1:
            return "spori"
        elif self.number == 2:
            return "random"
        else:
            return "preplaseni"

    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest





pygame.init()
vec = pygame.math.Vector2

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((SIRINA, VISINA))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'playing'
        self.cell_width = SIRINA_L // STUPCI
        self.cell_height = VISINA_L // REDCI
        self.walls = []
        self.coins = []
        self.enemies = []
        self.pozicija_neprijatelja = []
        self.pozicija_igraca = None
        self.ucitaj()
        self.player = Player(self, vec(self.pozicija_igraca))
        self.dodaj_neprijatelje()
        pygame.init()

    def run(self):
        while self.running:

            if self.state == 'playing':
                self.igranje_events()
                self.update_igre()
                self.crtanje_igre()
            elif self.state == 'game over':
                self.kraj_igre_events()
                self.kraj_igre_update()
                self.kraj_igre_crtanje()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def dodaj_tekst(self, rijeci, screen, pozicija, velicina, boja, ime_fonta, centered=False):
        font = pygame.font.SysFont(ime_fonta, velicina)
        text = font.render(rijeci, False, boja)
        text_size = text.get_size()
        if centered:
            pozicija[0] = pozicija[0] - text_size[0] // 2
            pozicija[1] = pozicija[1] - text_size[1] // 2
        screen.blit(text, pozicija)

    def ucitaj(self):
        self.BG = pygame.image.load('labirint1.png')
        self.BG = pygame.transform.scale(self.BG, (SIRINA_L, VISINA_L))

        with open("lab1.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.pozicija_igraca = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.pozicija_neprijatelja.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.BG, CRNA, (xidx * self.cell_width, yidx * self.cell_height,
                                                         self.cell_width, self.cell_height))

    def dodaj_neprijatelje(self):
        for idx, pos in enumerate(self.pozicija_neprijatelja):
            self.enemies.append(Enemy(self, vec(pos), idx))

    def crtanje_sustava(self):
        for x in range(SIRINA // self.cell_width):
            pygame.draw.line(self.BG, SIVA, (x * self.cell_width, 0), (x * self.cell_width, VISINA))
        for x in range(VISINA // self.cell_height):
            pygame.draw.line(self.BG, SIVA, (0, x * self.cell_height), (SIRINA, x * self.cell_height))

    def resetiranje(self):
        self.player.zivoti = 3
        self.player.bodovi = 0
        self.player.grid_pos = vec(self.player.pocetna_pozicija)
        self.player.pix_pos = self.player.pozicija_piksela()
        self.player.smjer *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.pozicija_piksela()
            enemy.direction *= 0
        self.coins = []
        with open("lab1.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"


    def igranje_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.kretanje(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.kretanje(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.kretanje(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.kretanje(vec(0, 1))

    def update_igre(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.ukloni_zivot()

    def crtanje_igre(self):
        self.screen.fill(CRNA)
        self.screen.blit(self.BG, (MARGINA // 2, MARGINA // 2))
        self.crtaj_novcice()
        self.dodaj_tekst('BODOVI: {}'.format(self.player.bodovi), self.screen, [400, 0], 18, ZUTA, "arial black")
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def ukloni_zivot(self):
        self.player.zivoti -= 1
        if self.player.zivoti == 0:
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.pocetna_pozicija)
            self.player.pix_pos = self.player.pozicija_piksela()
            self.player.smjer *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.pozicija_piksela()
                enemy.direction *= 0

    def crtaj_novcice(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (255, 255, 51),
                               (int(coin.x * self.cell_width) + self.cell_width // 2 + MARGINA // 2,
                                int(coin.y * self.cell_height) + self.cell_height // 2 + MARGINA // 2), 5)


    def kraj_igre_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.resetiranje()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False


    def kraj_igre_update(self):
        pass

    def kraj_igre_crtanje(self):
        self.screen.fill(CRNA)
        quit_text = " ESCAPE za kraj"
        again_text = " SPACE za ponovno igranje"
        self.dodaj_tekst("KRAJ IGRE ", self.screen, [SIRINA // 2, 100], 85, CRVENA, "verdana", centered=True)
        self.dodaj_tekst(again_text, self.screen, [
            SIRINA // 2, VISINA // 1.5], 30, (190, 190, 190), "verdana", centered=True)
        self.dodaj_tekst(quit_text, self.screen, [
            SIRINA // 2, VISINA // 1.25], 30, (190, 190, 190), "verdana", centered=True)
        pygame.display.update()


if __name__ == '__main__':
    app = App()
    app.run()


