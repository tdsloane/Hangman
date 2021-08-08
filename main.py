import pygame
import math
import random
from pygame import mixer

# Setup Display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load('asset/tdsloane.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Hangman')
background = pygame.image.load('asset/background.jpg')

FPS = 30;
clock = pygame.time.Clock()
run = True

# Load Images
images = []
for i in range(7):
    image = pygame.image.load("asset/hangman" + str(i) + ".png")
    images.append(image)

# Sounds
failure_sound = mixer.Sound('asset/failure.mp3')
success_sound = mixer.Sound('asset/success.mp3')

# Button Varaibles
RADIUS = 20
GAP = 15
letters = []
A =65
startX = round(WIDTH - (RADIUS * 2 + GAP) * 28 / 2)
startY = 35
for i in range(26):
    x = startX + GAP * 2 + (RADIUS * 2 + GAP) * (i % 13)
    y = startY + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 60)

# Game Variables
hangman_status = 0
words = ["CODE", "SPOON", "WINTER", "DIOGENES", "PYTHON", "WITHOUT", "IDEA"]
word = random.choice(words)
guessed = []

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Display
def draw():
    # Background
    win.blit(background, (0, 0))
    # Title
    text = TITLE_FONT.render("Guess correctly or hang!", 5, BLACK)
    win.blit(text, (285, 130))
    # Draw Word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 2, BLACK)
    win.blit(text, (400, 200))


    # Draw Buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, width = 0)
            text = LETTER_FONT.render(ltr, 2, WHITE)
            win.blit(text, (x - text.get_width()/2, y - text.get_width()/2))

    # win.fill(WHITE)
    win.blit(images[hangman_status], (530, 275))
    pygame.display.update()
draw()


# Win/ Lose Function
def display_message(message):
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(delay)


# Game Loop
def main():
    global run
    global hangman_status
    global delay

    while run:
        clock.tick(FPS)

        # Events
        for event in pygame.event.get():
            # Enables closing of the game window
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) **2 + (y - m_y) **2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        if won:
            pygame.time.delay(1000)
            delay = 3000
            success_sound.play()
            display_message("You Won!")
            break
        if hangman_status == 6:
            pygame.time.delay(1000)
            delay = 5000
            failure_sound.play()
            display_message("You Lost!")
            break

main()
pygame.quit()