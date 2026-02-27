import mysql.connector
from mysql.connector import Error
from flask import Flask

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
    
def insert_into_player_identifying_information(pii_id, first_name, last_name, school):
    query = """
    INSERT INTO player_identifying_information (pii_id, first_name, last_name, school)
    VALUES (%s, %s, %s, %s)
    """
    params = (pii_id, first_name, last_name, school)
    execute_insert(query, params)
    return print("Player identifying information inserted successfully")

def insert_into_career_statistics(player_id, sets_played, kills, kills_per_set, 
errs, total_attempts, attack_percentage, assits, 
assists_per_set, serve_aces, serve_errors, serve_aces_per_set, 
reception_errors, digs, digs_per_set, block_solos, block_assists, 
blk, blk_per_s, block_errors, ball_handling_errors, points, pii_id):
    query = """
    INSERT INTO career_statistics (player_id, sets_played, kills, kills_per_set, 
    errs, total_attempts, attack_percentage, assits, 
    assists_per_set, serve_aces, serve_errors, serve_aces_per_set, 
    reception_errors, digs, digs_per_set, block_solos, block_assists, 
    blk, blk_per_s, block_errors, ball_handling_errors, points, piid_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    params = (player_id, sets_played, kills, kills_per_set, errs, total_attempts, attack_percentage, assits,
              assists_per_set, serve_aces, serve_errors, serve_aces_per_set, reception_errors, digs,
              digs_per_set, block_solos, block_assists, blk, blk_per_s, block_errors,
              ball_handling_errors, points, pii_id)
    execute_insert(query, params)

def insert_game_statistics(
    game_date, opponent, sets_played, kills, errs,
    total_attempts, attack_percentage, assists,
    serve_aces, serve_errors, reception_errors,
    digs, block_solos, block_assists,
    block_errors, ball_handling_errors, total_blocks,
    pii_id
):
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
        game_date, opponent, sets_played, kills, errs,
        total_attempts, attack_percentage, assists,
        serve_aces, serve_errors, reception_errors,
        digs, block_solos, block_assists,
        block_errors, ball_handling_errors, total_blocks,
        pii_id
    )
    return execute_insert(query, params)


def execute_read(query, params):
    connection = get_db_connection()
    if connection is not None:
        try:
            cursor = connection.cursor()
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

def get_player_id_by_information(first_name, last_name, school):
    query = """
    SELECT pii_id FROM player_identifying_information
    WHERE first_name = %s AND last_name = %s AND school = %s
    """
    params = (first_name, last_name, school)
    results = execute_read(query, params)
    if results:
        return results[0][0]
    else:
        print("No player found with the given information.")
        return None

def get_career_statistics_by_player_id(player_id):
    query = "SELECT * FROM career_statistics WHERE player_id = %s"
    return execute_read(query, player_id)

def get_game_statistics_by_player_id(player_id):
    query = "SELECT * FROM game_statistics WHERE player_id = %s"
    return execute_read(query, player_id)

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

def update_career_statistics(player_id, sets_played, kills, kills_per_set, 
errs, total_attempts, attack_percentage, assits, 
assists_per_set, serve_aces, serve_errors, serve_aces_per_set, 
reception_errors, digs, digs_per_set, block_solos, block_assists, 
blk, blk_per_s, block_errors, ball_handling_errors, points, pii_id):
    query = """
    UPDATE career_statistics 
    SET sets_played = %s, kills = %s, kills_per_set = %s, 
    errs = %s, total_attempts = %s, attack_percentage = %s, assits = %s, 
    assists_per_set = %s, serve_aces = %s, serve_errors = %s, serve_aces_per_set = %s, 
    reception_errors = %s, digs = %s, digs_per_set = %s, block_solos = %s, block_assists = %s, 
    blk = %s, blk_per_s = %s, block_errors = %s, ball_handling_errors = %s, points = %s
    WHERE player_id = %s AND piid_id = %s
    """
    params = (sets_played, kills, kills_per_set, errs, total_attempts, attack_percentage, assits,
              assists_per_set, serve_aces, serve_errors, serve_aces_per_set, reception_errors, digs,
              digs_per_set, block_solos, block_assists, blk, blk_per_s, block_errors,
              ball_handling_errors, points, player_id, pii_id)
    execute_update(query, params)

def update_game_statistics( game_date, opponent, sets_played, kills, errs,
    total_attempts, attack_percentage, assists,
    serve_aces, serve_errors, reception_errors,
    digs, block_solos, block_assists,
    block_errors, ball_handling_errors, total_blocks,
    pii_id):
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
        game_date, opponent, sets_played, kills, errs,
        total_attempts, attack_percentage, assists,
        serve_aces, serve_errors, reception_errors,
        digs, block_solos, block_assists,
        block_errors, ball_handling_errors, total_blocks,
        pii_id, game_date, opponent
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
    
conn = get_db_connection()
if conn is not None:
    print("Database connection successful.")
    conn.close()
