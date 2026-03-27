import matplotlib.pyplot as plt
import DatabaseConnection as db
import numpy as np
import pandas as pd

### Generate stat category scores -- this could be changed to be more rigourous, but simple for now 
### Scores for: Attack, Set, Serve, Dig, Reception, Block 
def calculate_attack_cumulative_score(pii_id):
    career_stats = db.get_career_statistics_by_pii_id_as_class(pii_id)
    if not career_stats:
        return 0  

    #effeciency weighted slightly above volume -- arbitrary for now, talk to client
    attack_score = (career_stats.kills_per_set * 0.4) + (career_stats.attack_percentage * 100 * 0.6)

    return round(attack_score, 2)

def calculate_set_cumulative_score(pii_id):
    career_stats = db.get_career_statistics_by_pii_id_as_class(pii_id)
    if not career_stats:
        return 0  

    assists_per_set = career_stats.assists / career_stats.sets_played
    set_score = (career_stats.assists_per_set * 0.4) + (assists_per_set * 0.6)

    return round(set_score, 2)

def calculate_serve_cumulative_score(pii_id):
    career_stats = db.get_career_statistics_by_pii_id_as_class(pii_id)
    if not career_stats:
        return 0  

    errors_per_set = career_stats.serve_errors / career_stats.sets_played

    # Weight aces positively, errors negatively
    serve_score = (career_stats.serve_aces_per_set * 0.6) - (errors_per_set * 0.4)
    return round(serve_score, 2)

def calculate_dig_cumulative_score(pii_id):
    career_stats = db.get_career_statistics_by_pii_id_as_class(pii_id)
    if not career_stats:
        return 0
    
    # placeholder for if/when score calculation becomes more complex
    return round(career_stats.digs_per_set)


def calculate_reception_cumulative_score(pii_id):
    career_stats = db.get_career_statistics_by_pii_id_as_class(pii_id)
    if not career_stats or career_stats.sets_played == 0:
        return 0

    reception_errors_per_set = career_stats.reception_errors / career_stats.sets_played
    reception_score = max(0, 10 - (reception_errors_per_set * 10))

    return round(reception_score, 2)

def calculate_block_cumulative_score(pii_id):
    career_stats = db.get_career_statistics_by_pii_id_as_class(pii_id)
    if not career_stats or career_stats.sets_played == 0:
        return 0

    block_errors_per_set = career_stats.block_errors / career_stats.sets_played
    block_score = (career_stats.blk_per_s * 0.6) - (block_errors_per_set * 0.4)

    return round(max(0, block_score), 2)


print(calculate_attack_cumulative_score(1))
print(calculate_set_cumulative_score(1))
print(calculate_serve_cumulative_score(1))
print(calculate_dig_cumulative_score(1))
print(calculate_reception_cumulative_score(1))
print(calculate_block_cumulative_score(1))