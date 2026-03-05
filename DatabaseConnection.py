from dataclasses import dataclass

import mysql.connector
from mysql.connector import Error
from flask import Flask

@dataclass
class PlayerIdentifyingInformation:
    pii_id: int
    first_name: str
    last_name: str
    school: str

@dataclass
class CareerStatistics:
    player_id: int
    sets_played: int
    kills: int
    kills_per_set: float
    errs: int
    total_attempts: int
    attack_percentage: float
    assits: int
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

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="radyweb.wsc.western.edu",
            user="ncaa_user",
            password="StrongPass01!",
            database="ncaa_transfer_portal_assistant"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    

def execute_insert(query, params):
    connection = get_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            print("Insert successful.")
        except Error as e:
            print(f"Error executing insert: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")
    
def insert_into_player_identifying_information(pii):
    query = """
    INSERT INTO player_identifying_information (first_name, last_name, school)
    VALUES ( %s, %s, %s)
    """
    params = (pii.first_name, pii.last_name, pii.school)
    execute_insert(query, params)
    return print("Player identifying information inserted successfully")

def insert_into_career_statistics(career_stats):
    query = """
    INSERT INTO career_statistics (sets_played, kills, kills_per_set, 
    errs, total_attempts, attack_percentage, assits, 
    assists_per_set, serve_aces, serve_errors, serve_aces_per_set, 
    reception_errors, digs, digs_per_set, block_solos, block_assists, 
    blk, blk_per_s, block_errors, ball_handling_errors, points, pii_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    params = (career_stats.sets_played, career_stats.kills, career_stats.kills_per_set, career_stats.errs, career_stats.total_attempts, career_stats.attack_percentage, career_stats.assits,
              career_stats.assists_per_set, career_stats.serve_aces, career_stats.serve_errors, career_stats.serve_aces_per_set, career_stats.reception_errors, career_stats.digs,
              career_stats.digs_per_set, career_stats.block_solos, career_stats.block_assists, career_stats.blk, career_stats.blk_per_s, career_stats.block_errors,
              career_stats.ball_handling_errors, career_stats.points, career_stats.pii_id)
    execute_insert(query, params)

def insert_game_statistics(game_stats):
    query = """
        INSERT INTO game_statistics (
            game_date, opponent, sets_played, kills, errs,
            total_attempts, attack_percentage, assits,
            serve_aces, serve_errors, reception_errors,
            digs, block_solos, block_assists,
            block_errors, ball_handling_errors, total_blocks,
            pii_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        game_stats.game_date, game_stats.opponent, game_stats.sets_played, game_stats.kills, game_stats.errs,
        game_stats.total_attempts, game_stats.attack_percentage, game_stats.assists,
        game_stats.serve_aces, game_stats.serve_errors, game_stats.reception_errors,
        game_stats.digs, game_stats.block_solos, game_stats.block_assists,
        game_stats.block_errors, game_stats.ball_handling_errors, game_stats.total_blocks,
        game_stats.pii_id
    )
    return execute_insert(query, params)


def execute_read(query, params):
    connection = get_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except Error as e:
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
    WHERE first_name = %s AND last_name = %s AND school = %s
    """
    params = (pii.first_name, pii.last_name, pii.school)
    results = execute_read(query, params)
    if results:
        return results[0]["pii_id"]
    else:
        print("No player found with the given information.")
        return None

def get_career_statistics_by_player_id(player_id):
    query = "SELECT * FROM career_statistics WHERE player_id = %s"
    results = execute_read(query, (player_id,))
    if results:
        return results[0]
    else:
        print("No career statistics found for the given player ID.")
        return None

def get_game_statistics_by_player_id(player_id):
    query = "SELECT * FROM game_statistics WHERE player_id = %s"
    return execute_read(query, (player_id,))

def execute_update(query, params):
    connection = get_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            print("Update successful.")
        except Error as e:
            print(f"Error executing update: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")

def update_player_school(pii_id, new_school):
    query = "UPDATE player_identifying_information SET school = %s WHERE pii_id = %s"
    params = (new_school, pii_id)
    execute_update(query, params)

def update_career_statistics(career_stats):
    query = """
    UPDATE career_statistics 
    SET sets_played = %s, kills = %s, kills_per_set = %s, 
    errs = %s, total_attempts = %s, attack_percentage = %s, assits = %s, 
    assists_per_set = %s, serve_aces = %s, serve_errors = %s, serve_aces_per_set = %s, 
    reception_errors = %s, digs = %s, digs_per_set = %s, block_solos = %s, block_assists = %s, 
    blk = %s, blk_per_s = %s, block_errors = %s, ball_handling_errors = %s, points = %s
    WHERE player_id = %s AND piid_id = %s
    """
    params = (career_stats.sets_played, career_stats.kills, career_stats.kills_per_set, career_stats.errs, career_stats.total_attempts, career_stats.attack_percentage, career_stats.assists,
              career_stats.assists_per_set, career_stats.serve_aces, career_stats.serve_errors, career_stats.serve_aces_per_set, career_stats.reception_errors, career_stats.digs,
              career_stats.digs_per_set, career_stats.block_solos, career_stats.block_assists, career_stats.blk, career_stats.blk_per_s, career_stats.block_errors,
              career_stats.ball_handling_errors, career_stats.points, career_stats.player_id, career_stats.pii_id)
    execute_update(query, params)

def update_game_statistics(game_stats):
    query = """
        UPDATE game_statistics
        SET game_date = %s, opponent = %s, sets_played = %s, kills = %s, errs = %s,
            total_attempts = %s, attack_percentage = %s, assits = %s,
            serve_aces = %s, serve_errors = %s, reception_errors = %s,
            digs = %s, block_solos = %s, block_assists = %s,
            block_errors = %s, ball_handling_errors = %s, total_blocks = %s
        WHERE piid_id = %s AND game_date = %s AND opponent = %s
    """
    params = (
        game_stats.game_date, game_stats.opponent, game_stats.sets_played, game_stats.kills, game_stats.errs,
        game_stats.total_attempts, game_stats.attack_percentage, game_stats.assists,
        game_stats.serve_aces, game_stats.serve_errors, game_stats.reception_errors,
        game_stats.digs, game_stats.block_solos, game_stats.block_assists,
        game_stats.block_errors, game_stats.ball_handling_errors, game_stats.total_blocks,
        game_stats.pii_id, game_stats.game_date, game_stats.opponent
    )
    execute_update(query, params)

def execute_delete(query, params):
    connection = get_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            print("Delete successful.")
        except Error as e:
            print(f"Error executing delete: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database.")

def delete_player_by_id(pii_id):
    query = "DELETE FROM player_identifying_information WHERE pii_id = %s"
    execute_delete(query, pii_id)

def delete_career_statistics_by_player_id(pii_id):
    query = "DELETE FROM career_statistics WHERE piid_id = %s"
    execute_delete(query, pii_id)

def delete_game_statistics_by_player_id_and_game_date(pii_id, game_date):
    query = "DELETE FROM game_statistics WHERE piid_id = %s AND game_date = %s"
    params = (pii_id, game_date)
    execute_delete(query, params)


def get_all_player_data():
    query = "SELECT * FROM player_identifying_information"
    return execute_read(query, ())

def get_career_statistics_by_pii_id(pii_id):
    query = "SELECT * FROM career_statistics WHERE pii_id = %s"
    return execute_read(query, (pii_id,))



    
conn = get_db_connection()
if conn is not None:
    print("Database connection successful.")


###INSERTING TEST DATA INTO DATABASE###
# PlayerIdentifyingInformation1 = PlayerIdentifyingInformation(pii_id=None, first_name="Jane", last_name="Doe", school="University B")
# insert_into_player_identifying_information(PlayerIdentifyingInformation1)

# career_stats = CareerStatistics(player_id=1, sets_played=100, kills=500, kills_per_set=5.0, errs=50, total_attempts=1000, attack_percentage=0.45, assits=200,
#               assists_per_set=2.0, serve_aces=30, serve_errors=10, serve_aces_per_set=0.3, reception_errors=20, digs=150,
#               digs_per_set=1.5, block_solos=10, block_assists=40, blk=50, blk_per_s=0.5, block_errors=5, ball_handling_errors=15, points=600, pii_id=1)
# insert_into_career_statistics(career_stats)

# game_stats = GameStatistics(game_date="2024-01-01", opponent="Team A", sets_played=3, kills=15, errs=2, total_attempts=30, attack_percentage=0.43, assists=5,
#     serve_aces=2, serve_errors=1, reception_errors=0, digs=10, block_solos=1, block_assists=2, block_errors=0, ball_handling_errors=1, total_blocks=3, pii_id=1)
# insert_game_statistics(game_stats)

test_career_stats = get_career_statistics_by_player_id()
print(test_career_stats)

conn.close()
