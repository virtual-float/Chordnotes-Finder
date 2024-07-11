from pygame import Surface, SRCALPHA, Rect, mouse

from bin.label import Label
from typing import Final


# Klasa przycisku (Button)
class Button(Surface):
    # Konstruktor przycisku
    def __init__(self, text: str, font_size: int, background: Surface, value, size: tuple[int, int], pos: tuple[int, int]) -> None:
        # Wywołaj konstruktor nadrzędny powierzchni ze wsparciem dla kanału alpha
        super().__init__(size, SRCALPHA)
        # Narysuj tło
        self.blit(background, (0, 0))

        # Stały tekst przycisku
        self.text: Final[str] = text
        # Stały rozmiar przycisku
        self.size: Final[tuple[int, int]] = size
        # Stały rozmiar czcionki
        self.font_size: Final[int] = font_size
        # Stała wartość przycisku
        self.value: Final = value

        # Stałe tło przycisku
        self.background: Final[Surface] = background

        # Figura kolizyjna przycisku
        self.rect: Rect = self.get_rect()
        # Ustawianie pozycji figury
        self.rect.topleft = pos

        # Stały objekt tabliczki
        self.label: Final[Label] = Label(self.text, (self.font_size, 'Arial', (250, 250, 250)))

        # Narysuj tekst na powierzchni (wyśrodkowany)
        center_x: Final[int] = (self.get_width() - self.label.get_width()) // 2
        center_y: Final[int] = (self.get_height() - self.label.get_height()) // 2

        self.blit(self.label, (center_x, center_y))

    # Metoda, która sprawdza czy przycisk koliduje się z myszką (myszka najeżdża na przycisk)
    def hovered(self) -> bool:
        # Pobierz pozycję myszki
        mouse_pos = mouse.get_pos()

        # Zwróć wynik kolizji pozycji myszki z figurą przycisku
        return self.rect.collidepoint(mouse_pos)
    
    # Metoda, która sprawdza czy przycisk został kliknięty
    def clicked(self) -> bool:
        # Pobierz stan kliknięcia lewego przycisku myszki
        lm_pressed: Final[bool] = mouse.get_pressed()[0]

        # Sprawdź czy kursor najeżdza na przycisk
        if self.hovered():
            # Sprawdź czy wciśnięto lewy przycisk myszki i czy nie został przycisk wcześniej kliknięty
            if lm_pressed and not self.clicked_before:
                # Ustaw na True
                self.clicked_before = True

                # Zwróć True
                return True
        
        # Jeżeli nie wykryto kliknięcia przycisku
        if not lm_pressed:
            # Ustaw na False
            self.clicked_before = False

            # Zwróć False
            return False