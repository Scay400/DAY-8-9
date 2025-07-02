import pygame
import random
import pygine

wish_dict = {
    "текст1":["большой нос","сигма уй"],
    "текст2":["маленький нос","свинья"],
    "текст3":["ez","niga"],
}

# if "большой нос" in wish_dict[1]["текст который говорят"]:
#     print("ez")

class Klient():
    def __init__(self):
        self.gender = random.choice(["муж","жен"])    

        if self.gender == "муж":
            self.body = "муж"
            self.clothing = random.choice(["смокинг","спортивка","поседнев"])
            self.hair = random.choice(["короткая","средняя","длинная"])

        else:
            self.body = "жен"
            self.clothing = random.choice(["платье","спортивка","поседнев"])
            self.hair = random.choice(["карэ","средняя","длинная"])

        self.wish_text = None

        self.wish_text = random.choice(list(wish_dict.keys()))
        self.wish = wish_dict[self.wish_text]

    def print_info(self):
        print(self.gender,"\n",self.body,"\n",self.clothing,"\n",self.hair,"\n",self.wish_text,"\n",self.wish)

npc = Klient()

npc.print_info()