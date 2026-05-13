import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-prod")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-change-in-prod")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

    # Fix "postgres://" -> "postgresql://" for SQLAlchemy compatibility
    @staticmethod
    def fix_db_url(url):
        if url and url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql://", 1)
        return url


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = Config.fix_db_url(
        os.getenv("DATABASE_URL", "sqlite:///stack_battle_dev.db")
    )
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = Config.fix_db_url(os.getenv("DATABASE_URL"))
    DEBUG = False


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(env="development"):
    return config_map.get(env, DevelopmentConfig)
