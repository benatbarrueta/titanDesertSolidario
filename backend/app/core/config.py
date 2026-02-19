import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

SQLITE_DB_PATH = os.environ.get(
    "SQLITE_DB_PATH",
    os.path.join(BASE_DIR, "titanDB", "data", "titan_desert_solidario.db")
)
