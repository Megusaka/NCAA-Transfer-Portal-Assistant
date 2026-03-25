    player_career_stats = []
    players = db.get_all_player_data()
    
    for player in players:
        pii_id = player["pii_id"]
        career_stats = db.get_career_statistics_by_pii_id(pii_id)
        for stat in career_stats:
            print(stat["sets_played_offensive"], stat["kills"], stat["assists_per_set"], 
                  stat["errs"], stat["total_attempts"], stat["attack_percentage"],
                   stat["assist"], stat["assists_per_set"], stat["serve_aces"],
                   stat["serve_errors"], stat["serve_aces_per_set"], stat["sets_played_defense"],
                   stat["reception_errors"], stat["digs"], stat["digs_per_set"], stat["block_solos"],
                   stat["block_assists"], stat["blk"], stat["blk_per_s"], stat["block_errors"], 
                   stat["ball_handling_errors"], stat["points"])
        
        game_stats = db.get_game_statistics_by_player_id(pii_id)
        for stat in game_stats:
            print(stat["game_date"], stat["opponet"], stat["sets_played"],
                  stat["kills"], stat["errs"], stat["total_attempts"], stat["attack_percentage"],
                  stat["assists"], stat["service_aces"], stat["service_errors"], stat["reception_errors"],
                  stat["digs"], stat["block_solos"], stat["block_assists"], stat["block_errors"],
                  stat["ball_handling_errors"], stat["total_blocks"]
                )

        if career_stats:
            career_dict = career_stats[0]
        else:
            None

        if game_stats:
            game_dict = game_stats[0]
        else:
            None
        
        player_career_stats.append({
             "identifying" : player,
             "career" : career_dict,
             "gameBygame" : game_dict
        })
