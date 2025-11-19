import snowflake.connector
import os

conn = snowflake.connector.connect(
    account=os.getenv("SNOW_ACCOUNT"),
    user=os.getenv("SNOW_USER"),
    password=os.getenv("SNOW_PASSWORD"),
    role=os.getenv("SNOW_ROLE"),
    warehouse=os.getenv("SNOW_WH"),
    database=os.getenv("SNOW_DB"),
    schema=os.getenv("SNOW_SCHEMA"),
)

cur = conn.cursor()
cur.execute("SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()")
print(cur.fetchall())
