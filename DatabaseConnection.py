from dataclasses import dataclass

import sqlite3

@dataclass
class PlayerIdentifyingInformation:
    pii_id: int
    first_name: str
    last_name: str
    school: str
    hometown: str
    eligibility: str
    position: str
    height: str
    is_favorite: bool
    contact_status: int

@dataclass
class CareerStatistics:
    player_id: int
    sets_played: int
    kills: int
    kills_per_set: float
    errs: int
    total_attempts: int
    attack_percentage: float
    assists: int
    assists_per_set: float
    serve_aces: int
    serve_errors: int
    serve_aces_per_set: float
    reception_errors: int
    digs: int
    digs_per_set: float
    block_solos: int
    block_assists: int
    blk: int
    blk_per_s: float
    block_errors: int
    ball_handling_errors: int
    points: int
    pii_id: int

@dataclass
class GameStatistics:
    game_id: int
    game_date: str
    opponent: str
    sets_played: int
    kills: int
    errs: int
    total_attempts: int
    attack_percentage: float
    assists: int
    serve_aces: int
    serve_errors: int
    reception_errors: int
    digs: int
    block_solos: int
    block_assists: int
    block_errors: int
    ball_handling_errors: int
    total_blocks: int
    pii_id: int
    
###MYSQL ARTIFACT###
# def get_db_connection():
#     try:
#         connection = mysql.connector.connect(
#             host="radyweb.wsc.western.edu",
#             user="ncaa_user",
#             password="StrongPass01!",
#             database="ncaa_transfer_portal_assistant"
#         )
#         return connection
#     except Error as e:
#         print(f"Error connecting to MySQL: {e}")
#         return None

def create_table_if_not_exists_player_identifying_information(connection):
    #connection = get_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            #Contact Status: 0 = Not Contacted, 1 = In communication, 2 = Committed, 3 = Dropped
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS player_identifying_information (
                    pii_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    school TEXT NOT NULL,
                    hometown TEXT,
                    eligibility TEXT,
                    position TEXT,
                    height TEXT,
                    is_favorite BOOLEAN DEFAULT 0,
                    contact_status INTEGER DEFAULT 0 
                )
            """)
            connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

def create_table_if_not_exists_career_statistics(connection):
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS career_statistics (
                    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sets_played INTEGER,
                    kills INTEGER,
                    kills_per_set REAL,
                    errs INTEGER,
                    total_attempts INTEGER,
                    attack_percentage REAL,
                    assists INTEGER,
                    assists_per_set REAL,
                    serve_aces INTEGER,
                    serve_errors INTEGER,
                    serve_aces_per_set REAL,
                    reception_errors INTEGER,
                    digs INTEGER,
                    digs_per_set REAL,
                    block_solos INTEGER,
                    block_assists INTEGER,
                    blk INTEGER,
                    blk_per_s REAL,
                    block_errors INTEGER,
                    ball_handling_errors INTEGER,
                    points INTEGER,
                    pii_id INTEGER NOT NULL,
                    FOREIGN KEY (pii_id) REFERENCES player_identifying_information(pii_id)
                )
            """)
            connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

def create_table_if_not_exists_game_statistics(connection):
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_statistics (
                    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_date TEXT NOT NULL,
                    opponent TEXT NOT NULL,
                    sets_played INTEGER,
                    kills INTEGER,
                    errs INTEGER,
                    total_attempts INTEGER,
                    attack_percentage REAL,
                    assists INTEGER,
                    serve_aces INTEGER,
                    serve_errors INTEGER,
                    reception_errors INTEGER,
                    digs INTEGER,
                    block_solos INTEGER,
                    block_assists INTEGER,
                    block_errors INTEGER,
                    ball_handling_errors INTEGER,
                    total_blocks INTEGER,
                    pii_id INTEGER NOT NULL,
                    FOREIGN KEY (pii_id) REFERENCES player_identifying_information(pii_id)
                )
            """)
            connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

def get_db_connection():
    db_filepath = "transferPortalAssistant.db"
    try:
        connection = sqlite3.connect(db_filepath)
        connection.row_factory = sqlite3.Row
        create_table_if_not_exists_player_identifying_information(connection)
        create_table_if_not_exists_career_statistics(connection)
        create_table_if_not_exists_game_statistics(connection)
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")
        return None
    

def execute_insert(query, params):
    connection = get_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            print("Insert successful.")
        except sqlite3.Error as e:
            print(f"Error executing insert: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")
    
def insert_into_player_identifying_information(pii):
    query = """
    INSERT INTO player_identifying_information (first_name, last_name, school, hometown, eligibility, position, height)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        pii.first_name, 
        pii.last_name, 
        pii.school, 
        pii.hometown, 
        pii.eligibility, 
        pii.position, 
        pii.height
        )
    execute_insert(query, params)
    return print("Player identifying information inserted successfully")


def insert_into_career_statistics(career_stats):
    query = """
    INSERT INTO career_statistics (sets_played, kills, kills_per_set, 
    errs, total_attempts, attack_percentage, assists, 
    assists_per_set, serve_aces, serve_errors, serve_aces_per_set, 
    reception_errors, digs, digs_per_set, block_solos, block_assists, 
    blk, blk_per_s, block_errors, ball_handling_errors, points, pii_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        career_stats.sets_played,
        career_stats.kills,
        career_stats.kills_per_set,
        career_stats.errs,
        career_stats.total_attempts,
        career_stats.attack_percentage,
        career_stats.assists,
        career_stats.assists_per_set,
        career_stats.serve_aces,
        career_stats.serve_errors,
        career_stats.serve_aces_per_set,
        career_stats.reception_errors,
        career_stats.digs,
        career_stats.digs_per_set,
        career_stats.block_solos,
        career_stats.block_assists,
        career_stats.blk,
        career_stats.blk_per_s,
        career_stats.block_errors,
        career_stats.ball_handling_errors,
        career_stats.points,
        career_stats.pii_id
    )
    execute_insert(query, params)
    return print("Career statistics inserted successfully")


def insert_game_statistics(game_stats):
    query = """
        INSERT INTO game_statistics (
            game_date, opponent, sets_played, kills, errs,
            total_attempts, attack_percentage, assists,
            serve_aces, serve_errors, reception_errors,
            digs, block_solos, block_assists,
            block_errors, ball_handling_errors, total_blocks,
            pii_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        game_stats.game_date,
        game_stats.opponent,
        game_stats.sets_played,
        game_stats.kills,
        game_stats.errs,
        game_stats.total_attempts,
        game_stats.attack_percentage,
        game_stats.assists,
        game_stats.serve_aces,
        game_stats.serve_errors,
        game_stats.reception_errors,
        game_stats.digs,
        game_stats.block_solos,
        game_stats.block_assists,
        game_stats.block_errors,
        game_stats.ball_handling_errors,
        game_stats.total_blocks,
        game_stats.pii_id
    )

    execute_insert(query, params)
    return print("Game statistics inserted successfully")


def execute_read(query, params):
    connection = get_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error executing read: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")
        return None

def get_player_id_by_information(pii):
    query = """
    SELECT pii_id FROM player_identifying_information
    WHERE first_name = ? AND last_name = ? AND school = ?
    """
    params = (pii.first_name, pii.last_name, pii.school)
    results = execute_read(query, params)
    if results:
        return results[0][0]
    else:
        print("No player found with the given information.")
        return None
    
def get_pii_id_by_name_and_school(first_name, last_name, school):
    query = """
    SELECT pii_id FROM player_identifying_information
    WHERE first_name = ? AND last_name = ? AND school = ?
    """
    params = (first_name, last_name, school)
    results = execute_read(query, params)
    if results:
        return results[0][0]
    else:
        print("No player found with the given name and school.")
        return None

def get_career_statistics_by_player_id(player_id):
    query = "SELECT * FROM career_statistics WHERE player_id = ?"
    results = execute_read(query, (player_id,))
    if results:
        return results[0]
    else:
        print("No career statistics found for the given player ID.")
        return None
    
def get_player_identifying_information_by_pii_id(pii_id):
    query = "SELECT * FROM player_identifying_information WHERE pii_id = ?"
    results = execute_read(query, (pii_id,))
    if results:
        return results[0]
    else:
        print("No player found with the given PII ID.")
        return None

def get_game_statistics_by_pii_id(pii_id):
    query = "SELECT * FROM game_statistics WHERE pii_id = ?"
    return execute_read(query, (pii_id,))

def get_career_statistics_by_pii_id(pii_id):
    query = "SELECT * FROM career_statistics WHERE pii_id = ?"
    results = execute_read(query, (pii_id,))
    if results:
        return results[0]
    else:
        print("No career statistics found for the given PII ID.")
        return None
    
def get_all_career_statistics():
    query = "SELECT * FROM career_statistics"
    return execute_read(query, ())

def get_all_game_statistics():
    query = "SELECT * FROM game_statistics"
    return execute_read(query, ())

##logan's gets
def get_all_player_data():
    query = "SELECT * FROM player_identifying_information"
    return execute_read(query, ())

def get_career_statistics_by_pii_id(pii_id):
    query = "SELECT * FROM career_statistics WHERE pii_id = ?"
    return execute_read(query, (pii_id,))

def get_player_by_favorite():
    query = "SELECT * FROM player_identifying_information WHERE is_favorite = TRUE"
    return execute_read(query, ())

def execute_update(query, params):
    connection = get_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            print("Update successful.")
        except sqlite3.Error as e:
            print(f"Error executing update: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")

def update_player_school(pii_id, new_school):
    query = "UPDATE player_identifying_information SET school = ? WHERE pii_id = ?"
    params = (new_school, pii_id)
    execute_update(query, params)

def update_career_statistics(career_stats):
    query = """
    UPDATE career_statistics SET 
    sets_played = ?, 
    kills = ?, 
    kills_per_set = ?, 
    errs = ?, 
    total_attempts = ?, 
    attack_percentage = ?, 
    assists = ?, 
    assists_per_set = ?, 
    serve_aces = ?, 
    serve_errors = ?, 
    serve_aces_per_set = ?, 
    reception_errors = ?, 
    digs = ?, 
    digs_per_set = ?, 
    block_solos = ?, 
    block_assists = ?, 
    blk = ?, 
    blk_per_s = ?, 
    block_errors = ?, 
    ball_handling_errors = ?, 
    points = ?
    WHERE player_id = ? AND pii_id = ?
    """
    params = (career_stats.sets_played, 
              career_stats.kills, 
              career_stats.kills_per_set, 
              career_stats.errs, 
              career_stats.total_attempts, 
              career_stats.attack_percentage, 
              career_stats.assists,
              career_stats.assists_per_set, 
              career_stats.serve_aces, 
              career_stats.serve_errors, 
              career_stats.serve_aces_per_set, 
              career_stats.reception_errors, 
              career_stats.digs,
              career_stats.digs_per_set, 
              career_stats.block_solos, 
              career_stats.block_assists, 
              career_stats.blk, 
              career_stats.blk_per_s, 
              career_stats.block_errors,
              career_stats.ball_handling_errors, 
              career_stats.points, 
              career_stats.player_id, 
              career_stats.pii_id
              )
    execute_update(query, params)

def update_game_statistics(game_stats):
    query = """
        UPDATE game_statistics
        SET game_date = ?, opponent = ?, sets_played = ?, kills = ?, errs = ?,
            total_attempts = ?, attack_percentage = ?, assists = ?,
            serve_aces = ?, serve_errors = ?, reception_errors = ?,
            digs = ?, block_solos = ?, block_assists = ?,
            block_errors = ?, ball_handling_errors = ?, total_blocks = ?
        WHERE pii_id = ? AND game_date = ? AND opponent = ?
    """
    params = (
        game_stats.game_date, 
        game_stats.opponent, 
        game_stats.sets_played, 
        game_stats.kills, 
        game_stats.errs,
        game_stats.total_attempts, 
        game_stats.attack_percentage, 
        game_stats.assists,
        game_stats.serve_aces, 
        game_stats.serve_errors, 
        game_stats.reception_errors,
        game_stats.digs, 
        game_stats.block_solos, 
        game_stats.block_assists,
        game_stats.block_errors, 
        game_stats.ball_handling_errors, 
        game_stats.total_blocks,
        game_stats.pii_id, 
        game_stats.game_date, 
        game_stats.opponent
    )
    execute_update(query, params)

def update_player_favorite_status(pii_id, is_favorite):
    query = "UPDATE player_identifying_information SET is_favorite = ? WHERE pii_id = ?"
    params = (is_favorite, pii_id)
    execute_update(query, params)

def update_player_contact_status(pii_id, contact_status):
    query = "UPDATE player_identifying_information SET contact_status = ? WHERE pii_id = ?"
    params = (contact_status, pii_id)
    execute_update(query, params)

def execute_delete(query, params):
    connection = get_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            print("Delete successful.")
        except sqlite3.Error as e:
            print(f"Error executing delete: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")

def delete_player_by_id(pii_id):
    query = "DELETE FROM player_identifying_information WHERE pii_id = ?"
    execute_delete(query, (pii_id,))

def delete_career_statistics_by_player_id(pii_id):
    query = "DELETE FROM career_statistics WHERE pii_id = ?"
    execute_delete(query, (pii_id,))

def delete_game_statistics_by_player_id_and_game_date(pii_id, game_date):
    query = "DELETE FROM game_statistics WHERE pii_id = ? AND game_date = ?"
    params = (pii_id, game_date)
    execute_delete(query, params)

def drop_player_identifying_information_table():
    query = "DROP TABLE IF EXISTS player_identifying_information"
    execute_delete(query, ())

def drop_career_statistics_table():
    query = "DROP TABLE IF EXISTS career_statistics"
    execute_delete(query, ())

def drop_game_statistics_table():
    query = "DROP TABLE IF EXISTS game_statistics"
    execute_delete(query, ())


conn = get_db_connection()
if conn is not None:
    print("Database connection successful.")
    conn.close()


###INSERTING TEST DATA INTO DATABASE###
# PlayerIdentifyingInformation1 = PlayerIdentifyingInformation(pii_id=None, first_name="Jane", last_name="Doe", school="University B")
# insert_into_player_identifying_information(PlayerIdentifyingInformation1)

# career_stats = CareerStatistics(player_id=1, sets_played=100, kills=500, kills_per_set=5.0, errs=50, total_attempts=1000, attack_percentage=0.45, assists=200,
#               assists_per_set=2.0, serve_aces=30, serve_errors=10, serve_aces_per_set=0.3, reception_errors=20, digs=150,
#               digs_per_set=1.5, block_solos=10, block_assists=40, blk=50, blk_per_s=0.5, block_errors=5, ball_handling_errors=15, points=600, pii_id=1)
# insert_into_career_statistics(career_stats)

# game_stats = GameStatistics(game_date="2024-01-01", opponent="Team A", sets_played=3, kills=15, errs=2, total_attempts=30, attack_percentage=0.43, assists=5,
#     serve_aces=2, serve_errors=1, reception_errors=0, digs=10, block_solos=1, block_assists=2, block_errors=0, ball_handling_errors=1, total_blocks=3, pii_id=1)
# insert_game_statistics(game_stats)

#olive_pii = PlayerIdentifyingInformation(pii_id=None, first_name="Olive", last_name="Rolseth", school="Western Colorado University", hometown="Grand Junction, CO", eligibility="Senior", position="Outside Hitter", height="6'0\"", is_favorite=False, contact_status=0)
#insert_into_player_identifying_information(olive_pii)




#olive_pii = PlayerIdentifyingInformation(pii_id=None, first_name="Olive", last_name="Rolseth", school="Western Colorado University", hometown="Grand Junction, CO", eligibility="Senior", position="Outside Hitter", height="6'0\"", is_favorite=False, contact_status=0)
#insert_into_player_identifying_information(olive_pii)

#nina_pii = PlayerIdentifyingInformation(pii_id=None, first_name="Nina", last_name="Cowan", school="Western Colorado University", hometown="Pueblo, CO", eligibility="Freshman", position="Libero", height="5-2", is_favorite=False, contact_status=0)
#insert_into_player_identifying_information(nina_pii)

#drop_player_identifying_information_table()
#drop_career_statistics_table()
#drop_game_statistics_table()

# print(get_all_player_data())

#print(get_all_career_statistics())
#print(get_career_statistics_by_pii_id(1))

#print(get_all_game_statistics())


