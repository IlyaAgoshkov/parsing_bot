import asyncio
import json

DATA_FILE = 'vanek.json'


def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'streamers': {}, 'min_percent': 0, 'max_percent': 100, 'monitoring_active': False}
    except json.JSONDecodeError:
        print("Ошибка чтения файла данных. Использование начальных значений.")
        return {'streamers': {}, 'min_percent': 0, 'max_percent': 100, 'monitoring_active': False}


def save_data(data):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")


class StreamerManager:
    def __init__(self):
        self.data = load_data()
        self.streamers = self.data.get('streamers', {})
        self.min_percent = self.data.get('min_percent', 0)
        self.max_percent = self.data.get('max_percent', 100)
        self.monitoring_active = self.data.get('monitoring_active', False)

    def load_data(self):
        self.data = load_data()
        self.streamers = self.data.get('streamers', {})
        self.min_percent = self.data.get('min_percent', 0)
        self.max_percent = self.data.get('max_percent', 100)

    def add_streamer(self, channel_name):
        self.streamers[channel_name] = {"percent": 0}
        self.save()

    def remove_streamer(self, channel_name):
        del self.streamers[channel_name]
        self.save()
        self.load_data()

    def set_min_percent(self, percent):
        self.min_percent = percent
        self.save()
        self.load_data()

    def set_max_percent(self, percent):
        self.max_percent = percent
        self.save()
        self.load_data()

    def set_monitoring_active(self, active):
        self.monitoring_active = active
        self.save()
        self.load_data()

    def is_monitoring_active(self):
        return self.monitoring_active

    def get_streamers(self):
        return self.streamers

    def update_percent(self, channel_name, percent):
        if channel_name in self.streamers:
            self.streamers[channel_name]["percent"] = percent
            self.save()
        else:
            return 0

    def save(self):
        self.data['streamers'] = self.streamers
        self.data['min_percent'] = self.min_percent
        self.data['max_percent'] = self.max_percent
        self.data['monitoring_active'] = self.monitoring_active
        save_data(self.data)
        self.load_data()

    async def save_async(self):
        await asyncio.to_thread(self.save)
