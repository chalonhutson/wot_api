class Character:
    def __init__(self, name, title, race, homeland):
        self.name = name
        self.title = title
        self.race = race
        self.homeland = homeland

    def __repr__(self):
        return f"<Character Name={self.name}>"

wot_characters = (
    Character("Rand al-Thor", "The Dragon Reborn", "Human", "The Two Rivers"),
    Character("Moraine Damodred", "Aes Sedia", "Human", "Cairhien"),
    Character("Lan", "Warder", "Human", "Malkier"),
    Character("Loial", None, "Ogier", "Stedding Shangtai"),
    Character("Egwene al'Vere", None, "Human", "The Two Rivers"),
    Character("Nynaeve al'Meara", "Wisdom", "Human", "The Two Rivers"),
    Character("Thom Merrilin", "Gleeman", "Human", "Andor")
)