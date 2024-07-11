import pygame


from typing import Final

from bin.table import Table
from bin.fretboard import Fretboard

pygame.init()

SCREEN_WIDTH: Final[int] = 1000
SCREEN_HEIGHT: Final[int] = 620

SCREEN_TITLE: Final[str] = "Chordnotes Finder"


def main():

    display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption(SCREEN_TITLE)

    chords_table = Table((SCREEN_WIDTH, 320))

    fretboard_image = pygame.image.load('assets\\fretboard.png')
    fretboard = Fretboard(fretboard_image)

    print(chords_table.get_width(), SCREEN_WIDTH)

    running = True
    while running:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        
        display.fill((40, 40, 40))

        display.blit(chords_table, (0, 0))
        display.blit(fretboard, ((SCREEN_WIDTH - fretboard.get_width()) // 2, chords_table.get_height() + 16))

        selected_chord = chords_table.selected

        if selected_chord != None:
            fretboard.queue_notes(selected_chord.value)
        
        chords_table.update()
        fretboard.update()

        pygame.display.flip()


    pygame.quit()


if __name__ == "__main__":
    main()