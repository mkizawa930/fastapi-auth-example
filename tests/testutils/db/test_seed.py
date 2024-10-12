from tests.testutils.db.seed import UserFactory


class Test_UserFactory:
    def test_create_users(self):
        factory = UserFactory
        users = factory.create_batch(5)
        assert len(users) == 5
