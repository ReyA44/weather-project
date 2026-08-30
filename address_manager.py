import logging

logger = logging.getLogger(__name__)

class AddressManager:
    def __init__(self):
        self.addresses = []  # list of strings: ["Tel Aviv", "London"]

    def add(self, city):
        if not city or not isinstance(city, str):
            raise ValueError("Invalid city name")
        city = city.strip()
        if city not in self.addresses:
            self.addresses.append(city)
            logger.info("Added address: %s", city)
        return self.addresses

    def get_all(self):
        return self.addresses

    def delete(self, city):
        if city in self.addresses:
            self.addresses.remove(city)
            logger.info("Deleted address: %s", city)
            return True
        return False