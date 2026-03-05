use TransPort;

CREATE TABLE IF NOT EXISTS player_identifying_information (
	pii_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    Hometown VARCHAR(50) NOT NULL,
    Eligibility VARCHAR(20) NOT NULL,
    Position VARCHAR(50) NOT NULL,
    Height FLOAT NOT NULL,
    school VARCHAR(50) NOT NULL

);

CREATE TABLE IF NOT EXISTS career_statistics (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    sets_played INT NOT NULL, 
    kills INT NOT NULL,
    kills_per_set FLOAT NOT NULL,
    errs INT NOT NULL, -- Errors
    total_attempts INT NOT NULL, 
    attack_percentage FLOAT NOT NULL, -- Maybe?
    assits INT NOT NULL,
    assists_per_set FLOAT NOT NULL,
    serve_aces INT NOT NULL,
    serve_errors INT NOT NULL,
    serve_aces_per_set FLOAT NOT NULL,
    reception_errors INT NOT NULL,
    digs INT NOT NULL,
    digs_per_set FLOAT NOT NULL,
    block_solos INT NOT NULL,
    block_assists INT NOT NULL,
    blk FLOAT NOT NULL, -- IDK
    blk_per_s FLOAT NOT NULL, -- IDK BLK
    block_errors INT NOT NULL,
    ball_handling_errors INT NOT NULL,
    points FLOAT NOT NULL,
    
    pii_id int,
    FOREIGN KEY (pii_id) REFERENCES player_identifying_information (pii_id)
);

CREATE TABLE IF NOT EXISTS game_statistics (
	game_id INT AUTO_INCREMENT PRIMARY KEY,
    game_date DATE NOT NULL,
    opponent VARCHAR(50) NOT NULL,
    sets_played INT NOT NULL,
	kills INT NOT NULL,
    errs INT NOT NULL, -- Errors
    total_attempts INT NOT NULL, 
    attack_percentage FLOAT NOT NULL, -- Maybe?
    assits INT NOT NULL,
    serve_aces INT NOT NULL,
    serve_errors INT NOT NULL,
    reception_errors INT NOT NULL,
    digs INT NOT NULL,
    block_solos INT NOT NULL,
    block_assists INT NOT NULL,
    block_errors INT NOT NULL,
    ball_handling_errors INT NOT NULL,
	total_blocks INT NOT NULL,
    
    pii_id INT NOT NULL,
    FOREIGN KEY (pii_id) REFERENCES player_identifying_information (pii_id)
);
