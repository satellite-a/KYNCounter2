import json
import os

class ConfigManager:
    def __init__(self, config_path=os.path.join(os.path.expanduser("~"), ".kyncounter2", "config.json")):
        self.config_path = config_path
        self.data = self._load_config()

    def _load_config(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {
                "text_template": "$w勝 $l敗\n$s連勝中",
                "count": {
                    "win": 0,
                    "lose": 0,
                    "streak": 0
                }
            }
            conf_dir = os.path.dirname(self.config_path)
            if conf_dir and not os.path.exists(conf_dir):
                os.makedirs(conf_dir)
            with open(self.config_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        return data

    def save_config(self):
        with open(self.config_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.save_config()

    def get_count_data(self):
        return self.data["count"]

    def set_count_data(self, win, lose, streak):
        self.data["count"]["win"] = win
        self.data["count"]["lose"] = lose
        self.data["count"]["streak"] = streak
        self.save_config()



class Counter:
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        data = self.config_manager.data
        
        self.count_win = data["count"]["win"]
        self.count_lose = data["count"]["lose"]
        self.count_streak = data["count"]["streak"]
        self.record = []


    def win(self):
        self.append_record()
        self.count_win += 1
        self.count_streak += 1

    def lose(self):
        self.append_record()
        self.count_lose += 1
        self.count_streak = 0

    def clear(self):
        self.append_record()
        self.count_win = 0
        self.count_lose = 0
        self.count_streak = 0

    def rollback(self):
        record = self.pop_record()
        if record:
            self.count_win = record['win']
            self.count_lose = record['lose']
            self.count_streak = record['streak']

    def append_record(self):
        self.record.append(
            {'win': self.count_win, 'lose': self.count_lose,'streak': self.count_streak}
        )

    def pop_record(self):
        if self.record:
            return self.record.pop()
        return None


    def get_text(self):
        conversion_table = {"$w" : str(self.count_win), "$l": str(self.count_lose), "$s": str(self.count_streak)}
        text = self.get_text_template()
        
        for key,value in conversion_table.items():
            text = text.replace(key, value)
        
        return text
    
    def get_text_template(self):
        return self.config_manager.get("text_template")
    

    def set_text_template(self, value):
        self.config_manager.set("text_template", value)
    
    def update_count(self):
        self.config_manager.set_count_data(self.count_win, self.count_lose, self.count_streak)