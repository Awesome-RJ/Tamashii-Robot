class Config(object):
    LOGGER = True
    TOKEN = "1461817097:AAEPoSg4D1bg301iGH_wVOlKWfKuyIzSpSU"
    DB_URI = "postgresql://lirinun:Rajkumar27$@45.10.153.214:5432/lirinnm"
    OWNER_ID = 895373440


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
