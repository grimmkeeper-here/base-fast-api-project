import os

import pytz
from pydantic import BaseSettings, PostgresDsn, RedisDsn

# Define
app_dir = os.path.dirname(os.path.dirname(__file__))
root_dir = app_dir + "/../.."


class Secrets(BaseSettings):
    DB_POSTGRES_DSN: PostgresDsn
    REDIS_DSN: RedisDsn
    AMPQ_DSN: str

    APP_ENV: str = "dev"

    class Config:
        env_file = ".env"
        case_sensitive = True

class Constants:
    # Base
    PROJECT_NAME: str = "Project Name"

    # Yoyo
    DB_LOCATION: str = f"{root_dir}/migrations"

    # logoru
    LOG_LEVEL: str = "INFO"

    # timezone
    TIMEZONE = pytz.timezone("Asia/Ho_Chi_Minh")


secrets = (
    Secrets(_env_file=f"{root_dir}/env/dev.env")
    if os.path.isfile(f"{root_dir}/env/dev.env")
    else Secrets()
)
constants = Constants()
