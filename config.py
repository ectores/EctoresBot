import pandas as pd

class Config():
    def __init__(self):
        self.config_file = pd.read_json("config.json")
    
    def add_user(self, server_id, user_id, sound):
        self.server_id = str(server_id)
        self.user_id = str(user_id)
        self.sound = sound

        self.config_file["Information"]["Server"][self.server_id][self.user_id] = self.sound
        self.config_file.to_json("config.json")
    
    def search_sound(self, server_id, user_id):
        return self.config_file["Information"]["Server"][server_id][user_id]