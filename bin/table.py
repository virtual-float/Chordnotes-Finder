import pygame
from typing import Final, Optional

from bin.button import Button
from bin.chords import Chords



# Klasa tabeli (Table)
class Table(pygame.Surface):
    # Konstruktor klasy tablie (Table)
    def __init__(self, surface_size: tuple[int, int]) -> None:
        # Wywołaj konstruktor nadrzędny powierzchni ze wsparciem dla kanału alpha
        super().__init__(surface_size, pygame.SRCALPHA)

        # Rozmiary komórek w tabeli
        self.cell_width: Final[int] = 50
        self.cell_height: Final[int] = 34

        # Lista przycisków
        self.buttons: list[Button] = []

        # Tło dla przycisków
        background: pygame.Surface = pygame.Surface((self.cell_width, self.cell_height), pygame.SRCALPHA)
        background.fill((56, 56, 56))

        # Algorytm uzupełniania przycisków
        for name, notes in Chords.items():
            # Utwórz przyciski akordów
            chord_option: Button = Button(name, 19, background, notes, background.get_size(), (0, 0))

            # Przypisz objekty przycisków do listy przycisków
            self.buttons.append(chord_option)

        # Atrybut, która przechowa wybrany przez nas akord (Domyślnie jest ustawiona jako None)
        self.selected: Optional[Button] = None
    
    # Metoda, która pozwala na aktualizowanie stanu objektu
    def update(self) -> None:
        # Wyczyść powierzchnię
        self.fill((0, 0, 0, 0))

        # Przeiteruj przyciski oraz je wyświetl 
        temp_y: int = 0
        for i, button in enumerate(self.buttons, 0):
            temp_x = (i % 20) * self.cell_width

            if i % 20 == 0 and i > 0:
                temp_y += self.cell_height

            button.rect.topleft = (temp_x, temp_y)

            self.blit(button, button.rect.topleft)

            if button.clicked():
                self.selected = button