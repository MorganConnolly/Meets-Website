import sqlite3
from datetime import datetime

# Dates must be of this format: YYYY-MM-DD HH:MM:SS

class Database():
  def __init__(self, db_name):
    # Initialising database curs & conn.
    self.conn = sqlite3.connect(db_name)
    self.conn.row_factory = sqlite3.Row
    self.curs = self.conn.cursor()
    self.curs.execute("PRAGMA foreign_keys = 1;")

    # If tables don't exist, create them.
    self.create_tables()

  # Validation.
  def varchar(self, x, n):
    if (len(x) < 0) or (len(x) > n):
      print("Varchar failed.")
      return False 
    else:
      return True
      
  def char(self, x, n):
    if len(x) == n:
      return True 
    else:
      return False
    
  def presence_check(self, x):
    if len(x) == 0:
      return False 
    else:
      return True 

  def unique_check(self, x, field, table):

    results = self.curs.execute(f"""
      SELECT {field}
      FROM {table}
      WHERE ({field} == {x});
    """).fetchall()
    
    if results == []:
      return True 
    else:
      return False
    
  def type_check(self, x, type):
    if type == "datetime":
      try:
        int(x[0:4])
        int(x[5:7])
        int(x[8:10])
        int(x[11:13])
        int(x[14:16])
        int(x[17:19])
        if ((x[4] != "-") or (x[7] != "-") or (x[10] != " ") or (x[13] != ":") or (x[16] != ":") or (len(x) != 19)):
          return False
        else:
          return True 
      except:
        return False
    if type(x) is type:
      return True 
    else:
      return False

  def generate_primary(self, field, table):

    result = self.curs.execute(f"""
      SELECT {field}
      FROM {table};
      """).fetchall()
    result = [record[0] for record in result]

    try:
      return str(int(max(result)) + 1)
    except:
      return "1"

  def add_https(self, url):
    if (url == ""):
      return ""
    elif ("https://" not in url):
      return "https://" + url 
    return url

  # Creation methods.
  def create_tables(self):

    self.curs.execute("""
      CREATE TABLE IF NOT EXISTS a_group (
      name VARCHAR(50) NOT NULL UNIQUE,
      organisers VARCHAR(50) NOT NULL,
      website VARCHAR(50),
      discord VARCHAR(50) NOT NULL,
      desc VARCHAR(200),
      PRIMARY KEY(name)
      ); """)
    self.curs.execute("""
      CREATE TABLE IF NOT EXISTS a_meet (
      id CHAR(4) NOT NULL UNIQUE,
      name VARCHAR(50) NOT NULL,
      start_time DATETIME NOT NULL,
      end_time DATETIME NOT NULL,
      city VARCHAR(50) NOT NULL,
      desc VARCHAR(200) NOT NULL,
      group_name VARCHAR(50) NOT NULL,
      PRIMARY KEY(id),
      FOREIGN KEY(group_name) REFERENCES a_group(name)
      ); """)
    self.curs.execute("""
      CREATE TABLE IF NOT EXISTS a_venue(
      id CHAR(4) NOT NULL UNIQUE,
      name VARCHAR(50) NOT NULL,
      start DATETIME NOT NULL,
      address VARCHAR(100) NOT NULL,
      website VARCHAR(50),
      meet_id CHAR(4),
      PRIMARY KEY(id),
      FOREIGN KEY(meet_id) REFERENCES a_meet(id)
      ); """)
    self.conn.commit()

  def create_group(self):

    name = input("Name: ").lower().title()
    organisers = input("Organisers: ")
    website = input("Website: ")
    discord = input("Discord: ")
    desc = input("Description: ")

    if (self.varchar(name, 50) and self.varchar(organisers, 50) and self.varchar(website, 50) and self.varchar(discord, 50) and self.varchar(desc, 400)):
      try:
        self.curs.execute("""
        INSERT INTO a_group
        VALUES(?, ?, ?, ?, ?);
        """, (name, organisers, self.add_https(website), self.add_https(discord), desc))
        self.conn.commit()
      except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    else:
      print("Failed validation.")

  def create_meet(self):

    id = self.generate_primary("id", "a_meet")
    name = input("Name: ").lower().title()
    start_time = input("Start Time (w/ date): ")
    end_time = input("End Time (w/ date): ")
    city = input("City: ").lower().title()
    desc = input("Description: ")
    group_name = input("Group: ").lower().title()

    if not self.varchar(name, 50):
      print(1)
    elif not self.type_check(start_time, "datetime"):
      print(2)
    elif not self.type_check(end_time, "datetime"):
      print(3)
    elif not self.varchar(city, 50):
      print(4)
    elif not self.varchar(desc, 400):
      print(5)

    if (self.varchar(name, 50) and self.type_check(start_time, "datetime") and self.type_check(end_time, "datetime") and self.varchar(city, 50) and self.varchar(desc, 400)):
      try:
        self.curs.execute("""
          INSERT INTO a_meet
          VALUES(?, ?, ?, ?, ?, ?, ?);
        """, (id, name, start_time, end_time, city, desc, group_name))
        self.conn.commit()
      except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    else:
      print("Failed validation.")

  def create_venue(self):

    id = self.generate_primary("id", "a_venue")
    name = input("Name: ").lower().title()
    start = input("Start: ")
    address = input("Address: ")
    website = input("Website (Full URL): ")
    meet_id = input("Meet ID: ")

    if (self.varchar(name, 50) and self.type_check(start, "datetime") and self.varchar(website, 50) and self.varchar(address, 100)):
      try:
        self.curs.execute("""
          INSERT INTO a_venue
          VALUES(?, ?, ?, ?, ?, ?);
        """, (id, name, start, address, self.add_https(website), meet_id))
        self.conn.commit()
      except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
    else:
      print("Failed validation.")

  # Get all futures meets to display on home page.
  def get_future_meets(self):

    meets = self.curs.execute("""
      SELECT *
      FROM a_meet
      WHERE start_time >= ?
      ORDER BY start_time ASC;
    """, (datetime.now(),)).fetchall()

    return meets

  # Get group names to generate pages for each group.
  def get_groups(self):
      
    group_names = self.curs.execute("""
      SELECT *
      FROM a_group
      ORDER BY name ASC;
    """).fetchall()

    return group_names

  # Get all upcoming meets for a given group.
  def get_group_meets(self, group_name):
     
    group_meets = self.curs.execute("""
      SELECT *
      FROM a_meet
      WHERE group_name == ?
      ORDER BY start_time ASC;
    """, (group_name,)).fetchall()

    return group_meets

if __name__ == "__main__":
  meets_database = Database("meets.db")
  meets_database.create_meet()