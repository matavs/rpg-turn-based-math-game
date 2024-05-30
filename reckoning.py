import random
import pygame_gui
import pygame, sys
from button import Button

pygame.init()

clock = pygame.time.Clock()
fps = 60

# Game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

# Pygame GUI
MANAGER = pygame_gui.UIManager((screen_width, screen_height))

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('OPERATION RECKONING')

# GUI text
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((screen_width // 2 - 50, 50), (100, 30)),  # Adjust position
manager=MANAGER)

# Background image
background_img = pygame.image.load('rpgimages/background/istockphoto-1333010525-612x612.jpg').convert_alpha()
backgroundscale = pygame.transform.scale(background_img, (800, 400))

# Define font
font = pygame.font.Font("assets/font.ttf", 15)

# Define color
red = (255, 0, 0)
green = (0, 255, 0)

# Panel image
panel_img = pygame.image.load('rpgimages/panel/work.png')
panelscale = pygame.transform.scale(panel_img, (800, 150))

# restart and main menu img 
restartimg = pygame.transform.scale(panel_img, (800, 150))

# Load victory or defeat
defeat = pygame.image.load('rpgimages/gameover screen/gameover.png')
defeatscale = pygame.transform.scale(defeat, (500, 500))
victory1 = pygame.image.load('rpgimages/gameover screen/victory.png')
victory1scale = pygame.transform.scale(victory1, (100, 100))

BG = pygame.image.load("assets/Background.png")


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def strengthE(current_strength=[10]):
    # Modify the value of current_strength
    current_strength[0] += 1
current_strength = [10]

def play():

    # Define game variables
    
    gameover = 0

        # Function for drawing text
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    def generate_math_problem():
        num1 = random.randint(1, 5)
        num2 = random.randint(1, 5)
        operator = random.choice(['+', '*'])
        problem = f"{num1} {operator} {num2}"
        solution = eval(problem)  # Evaluate the expression to get the solution
        return problem, solution

    # Function panel image
    def draw_panel():
        screen.blit(panelscale, (0, screen_height - bottom_panel))
        # Show knight stats
        draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100 , screen_height - bottom_panel + 10)
        for count, i in enumerate(bandit_list):
            # Show name and health
            draw_text(f'{i.name} HP: {i.hp}', font, red, 520, (screen_height - bottom_panel + 10) + count * 60)
        
    # Function for background
    def draw_background():
        screen.blit(backgroundscale, (0, 0))

    class Fighter():
        def __init__(self, x, y, name, max_hp, strength):
            self.name = name
            self.max_hp = max_hp
            self.hp = max_hp
            self.strength = strength
            self.alive = True
            self.animation_list = []
            self.frame_index = 0
            self.action = 0 # 0:idle 1:attack 2:hurt 3:dead
            self.update_time = pygame.time.get_ticks()
            # Load idle images
            temp_list = []
            for i in range(8):
                img = pygame.image.load(f'rpgimages/{self.name}/Idle/F{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 1, img.get_height() * 1))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            # Load attack images
            temp_list = []
            for i in range(8):
                img = pygame.image.load(f'rpgimages/{self.name}/attack/F{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 1, img.get_height() * 1))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            # Load hurt images
            temp_list = []
            for i in range(8):
                img = pygame.image.load(f'rpgimages/{self.name}/hurt/F{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 1, img.get_height() * 1))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            # Load hurt images
            temp_list = []
            for i in range(8):
                img = pygame.image.load(f'rpgimages/{self.name}/hurt/F{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 1, img.get_height() * 1))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        def update(self):
            animation_cooldown = 100 
            # Handle animation
            # Update image
            self.image = self.animation_list[self.action][self.frame_index]
            # Check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            # If the animation has run out then reset back to the start
            if self.frame_index >= len(self.animation_list[self.action]):
                self.idle()

        def idle(self):
            # Set variables to attack animation
            self.action = 0
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        def hurt(self):
            # Set variables to hurt animation
            self.action = 2
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        def attack(self, target):
            # Deal damage to enemy
            rand = random.randint(-5, 5)
            damage = self.strength + rand
            target.hp -= damage
            #run hurt animation
            target.hurt()
            # Check if target has died
            if target.hp < 1:
                target.hp = 0
                target.alive = False
            # Set variables to attack animation
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
        def reset(self):
            self.alive = True
            self.hp = self.max_hp
            self.frame_index = 0
            self.action = 0


        def draw(self):
            screen.blit(self.image, self.rect)

    class HealthBar():
        def __init__(self, x, y, hp, max_hp):
            self.x = x
            self.y = y
            self.hp = hp
            self.max_hp = max_hp

        def draw(self, hp):
            # Update with new health 
            self.hp = hp
            # Calculate hp
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
            pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


    # Class fighter (x, y, name, health, strenght)
    knight = Fighter(200, 260, 'MC', 100, 31)
    bandit1 = Fighter(590, 230, 'skeleton', 100, current_strength[0])

    bandit_list = []
    bandit_list.append(bandit1)

    knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
    bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)

    # Define initial math problem
    math_problem = generate_math_problem()

    
    # Buttons for game
    restart_button = Button(image=pygame.image.load("assets/bt21.png"), pos=(330, 120), 
                            text_input="QUIT", font=get_font(20), base_color="#d7fcd4", hovering_color="White", size=(120, 30))


    while True:
        UI_REFRESH_RATE = clock.tick(60)/1000

        clock.tick(fps)
        # Draw panel
        draw_panel()
        knight_health_bar.draw(knight.hp)
        bandit1_health_bar.draw(bandit1.hp)

        # Draw background
        draw_background()

        # Draw fighter
        knight.update()
        knight.draw()

        for bandit in bandit_list:
            bandit.update()
            bandit.draw()

        # Control action player
        # Reset action variables
        attack = False
        target = None
        
        # Function to display math problem
        def display_math_problem():
            problem_text = font.render(math_problem[0], True, (255, 255, 255))  # Render the problem text
            screen.blit(problem_text, (screen_width // 2 - problem_text.get_width() // 2, 20))  # Position the text

        # Call the function to display the math problem
        display_math_problem()

        # Display gameover
        GAME_MOUSE_POS = pygame.mouse.get_pos()
        if gameover != 0:
            restart_button = Button(image=pygame.image.load("assets/bt21.png"), pos=(300, 120), 
                            text_input="RESTART", font=get_font(20), base_color="#d7fcd4", hovering_color="White", size=(190, 30))
            main_menu_button = Button(image=pygame.image.load("assets/bt21.png"), pos=(510, 120), 
                            text_input="MAIN MENU", font=get_font(20), base_color="#d7fcd4", hovering_color="White", size=(200, 30))
            for button in [restart_button, main_menu_button]:
                button.changeColor(GAME_MOUSE_POS)
                button.update(screen)
            if gameover == 1:
                screen.blit(victory1scale, (350, 100))
            if gameover == -1:
                screen.blit(defeatscale, (150, 30))           
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.checkForInput(GAME_MOUSE_POS):
                    knight.reset()
                    bandit1.reset()
                    gameover = 0
                if main_menu_button.checkForInput(GAME_MOUSE_POS):
                    main_menu()
            



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if gameover == 0:
                if event.type == pygame.KEYDOWN:               
                    if event.key == pygame.K_RETURN:  # Check if the Enter key is pressed
                        # Check if the answer is correct                                                               
                        if text_input.get_text().isdigit():  # Ensure the input is a digit
                            answer = int(text_input.get_text())
                            if answer == math_problem[1]:
                                # Attack the bandit if the answer is correct
                                knight.attack(bandit1)
                            else:
                                # Handle incorrect answers and attacks knight
                                print("Your attack missed!")
                                bandit1.attack(knight)
                            # Generate a new math problem regardless of the answer
                            math_problem = generate_math_problem()
                            # Clear the text input field after answering
                            text_input.set_text('')
                    if bandit1.alive == False:
                        gameover = 1
                    if knight.alive == False:
                        gameover = -1
            MANAGER.process_events(event)
        MANAGER.update(UI_REFRESH_RATE)
        MANAGER.draw_ui(screen)
        pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(BG, (0, 0))

        OPTIONS_BACK = Button(image=pygame.image.load("assets/bt21.png"), pos=(640, 460), 
                            text_input="BACK", font=get_font(20), base_color="Black", hovering_color="Green", size=(100, 50) )
        
        EASY_BUTTON = Button(image=pygame.image.load("assets/bt21.png"), pos=(300, 200), 
                            text_input="EASY", font=get_font(25), base_color="#d7fcd4", hovering_color="White", size=(170, 70))
        NORMAL_BUTTON = Button(image=pygame.image.load("assets/bt21.png"), pos=(300, 300), 
                            text_input="NORMAL", font=get_font(25), base_color="#d7fcd4", hovering_color="White", size=(170, 70))
        HARD_BUTTON = Button(image=pygame.image.load("assets/bt21.png"), pos=(300, 400), 
                            text_input="HARD", font=get_font(25), base_color="#d7fcd4", hovering_color="White", size=(170, 70))

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)
        for button in [EASY_BUTTON, NORMAL_BUTTON, HARD_BUTTON]:
                button.changeColor(OPTIONS_MOUSE_POS)
                button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if EASY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    current_strength [0] = 10
                    strengthE(current_strength)
                    print(current_strength[0]) 
                if NORMAL_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    current_strength [0] = 30
                    strengthE(current_strength)
                    print(current_strength[0])
                if HARD_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    current_strength [0] = 60
                    strengthE(current_strength)
                    print(current_strength[0])
            
        pygame.display.update()

def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        Title = pygame.image.load('assets/Title.png')
        Title1 = pygame.transform.scale(Title, (400, 400))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/bt21.png"), pos=(380, 290), 
                            text_input="PLAY", font=get_font(20), base_color="#d7fcd4", hovering_color="White", size=(200, 100))
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/bt21.png"), pos=(380, 390), 
                            text_input="OPTIONS", font=get_font(15), base_color="#d7fcd4", hovering_color="White", size=(200, 100))
        QUIT_BUTTON = Button(image=pygame.image.load("assets/bt21.png"), pos=(380, 490), 
                            text_input="QUIT", font=get_font(20), base_color="#d7fcd4", hovering_color="White", size=(200, 100))

        screen.blit(Title1, (200, -100))

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
