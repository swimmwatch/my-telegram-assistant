"""
Database test utilities.
"""
from pathlib import Path

import alembic

from services.db.config import DatabaseSettings


def _upgrade_head(settings: DatabaseSettings, rootdir: str) -> None:
    """
    Upgrade the test database to head.

    :param settings: Database settings
    :param rootdir: Root project directory
    """
    config = alembic.config.Config()
    alembic_folder = Path(rootdir) / Path("src") / Path("migrations")
    config.set_main_option("script_location", str(alembic_folder))
    config.set_main_option("sqlalchemy.url", settings.url)

    # heads means all migrations from all branches (in case there are split branches)
    alembic.command.upgrade(config, "heads")
