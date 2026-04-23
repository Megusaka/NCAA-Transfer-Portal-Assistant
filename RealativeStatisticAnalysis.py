import DatabaseConnection as db

def order_players_by_kills():
    query = """
        SELECT pii_id, kills 
        FROM career_statistics 
        WHERE kills IS NOT NULL
        ORDER BY kills DESC
    """
    results = db.execute_read(query, ())
    
    # Unpack the tuple and print a formatted string
    if results:
        for pii_id, kills in results:
            print(f"Player ID: {pii_id} - Kills: {kills}")
            
    return results

def get_player_ranking_by_statistic(pii_id: int, stat_column: str):
    query = f"""
        WITH RankedPlayers AS (
            SELECT 
                pii_id, 
                RANK() OVER (ORDER BY {stat_column} DESC) as player_rank,
                COUNT(*) OVER () as total_players
            FROM career_statistics
        )
        SELECT player_rank, total_players 
        FROM RankedPlayers 
        WHERE pii_id = ?
    """
    
    params = (pii_id,)
    results = db.execute_read(query, params)
    
    if results:
        # results[0] will be a tuple: (27, 129) -> (player_rank, total_players)
        player_rank = results[0][0]
        total_players = results[0][1]
        return str(player_rank) + "/" + str(total_players)
    else:
        print("No statistics found for the given player.")
        return None

def rank_full_database_by_stat(stat_column: str):
    query = f"""
        SELECT 
            pii_id, 
            {stat_column},
            RANK() OVER (ORDER BY {stat_column} DESC) as player_rank
        FROM career_statistics
        ORDER BY player_rank ASC
    """
    
    results = db.execute_read(query, ())
    
    if results:
        return results 
    else:
        return []

#print(db.get_player_identifying_information_by_pii_id(13))
# order_players_by_kills()
# print(get_player_ranking_by_statistic(13, "kills"))

print(rank_full_database_by_stat("kills"))