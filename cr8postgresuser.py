## Prerequisuites: Install the psycopg2-binary and sql packages
## pip install psycopg2-binary


import psycopg2
from psycopg2 import sql, OperationalError

# Modify these with your actual values
DB_HOST = "192.168.64.2"        # Or use the VM's IP, e.g., "192.168.64.2"
DB_PORT = 5432               # 5432 if direct, or 5433 if forwarded
DB_NAME = "WESHAI"         # Or your specific database
DB_USER = "postgres"         # Admin user
DB_PASSWORD = "postgres"

NEW_APP_USER = "FOOTYUSER"
NEW_APP_PASSWORD = "LuvUYanitedGG"

def create_app_user():
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
            "CREATE ROLE {user} WITH LOGIN PASSWORD %s; GRANT CONNECT ON DATABASE {db} TO {user};"
        ).format(
            user=sql.Identifier(NEW_APP_USER),
            db=sql.Identifier(DB_NAME)
        )

        cursor.execute(create_user_query, [NEW_APP_PASSWORD])
        connection.commit()

        print(f"✅ Application user '{NEW_APP_USER}' created successfully.")

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
    create_app_user()
