from pydantic import BaseSettings, Field
from app.db.dsn import generate_dsn_postgres


class Settings(BaseSettings):
    DB_USERNAME: str = Field(env='POSTGRES_USER')
    DB_PASSWORD: str = Field(env='POSTGRES_PASSWORD')
    DB_PORT: int = Field(env='POSTGRES_PORT')
    DB_HOST: str = Field(env='POSTGRES_HOST')
    DB_BASENAME: str = Field(env='POSTGRES_DB')

    JWT_SECRET: str = Field(
        env='JWT_SECRET', default="31f04487001ce91ec7c2fa1615fcd744614a3c4fda18f1ad"
        )
    JWT_ALGORITHM: str = Field(env='JWT_ALGORITHM', default="HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        env='JWT_ACCESS_TOKEN_EXPIRE_MINUTES', default=525600
        )

    BASE_DOMAIN: str = Field(env='BASE_DOMAIN', default='127.0.0.1:8000')
    MEDIA_URL: str = Field(env='MEDIA_URL', default='/api/v1/files/')

    @property
    def dsn(self):
        return generate_dsn_postgres(
            user=self.DB_USERNAME, password=self.DB_PASSWORD,
            host=self.DB_HOST, port=self.DB_PORT, database_name=self.DB_BASENAME
        )

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings_app = Settings()
