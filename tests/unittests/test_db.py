from gpm.fixtures import IntegrationTestFixture

from gpm.db.database import Database


class AClass:
    def __init__(self, variable):
        self.variable = variable


class DBTestCase(IntegrationTestFixture):
    def test_key_value_db(self):
        db = Database()
        db_second = Database()

        for i in range(100):
            db.store("test" + str(i), AClass("Some text" + str(i)))
            if i % 2 == 0:
                db_second.store("test" + str(i), AClass("Another text" + str(i)))

        for i in range(100):
            if i % 2 == 0:
                text = "Another text" + str(i)
            else:
                text = "Some text" + str(i)
            self.assertEqual(db.get("test" + str(i)).variable, text)
            self.assertEqual(db_second.get("test" + str(i)).variable, text)

    def test_pickled(self):
        db = Database()

        some_instance = AClass("Some content")

        key = db.store(some_instance)

        self.assertEqual(db.get(key).variable, some_instance.variable)

    def test_add(self):
        db = Database()

        some_instance = AClass("Some content")
        another_instance = AClass("Another content")

        db.add("a_key", some_instance)

        self.assertEqual(len(db.get("a_key")), 1)
        self.assertEqual(db.get("a_key")[0].variable, "Some content")

        db.add("a_key", another_instance)

        self.assertEqual(len(db.get("a_key")), 2)
        self.assertEqual(db.get("a_key")[0].variable, "Some content")
        self.assertEqual(db.get("a_key")[1].variable, "Another content")



