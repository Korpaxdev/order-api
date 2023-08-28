from django.core import management

from backend.utils.price_file_utils import ids_to_string


def dump_data(table: str, output: str, **params):
    """Создает fixtures из переданной table"""
    for key in params:
        if key in ["pks", "primary_keys"]:
            params[key] = ids_to_string(params[key])
    management.call_command("dumpdata", table, output=output, **params)
    print(f"Dumped {table} to {output}")


def load_data(fixture: str):
    """Восстанавливает переданную fixture в бд"""
    management.call_command("loaddata", fixture)
    print(f"Load data from {fixture}")
