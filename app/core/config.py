from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Микросервис по работе с VK'
    app_description: str = (
        'Микросервис предоставляет возможность '
        'получение информации по пользователю VK'
    )
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    client_id: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    db_host: str
    db_port: int

    class Config:
        env_file = '.env'


settings = Settings()
