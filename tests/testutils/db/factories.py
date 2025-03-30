import factory
from faker import Faker

from app import models
from app.api.endpoints.auth_helper import PasswordHasher
from tests.helpers import get_random_string

Faker.seed(0)
faker = Faker("ja_JP")


class UserFactory(factory.Factory):
    class Meta:
        model = models.User

    username = factory.LazyFunction(lambda: faker.last_romanized_name().lower() + get_random_string(5))
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")

    @factory.lazy_attribute
    def username(obj):
        return faker.last_romanized_name() + get_random_string(5)

    @factory.lazy_attribute
    def email(obj):
        return

    @factory.lazy_attribute
    def password_hashed(obj):
        password = "password"
        hasher = PasswordHasher()
        return hasher.hash_password(password)
