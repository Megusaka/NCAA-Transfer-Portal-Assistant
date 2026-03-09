import random
import DatabaseConnection as db

def generate_test_pii(N):

    for i in range(N):
        p = db.PlayerIdentifyingInformation(
            pii_id=None,
            first_name=f"FirstName{i}",
            last_name=f"LastName{i}",
            school=f"School{i}"
        )
        db.insert_into_player_identifying_information(p)
    return print("Test pii data generated successfully.")

def generate_test_career_stats(N):
    for i in range(N):
        kills=random.randint(1, 230)
        assists=random.randint(1, 400)
        digs=random.randint(1, 400)
        blk=random.randint(1, 100)
        sets_played=random.randint(1, 100)
        cs = db.CareerStatistics(
            player_id=None,
            sets_played=sets_played,
            kills=kills,
            errs=random.randint(1, 150),
            total_attempts=random.randint(1, 800),
            attack_percentage=round(random.uniform(0.0, 0.2), 3),
            assists=assists,
            serve_aces=random.randint(1, 50),
            serve_errs=random.randint(1, 50),
            reception_errors=random.randint(1, 50),
            digs=digs,
            block_solos=random.randint(1, 25),
            block_assists=random.randint(1, 75),
            blk=blk,
            block_errors=random.randint(1, 10),
            ball_handling_errors=random.randint(1, 5),
            kills_per_set = round((kills / sets_played), 2),
            assists_per_set = round((assists / sets_played), 2),
            digs_per_set = round((digs / sets_played), 2),
            blk_per_set = round((blk / sets_played), 2),
            pii_id=i
        )
        db.insert_into_career_statistics(cs)

    return print("Test career stats data generated successfully.")

#generate_test_pii(10)
print(db.get_all_player_data())
