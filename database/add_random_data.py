import sqlite3
import random

from faker import Faker


fake = Faker()

con = sqlite3.connect("database/db.db")
cur = con.cursor()

for _ in range(15):
    cur.execute(
        """INSERT INTO ASSET (name, asset_class, created_at) values (?, ?, ?)""",
        (fake.unique.first_name(), random.randrange(1, 5), str(fake.date_time())),
    )
con.commit()
con.close()
