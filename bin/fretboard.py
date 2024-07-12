from pygame import SRCALPHA, Surface

from typing import Final
from bin.chords import Chords
from bin.label import Label


# Stała lista nut w muzyce
NOTES: Final[list[str]] = [
    'A', 'A#',
    'B', 'C',
    'C#', 'D',
    'D#', 'E',
    'F', 'F#',
    'G', 'G#'
]


#
# Funkcja, która pobiera początkową nutę oraz uporządkowuje
#   kolejność względem początkowej nuty
#
# Przykład: podamy nutę początkową jako 'C'
#           Następnie zaczyna zwracać nuty, 
#           które są po nucie C
#
def get_ordered_notes(start_note: str) -> list[str]:
    # Sprawdź czy przypadkiem nuta podana nie istnieje
    if start_note not in NOTES:
        # Zwróć pustą listę
        return []
    
    # Pobierz pozycje nuty z listy nut
    note_pos = NOTES.index(start_note)

    # Zwróć serię podporządkowanych nut względem podanej początkowej nuty
    return NOTES[note_pos + 1:] + NOTES[:note_pos + 1]

# Klasa Nuty (Note)
class Note(Surface):
    # Konstruktor klasy Nuty (Note)
    def __init__(self, note: str, surface_size: tuple[int, int]) -> None:
        # Wywołaj konstruktor nadrzędny powierzchni ze wsparciem dla kanału alpha
        super().__init__(surface_size, SRCALPHA)
        
        # Stała nazwa nuty
        self.note: Final[str] = note
        # Stały rozmiar powierzchni dla nuty
        self.size: Final[tuple[int, int]] = surface_size
        # Flaga 'active'
        #   Mówi czy powinna się renderować (Domyślnie False)
        #self.active: bool = False

        # Tekst przedni
        front_text = Label(self.note, (26, 'Arial', (255, 255, 255)))
        # Tekst tylny
        back_text = Label(self.note, (28, 'Arial', (0, 0, 0)))

        # Pobierz figurę kolizyjną z powierzchni klasy nadrzędnej
        self.rect = self.get_rect()
        # Ustaw pozycje figury kolizyjnej domyślnie na x: 0, y: 0
        self.rect.topleft = (0, 0)

        # Narysuj tekst tylny na środku powierzchni
        self.blit(back_text, ((self.size[0] - back_text.get_width()) // 2, (self.size[1] - back_text.get_height()) // 2))
        # Narysuj tekst przedni na środku powierzchni
        self.blit(front_text, ((self.size[0] - front_text.get_width()) // 2, (self.size[1] - front_text.get_height()) // 2))


# Klasa Struny (String)
class String(Surface):
    # Konstruktor klasy Struny (String)
    def __init__(self, inactive_symbol: Surface, string_tune: str, surface_size: tuple[int, int]) -> None:
        # Wywołaj konstruktor nadrzędny powierzchni ze wsparciem dla kanału alpha
        super().__init__(surface_size, SRCALPHA)

        # Ton struny
        self.tune: Final[str] = string_tune.upper()
        # Rozmiar powierzchni
        self.size: Final[tuple[int, int]] = surface_size
        # Lista nut
        self.notes: list[Note] = []
        # Lista nut, które mają być renderowane
        self.__notes_queue: list[Note] = []

        # Tabliczka z nazwą nuty tonu struny
        self.tune_info: Label = Label(self.tune, (24, 'Arial', (250, 250, 250)))
        # Powierzchnia dla informacji o tonie struny oraz czy ta struna nie jest grana
        self.string_info: Surface = Surface((32, 32), SRCALPHA)
        # Pobierz powierzchnię obrazu dla nieaktywnej struny z kanałej alpha (32x32) 
        self.inactive_string_symbol = inactive_symbol

        # Zmienna lokalna, która przechowuje rozmiary powierzchni dla nut
        note_widths = [70, 66, 64, 66, 64, 58, 52, 54, 52, 48, 44, 38, 36]
        # Zmienna lokalna, która przechowuje sumę poprzednich rozmiarów (z zmiennej powyżej)
        previous_widths_sum = 0
        # Zmienna lokalna, która przechowuje uporządkowane nuty
        ordered_notes = get_ordered_notes(self.tune)

        # Algorytm ustalania pozycji dla nut (które mają być w przyszłości wyświetlane)
        for i, note in enumerate(ordered_notes, 0):
            # Utwórz objekt klasy Note
            temp_note = Note(note, (note_widths[i], 32))
            # Przypisz korespondującą pozycję powierzchni nuty
            temp_note.rect.topleft = (previous_widths_sum, 0)

            # Zwiększ sumę o aktualną szerokość nuty
            previous_widths_sum += note_widths[i] + 8 # + 8 ponieważ grubość progów wynosi równe 8 [cm]

            # Dodaj objekt do zbioru nut
            self.notes.append(temp_note)
        
        # Flaga znalezienia przynajmniej jednej nuty w danym obrębie progów
        self.__found: bool = False
        # Zmienna, która przechowuje informacje o początku wyświetlania nut (w progach). Domyślnie wynosi 1 (od otwartej struny)
        self.__begin_at: int = 1
        # Zmienna, która przechowuje informacje o końcu wyświetlania nut (w progach). Domyślnie wynosi 12 (do oktawy tonu struny)
        self.__end_at: int = 12


    # Metoda, która pozwala na modyfikację początku jak i końcu wyświetlania nut (w progach)
    def change_frets_render(self, distance: tuple[int, int]) -> None:
        # Przypisz początkowy próg wyświetlania nut
        self.__begin_at = distance[0]
        # Przypisz końcowy próg wyświetlania nut
        self.__end_at = distance[1]

    # Metoda, która sprawdza czy istnieją podane nuty na strunie, oczywiście patrząc też na granice wyświetlania (początkowy i końcowy próg) 
    def queue_chord_notes(self, notes: list[str]) -> None:
        # Ustaw początkowo flagę znalezienia na False
        self.__found = False
        
        # Wyczyść początkowo listę nut do wyświetlenia
        self.__notes_queue.clear()

        # Przeiteruj listę objektów nut
        for note in self.notes:
            # Przechowaj w zmiennej lokalnej aktualną nazwę nuty
            current_note = note.note

            # Sprawdź czy aktualna nazwa nuty jest w liście nut akordu podanej przez użytkownika (notes)
            if current_note in notes:
                # Dodaj nutę do kolejki nut do wyświetlenia
                self.__notes_queue.append(note)

                # Ustaw flagę znalezienia na True
                self.__found = True
    
    # Metoda, która pozwala na aktualizacje stanu struny
    def update(self) -> None:
        # Wyczyść powierzchnię
        self.fill((0, 0, 0, 0))
        # Wyczyść powierzchnię informacji o strunie
        self.string_info.fill((0, 0, 0, 0))
        
        # Narysuj informację o tonie struny na powierzchni informacji o strunie (z wyśrodkowaniem)
        center_x: int = (self.string_info.get_width() - self.tune_info.get_width()) // 2
        center_y: int = (self.string_info.get_height() - self.tune_info.get_height()) // 2

        self.string_info.blit(self.tune_info, (center_x, center_y))

        # Sprawdź czy flaga znalezienia wynosi True
        if self.__found:
            # Utwórz powierzchnię dla nut
            temp_notes_surface: Surface = Surface((self.get_width() - 32, self.get_height()), SRCALPHA)
            # Algorytm renderowania nut
            for note in self.__notes_queue:
                temp_notes_surface.blit(note, note.rect.topleft)
            
            # Wyświetl powierzchnię dla nut
            self.blit(temp_notes_surface, (32, 0))
        else:
            # W przeciwnym razie, wyświetl tylko krzyżyk na tonie struny (sygnalizuje, że ta struna nie jest grana)
            self.string_info.blit(self.inactive_string_symbol, (0, 0))
        
        # Wyświetl informacje o strunie
        self.blit(self.string_info, (0, 0))


# Klasa gryfu (Fretboard)
class Fretboard(Surface):
    # Konstruktor klasy gryfu (Fretboard)
    def __init__(self, inactive_symbol: Surface, fretboard_background: Surface) -> None:
        # Wywołaj konstruktor nadrzędny powierzchni ze wsparciem dla kanału alpha
        super().__init__((fretboard_background.get_width() + 32, fretboard_background.get_height()), SRCALPHA)
        # Wypełnij powierzchnię
        self.fill((0, 0, 0))

        # Tło powierzchni
        self.bg: Final[Surface] = fretboard_background
        # Stała tonacja strun
        self.tuning: Final[str] = ['E', 'A', 'D', 'G', 'B', 'E']
        
        # Lista objektów String
        self.strings: list[String] = []

        # Szerokość strun
        self.string_width: Final[int] = self.bg.get_width()
        # Wysokość strun
        self.string_height: Final[int] = self.bg.get_height() // 6
        # Odstęp między strunami
        self.string_interline: Final[int] = round((self.bg.get_height() / 6) - self.string_height)

        inactive_string_symbol: Final[Surface] = inactive_symbol

        # Algorytm, który tworzy objekty strun i dodaje te objekty do listy strun
        for tune in self.tuning:
            # Utwórz objekt klasy String
            string_obj = String(inactive_string_symbol, tune, (self.string_width, self.string_height))

            # Przypisz objekt do listy strun
            self.strings.append(string_obj)
        
        # Wyświetl tło gryfu na x: 32, y: 0
        # self.blit(fretboard_background, (32, 0))
    
    # Metoda, która wyszuka możliwość wyświetlenia nut na strunie
    def queue_notes(self, notes: list[str]) -> None:
        # Przeiteruj struny
        for string in self.strings:
            # Zaktualizuj dane o oczekiwanych nutach
            string.queue_chord_notes(notes)

    # Metoda, która pozwala na modyfikacje wyświetlania nut (początkowy oraz końcowy próg)
    def set_render_distance(self, distance: tuple[int, int]) -> None:
        # Przeiteruj struny
        for string in self.strings:
            # Zaktualizuj dane o renderowaniu nut
            string.change_frets_render(distance)
    
    # Metoda, która pozwala na aktualizowanie stanu powierzchni
    def update(self) -> None:
        # Wyczyść powierzchnię
        self.fill((0, 0, 0, 0))
        # Rysuj tło
        self.blit(self.bg, (32, 0))

        # Renderuj każdą strunę
        for i, string in enumerate(self.strings, 0):
            # Jeżeli i jest większe od 0
            self.blit(string, (0, i * self.string_height + self.string_interline))

            # Wywołaj metodę update dla każdej struny
            string.update()