from database import engine
from sqlalchemy import text

print('DB URL:', engine.url)
with engine.connect() as conn:
    print('connected')
    result = conn.execute(text("SELECT 1"))
    print('query', result.scalar())
