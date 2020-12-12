import random


class MasterSlaveRouter:

    @staticmethod
    def db_for_read(model, **hints):
        return random.choice(['slave_1', 'slave_2', 'slave_3'])

    @staticmethod
    def db_for_write(model, **hints):
        return 'default'

    @staticmethod
    def allow_relation(obj1, obj2, **hints):
        return None

    @staticmethod
    def allow_migrate(db, app_label, model_name=None, **hints):
        return True
