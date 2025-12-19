from sqlalchemy import Column, String, Text


from src.core.database.base_class import Base

class KVStore(Base):
    __tablename__ = "kv_store"
    __table_args__ = {
        "prefixes": ["UNLOGGED"]
    }

    key = Column(String(255), primary_key=True)
    value = Column(Text, nullable=False)
