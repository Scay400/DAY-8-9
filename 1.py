import pygame
import pygine as pg
import random

# Инициализация игры
game = pg.Game(1280, 720, "Walter's Bar")

# Инициализация микшера для звука
pygame.mixer.init()

# Загрузка и воспроизведение фоновой музыки для меню
pygame.mixer.music.load("crs.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Состояния игры
game_state = "menu"  # menu, playing, settings_main, settings_in_game, exploded
previous_state = None
timer = 5.0

# Цвета
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (100, 100, 100)
COLOR_DARK_GRAY = (50, 50, 50)
COLOR_BUTTON_NORMAL = (30, 30, 30, 150)  # Добавлена прозрачность
COLOR_BUTTON_HOVER = (70, 70, 70, 150)   # Добавлена прозрачность
COLOR_SLIDER_BG = (60, 60, 60)
COLOR_SLIDER_FG = (255, 215, 0)
COLOR_SHADOW = (0, 0, 0, 150)
COLOR_TEXT_MENU = (162, 162, 208)
COLOR_TOOLTIP_BG = (30, 30, 30, 220)
COLOR_TOOLTIP_TEXT = (255, 255, 200)

# Загрузка текстур фона
original_bg_img = pygame.image.load("background.png").convert()
background_img = pygame.transform.scale(original_bg_img, (game.width, game.height))
original_bg_img_game = pygame.image.load("background1.png").convert()
background_img_game = pygame.transform.scale(original_bg_img_game, (game.width, game.height))
bg_offset_x = 0

# Загрузка спрайт-листа Волтера
walter_spritesheet_img = pygame.image.load("walter_sprites.png").convert_alpha()

# Размеры одного кадра на спрайт-листе
FRAME_WIDTH = 100
FRAME_HEIGHT = 100
SHEET_COLUMNS = 7  # 7 кадров в ряду
SHEET_ROWS = 3     # 3 ряда

# Функция для вырезки кадра из спрайт-листа
def get_frame(sheet, frame_index):
    col = frame_index % SHEET_COLUMNS
    row = frame_index // SHEET_COLUMNS
    rect = pygame.Rect(col * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT)
    frame = sheet.subsurface(rect)
    return frame

# Класс анимации Волтера
class WalterAnimation:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animations = {
            "idle": [0],  # стойка
            "pouring": [1, 2, 3, 4, 5, 6],
            "throw_bottle": [8, 9, 10, 11, 12, 13],
            "throw_bomb": [14, 15, 16, 17, 18, 19, 20, 21],
        }
        self.current_animation = "idle"
        self.current_frame_index = 0
        self.frame_timer = 0.0
        self.frame_duration = 0.1  # секунды на кадр
        self.is_playing = False
        self.callback_on_finish = None

    def play_animation(self, name, callback=None):
        if name not in self.animations:
            print(f"Animation '{name}' not found!")
            return
        self.current_animation = name
        self.current_frame_index = 0
        self.frame_timer = 0.0
        self.is_playing = True
        self.callback_on_finish = callback

    def update(self, delta):
        if not self.is_playing:
            return
        self.frame_timer += delta
        if self.frame_timer >= self.frame_duration:
            self.frame_timer -= self.frame_duration
            self.current_frame_index += 1
            if self.current_frame_index >= len(self.animations[self.current_animation]):
                # Анимация закончилась
                self.is_playing = False
                self.current_animation = "idle"
                self.current_frame_index = 0
                if self.callback_on_finish:
                    self.callback_on_finish()
                    self.callback_on_finish = None

    def draw(self, surface):
        frame_id = self.animations[self.current_animation][self.current_frame_index]
        frame = get_frame(walter_spritesheet_img, frame_id)
        scaled_frame = pygame.transform.scale(frame, (FRAME_WIDTH * 3, FRAME_HEIGHT * 3))
        surface.blit(scaled_frame, (self.x, self.y - FRAME_HEIGHT))


# Отрисовка текста с тенью
def draw_text_with_shadow(surface, text_obj, shadow_offset=(2, 2), shadow_color=(0,0,0)):
    shadow_pos = (text_obj.rect.x + shadow_offset[0], text_obj.rect.y + shadow_offset[1])
    shadow_surf = text_obj.font.render(text_obj.text, True, shadow_color)
    surface.blit(shadow_surf, shadow_pos)
    text_obj.draw(surface)

# Текстовые элементы меню
menu_title = pg.Text(game.width // 2, 150, "Walter's Bar", size=100, color=COLOR_TEXT_MENU)
menu_title.rect.centerx = game.width // 2

# Список "пасхалок" под заголовком
subtitle_texts = ["Подмешайте крысиный яд", "Привет"]
current_subtitle_index = random.randint(0, len(subtitle_texts) - 1)
subtitle_timer = 0.0
subtitle_interval = 2.0

# ========== УПРОЩЕННОЕ СОЗДАНИЕ КНОПОК ==========
class ButtonManager:
    def __init__(self):
        self.buttons = {
            "menu": [],
            "playing": [],
            "settings_main": [],
            "settings_in_game": []
        }
    
    def add_button(self, state, x, y, width, height, text, 
                  font_size=30, border_radius=10, 
                  callback=None, colors=None):
        """Добавляет новую кнопку в указанное состояние"""
        btn = pg.Button(x, y, width, height, text, 
                       border_radius=border_radius, 
                       font_size=font_size)
        
        if callback:
            btn.callback = callback
        
        self.buttons[state].append(btn)
        return btn

# Создаем менеджер кнопок
button_manager = ButtonManager()

# Функции для кнопок
def start_game():
    global game_state, timer
    game_state = "playing"
    timer = 5.0
    print("Игра началась!")

def open_settings_main():
    global game_state, previous_state
    previous_state = "menu"
    game_state = "settings_main"
    print("Открыты настройки из главного меню")

def exit_game():
    pygame.quit()
    exit()

def back_to_menu_from_settings_main():
    global game_state, previous_state
    if previous_state == "settings_in_game" or previous_state == "playing":
        game_state = "settings_in_game" if previous_state == "settings_in_game" else "playing"
    else:
        game_state = "menu"
    previous_state = None

def back_to_game_from_settings_in_game():
    global game_state
    game_state = "playing"

def open_settings_in_game():
    global game_state, previous_state
    previous_state = "settings_in_game"
    game_state = "settings_main"
    print("Открыты настройки из игры")

def save_and_exit():
    print("Сохранение и выход в меню")
    global game_state, previous_state
    game_state = "menu"
    previous_state = None

# ========== СОЗДАЕМ КНОПКИ ПРОСТО И УДОБНО ==========
# Главное меню
button_manager.add_button(
    state="menu",
    x=game.width // 2 - 150,
    y=300,
    width=300,
    height=70,
    text="Начать игру",
    font_size=40,
    border_radius=12,
    callback=start_game
)

button_manager.add_button(
    state="menu",
    x=game.width // 2 - 150,
    y=390,
    width=300,
    height=70,
    text="Настройки",
    font_size=40,
    border_radius=12,
    callback=open_settings_main
)

button_manager.add_button(
    state="menu",
    x=game.width // 2 - 150,
    y=480,
    width=300,
    height=70,
    text="Выход",
    font_size=40,
    border_radius=12,
    callback=exit_game
)

# Игровые кнопки (прозрачные)
button_manager.add_button(
    state="playing",
    x=624,
    y=219,
    width=21,
    height=64,
    text="Действие 1",
    callback=lambda: print("Выполняется действие 1")
)

button_manager.add_button(
    state="playing",
    x=650,
    y=219,
    width=21,
    height=64,
    text="Действие 2",
    callback=lambda: print("Выполняется действие 2")
)

button_manager.add_button(
    state="playing",
    x=677,
    y=219,
    width=21,
    height=64,
    text="Действие 3",
    callback=lambda: print("Выполняется действие 3")
)

button_manager.add_button(
    state="playing",
    x=757,
    y=219,
    width=21,
    height=64,
    text="Действие 4",
    callback=lambda: print("Выполняется действие 4")
)

button_manager.add_button(
    state="playing",
    x=784,
    y=219,
    width=21,
    height=64,
    text="Действие 4",
    callback=lambda: print("Выполняется действие 4")
)

button_manager.add_button(
    state="playing",
    x=810,
    y=219,
    width=21,
    height=64,
    text="Действие 4",
    callback=lambda: print("Выполняется действие 4")
)

button_manager.add_button(
    state="playing",
    x=890,
    y=219,
    width=21,
    height=64,
    text="Действие 4",
    callback=lambda: print("Выполняется действие 4")
)

button_manager.add_button(
    state="playing",
    x=917,
    y=219,
    width=21,
    height=64,
    text="Действие 4",
    callback=lambda: print("Выполняется действие 4")
)

button_manager.add_button(
    state="playing",
    x=943,
    y=219,
    width=21,
    height=64,
    text="Действие 4",
    callback=lambda: print("Выполняется действие 4")
)

button_manager.add_button(
    state="playing",
    x=1024,
    y=219,
    width=21,
    height=64,
    text="Действие 4",
    callback=lambda: print("Выполняется действие 4")
)

button_manager.add_button(
    state="playing",
    x=1050,
    y=219,
    width=21,
    height=64,
    text="Действие 4",
    callback=lambda: print("Выполняется действие 4")
)

button_manager.add_button(
    state="playing",
    x=1077,
    y=219,
    width=21,
    height=64,
    text="Действие 4",
    callback=lambda: print("Выполняется действие 4")
)

button_manager.add_button(
    state="playing",
    x=1152,
    y=219,
    width=21,
    height=64,
    text="Действие 4",
    callback=lambda: print("Выполняется действие 4")
)

button_manager.add_button(
    state="playing",
    x=1178,
    y=219,
    width=21,
    height=64,
    text="Действие 4",
    callback=lambda: print("Выполняется действие 4")
)

button_manager.add_button(
    state="playing",
    x=1205,
    y=219,
    width=21,
    height=64,
    text="Действие 4",
    callback=lambda: print("Выполняется действие 4")
)

# Кнопки для меню настроек
button_manager.add_button(
    state="settings_main",
    x=50,
    y=game.height - 100,
    width=150,
    height=50,
    text="Назад",
    font_size=30,
    border_radius=12,
    callback=back_to_menu_from_settings_main
)

button_manager.add_button(
    state="settings_in_game",
    x=game.width // 2 - 150,
    y=250,
    width=300,
    height=70,
    text="Вернуться в игру",
    font_size=40,
    border_radius=12,
    callback=back_to_game_from_settings_in_game
)

button_manager.add_button(
    state="settings_in_game",
    x=game.width // 2 - 150,
    y=340,
    width=300,
    height=70,
    text="Сохранить и выйти",
    font_size=40,
    border_radius=12,
    callback=save_and_exit
)

button_manager.add_button(
    state="settings_in_game",
    x=game.width // 2 - 150,
    y=430,
    width=300,
    height=70,
    text="Настройки",
    font_size=40,
    border_radius=12,
    callback=open_settings_in_game
)

# Настройки по умолчанию
volume = 0.5
graphics_quality_options = ["Плохая", "Средняя", "Хорошая"]
graphics_quality_index = 1

# Реализация ползунка громкости
class VolumeSlider:
    def __init__(self, x, y, width, height, initial=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_radius = height // 2 + 2
        self.handle_x = x + int(initial * width)
        self.handle_y = y + height // 2
        self.dragging = False
        self.value = initial

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.get_handle_rect().collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_x = max(self.rect.left, min(event.pos[0], self.rect.right))
            self.handle_x = new_x
            self.value = (self.handle_x - self.rect.left) / self.rect.width

    def get_handle_rect(self):
        return pygame.Rect(self.handle_x - self.handle_radius, self.handle_y - self.handle_radius,
                         self.handle_radius * 2, self.handle_radius * 2)

    def draw(self, surface):
        pygame.draw.rect(surface, COLOR_SLIDER_BG, self.rect, border_radius=self.rect.height // 2)
        filled_width = self.handle_x - self.rect.left
        if filled_width > 0:
            filled_rect = pygame.Rect(self.rect.left, self.rect.top, filled_width, self.rect.height)
            pygame.draw.rect(surface, COLOR_SLIDER_FG, filled_rect, border_radius=self.rect.height // 2)
        shadow_color = (0, 0, 0, 100)
        shadow_surf = pygame.Surface((self.handle_radius*2+6, self.handle_radius*2+6), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surf, shadow_color, (self.handle_radius+3, self.handle_radius+3), self.handle_radius+3)
        surface.blit(shadow_surf, (self.handle_x - self.handle_radius - 3, self.handle_y - self.handle_radius - 3))
        pygame.draw.circle(surface, COLOR_YELLOW, (self.handle_x, self.handle_y), self.handle_radius)

volume_slider = VolumeSlider(game.width // 2 - 150, 300, 300, 30, initial=volume)

# Переключатель качества графики
class GraphicsQualitySelector:
    def __init__(self, x, y, options, selected_index=1):
        self.x = x
        self.y = y
        self.options = options
        self.selected_index = selected_index
        self.font = pygame.font.SysFont(None, 36)
        self.option_rects = []
        self.create_option_rects()

    def create_option_rects(self):
        self.option_rects = []
        spacing = 180
        start_x = self.x
        for i, option in enumerate(self.options):
            rect = pygame.Rect(start_x + i * spacing, self.y, 160, 50)
            self.option_rects.append(rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(pos):
                    self.selected_index = i
                    print(f"Выбрано качество графики: {self.options[i]}")

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.option_rects):
            hovered = rect.collidepoint(mouse_pos)
            base_color = COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON_NORMAL
            if i == self.selected_index:
                base_color = (255, 230, 100)
            shadow_rect = rect.move(3, 3)
            pygame.draw.rect(surface, COLOR_DARK_GRAY, shadow_rect, border_radius=10)
            pygame.draw.rect(surface, base_color, rect, border_radius=10)
            text_color = COLOR_DARK_GRAY if i == self.selected_index else COLOR_WHITE
            text_surf = self.font.render(self.options[i], True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)

graphics_selector = GraphicsQualitySelector(game.width // 2 - 270, 420, graphics_quality_options, graphics_quality_index)

# --- Новое: Класс для колбочек (пробирок) с подсказками ---
class Flask:
    def __init__(self, x, y, width, height, name, property_text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.property_text = property_text
        self.color = color  # для отрисовки колбы (цвет)
        self.hovered = False

    def draw(self, surface):
        # Отрисовка колбы (простой прямоугольник с цветом)
        pygame.draw.rect(surface, self.color, self.rect, border_radius=6)
        # Нарисуем "горлышко" колбы (узкий прямоугольник сверху)
        neck_rect = pygame.Rect(self.rect.centerx - self.rect.width // 6, self.rect.top - self.rect.height // 4, self.rect.width // 3, self.rect.height // 4)
        pygame.draw.rect(surface, self.color, neck_rect, border_radius=4)

    def is_hovered(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered

# --- Создаем колбочки ---
flasks = [
    Flask(50, 600, 40, 60, "Яд крысы", "Отравляет гостя", (180, 0, 0)),
    Flask(110, 600, 40, 60, "Успокоительное", "Снижает агрессию", (0, 180, 180)),
    Flask(170, 600, 40, 60, "Эликсир силы", "Увеличивает силу", (0, 180, 0)),
]

# --- Текст для подсказки ---
tooltip_font = pygame.font.SysFont(None, 28)

# --- Кнопки для анимаций Волтера ---
# Позиция Волтера (у стойки)
walter_x = 470
walter_y = 420

walter = WalterAnimation(walter_x, walter_y)

# Состояния анимаций
animation_state = "idle"  # idle, pouring, throw_bottle, throw_bomb

# Функции для кнопок анимаций
def on_pouring_finished():
    print("Анимация наливания завершена")

def on_throw_bottle_finished():
    print("Анимация броска бутылки завершена")

def on_throw_bomb_finished():
    print("Анимация броска бомбы завершена")

def start_pouring():
    global animation_state
    if not walter.is_playing:
        animation_state = "pouring"
        walter.play_animation("pouring", callback=on_pouring_finished)

def throw_bottle():
    global animation_state
    if not walter.is_playing:
        animation_state = "throw_bottle"
        walter.play_animation("throw_bottle", callback=on_throw_bottle_finished)

def throw_bomb():
    global animation_state
    if not walter.is_playing:
        animation_state = "throw_bomb"
        walter.play_animation("throw_bomb", callback=on_throw_bomb_finished)

# Кнопки для управления анимациями (игровое состояние)
button_manager.add_button(
    state="playing",
    x=50,
    y=520,
    width=160,
    height=50,
    text="Налить пробирку",
    font_size=24,
    border_radius=12,
    callback=start_pouring
)

button_manager.add_button(
    state="playing",
    x=50,
    y=580,
    width=160,
    height=50,
    text="Бросить бутылку",
    font_size=24,
    border_radius=12,
    callback=throw_bottle
)

button_manager.add_button(
    state="playing",
    x=50,
    y=640,
    width=160,
    height=50,
    text="Бросить бомбу",
    font_size=24,
    border_radius=12,
    callback=throw_bomb
)

def update():
    global game_state, timer, bg_offset_x, volume, graphics_quality_index
    global subtitle_timer, current_subtitle_index

    delta = game.get_delta_time()

    # Обновляем кнопки для текущего состояния
    for btn in button_manager.buttons[game_state]:
        btn.update(delta)

    if game_state == "menu":
        subtitle_timer += delta
        if subtitle_timer >= subtitle_interval:
            subtitle_timer = 0.0
            current_subtitle_index = (current_subtitle_index + 1) % len(subtitle_texts)

    bg_offset_x += 50 * delta
    if bg_offset_x > game.width:
        bg_offset_x -= game.width

    pygame.mixer.music.set_volume(volume_slider.value)

    # Обновляем анимацию Волтера если в игре
    if game_state == "playing":
        walter.update(delta)

def draw_tooltip(surface, x, y, name, property_text):
    padding = 8
    # Рендерим текст
    name_surf = tooltip_font.render(name, True, COLOR_TOOLTIP_TEXT)
    prop_surf = tooltip_font.render(property_text, True, COLOR_TOOLTIP_TEXT)
    width = max(name_surf.get_width(), prop_surf.get_width()) + padding * 2
    height = name_surf.get_height() + prop_surf.get_height() + padding * 3

    # Создаем фон с прозрачностью
    bg_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(bg_surf, COLOR_TOOLTIP_BG, (0, 0, width, height), border_radius=8)

    # Рисуем текст на фоне
    bg_surf.blit(name_surf, (padding, padding))
    bg_surf.blit(prop_surf, (padding, padding + name_surf.get_height() + padding // 2))

    # Отрисовываем на основном surface
    surface.blit(bg_surf, (x, y))

def draw():
    width = game.screen.get_width()
    height = game.screen.get_height()

    # Отрисовка фона
    x = -bg_offset_x
    while x < width:
        game.screen.blit(background_img, (x, 0))
        x += width

    if game_state == "menu":
        draw_text_with_shadow(game.screen, menu_title, shadow_offset=(3,3), shadow_color=(30,30,30))

        subtitle_font = pygame.font.SysFont(None, 36)
        subtitle_text = subtitle_texts[current_subtitle_index]
        subtitle_surf_shadow = subtitle_font.render(subtitle_text, True, (30, 30, 30))
        subtitle_surf = subtitle_font.render(subtitle_text, True, COLOR_YELLOW)
        subtitle_rect = subtitle_surf.get_rect()
        subtitle_rect.centerx = game.width // 2
        subtitle_rect.top = menu_title.rect.bottom + 10

        game.screen.blit(subtitle_surf_shadow, (subtitle_rect.x + 2, subtitle_rect.y + 2))
        game.screen.blit(subtitle_surf, subtitle_rect)

    elif game_state == "settings_main":
        settings_title = pg.Text(game.width // 2, 100, "Настройки", size=72, color=COLOR_YELLOW)
        settings_title.rect.centerx = game.width // 2
        draw_text_with_shadow(game.screen, settings_title, shadow_offset=(3,3), shadow_color=(30,30,30))

        volume_label = pg.Text(game.width // 2, 260, f"Громкость: {int(volume_slider.value * 100)}%", size=32, color=COLOR_WHITE)
        volume_label.rect.centerx = game.width // 2
        draw_text_with_shadow(game.screen, volume_label, shadow_offset=(2,2), shadow_color=(20,20,20))
        volume_slider.draw(game.screen)

        graphics_label = pg.Text(game.width // 2, 380, "Качество графики:", size=32, color=COLOR_WHITE)
        graphics_label.rect.centerx = game.width // 2
        draw_text_with_shadow(game.screen, graphics_label, shadow_offset=(2,2), shadow_color=(20,20,20))
        graphics_selector.draw(game.screen)

    elif game_state == "settings_in_game":
        settings_title = pg.Text(game.width // 2, 150, "Меню паузы", size=72, color=COLOR_YELLOW)
        settings_title.rect.centerx = game.width // 2
        draw_text_with_shadow(game.screen, settings_title, shadow_offset=(3,3), shadow_color=(30,30,30))

    elif game_state == "playing":
        game.screen.blit(background_img_game, (0, 0))
        info_font = pygame.font.SysFont(None, 28)
        info_text = info_font.render("Нажмите ESC для вызова меню паузы", True, COLOR_WHITE)
        game.screen.blit(info_text, (10, 10))

        # Рисуем Волтера
        walter.draw(game.screen)

        # Рисуем колбочки
        mouse_pos = pygame.mouse.get_pos()
        hovered_flask = None
        for flask in flasks:
            flask.draw(game.screen)
            if flask.is_hovered(mouse_pos):
                hovered_flask = flask

        # Отрисовка подсказки (если есть наведенная колба)
        if hovered_flask:
            # Рисуем поле с названием и свойством чуть выше колбы
            tooltip_x = hovered_flask.rect.x
            tooltip_y = hovered_flask.rect.y - 60
            draw_tooltip(game.screen, tooltip_x, tooltip_y, hovered_flask.name, hovered_flask.property_text)

    # Отрисовываем кнопки для текущего состояния
    mouse_pos = pygame.mouse.get_pos()
    for btn in button_manager.buttons[game_state]:
        hovered = btn.rect.collidepoint(mouse_pos)
        
        # Для игрового режима используем прозрачные цвета
        if game_state == "playing":
            base_color = COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON_NORMAL
            shadow_color = (0, 0, 0, 50)  # Прозрачная тень
        else:
            base_color = (COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON_NORMAL)[:3]  # Без прозрачности
            shadow_color = COLOR_DARK_GRAY
        
        # Тень
        shadow_rect = btn.rect.move(4, 4)
        shadow_surf = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, shadow_color, (0, 0, shadow_rect.width, shadow_rect.height), 
                        border_radius=btn.border_radius)
        game.screen.blit(shadow_surf, shadow_rect)
        
        # Основная кнопка
        btn_surf = pygame.Surface((btn.rect.width, btn.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(btn_surf, base_color, (0, 0, btn.rect.width, btn.rect.height), 
                        border_radius=btn.border_radius)
        game.screen.blit(btn_surf, btn.rect)
        
        # Текст кнопки
        btn.draw(game.screen)

def handle_event(event):
    global volume, graphics_quality_index, game_state

    # Обрабатываем кнопки для текущего состояния
    for btn in button_manager.buttons[game_state]:
        btn.handle_event(event)

    if game_state == "settings_main":
        volume_slider.handle_event(event)
        graphics_selector.handle_event(event)
        volume = volume_slider.value
        graphics_quality_index = graphics_selector.selected_index

    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        if game_state == "playing":
            global previous_state
            previous_state = "playing"
            game_state = "settings_in_game"
        elif game_state == "settings_in_game":
            back_to_game_from_settings_in_game()
        elif game_state == "settings_main":
            back_to_menu_from_settings_main()
        elif game_state == "menu":
            pass

game.add_event_callback(handle_event)

# Запуск игры
game.run(update, draw)
