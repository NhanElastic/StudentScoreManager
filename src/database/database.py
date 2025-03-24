from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from database.database_config import settings

# Define the Base model for SQLAlchemy
class Base(DeclarativeBase):
    pass
# Create an async engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Async session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Initialize database (Create tables)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency to get a database session
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db  # Provide the session
    finally:
        await db.close()  # Ensure session is closed

async def close_db():
    await engine.dispose()
