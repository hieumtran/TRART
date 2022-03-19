import pygame
import pygame.midi
from time import sleep
import sys
from random import choice, randrange


C = 74
MAX = 127
brief = .5

count = 0
inst = 0
def midi(note=[C], volume=MAX, length=brief):
    global count, inst

    inst += 1
    count += 1
    if randrange(-1, 10) > 1:
        midi_out.set_instrument(choice([0, 1, 2]))
        print(inst)
        # count < 4:
        l = randrange(1, 50)
        length = l / 30
        for n in note:
            midi_out.note_on(n, volume) # 74 is middle C, 127 is "how loud" - max is 127
        sleep(brief)
        for n in note: 
            midi_out.note_off(n, volume)
    else:
        sleep(brief)
        count = 0

    # sleep(brief)


#                init
# =======================================
GRAND_PIANO = 0
CHURCH_ORGAN = 0
instrument = randrange(1, 20)
pygame.init()
pygame.midi.init()
port = pygame.midi.get_default_output_id()
midi_out = pygame.midi.Output(port, 0)
midi_out.set_instrument(instrument)
print ("using output_id :%s:" % port)
# =======================================

def exit():
    global midi_out, music

    music = 0
    del midi_out
    pygame.midi.quit()
    pygame.quit()
    sys.exit()

def casual():
    # a = [70, 71, 72, 73]
    a = choice([C, CM, D, E, Dm, F, G, A, FM, Em])
    # a[0] = a[0] + randrange(-1, 1) * 12
    return a

CM = [74, 78, 81]
C = [62]
Dm = [74, 76, 81]
D = [76]
E = [78]
Em = [78, 81, 85]
F = [79]
G = [81]
A = [83]
FM = [72, 76, 79]
screen = pygame.display.set_mode((400, 400))
music = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()

    if music:
        x = []
        for s in range(4):
            a = casual()
            x.append(a)
            midi(a)
            print(a)
        for s in range(4):
            midi(x[3 - s])
            print(x[3 -s])
        print("-----------")



