import pygame
import sys

from traceback import print_exception
from typing import Final, Optional
from bin.table import Table
from bin.fretboard import Fretboard
from os.path import isfile, dirname


pygame.init()

SCREEN_WIDTH: Final[int] = 1000
SCREEN_HEIGHT: Final[int] = 620
SCREEN_TITLE: Final[str] = "Chordnotes Finder"


def get_exception_output(exc_type, exc_value, tb):
    print_exception(exc_type, exc_value, tb)
    input('')

    sys.exit(-1)

# Funkcja, która załadowywuje powierzchnię z ścieżki
def get_texture(texture_path: str) -> Optional[pygame.Surface]:
    # Pobierz aktualną ścieżkę
    working_directory: Final[str] = dirname(__file__)

    #print(working_directory + texture_path)

    # Sprawdź czy istnieje taki plik
    if not isfile(working_directory + texture_path):
        # Jeżeli nie, zwróć None
        return None
    
    # Pobierz obraz z ścieżki
    texture: pygame.Surface = pygame.image.load(working_directory + texture_path).convert_alpha()

    # Zwróć obraz
    return texture

def main():

    display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption(SCREEN_TITLE)

    chords_table = Table((SCREEN_WIDTH, 320))

    fretboard_image = get_texture('\\assets\\fretboard.png')
    inactive = get_texture('\\assets\\inactive.png')

    fretboard = Fretboard(inactive, fretboard_image)

    #print(chords_table.get_width(), SCREEN_WIDTH)

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
    sys.excepthook = get_exception_output
    main()
    