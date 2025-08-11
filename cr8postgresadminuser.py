## Prerequisites: Install the psycopg2-binary package
## pip install psycopg2-binary

import psycopg2
from psycopg2 import sql, OperationalError

# Connection info for an existing superuser
DB_HOST = "192.168.64.2"
DB_PORT = 5432
DB_NAME = "WESHAI"
DB_USER = "postgres"      # Existing superuser
DB_PASSWORD = "postgres"

# New superuser details
NEW_SUPERUSER = "FOOTYADMIN"
NEW_SUPERUSER_PASSWORD = "LuvUYanitedGG"

def create_superuser():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        create_user_query = sql.SQL(
            """
            CREATE ROLE {user} 
            WITH LOGIN SUPERUSER CREATEDB CREATEROLE PASSWORD %s;
            """
        ).format(
            user=sql.Identifier(NEW_SUPERUSER)
        )

        cursor.execute(create_user_query, [NEW_SUPERUSER_PASSWORD])
        connection.commit()

        print(f"✅ Superuser '{NEW_SUPERUSER}' created successfully.")

    except OperationalError as e:
        print(f"❌ Could not connect to the database: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    create_superuser()
