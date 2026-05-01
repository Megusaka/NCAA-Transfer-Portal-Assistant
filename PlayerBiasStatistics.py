from io import BytesIO

import DatabaseConnection as db
import matplotlib.pyplot as plt
import numpy as np
import base64

def get_player_name_by_pii_id(pii_id: int) -> str:
    query = "SELECT first_name, last_name FROM player_identifying_information WHERE pii_id = ?"
    result = db.execute_read(query, (pii_id,))
    
    if result:
        first_name, last_name = result[0]
        return f"{first_name} {last_name}"
    else:
        return "Unknown Player"

def get_all_career_stats_as_dataclass_array() -> list[db.CareerStatistics]:
    query = "SELECT * FROM career_statistics"
    results = db.execute_read(query, ())
    
    career_stats = []
    for row in results:
        stat = db.CareerStatistics(
            player_id=row[0],
            sets_played=row[1],
            kills=row[2],
            kills_per_set=row[3],
            errs=row[4],
            total_attempts=row[5],
            attack_percentage=row[6],
            assists=row[7],
            assists_per_set=row[8],
            serve_aces=row[9],
            serve_errors=row[10],
            serve_aces_per_set=row[11],
            reception_errors=row[12],
            digs=row[13],
            digs_per_set=row[14],
            block_solos=row[15],
            block_assists=row[16],
            blk=row[17],
            blk_per_s=row[18],
            block_errors=row[19],
            ball_handling_errors=row[20],
            points=row[21],
            pii_id=row[22]
        )
        career_stats.append(stat)
    return career_stats

def generate_cumulative_scores(pii_id: int) -> list[int]:
    all_players = get_all_career_stats_as_dataclass_array()
    
    # Indexes: 0=Attack, 1=Set, 2=Serve, 3=Dig, 4=Reception, 5=Block
    mins = [float('inf')] * 6
    maxes = [float('-inf')] * 6
    
    target_raw_scores = None

    for player in all_players:
        if player.sets_played == 0:
            if player.pii_id == pii_id:
                return [0, 0, 0, 0, 0, 0]
            continue
            
        # Calculate raw scores
        raw_attack = player.attack_percentage
        raw_set = player.assists_per_set - (player.ball_handling_errors / player.sets_played)
        raw_serve = (player.serve_aces - player.serve_errors) / player.sets_played
        raw_dig = player.digs_per_set
        raw_reception = -(player.reception_errors / player.sets_played)
        raw_block = player.blk_per_s - (player.block_errors / player.sets_played)
        
        raw_scores = [raw_attack, raw_set, raw_serve, raw_dig, raw_reception, raw_block]
        
        # Save the target player's scores when we find them
        if player.pii_id == pii_id:
            target_raw_scores = raw_scores
            
        # Update mins and maxes
        for i in range(6):
            if raw_scores[i] < mins[i]:
                mins[i] = raw_scores[i]
            if raw_scores[i] > maxes[i]:
                maxes[i] = raw_scores[i]

    # If player not found
    if not target_raw_scores:
        return [0, 0, 0, 0, 0, 0]

    # Normalization scale 1-100
    final_scores = []
    for i in range(6):
        # In case only one entry exists
        if maxes[i] == mins[i]:
            final_scores.append(50) 
        else:
            normalized = ((target_raw_scores[i] - mins[i]) / (maxes[i] - mins[i])) * 100
            # Round to nearest integer for readability
            final_scores.append(round(normalized))

    return final_scores

def plot_player_radar_chart_b64(pii_id: int) -> str:
    # 1. Define the categories
    categories = ['Attack', 'Set', 'Serve', 'Dig', 'Reception', 'Block']
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    scores = generate_cumulative_scores(pii_id)

    angles = angles + [angles[0]]
    scores = scores + [scores[0]]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    ax.plot(angles, scores, color="#000000", linewidth=2, linestyle='solid')
    ax.fill(angles, scores, color="#dd880a", alpha=0.4)
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12, fontweight='bold')
    
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], color="grey", size=10)
    ax.set_ylim(0, 100)

    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    plt.close(fig)

    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64
    # player_name = get_player_name_by_pii_id(pii_id)
    # plt.title(f"Player Profile: {player_name}", size=15, y=1.1)
    # plt.show()


# dummyClass = get_career_statistics_by_pii_id_as_dataclass(1)

# print(dummyClass.assists_per_set)

# dummyScores = generate_cumulative_scores(1)
# for score in dummyScores:
#     print(score)

# fullCareerStats = get_all_career_stats_as_dataclass_array()
# for stat in fullCareerStats:
#     print(stat)

# normalizedScores = generate_cumulative_scores(1)
# for score in normalizedScores:
#     print(score)

# testScores = generate_cumulative_scores(1)
# plot_player_radar_chart("Test Player", testScores)

# plot_player_radar_chart(10)