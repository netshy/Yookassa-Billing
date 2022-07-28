from faker import Faker
from faker.providers import address

fake = Faker()
fake.add_provider(address)


class FilmService:
    def get_film_name(self, film_id):
        return fake.city()
