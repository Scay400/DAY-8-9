import pygame
import pygine as pg
import random

# Инициализация игры
game = pg.Game(1280, 720, "Walter's Bar")

# Инициализация микшера для звука (лучше делать до загрузки музыки)
pygame.mixer.init()

# Загрузка и воспроизведение фоновой музыки для меню
pygame.mixer.music.load("crs.mp3")
pygame.mixer.music.set_volume(0.5)  # начальная громкость 50%
pygame.mixer.music.play(-1)  # -1 для бесконечного повторения

# Состояния игры
game_state = "menu"  # menu, playing, settings_main, settings_in_game, exploded
previous_state = None  # Для отслеживания откуда открыты настройки
timer = 5.0

# Цвета
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (100, 100, 100)
COLOR_DARK_GRAY = (50, 50, 50)
COLOR_BUTTON_NORMAL = (30, 30, 30)
COLOR_BUTTON_HOVER = (70, 70, 70)
COLOR_SLIDER_BG = (60, 60, 60)
COLOR_SLIDER_FG = (255, 215, 0)
COLOR_SHADOW = (0, 0, 0, 150)  # для тени
COLOR_TEXT_MENU = (162, 162, 208)

# Загрузка текстуры фона для меню
original_bg_img = pygame.image.load("background.png").convert()
background_img = pygame.transform.scale(original_bg_img, (game.width, game.height))
bg_offset_x = 0

# Загрузка текстуры фона для игры (playing)
original_bg_img_game = pygame.image.load("background1.png").convert()
background_img_game = pygame.transform.scale(original_bg_img_game, (game.width, game.height))

# Функция для отрисовки текста с тенью
def draw_text_with_shadow(surface, text_obj, shadow_offset=(2, 2), shadow_color=(0,0,0)):
    shadow_pos = (text_obj.rect.x + shadow_offset[0], text_obj.rect.y + shadow_offset[1])
    shadow_surf = text_obj.font.render(text_obj.text, True, shadow_color)
    surface.blit(shadow_surf, shadow_pos)
    text_obj.draw(surface)

# Текстовые элементы меню
menu_title = pg.Text(game.width // 2, 150, "Walter's Bar", size=100, color=COLOR_TEXT_MENU)
menu_title.rect.centerx = game.width // 2

# --- Добавлено: список "пасхалок" под заголовком ---
subtitle_texts = [
    "Подмешайте крысиный яд",
    "Привет"
]

current_subtitle_index = random.randint(0, len(subtitle_texts) - 1)
subtitle_timer = 0.0
subtitle_interval = 2.0  # менять текст каждые 2 секунды

# Кнопки главного меню
button_width = 300
button_height = 70
button_x = game.width // 2 - button_width // 2
button_y_start = 300
button_gap = 20

start_button = pg.Button(button_x, button_y_start, button_width, button_height, "Начать игру", border_radius=12, font_size=40)
settings_button = pg.Button(button_x, button_y_start + button_height + button_gap, button_width, button_height, "Настройки", border_radius=12, font_size=40)
exit_button = pg.Button(button_x, button_y_start + 2 * (button_height + button_gap), button_width, button_height, "Выход", border_radius=12, font_size=40)

# Кнопка назад в настройках (для settings_main)
back_button = pg.Button(50, game.height - 100, 150, 50, "Назад", border_radius=12, font_size=30)

# --- Новые кнопки для меню настроек в игре (settings_in_game) ---
resume_button = pg.Button(game.width // 2 - 150, 250, 300, 70, "Вернуться в игру", border_radius=12, font_size=40)
save_exit_button = pg.Button(game.width // 2 - 150, 340, 300, 70, "Сохранить и выйти", border_radius=12, font_size=40)
settings_in_game_button = pg.Button(game.width // 2 - 150, 430, 300, 70, "Настройки", border_radius=12, font_size=40)

# Настройки по умолчанию
volume = 0.5  # от 0.0 до 1.0
graphics_quality_options = ["Плохая", "Средняя", "Хорошая"]
graphics_quality_index = 1  # по умолчанию "Средняя"

# UI элементы меню и настроек
menu_ui = [start_button, settings_button, exit_button]
settings_main_ui = [back_button]
settings_in_game_ui = [resume_button, save_exit_button, settings_in_game_button]

# Функции кнопок главного меню
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
    # Возвращаемся в предыдущее состояние
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
    game_state = "settings_main"  # Открываем то же меню настроек, но с возвратом в игру
    print("Открыты настройки из игры")

def save_and_exit():
    # Здесь можно добавить сохранение прогресса, если нужно
    print("Сохранение и выход в меню")
    global game_state, previous_state
    game_state = "menu"
    previous_state = None

def exit_to_menu():
    print("Выход в главное меню")
    global game_state, previous_state
    game_state = "menu"
    previous_state = None

start_button.callback = start_game
settings_button.callback = open_settings_main
exit_button.callback = exit_game

back_button.callback = back_to_menu_from_settings_main

resume_button.callback = back_to_game_from_settings_in_game
save_exit_button.callback = save_and_exit
settings_in_game_button.callback = open_settings_in_game

# --- Реализация ползунка громкости ---

class VolumeSlider:
    def __init__(self, x, y, width, height, initial=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_radius = height // 2 + 2  # чуть больше для красоты
        self.handle_x = x + int(initial * width)
        self.handle_y = y + height // 2
        self.dragging = False
        self.value = initial  # 0.0 - 1.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.get_handle_rect().collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Ограничиваем движение по ширине слайдера
            new_x = max(self.rect.left, min(event.pos[0], self.rect.right))
            self.handle_x = new_x
            self.value = (self.handle_x - self.rect.left) / self.rect.width

    def get_handle_rect(self):
        return pygame.Rect(self.handle_x - self.handle_radius, self.handle_y - self.handle_radius,
                           self.handle_radius * 2, self.handle_radius * 2)

    def draw(self, surface):
        # Фон слайдера
        pygame.draw.rect(surface, COLOR_SLIDER_BG, self.rect, border_radius=self.rect.height // 2)
        # Заполненная часть - рисуем чуть шире, чтобы не было зазора под кружочком
        filled_width = self.handle_x - self.rect.left
        if filled_width > 0:
            filled_rect = pygame.Rect(self.rect.left, self.rect.top, filled_width, self.rect.height)
            pygame.draw.rect(surface, COLOR_SLIDER_FG, filled_rect, border_radius=self.rect.height // 2)
        # Тень под кружочком для глубины
        shadow_color = (0, 0, 0, 100)
        shadow_surf = pygame.Surface((self.handle_radius*2+6, self.handle_radius*2+6), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surf, shadow_color, (self.handle_radius+3, self.handle_radius+3), self.handle_radius+3)
        surface.blit(shadow_surf, (self.handle_x - self.handle_radius - 3, self.handle_y - self.handle_radius - 3))
        # Круглый ползунок
        pygame.draw.circle(surface, COLOR_YELLOW, (self.handle_x, self.handle_y), self.handle_radius)

volume_slider = VolumeSlider(game.width // 2 - 150, 300, 300, 30, initial=volume) 

# --- Переключатель качества графики ---

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
            # Если выбран - светлее желтый фон
            if i == self.selected_index:
                base_color = (255, 230, 100)
            # Тень для кнопок
            shadow_rect = rect.move(3, 3)
            pygame.draw.rect(surface, COLOR_DARK_GRAY, shadow_rect, border_radius=10)
            pygame.draw.rect(surface, base_color, rect, border_radius=10)
            text_color = COLOR_DARK_GRAY if i == self.selected_index else COLOR_WHITE
            text_surf = self.font.render(self.options[i], True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)

graphics_selector = GraphicsQualitySelector(game.width // 2 - 270, 420, graphics_quality_options, graphics_quality_index)

def update():
    global game_state, timer, bg_offset_x, volume, graphics_quality_index
    global subtitle_timer, current_subtitle_index

    delta = game.get_delta_time()

    if game_state == "menu":
        for element in menu_ui:
            element.update(delta)
        # Обновляем таймер для смены подзаголовка
        subtitle_timer += delta
        if subtitle_timer >= subtitle_interval:
            subtitle_timer = 0.0
            current_subtitle_index = (current_subtitle_index + 1) % len(subtitle_texts)

    elif game_state == "settings_main":
        for element in settings_main_ui:
            element.update(delta)

    elif game_state == "settings_in_game":
        for element in settings_in_game_ui:
            element.update(delta)

    # Обновляем смещение фона для движения
    bg_offset_x += 50 * delta
    if bg_offset_x > game.width:
        bg_offset_x -= game.width

    # Обновляем громкость музыки, если изменился volume_slider.value
    pygame.mixer.music.set_volume(volume_slider.value)

def draw():
    width = game.screen.get_width()
    height = game.screen.get_height()

    # Отрисовка двигающегося фона с повторением (меню)
    x = -bg_offset_x
    while x < width:
        game.screen.blit(background_img, (x, 0))
        x += width

    if game_state == "menu":
        # Отрисовка заголовка с тенью
        draw_text_with_shadow(game.screen, menu_title, shadow_offset=(3,3), shadow_color=(30,30,30))

        # Рисуем подзаголовок под заголовком
        subtitle_font = pygame.font.SysFont(None, 36)
        subtitle_text = subtitle_texts[current_subtitle_index]
        subtitle_surf_shadow = subtitle_font.render(subtitle_text, True, (30, 30, 30))
        subtitle_surf = subtitle_font.render(subtitle_text, True, COLOR_YELLOW)
        subtitle_rect = subtitle_surf.get_rect()
        subtitle_rect.centerx = game.width // 2
        subtitle_rect.top = menu_title.rect.bottom + 10  # чуть ниже заголовка

        # Сначала тень
        shadow_pos = (subtitle_rect.x + 2, subtitle_rect.y + 2)
        game.screen.blit(subtitle_surf_shadow, shadow_pos)
        # Потом текст
        game.screen.blit(subtitle_surf, subtitle_rect)

        # Отрисовка кнопок с эффектом наведения и тенью
        mouse_pos = pygame.mouse.get_pos()
        for button in menu_ui:
            hovered = button.rect.collidepoint(mouse_pos)
            base_color = COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON_NORMAL
            # Тень под кнопкой
            shadow_rect = button.rect.move(4, 4)
            pygame.draw.rect(game.screen, COLOR_DARK_GRAY, shadow_rect, border_radius=button.border_radius)
            pygame.draw.rect(game.screen, base_color, button.rect, border_radius=button.border_radius)
            button.draw(game.screen)

    elif game_state == "settings_main":
        # Заголовок настроек с тенью
        settings_title = pg.Text(game.width // 2, 100, "Настройки", size=72, color=COLOR_YELLOW)
        settings_title.rect.centerx = game.width // 2
        draw_text_with_shadow(game.screen, settings_title, shadow_offset=(3,3), shadow_color=(30,30,30))

        # Отрисовка слайдера громкости
        volume_label = pg.Text(game.width // 2, 260, f"Громкость: {int(volume_slider.value * 100)}%", size=32, color=COLOR_WHITE)
        volume_label.rect.centerx = game.width // 2
        draw_text_with_shadow(game.screen, volume_label, shadow_offset=(2,2), shadow_color=(20,20,20))
        volume_slider.draw(game.screen)

        # Отрисовка выбора качества графики
        graphics_label = pg.Text(game.width // 2, 380, "Качество графики:", size=32, color=COLOR_WHITE)
        graphics_label.rect.centerx = game.width // 2
        draw_text_with_shadow(game.screen, graphics_label, shadow_offset=(2,2), shadow_color=(20,20,20))
        graphics_selector.draw(game.screen)

        # Кнопка назад с тенью и эффектом наведения
        mouse_pos = pygame.mouse.get_pos()
        for button in settings_main_ui:
            hovered = button.rect.collidepoint(mouse_pos)
            base_color = COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON_NORMAL
            shadow_rect = button.rect.move(4, 4)
            pygame.draw.rect(game.screen, COLOR_DARK_GRAY, shadow_rect, border_radius=button.border_radius)
            pygame.draw.rect(game.screen, base_color, button.rect, border_radius=button.border_radius)
            button.draw(game.screen)

    elif game_state == "settings_in_game":
        # Заголовок меню настроек в игре
        settings_title = pg.Text(game.width // 2, 150, "Меню паузы", size=72, color=COLOR_YELLOW)
        settings_title.rect.centerx = game.width // 2
        draw_text_with_shadow(game.screen, settings_title, shadow_offset=(3,3), shadow_color=(30,30,30))

        mouse_pos = pygame.mouse.get_pos()
        for button in settings_in_game_ui:
            hovered = button.rect.collidepoint(mouse_pos)
            base_color = COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON_NORMAL
            shadow_rect = button.rect.move(4, 4)
            pygame.draw.rect(game.screen, COLOR_DARK_GRAY, shadow_rect, border_radius=button.border_radius)
            pygame.draw.rect(game.screen, base_color, button.rect, border_radius=button.border_radius)
            button.draw(game.screen)

    elif game_state == "playing":
        # Рисуем фон игры из background1.png
        game.screen.blit(background_img_game, (0, 0))

        # Инструкция: нажмите ESC для вызова меню паузы
        info_font = pygame.font.SysFont(None, 28)
        info_text = info_font.render("Нажмите ESC для вызова меню паузы", True, COLOR_WHITE)
        game.screen.blit(info_text, (10, 10))

def handle_event(event):
    global volume, graphics_quality_index, game_state

    if game_state == "menu":
        for element in menu_ui:
            element.handle_event(event)

    elif game_state == "settings_main":
        for element in settings_main_ui:
            element.handle_event(event)
        volume_slider.handle_event(event)
        graphics_selector.handle_event(event)
        # Обновляем значения настроек
        volume = volume_slider.value
        graphics_quality_index = graphics_selector.selected_index

    elif game_state == "settings_in_game":
        for element in settings_in_game_ui:
            element.handle_event(event)

    elif game_state == "playing":
        # В игре можно обрабатывать другие события
        pass

    # Обработка нажатия ESC
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        if game_state == "playing":
            # Открываем меню паузы
            global previous_state
            previous_state = "playing"
            game_state = "settings_in_game"
        elif game_state == "settings_in_game":
            # Возврат в игру
            back_to_game_from_settings_in_game()
        elif game_state == "settings_main":
            # Возврат в предыдущее состояние
            back_to_menu_from_settings_main()
        elif game_state == "menu":
            # Можно не делать ничего, чтобы не мигало меню
            pass

# Добавляем обработчик событий
game.add_event_callback(handle_event)

# Запуск игры
game.run(update, draw)
