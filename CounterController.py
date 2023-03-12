import json
import os

class Singleton(object):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

class Counter(Singleton):
    
    def __init__(self):
        data = self._get_json_data()
        
        self.set_text_template(data["text_template"])
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
        # TODO ロールバック処理を行う
        try:
            record = self.pop_record()
        except:
            # popできるレコードが無かった場合、特に何も起こさない
            pass
        else:
            self.count_win = record['win']
            self.count_lose = record['lose']
            self.count_streak = record['streak']

    def append_record(self):
        self.record.append(
            {'win': self.count_win, 'lose': self.count_lose,'streak': self.count_streak}
        )

    def pop_record(self):
        try:
            return self.record.pop()
        except:
            raise Exception()


    def get_text(self):
        conversion_table = {"$w" : str(self.count_win), "$l": str(self.count_lose), "$s": str(self.count_streak)}
        text = self.get_text_template()
        
        for key,value in conversion_table.items():
            text = text.replace(key, value)
        
        return text
    
    def get_text_template(self):
        data = self._get_json_data()
        
        return data["text_template"]
    

    def set_text_template(self, value):
        data = self._get_json_data()
                            
        data["text_template"] = value
        
        with open('conf/config.json', "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    
    def update_count(self):
        data = self._get_json_data()
        
        data["count"]["win"] = self.count_win
        data["count"]["lose"] = self.count_lose
        data["count"]["streak"] = self.count_streak
        
        with open('conf/config.json', "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            
        with open('count.txt', 'w', encoding='utf-8') as file:
            file.write(self.get_text())
    
    def _get_json_data(self):        
        try:
            with open('conf/config.json', "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("filenotfounderror")
            data = {
                "text_template": "$w勝 $l敗\n$s連勝中",
                "count": {
                    "win": 0,
                    "lose": 0,
                    "streak": 0
                }
            }
            
            conf_dir = 'conf'
            if not os.path.exists(conf_dir):
                os.makedirs(conf_dir)
            
            with open('conf/config.json', "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        
        return data