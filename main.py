import random
import pygame

# inicializēt Pygame
pygame.init()

# uzstādit jaunu  logu
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Akemeni")

# izveidot assets
BACKGROUND = pygame.transform.scale(pygame.image.load("assets/backgrounds/garden.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT))
PLAYER = pygame.image.load("assets/items/nerd.png")
COMPUTER = pygame.image.load("assets/items/robot.png")
STONE = pygame.image.load("assets/items/stone.png")
# BACKGROUND_SOUND = pygame.mixer.Sound("assets/sounds/background.mp3")

# izveidot pulksteni
clock = pygame.time.Clock()

# izveidot fontus
pygame.font.init()

TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000)  # trigger the event every 1000 milliseconds (1 second)

MIN = 100
MAX = 300

TURN = "Player"


def main():
    # BACKGROUND_SOUND.play()

    turn = TURN
    winner = ""
    pile_of_stones = random.randint(MIN, MAX)
    # random position for each stone
    positions = []
    for i in range(pile_of_stones):
        positions.append((random.randint(int(WINDOW_WIDTH / 2 - 100), int(WINDOW_WIDTH / 2 + 100)),
                          random.randint(int(WINDOW_HEIGHT / 2 + 150), int(WINDOW_HEIGHT / 2 + 250))))

    player_moves_history = []
    computer_moves_history = []

    # play again and quit buttons
    button_1 = pygame.Rect(WINDOW_WIDTH / 2 - 90, 210, 200, 50)
    button_2 = pygame.Rect(WINDOW_WIDTH / 2 - 90, 310, 200, 50)

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == TIMER_EVENT:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint(event.pos):
                    main()
                if button_2.collidepoint(event.pos):
                    run = False

        # uzzīmējiet fonu
        window.blit(BACKGROUND, (0, 0))

        # palikušie akmeņi
        draw_text("Stones left: " + str(pile_of_stones), (0, 0, 0), WINDOW_WIDTH / 2 - 75, 100, 25)

        # nejauši uzzīmējiet akmeņu kaudzi ekrāna 25% diapazona centrā
        for i in range(pile_of_stones):
            window.blit(STONE, positions[i])

        # uzzīmējiet spēlētāju
        window.blit(PLAYER, (50, WINDOW_HEIGHT - 250))

        # uzzīmējiet datoru
        window.blit(COMPUTER, (WINDOW_WIDTH - 150, WINDOW_HEIGHT - 250))

        # uzzīmējiet instrukcijas
        draw_text("Press 1, 2 or 3 to take 1, 2 or 3 stones", (0, 0, 0), WINDOW_WIDTH / 2 - 150, 50, 25)

        # uzzimet spēlētāja kustību vēsturi ekrāna apakšā
        draw_text(str(player_moves_history), (0, 0, 0), 40, WINDOW_HEIGHT - 100, 15)
        # draw computer's moves history at bottom of the screen
        draw_text(str(computer_moves_history), (0, 0, 0), WINDOW_WIDTH - 250, WINDOW_HEIGHT - 100, 15)

        # tas spēlētājs, kurš paņem pēdējo akmeni, uzvar
        if pile_of_stones == 0:
            if winner == "Player":
                draw_text("You Win!", (0, 0, 0), 50, WINDOW_HEIGHT / 2 - 25, 40)
            else:
                draw_text("You Lost!", (0, 0, 0), WINDOW_WIDTH - 150, WINDOW_HEIGHT / 2 - 25, 40)

            pygame.draw.rect(window, (0, 0, 0), button_1)
            pygame.draw.rect(window, (0, 0, 0), button_2)
            draw_text("Play Again", (255, 255, 255), WINDOW_WIDTH / 2 - 50, 215, 30)
            draw_text("Quit", (255, 255, 255), WINDOW_WIDTH / 2 - 15, 315, 30)

        pygame.display.update()

        stones_taken = 0
        if pile_of_stones != 0:
            # take input from keyboard and wait for the player to press enter
            if turn == "Player":
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_1:
                                stones_taken = 1
                                if pile_of_stones - stones_taken < 0:
                                    continue
                                pile_of_stones -= stones_taken
                                player_moves_history.append(stones_taken)
                                turn = "Computer"
                                break
                            elif event.key == pygame.K_2:
                                stones_taken = 2
                                if pile_of_stones - stones_taken < 0:
                                    continue
                                pile_of_stones -= stones_taken
                                player_moves_history.append(stones_taken)
                                turn = "Computer"
                                break
                            elif event.key == pygame.K_3:
                                stones_taken = 3
                                if pile_of_stones - stones_taken < 0:
                                    continue
                                pile_of_stones -= stones_taken
                                player_moves_history.append(stones_taken)
                                turn = "Computer"
                                break
                    if turn == "Computer":
                        break

            if pile_of_stones == 0:
                winner = "Player"

            if pile_of_stones != 0:
                # computer's turn
                if turn == "Computer":
                    while True:
                        # # computer takes 1, 2 or 3 stones randomly
                        # stones_taken = random.randint(1, 3)
                        # Choose the best move using Monte Carlo simulation
                        stones_taken = find_best_move(pile_of_stones, player_moves_history, computer_moves_history)
                        if pile_of_stones - stones_taken < 0:
                            continue
                        pile_of_stones -= stones_taken
                        computer_moves_history.append(stones_taken)
                        turn = "Player"
                        break

            if pile_of_stones == 0 and winner == "":
                winner = "Computer"

    pygame.quit()

def main_menu():
    global BACKGROUND
    run = True
    while run:
        window.blit(BACKGROUND, (0, 0))
        draw_text("Main Menu", (255, 255, 255), WINDOW_WIDTH / 2 - 50, 50, 30)
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(WINDOW_WIDTH / 2 - 90, 210, 200, 50)
        button_2 = pygame.Rect(WINDOW_WIDTH / 2 - 90, 310, 200, 50)
        button_3 = pygame.Rect(WINDOW_WIDTH / 2 - 90, 410, 200, 50)

        # blue color
        color = (0, 0, 255)
        pygame.draw.rect(window, color, button_1)
        pygame.draw.rect(window, color, button_2)
        pygame.draw.rect(window, color, button_3)
        draw_text("Start Game", (255, 255, 255), WINDOW_WIDTH / 2 - 50, 215, 30)
        draw_text("Options", (255, 255, 255), WINDOW_WIDTH / 2 - 30, 315, 30)
        draw_text("Exit", (255, 255, 255), WINDOW_WIDTH / 2 - 10, 415, 30)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if button_1.collidepoint((mx, my)):
            if click:
                main()
        if button_2.collidepoint((mx, my)):
            if click:
                option_menu()
        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()

        pygame.display.update()


# opciju izvēlne, lai atlasītu, kurš iet pirmais
def option_menu():
    global BACKGROUND, TURN
    run = True
    while run:
        window.blit(BACKGROUND, (0, 0))
        draw_text("Options", (255, 255, 255), WINDOW_WIDTH / 2 - 50, 50, 30)
        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(WINDOW_WIDTH / 2 - 90, 210, 200, 50)
        button_2 = pygame.Rect(WINDOW_WIDTH / 2 - 90, 310, 200, 50)
        button_3 = pygame.Rect(WINDOW_WIDTH / 2 - 90, 410, 200, 50)

        # blue color
        color = (0, 0, 255)
        if TURN == "Player":
            pygame.draw.rect(window, color, button_1)
        else:
            pygame.draw.rect(window, color, button_2)

        pygame.draw.rect(window, (255, 0, 0), button_3)
        draw_text("Player", (255, 255, 255), WINDOW_WIDTH / 2 - 30, 215, 30)
        draw_text("Computer", (255, 255, 255), WINDOW_WIDTH / 2 - 50, 315, 30)
        draw_text("Back", (255, 255, 255), WINDOW_WIDTH / 2 - 20, 415, 30)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if button_1.collidepoint((mx, my)):
            if click:
                TURN = "Player"
        if button_2.collidepoint((mx, my)):
            if click:
                TURN = "Computer"
        if button_3.collidepoint((mx, my)):
            if click:
                run = False

        pygame.display.update()


def draw_text(text, text_col, x, y, font_size):
    font = pygame.font.SysFont("Arial", font_size)

    words = text.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        if len(current_line) + len(word) + 1 > 50:  # check if adding the next word will exceed the 50-character limit
            lines.append(current_line)
            current_line = word
        else:
            current_line += ' ' + word

    lines.append(current_line)  # add the last line

    # atveido un izdzēsa teksta rindiņas ekrānā
    for i, line in enumerate(lines):
        img = font.render(line, True, text_col)
        window.blit(img, (x, y + i * font_size))


# monte carlo koku meklēšanas algoritms, lai dators izvēlētos labāko kustību
def monte_carlo_tree_search(pile_of_stones, player_moves_history, computer_moves_history, computer_move):
    # Make a copy of the game state, so we don't modify the original
    pile = pile_of_stones
    player_history = player_moves_history.copy()
    computer_history = computer_moves_history.copy()

    # izdarit gajienu prieks datora
    pile -= computer_move
    computer_history.append(computer_move)

    # spelet nakosho speles dalu kontroleti nejausi
    num_moves = len(player_history) + len(computer_history)
    while num_moves < pile_of_stones:
        # Player's turn
        player_move = random.randint(1, 3)
        pile -= player_move
        player_history.append(player_move)
        num_moves += 1
        if pile == 0:
            return False  # Player wins

        # datora gajiens
        computer_move = random.randint(1, 3)
        pile -= computer_move
        computer_history.append(computer_move)
        num_moves += 1
        if pile == 0:
            return True  # Computer wins

    # spele beidzas
    if pile == 0:
        return True  # Computer wins
    else:
        return False  # Player wins


def find_best_move(pile_of_stones, player_moves_history, computer_moves_history):
    # Izmēģiniet katru iespējamo datora kustību un pierakstiet laimestu
    win_rates = [0.0, 0.0, 0.0]  # uzvaras koificents par katru iespējamo gājienu (1, 2 vai 3 akmeņi)
    num_simulations = 1000

    for move in [1, 2, 3]:
        wins = 0
        for i in range(num_simulations):
            if monte_carlo_tree_search(pile_of_stones, player_moves_history, computer_moves_history, move):
                wins += 1
        win_rate = wins / num_simulations
        win_rates[move - 1] = win_rate

    # izveleties gajienu ar augstako uzvaras koificentu
    best_move = win_rates.index(max(win_rates)) + 1
    return best_move


if __name__ == "__main__":
    main_menu()
