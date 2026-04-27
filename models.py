from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

class MarketData(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(default="")
    url: Optional[str] = None
    
    # Odds expected as strings with '%' (e.g., '43%')
    yes_odds: str
    no_odds: str
    
    recommendation: str
    bet_amount: str
    expected_profit: str
    confidence: str
    icon: str
    
    @field_validator('yes_odds', 'no_odds')
    @classmethod
    def validate_odds(cls, v: str) -> str:
        if not v.endswith('%'):
            raise ValueError(f"Odds must end with '%', got {v}")
        try:
            num = int(v.replace('%', ''))
            if not 0 <= num <= 100:
                raise ValueError("Odds percentage must be between 0 and 100")
        except ValueError as e:
            if "between 0 and 100" in str(e):
                raise
            raise ValueError("Odds must be a valid percentage string")
        return v

    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v: str) -> str:
        if v == "High" or v == "Medium" or v == "Low":
            return v
        if not v.endswith('%'):
            raise ValueError(f"Confidence must be High/Medium/Low or a percentage, got {v}")
        return v
        
class MarketDataResponse(BaseModel):
    markets: List[MarketData]
    tomorrow_display: Optional[str] = None
    total_bet_amount: float
    total_expected_profit: float
    roi_percentage: float
    current_year: Optional[int] = None
    data_source: Optional[str] = "real"
