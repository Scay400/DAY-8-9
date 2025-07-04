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
game_state = "menu"  # menu, playing, settings_main, settings_in_game, exploded, instructions
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
        scaled_frame = pygame.transform.scale(frame, (FRAME_WIDTH * 4, FRAME_HEIGHT * 4))
        surface.blit(scaled_frame, (self.x, self.y - FRAME_HEIGHT))

# Класс клиента
class Klient():
    def __init__(self):
        self.gender = None
        self.gclothing = None
        self.clothing = None
        self.hair = None
        self.race = "human"
        self.skin = "standart"
        self.wish_text = None
        self.debuff_list = []
        self.bignose = False
        self.bigeye = False
        self.bigear = False
        
        self.randomize()
        
        # Спрайты клиента
        self.k_body = None
        self.k_clothing = None
        self.k_ear = None
        self.k_eye = None
        self.k_nose = None
        self.k_hair = None
        self.k_head = None
        
        self.create_sprites()
    
    def set_scale(self, sprite, scale):
        if not hasattr(sprite, 'original_image'):
            sprite.original_image = sprite.image
        
        original_rect = sprite.original_image.get_rect()
        new_width = int(original_rect.width * scale)
        new_height = int(original_rect.height * scale)
        
        scaled_image = pygame.transform.scale(sprite.original_image, (new_width, new_height))
        sprite.image = scaled_image
        sprite.rect = scaled_image.get_rect(center=sprite.rect.center)
    
    def get_fallback_sprite(self, path, default_path):
        try:
            return pg.AnimatedSprite(path, (38,65), (self.k_body.x, self.k_body.y))
        except:
            return pg.AnimatedSprite(default_path, (38,65), (self.k_body.x, self.k_body.y))
    
    def create_sprites(self):
        try:
            # Основные спрайты
            self.k_body = pg.AnimatedSprite('NPC/body.png', (38,65), (200, 400))
            
            # Голова (основа для позиционирования волос)
            head_path = f'NPC/heads/{self.skin}/{self.race}.png'
            default_head_path = f'NPC/heads/{self.skin}/human.png'
            self.k_head = self.get_fallback_sprite(head_path, default_head_path)
            
            # Одежда
            clothing_path = f'NPC/clothing/{self.gclothing}/{self.clothing}.png'
            self.k_clothing = pg.AnimatedSprite(clothing_path, (38,65), (self.k_body.x, self.k_body.y))
            
            # Уши
            ear_path = f'NPC/ears/{self.skin}/{self.race}.png'
            default_ear_path = f'NPC/ears/{self.skin}/human.png'
            self.k_ear = self.get_fallback_sprite(ear_path, default_ear_path)
            
            # Глаза
            eye_path = 'NPC/eyes/cock.png' if self.race == "cock" else 'NPC/eyes/human.png'
            self.k_eye = pg.AnimatedSprite(eye_path, (38,65), (self.k_body.x, self.k_body.y))
            
            # Нос
            if "goblin" in self.debuff_list:
                nose_path = 'NPC/noses/special/goblin.png'
            else:
                nose_path = f'NPC/noses/{self.skin}/{self.race}.png'
                default_nose_path = f'NPC/noses/{self.skin}/human.png'
                self.k_nose = self.get_fallback_sprite(nose_path, default_nose_path)
            
            # Волосы - позиционируем относительно головы
            if self.race == "human":
                hair_path = f'NPC/hair/{self.gender}/hear{random.randint(1, 3)}.png'
                self.k_hair = pg.AnimatedSprite(hair_path, (38,65), (self.k_head.x, self.k_head.y - 10))  # Смещение вверх
                
                # Подгоняем размер волос под размер головы
                if hasattr(self.k_head, 'rect') and hasattr(self.k_hair, 'rect'):
                    # Выравниваем по центру головы
                    self.k_hair.rect.centerx = self.k_head.rect.centerx
                    self.k_hair.rect.top = self.k_head.rect.top - 5  # Небольшое смещение вверх
            
            # Масштабирование
            scale_factor = 3.0
            for sprite in [self.k_body, self.k_clothing, self.k_head, self.k_ear, self.k_eye, self.k_nose, self.k_hair]:
                if sprite:
                    self.set_scale(sprite, scale_factor)
                    
            # Дополнительное масштабирование
            self.set_scale(self.k_nose, 3.5 if self.bignose else 3.0)
            self.set_scale(self.k_ear, 3.5 if self.bigear else 3.0)
            self.set_scale(self.k_eye, 3.5 if self.bigeye else 3.0)
            
        except Exception as e:
            print(f"Error loading sprite: {e}")
            self.create_fallback_sprites()
            
    def create_fallback_sprites(self):
        """Создает спрайты с использованием стандартных изображений при ошибках"""
        try:
            self.k_body = pg.AnimatedSprite('NPC/body.png', (38,65), (200, 400))
            self.k_head = pg.AnimatedSprite(f'NPC/heads/{self.skin}/human.png', (38,65), (self.k_body.x, self.k_body.y))
            self.k_clothing = pg.AnimatedSprite(f'NPC/clothing/{self.gclothing}/{self.clothing}.png', (38,65), (self.k_body.x, self.k_body.y))
            self.k_ear = pg.AnimatedSprite(f'NPC/ears/{self.skin}/human.png', (38,65), (self.k_body.x, self.k_body.y))
            self.k_eye = pg.AnimatedSprite('NPC/eyes/human.png', (38,65), (self.k_body.x, self.k_body.y))
            self.k_nose = pg.AnimatedSprite(f'NPC/noses/{self.skin}/human.png', (38,65), (self.k_body.x, self.k_body.y))
            
            if self.race == "human":
                self.k_hair = pg.AnimatedSprite(f'NPC/hair/{self.gender}/hear{random.randint(1, 3)}.png', (38,65), (self.k_body.x, self.k_body.y))
            else:
                self.k_hair = None
        except Exception as e:
            print(f"Critical error loading fallback sprites: {e}")
    
    def randomize(self):
        self.gender = random.choice(["male","female"])    
        self.debuff_list = []
        self.bignose = False
        self.bigeye = False
        self.bigear = False

        if self.gender == "male":
            self.gclothing = "male"
            self.clothing = random.choice(["suit","sportswear","casual"])
            self.hair = f"hear{random.randint(1, 3)}"
        else:
            self.gclothing = "female"
            self.clothing = random.choice(["dress","casual","casual2"])
            self.hair = f"hear{random.randint(1, 3)}"

        self.race = "human"
        self.skin = "standart"
        self.wish_text = None
    
    def apply_changes(self):
        # Сохраняем текущие параметры перед изменениями
        old_race = self.race
        old_skin = self.skin
        
        if "pig" in self.debuff_list:
            self.race = "pig"
        elif "ram" in self.debuff_list:
            self.race = "ram" 
        elif "cock" in self.debuff_list:
            self.race = "cock"   

        if "red" in self.debuff_list:
            self.skin = "red"
        elif "green" in self.debuff_list:
            self.skin = "green"
        elif "blue" in self.debuff_list:
            self.skin = "blue"
        elif "black" in self.debuff_list:
            self.skin = "black"
        elif "goblin" in self.debuff_list:
            self.skin = "green"

        self.bignose = "bignose" in self.debuff_list
        self.bigeye = "bigeye" in self.debuff_list
        self.bigear = "bigear" in self.debuff_list

        if "vampire" in self.debuff_list:
            self.gclothing = "special"
            self.clothing = "vampire"
        elif "werewolf" in self.debuff_list:
            self.gclothing = "special"
            self.clothing = "werewolf"
        elif "coconut" in self.debuff_list:
            self.gclothing = "special"
            self.clothing = "coconut"
        
        # Пересоздаем спрайты с новыми параметрами
        try:
            self.create_sprites()
        except:
            # Если не удалось создать спрайты с новыми параметрами, возвращаем старые
            self.race = old_race
            self.skin = old_skin
            self.create_sprites()
    
    def draw(self, surface):
        if not all([self.k_body, self.k_clothing, self.k_head, self.k_ear, self.k_eye, self.k_nose]):
            return
            
        surface.blit(self.k_body.image, self.k_body.rect)
        surface.blit(self.k_head.image, self.k_head.rect)
        surface.blit(self.k_clothing.image, self.k_clothing.rect)
        
        if self.race != "cock":
            surface.blit(self.k_ear.image, self.k_ear.rect)
            
        surface.blit(self.k_eye.image, self.k_eye.rect)
        surface.blit(self.k_nose.image, self.k_nose.rect)
        
        if self.race == "human" and self.k_hair:
            surface.blit(self.k_hair.image, self.k_hair.rect)
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
subtitle_texts = ["Подмешайте крысиный яд", "Добро Пожаловать в игру!","Не хотите попить кокосового молока?","also play MrFurry"]
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
            "settings_in_game": [],
            "instructions": []
        }
        self.invisible_buttons = []  # Для хранения невидимых кнопок
    
    def add_button(self, state, x, y, width, height, text, 
                  font_size=30, border_radius=10, 
                  callback=None, colors=None, effect_callback=None, invisible=False):
        """Добавляет новую кнопку в указанное состояние"""
        btn = pg.Button(x, y, width, height, text, 
                       border_radius=border_radius, 
                       font_size=font_size)
        
        if callback:
            btn.callback = callback
        
        btn.effect_callback = effect_callback
        btn.invisible = invisible  # Добавляем флаг невидимости
        
        if invisible:
            self.invisible_buttons.append(btn)
        else:
            self.buttons[state].append(btn)
        return btn

# Создаем менеджер кнопок
button_manager = ButtonManager()

# Создаем клиента
current_client = Klient()

# Функции для кнопок главного меню
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

def show_instructions():
    global game_state, previous_state
    previous_state = "menu"
    game_state = "instructions"
    print("Открыта инструкция")

# --- Эффекты для колбочек ---
def effect_hryu_hryu():
    if not "cock" in current_client.debuff_list and not "ram" in current_client.debuff_list and not "pig" in current_client.debuff_list and not "goblin" in current_client.debuff_list:
        current_client.debuff_list.append('pig')
    print("Колба Хряка/Превращает людей в свинок")

def effect_kukarek():
    if not "cock" in current_client.debuff_list and not "ram" in current_client.debuff_list and not "pig" in current_client.debuff_list and not "goblin" in current_client.debuff_list:
        current_client.debuff_list.append('cock')
    print("Колба Пташки/Превращает людей в петухов")

def effect_beee_beee():
    if not "cock" in current_client.debuff_list and not "ram" in current_client.debuff_list and not "pig" in current_client.debuff_list and not "goblin" in current_client.debuff_list:
        current_client.debuff_list.append('ram')
    print("Колба бэ-э-э/Превращает людей в баранов")

def effect_bigus_de_nous():
    if not "bignose" in current_client.debuff_list:
        current_client.debuff_list.append('bignose')
    print("Нос-великус/ Делает носы людей больше")

def effect_bigus_de_glazus():
    if not "bigeye" in current_client.debuff_list:
        current_client.debuff_list.append('bigeye')
    print("Глаза страха/ делает глаза людей больше")

def effect_bigus_de_ushes():
    if not "bigear" in current_client.debuff_list:
        current_client.debuff_list.append('bigear')
    print("Увелечение ушей/ делает уши людей больше")

def effect_de_greatus():
    if not "red" in current_client.debuff_list and not "green" in current_client.debuff_list and not "blue" in current_client.debuff_list and not "goblin" in current_client.debuff_list and not "black" in current_client.debuff_list:
        current_client.debuff_list.append('green')
    print("Зелёнка/ делает кожу зеленой")

def effect_de_krasnus():
    if not "red" in current_client.debuff_list and not "green" in current_client.debuff_list and not "blue" in current_client.debuff_list and not "goblin" in current_client.debuff_list and not "black" in current_client.debuff_list:
        current_client.debuff_list.append('red')
    print("Помидор/ делает кожу красной")

def effect_de_bluzes():
    if not "red" in current_client.debuff_list and not "green" in current_client.debuff_list and not "blue" in current_client.debuff_list and not "goblin" in current_client.debuff_list and not "black" in current_client.debuff_list:
        current_client.debuff_list.append('blue')
    print("Блю Баттерфляй/ делает кожу синей")

def effect_hop_hop_goblin():
    if not "red" in current_client.debuff_list and not "blue" in current_client.debuff_list and not "goblin" in current_client.debuff_list and not "black" in current_client.debuff_list:
        current_client.debuff_list.append('goblin')
    print("Гоблин колба/ делает из человека гоблина")

def effect_krovosos():
    if not "coconut" in current_client.debuff_list and not "werewolf" in current_client.debuff_list and not "vampire" in current_client.debuff_list:
        current_client.debuff_list.append('vampire')
    print("Дракула/ делает из человека вампира")

def effect_auuuuf():
    if not "coconut" in current_client.debuff_list and not "werewolf" in current_client.debuff_list and not "vampire" in current_client.debuff_list:
        current_client.debuff_list.append('werewolf')
    print("Полночь/ делает из человека оборотня")

def effect_coconat_milk():
    if not "coconut" in current_client.debuff_list and not "werewolf" in current_client.debuff_list and not "vampire" in current_client.debuff_list:
        current_client.debuff_list.append('coconut')
    print("Кокосовое Молоко/ делает из человека кокос")

def effect_temnaya():
    if not "red" in current_client.debuff_list and not "green" in current_client.debuff_list and not "blue" in current_client.debuff_list and not "goblin" in current_client.debuff_list and not "black" in current_client.debuff_list:
        current_client.debuff_list.append('black')
    print("Колба тёмности/ делает человека темнее")

def effect_slabaya():
    if not "poop" in current_client.debuff_list:
        current_client.debuff_list.append('poop')
    print("Колба поноса / Заставляет человека справить нужду прямо перед вами")

# Позиция Волтера (у стойки)
walter_x = 420
walter_y = 370
walter = WalterAnimation(walter_x, walter_y)

# Для хранения последнего эффекта, чтобы вызвать после анимации
last_effect_callback = None

# Функция запуска анимации наливания с эффектом
def play_pouring_with_effect(effect_callback):
    global animation_state, last_effect_callback
    if not walter.is_playing:
        animation_state = "pouring"
        last_effect_callback = effect_callback
        walter.play_animation("pouring", callback=on_pouring_finished)

def on_pouring_finished():
    global last_effect_callback
    print("Анимация наливания завершена")
    if last_effect_callback:
        last_effect_callback()
        last_effect_callback = None

def on_throw_bottle_finished():
    print("Анимация броска бутылки завершена")
    current_client.apply_changes()

def on_throw_bomb_finished():
    print("Анимация броска бомбы завершена")
    current_client.randomize()
    current_client.create_sprites()

def throw_bottle():
    global animation_state
    if len(current_client.debuff_list) > 0:
        if not walter.is_playing:
            animation_state = "throw_bottle"
            walter.play_animation("throw_bottle", callback=on_throw_bottle_finished)

def throw_bomb():
    global animation_state
    if not walter.is_playing:
        animation_state = "throw_bomb"
        walter.play_animation("throw_bomb", callback=on_throw_bomb_finished)

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
    text="Инструкция",
    font_size=40,
    border_radius=12,
    callback=show_instructions
)

button_manager.add_button(
    state="menu",
    x=game.width // 2 - 150,
    y=570,
    width=300,
    height=70,
    text="Выход",
    font_size=40,
    border_radius=12,
    callback=exit_game
)

# Список эффектов для каждой кнопки (по порядку)
effects_list = [
    effect_hryu_hryu,    # хрю-хрю (свинья)
    effect_kukarek,      # кукареку (петух)
    effect_beee_beee,    # беее (баран)
    effect_bigus_de_nous, # бигус де ноус (нос)
    effect_bigus_de_glazus, # бигус де глазус (глаза)
    effect_bigus_de_ushes, # бигус де ушес (уши)
    effect_de_krasnus,   # Де Краснус (красная кожа) - была на месте зелёной
    effect_de_greatus,   # Де Грейтус (зелёная кожа) - была на месте красной
    effect_de_bluzes,    # Де Блузес (синяя кожа)
    effect_hop_hop_goblin, # гоблин
    effect_krovosos,     # кровосос (вампир)
    effect_auuuuf,       # ауууф (оборотень)
    effect_temnaya,      # тёмная колба - была после COCONAT MILK
    effect_coconat_milk, # COCONAT MILK - была перед тёмной
    effect_slabaya       # слабая колба
]

# Тексты подсказок для эффектов (соответствуют новому порядку)
effects_tooltips = [
    ("Колба Хряков", "превращает людей в свинок"),
    ("Колба Кукареку", "превращает людей в петухов"),
    ("Колба бэ-э-э", "превращает людей в баранов"),
    ("Увеличение носа", "делает носы людей больше"),
    ("Увеличение глаз", "делает глаза людей больше"),
    ("Увеличение ушей", "делает уши людей больше"),
    ("Помидор", "делает кожу красной"),       # поменяли местами с зелёной
    ("Зелёнка", "делает кожу зеленой"),       # поменяли местами с красной
    ("БлюГай", "делает кожу синей"),
    ("Колба Гоблина", "делает из человека гоблина"),
    ("Дракула", "делает из человека вампира"),
    ("Проклятье Полночь", "делает из человека обортня"),
    ("Колба темноты", "делает человека темнее"),        # поменяли местами с COCONAT MILK
    ("Кокосовое Молоко", "делает из человека кокос"), # поменяли местами с тёмной
    ("Слабительное", "Заставит гостя справить нужду у вас на глазах")
]

action_buttons_positions = [
    624, 650, 677, 757, 784, 810, 890, 917, 943, 1024, 1050, 1077, 1152, 1178, 1205
]

# Кнопка "Кинуть напиток" (невидимая)
button_manager.add_button(
    state="playing",
    x=560,
    y=450,
    width=45,
    height=80,
    text="",  # Пустой текст
    font_size=25,
    border_radius=12,
    callback=throw_bottle,
    invisible=True  # Делаем кнопку невидимой
)

# Кнопка "Кинуть динамит" (невидимая)
button_manager.add_button(
    state="playing",
    x=1114,
    y=373,
    width=150,
    height=130,
    text="",  # Пустой текст
    font_size=25,
    border_radius=12,
    callback=throw_bomb,
    invisible=True  # Делаем кнопку невидимой
)

# Создаем игровые кнопки "Действие" (невидимые)
for idx, x_pos in enumerate(action_buttons_positions):
    effect_cb = effects_list[idx] if idx < len(effects_list) else None
    # Замыкание для корректной передачи функции
    def make_callback(effect_func):
        return lambda: play_pouring_with_effect(effect_func)
    button_manager.add_button(
        state="playing",
        x=x_pos,
        y=219,
        width=21,
        height=64,
        text="",  # Пустой текст
        callback=make_callback(effect_cb),
        effect_callback=effect_cb,
        invisible=True  # Делаем кнопку невидимой
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

# Кнопка "Назад" в инструкции
button_manager.add_button(
    state="instructions",
    x=game.width // 2 - 100,
    y=game.height - 100,
    width=200,
    height=50,
    text="Назад",
    font_size=30,
    border_radius=10,
    callback=back_to_menu_from_settings_main
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
            pygame.draw.rect(surface, base_color[:3], rect, border_radius=10)
            text_color = COLOR_DARK_GRAY if i == self.selected_index else COLOR_WHITE
            text_surf = self.font.render(self.options[i], True, text_color)
            text_rect = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect)

graphics_selector = GraphicsQualitySelector(game.width // 2 - 270, 420, graphics_quality_options, graphics_quality_index)

# Шрифт для подсказок
tooltip_font = pygame.font.SysFont(None, 24)

def update():
    global game_state, timer, bg_offset_x, volume, graphics_quality_index
    global subtitle_timer, current_subtitle_index

    delta = game.get_delta_time()

    # Обновляем кнопки для текущего состояния
    for btn in button_manager.buttons[game_state] + button_manager.invisible_buttons:
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

    elif game_state == "instructions":
        # Фон инструкции
        instructions_bg = pygame.Surface((game.width - 100, game.height - 100), pygame.SRCALPHA)
        instructions_bg.fill((0, 0, 0, 200))
        game.screen.blit(instructions_bg, (50, 50))
        
        # Заголовок инструкции
        instruction_title = pg.Text(game.width // 2, 80, "ИНСТРУКЦИЯ", size=60, color=COLOR_YELLOW)
        instruction_title.rect.centerx = game.width // 2
        draw_text_with_shadow(game.screen, instruction_title)
        
        # Текст инструкции
        instruction_lines = [
            "1. Используйте колбы для создания различных эффектов",
            "2. Нажимайте на колбы над стойкой для выбора колбы",
            "3. Нажмите на бутылку для того чтобы ее кинуть и для применения эффекта",
            "4. Используйте динамит для того чтобы убрать НПС",
            "5. ESC - открыть меню паузы",
            "",
            "Эффекты:",
            "- Хрю-хрю: превращает в свинок",
            "- Кукареку: превращает в петухов",
            "- Бигус де ноус: увеличивает носы",
            "и другие интересные эффекты!"
        ]
        
        y_offset = 150
        instruction_font = pygame.font.SysFont(None, 32)
        for line in instruction_lines:
            text_surf = instruction_font.render(line, True, COLOR_WHITE)
            game.screen.blit(text_surf, (100, y_offset))
            y_offset += 40

    elif game_state == "playing":
        game.screen.blit(background_img_game, (0, 0))
        info_font = pygame.font.SysFont(None, 28)
        info_text = info_font.render("Esc - открыть меню", True, COLOR_WHITE)
        game.screen.blit(info_text, (10, 10))

        # Рисуем Волтера
        walter.draw(game.screen)
        
        # Рисуем клиента
        current_client.draw(game.screen)

    # Отрисовываем кнопки для текущего состояния
    mouse_pos = pygame.mouse.get_pos()

    # Рисуем только видимые кнопки
    for btn in button_manager.buttons[game_state]:
        if not btn.invisible:  # Пропускаем невидимые кнопки
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

    # Отрисовка подсказки (tooltip) для невидимых кнопок "Действие" в игровом состоянии
    if game_state == "playing":
        for btn in button_manager.invisible_buttons:
            if btn.rect.collidepoint(mouse_pos):
                # Находим индекс кнопки в списке всех кнопок
                all_buttons = button_manager.buttons["playing"] + button_manager.invisible_buttons
                idx = all_buttons.index(btn)
                # Получаем соответствующую подсказку
                if idx-2 >= 0 and idx-2 < len(effects_tooltips):  # -2 сдвиг для первых двух кнопок
                    name, prop = effects_tooltips[idx-2]
                    draw_tooltip(game.screen, 10, 40, name, prop)
                break

def handle_event(event):
    global volume, graphics_quality_index, game_state

    # Обрабатываем все кнопки (видимые и невидимые)
    for btn in button_manager.buttons[game_state] + button_manager.invisible_buttons:
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
        elif game_state == "instructions":
            back_to_menu_from_settings_main()
        elif game_state == "menu":
            pass

game.add_event_callback(handle_event)

# Запуск игры
game.run(update, draw)
