import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Define the base class for models
Base = declarative_base()

class Trade(Base):
    """
    SQLAlchemy model for tracking Polymarket trades.
    """
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    bet_id = Column(String, unique=True, index=True)
    token_id = Column(String, index=True)
    question = Column(String)
    side = Column(String)  # BUY or SELL
    outcome = Column(String) # YES or NO
    price = Column(Float)
    size = Column(Float)
    total_amount = Column(Float)
    order_id = Column(String)
    tx_hash = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="OPEN") # OPEN, FILLED, CLOSED, FAILED
    pnl = Column(Float, default=0.0)
    
    def __repr__(self):
        return f"<Trade(bet_id='{self.bet_id}', question='{self.question[:30]}...', side='{self.side}', status='{self.status}')>"

# Database setup
DB_PATH = "poly_trader.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Helper to get a database session."""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

# Initialize on import
if not os.path.exists(DB_PATH):
    init_db()
