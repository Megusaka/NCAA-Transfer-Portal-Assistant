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
        cs = db.CareerStatistics(
            player_id=None,
            sets_played=random.randint(1, 100),
            kills=random.randint(1, 230),
            errs=random.randint(1, 150),
            total_attempts=random.randint(1, 800),
            attack_percentage=round(random.uniform(0.0, 0.2), 3),
            assists=random.randint(1, 400),
            




    return print("Test career stats data generated successfully.")

#generate_test_pii(10)
print(db.get_all_player_data())
