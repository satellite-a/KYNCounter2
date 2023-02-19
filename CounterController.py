import json

class Counter():
    def __init__(self):
        self.count_win = 0
        self.count_lose = 0
        self.count_streak = 0
        self.record = []
        
        with open('conf/config.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            self.set_text_template(data["text_template"], mode=0)
            self.count_win = data["count"]["win"]
            self.count_lose = data["count"]["lose"]
            self.count_streak = data["count"]["streak"]


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
        with open('conf/config.json', "r", encoding="utf-8") as file:
            data = json.load(file)
        
        return data["text_template"]
    

    def set_text_template(self, value, mode=1):        
        # modeが0(=初回起動時)は書き込みを行わない
        if mode != 0:
            with open('conf/config.json', "r", encoding="utf-8") as file:
                data = json.load(file)
                
            data["text_template"] = value
            
            with open('conf/config.json', "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
    
    def update_count(self):        
        with open('conf/config.json', "r", encoding="utf-8") as file:
            data = json.load(file)
        
        data["count"]["win"] = self.count_win
        data["count"]["lose"] = self.count_lose
        data["count"]["streak"] = self.count_streak
        
        with open('conf/config.json', "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            
        with open('count.txt', 'w', encoding='utf-8') as file:
            file.write(self.get_text())