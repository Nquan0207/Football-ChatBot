from sqlalchemy import create_engine
from app.core.config import settings
import sys

def test_database_connection():
    try:
        # Create engine with the DATABASE_URL from settings
        engine = create_engine(settings.DATABASE_URL)
        
        # Try to connect and execute a simple query
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("✅ Successfully connected to the database!")
            return True
            
    except Exception as e:
        print("❌ Failed to connect to the database!")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
