import pygame, os, sys
from pygame.locals import *
import random

pygame.mixer.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

click_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'sounds/Confirm.mp3'))

small_font = pygame.font.Font(None, int(HEIGHT/15))
medium_font = pygame.font.Font(None, int(HEIGHT/10))
large_font = pygame.font.Font(None, int(HEIGHT/3.5))

answer_box = pygame.Rect(WIDTH/2 - (650/2), HEIGHT*0.1, 650, 150)
input_box = pygame.Rect(WIDTH/2 -(650/2), HEIGHT * 0.4, 650, 100)

# WORDS = check_voca_list()
checkedAlphabets = set()
alphabet = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
        ]

order = list(range(0, 26))

# 파일을 화면에 끓어다 놓으면 해당 파일을 parameter로 받는 function으로 개선
def check_voca_list():
    VOCA = []
    with open ('words.txt', 'r') as words:
        DATA = words.readlines() # text file을 읽어 각각의 라인을 element로 갖는 리스트를 리턴해준다.
    
    for d in DATA:
        VOCA.append(d.upper().strip())

    return VOCA
   
def main():
    text = ''
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    displayedAnswer = ""
    active = False
    done = False
# To render a text, I need a string and surface to render a text on.
# 입력용 키패드를 그리는 function
    def drawKeypad():
        sept = "keyPad_"

        KEYPADS = []

        for i in alphabet:
            KEYPADS.append(sept+i)

        startX = WIDTH/2
        startY = 400
        keypadWidth = 48
        keypadHeight = 48
        offset = 60
        keypadColor = pygame.Color('white')
        
        # Make 26 Rects for each alphabet
        for i in range(0, 25+1):
            if i < 13:
                KEYPADS[i] = pygame.Rect(startX - (768/2) + offset * i, startY, keypadWidth, keypadHeight)
                pygame.draw.rect(screen, keypadColor, KEYPADS[i])
            else:
                KEYPADS[i] = pygame.Rect(startX - (768/2) + offset * (i-13), startY + 60, keypadWidth, keypadHeight)
                pygame.draw.rect(screen, keypadColor, KEYPADS[i])

        # Make 26 Surfaces for each alphabet.
        for i, j in zip(alphabet, order):
            i = medium_font.render(alphabet[j], True, (0, 0, 0))
            screen.blit(i, (KEYPADS[j].x+7 , KEYPADS[j].y+7))

        return KEYPADS

    # Check userInput and see if the input is in the answer
    # If it's True: Display the actual alphabet instead of underbar at the beginning. or
    # When I create underbar displayed, what about using 'join'
    # I think I need to zip underbar & element in checkedAlphabets
    # Let's first try without empty space between underbar. String is inconvenient to implement unberbar <-> answer.
    def spellCheck(spell, answer, words):
        displayedAnswer = list("_" * len(answer))  # ['_', '_', '_', '_', '_']
        checkedAlphabets.add(spell)

        print(f"Spell Check has been executed for {answer}!")
        print(checkedAlphabets)

        for userInput in checkedAlphabets:
            if userInput == answer:
                return randomize_answer(words)
            else:
                for j in range(len(answer)):
                    if userInput.upper() == answer[j]:
                        displayedAnswer[j] = userInput

        return str(" ").join(displayedAnswer)


    def randomize_answer(words):
        if len(words) != False:
            random.shuffle(words)
            answer = words.pop(0)
            answerConvertedList = "_" * len(answer)
            sept = ' '
            underbar = sept.join(answerConvertedList)
            underbar_surface = large_font.render(underbar, True, pygame.Color('lightskyblue3'))
            print(f"Answer: {answer}, underbar Surface: {underbar_surface}")

        else:
            print("No more words")

        return answer, underbar

    def makingAnswerSuface(text):

        answerSurface = large_font.render(text, True, pygame.Color('lightskyblue3'))

        return answerSurface

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active

                elif drawKeypad()[0].collidepoint(event.pos):
                    print("Keypad_A has been clicked")
                    click_sound.play()

                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_F1:
                        answer, underbar = randomize_answer(check_voca_list())
                        checkedAlphabets = set()
                        displayedAnswer = underbar
                        answer_surface = makingAnswerSuface(answer)
                        screen.blit(answer_surface, (answer_box.x+5, answer_box.y+5))
                    
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]

                    elif event.key == pygame.K_RETURN:
                        text += event.unicode
                        displayedAnswer = spellCheck(text, answer, check_voca_list())
                        text = ''

                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))

        # Render text.
        txt_input = medium_font.render(text, True, color)
        txt_answer = medium_font.render(displayedAnswer, True, color)

        
        # Blit the text.
        screen.blit(txt_input, (input_box.x+5, input_box.y+5))
        screen.blit(txt_answer, (answer_box.x+5, answer_box.y+5))

        # Resize the box if the text is too long.
        width = max(400, txt_input.get_width()+10)
        input_box.w = width

        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)
        
        # Blit the answer_box rect.
        pygame.draw.rect(screen, color, answer_box, 2)
        drawKeypad()
        pygame.display.flip()

        clock.tick(30)


# Need to make a variable assigned with string value first, and then I need to change the value of the variable through other function
# to change the displayed test on the screen.


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()

'''
Linux Path Concept
/ : Absolute Path(절대경로)
파일 시스템의 최상위부터 적어나가는 것. 
우분투 파일 시스템의 최상위는 / 이다. 
때문에 맨 앞이 / 로 시작하지 않는 path는 모두 상대경로!
./ : Current Path(현재경로)
../ : one upper level of current path
~/ : Home path
'''