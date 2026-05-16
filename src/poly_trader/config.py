from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field
from typing import Optional

class Settings(BaseSettings):
    # Flask settings
    flask_secret_key: SecretStr = Field(...)  # Required — set FLASK_SECRET_KEY in .env
    flask_port: int = 5001
    environment: str = "development"
    flask_debug: bool = Field(default=False)  # Set FLASK_DEBUG=true only in development
    
    # APIs
    openai_api_key: Optional[SecretStr] = None
    serpapi_api_key: Optional[SecretStr] = None
    
    # Polymarket & Web3
    polygon_wallet_private_key: Optional[SecretStr] = None
    
    # Trading configurations
    initial_bankroll: float = 1000.0
    max_bet_percentage: float = 0.05
    min_edge_percentage: float = 0.15
    
    # Configure pydantic to load from .env file
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

# Create a global settings instance to be imported across the app
settings = Settings()
