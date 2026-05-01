import base64
from io import BytesIO

import matplotlib.pyplot as plt
from dataclasses import dataclass
from datetime import date

@dataclass
class GameStatistics:
    game_id: int 
    game_date: date
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

g1 = GameStatistics(
    game_id=1,
    game_date=date(2025, 9, 6),
    opponent="Colorado Mesa",
    sets_played=4,
    kills=12,
    errs=5,
    total_attempts=38,
    attack_percentage=0.184, 
    assists=2,
    serve_aces=1,
    serve_errors=2,
    reception_errors=1,
    digs=9,
    block_solos=1,
    block_assists=2,
    block_errors=0,
    ball_handling_errors=1,
    total_blocks=3,
    pii_id=101
)

g2 = GameStatistics(
    game_id=2,
    game_date=date(2025, 9, 13),
    opponent="Fort Lewis",
    sets_played=5,
    kills=18,
    errs=7,
    total_attempts=52,
    attack_percentage=0.212,
    assists=1,
    serve_aces=3,
    serve_errors=4,
    reception_errors=2,
    digs=14,
    block_solos=0,
    block_assists=4,
    block_errors=1,
    ball_handling_errors=0,
    total_blocks=4,
    pii_id=101
)

g3 = GameStatistics(
    game_id=3,
    game_date=date(2025, 10, 2),
    opponent="UCCS",
    sets_played=3,
    kills=7,
    errs=1,
    total_attempts=19,
    attack_percentage=0.316,
    assists=0,
    serve_aces=0,
    serve_errors=1,
    reception_errors=0,
    digs=6,
    block_solos=2,
    block_assists=1,
    block_errors=0,
    ball_handling_errors=2,
    total_blocks=3,
    pii_id=205
)

g4 = GameStatistics(
    game_id=4,
    game_date=date(2025, 10, 9),
    opponent="Western State",
    sets_played=5,
    kills=15,
    errs=1,
    total_attempts=19,
    attack_percentage=0.316,
    assists=0,
    serve_aces=0,
    serve_errors=1,
    reception_errors=0,
    digs=6,
    block_solos=2,
    block_assists=1,
    block_errors=0,
    ball_handling_errors=2,
    total_blocks=3,
    pii_id=205
)

g5 = GameStatistics(
    game_id=5,
    game_date=date(2025, 10, 16),
    opponent="Montana State",
    sets_played=4,
    kills=21,
    errs=1,
    total_attempts=19,
    attack_percentage=0.316,
    assists=0,
    serve_aces=0,
    serve_errors=1,
    reception_errors=0,
    digs=6,
    block_solos=2,
    block_assists=1,
    block_errors=0,
    ball_handling_errors=2,
    total_blocks=3,
    pii_id=205
)

g6 = GameStatistics(
    game_id=6,
    game_date=date(2025, 10, 23),
    opponent="Northern Colorado",
    sets_played=0,
    kills=0,
    errs=0,
    total_attempts=0,
    attack_percentage=0.0,
    assists=0,
    serve_aces=0,
    serve_errors=0,
    reception_errors=0,
    digs=0,
    block_solos=0,
    block_assists=0,
    block_errors=0,
    ball_handling_errors=0,
    total_blocks=0,
    pii_id=205
)

test_games = [g1, g2, g3, g4, g5, g6]

import DatabaseConnection as db

def get_all_games_for_pii_id_as_dataclass_array(pii_id: int) -> list[db.GameStatistics]:
    query = "SELECT * FROM game_statistics WHERE pii_id = ?"
    params = (pii_id,)
    results = db.execute_read(query, params)
    
    games = []
    for row in results:
        game = db.GameStatistics(
            game_id=row[0],
            game_date=row[1],
            opponent=row[2],
            sets_played=row[3],
            kills=row[4],
            errs=row[5],
            total_attempts=row[6],
            attack_percentage=row[7],
            assists=row[8],
            serve_aces=row[9],
            serve_errors=row[10],
            reception_errors=row[11],
            digs=row[12],
            block_solos=row[13],
            block_assists=row[14],
            block_errors=row[15],
            ball_handling_errors=row[16],
            total_blocks=row[17],
            pii_id=row[18]
        )
        games.append(game)
    return games


def plot_stat_over_games_b64(games, stat_name) -> str:
    stat_values = [getattr(game, stat_name) for game in games]
    avg_value = sum(stat_values) / len(stat_values) if stat_values else 0

    game_dates = []
    for game in games:
        # Slices from the start to the 5th character. "10/11/2025" -> "10/11"
        date_str = game.game_date.rsplit('/', 1)[0]
        game_dates.append(date_str)

    plt.figure(figsize=(10, 5))

    plt.plot(game_dates, stat_values, marker='o')
    for i, val in enumerate(stat_values):
        plt.annotate(f"{val}",  (game_dates[i], val), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.axhline(avg_value, color='red', linestyle='--', label=f'Average: {avg_value:.2f}')
    plt.title(f'{stat_name.replace("_", " ").title()} Over Games')
    plt.xlabel('Game Date')
    plt.ylabel(stat_name.replace("_", " ").title())
    plt.xticks(rotation=45)
    plt.grid()
    plt.legend()

    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    plt.close()

    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

def trend_percentages(games, stat_name):
    increases = 0
    decreases = 0

    for i in range(1, len(games)):
        prev_value = getattr(games[i - 1], stat_name)
        curr_value = getattr(games[i], stat_name)

        if curr_value > prev_value:
            increases += 1
        elif curr_value < prev_value:
            decreases += 1

    total_comparisons = len(games) - 1

    increase_pct = (increases / total_comparisons) * 100
    decrease_pct = (decreases / total_comparisons) * 100

    return increase_pct, decrease_pct

def percent_of_games_played(games):
    total_games = len(games)
    games_played = 0
    games_not_played = 0

    for g in games:
        if g.sets_played > 0:
            games_played += 1
        else:
            games_not_played += 1

    pct_played = (games_played / total_games) * 100
    pct_not_played = (games_not_played / total_games) * 100
    
    return pct_played, pct_not_played

#plot_stat_over_games(test_games, 'kills')

# x, y = trend_percentages(test_games, 'kills')
# print(f"Kill increases: {x:.2f}%")
# print(f"Kill decreases: {y:.2f}%")

# a, b = percent_of_games_played(test_games)
# print(f"Games played: {a:.2f}%")
# print(f"Games not played: {b:.2f}%")

# games = get_all_games_for_pii_id_as_dataclass_array(14)

# plot_stat_over_games(games, 'kills')

# for g in games:
#     print(g.game_date, g.opponent, g.kills)