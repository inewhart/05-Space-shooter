import sys, logging, os, random, math, open_color, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Fall"
NUM_ENEMIES = 5
STARTING_LOCATION = (400,100)
Loc = (1000,1000)
BULLET_DAMAGE = 10
ENEMY_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100
class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        super().__init__("assets/bullet.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage
        

    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/ship.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION
class Enemy(arcade.Sprite):
    def __init__(self, position):
        
        super().__init__("assets/asteroid.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position
class GameOver(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/gameover.png", 0.5)
        (self.center_x,self.center_y)= Loc
class YouWin(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/youwin.png", 0.5)
        (self.center_x,self.center_y)= Loc
class Window(arcade.Window):

    def __init__(self, width, height, title):

        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.black)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0
        self.gameover = GameOver()
        self.youwin = YouWin()



    def setup(self):
        for i in range(NUM_ENEMIES):
            x = 130 * (i+1) + 10
            y = 500
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)  

    def update(self, delta_time):
        self.bullet_list.update()
        if self.score == 1000:
            self.youwin.center_y = 300
            self.youwin.center_x = 400
        for e in self.enemy_list:
            e.center_y += -0.2
            if arcade.check_for_collision(e,self.player) == True or e.center_y < -300:
                self.gameover.center_y = 300
                self.gameover.center_x = 400
                for f in self.enemy_list:
                    f.kill()
            t = arcade.check_for_collision_with_list(e,self.bullet_list)
            for a in t:
                a.kill()
                self.score += 10
                e.hp -= 10
                if e.hp == 0:
                    self.score += 100
                    e.kill()

    def on_draw(self):
        
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player.draw()
        self.gameover.draw()
        self.youwin.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()




    def on_mouse_motion(self, x, y, dx, dy):
        self.player.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        x = self.player.center_x
        y = self.player.center_y + 15
        bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
        self.bullet_list.append(bullet)
    def on_key_press(self, key, modifiers):

        if key == arcade.key.Q:
            sys.exit()

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()