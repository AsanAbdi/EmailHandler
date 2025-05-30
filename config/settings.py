from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = 'password'
    POSTGRES_DB: str = "Database"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    DEBUG: bool = True
    SECRET_KEY: str = "secret-key"
    MAX_LIMIT: int = 50
    API_V1_STR: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 300
    
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f'postgresql+psycopg2://{self.POSTGRES_USER}:'
            f'{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:'
            f'{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )
    
    class Config:
        env_file = ".env"
    

settings = Settings()