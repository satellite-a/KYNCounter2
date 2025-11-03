from WindowMain import App
from CounterController import Counter, ConfigManager

if __name__ == '__main__':
    config_manager = ConfigManager()
    counter = Counter(config_manager)
    app = App(counter)
    app.mainloop()
