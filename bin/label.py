from pygame import font, Surface, SRCALPHA


# Klasa tabliczki (Label)
class Label(Surface):
    # Konstruktor klasy tabliczki (Label)
    def __init__(self, text: str, font_data: tuple[int, str, tuple[int, int, int]]) -> None:
        # Słownik danych dla czcionki
        self.font: dict = {
            'size': font_data[0],
            'family': font.match_font(font_data[1]),
            'color': font_data[2]
        }
        # Renderer czcionki
        self.__renderer: font.Font = font.SysFont(self.font['family'], self.font['size'])
        # Zmienna lokalna powierzchni tekstu
        label: Surface = self.__renderer.render(text, True, self.font['color'])

        # Wywołaj konstruktor nadrzędny powierzchni ze wsparciem dla kanału alpha
        super().__init__(label.get_size(), SRCALPHA)
        # Narysuj tekst na powierzchni
        self.blit(label, (0, 0))
