import sqlite3

connection = sqlite3.connect("user_data.db")
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS accounts(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, rightscore INTEGER, leftscore INTEGER, indscore INTEGER)"""
#command = """INSERT INTO polls (name, party, bio, state, run) VALUES ('Val Demings', 'Democratic Party', 'Congresswoman Val Demings represents Floridas 10th Congressional District in the U.S. House of Representatives. Demings is a lifelong public servant who broke numerous glass ceilings in her rise through the Orlando Police Department and her election to Congress. Today, she works on the House Judiciary, Homeland Security, and Intelligence Committees. In 2020, she broke another glass ceiling and continued her career as a guardian of the law when she became one of the first women and one of the first Black Americans to prosecute a presidential impeachment before the U.S. Senate.', 'FL', 'Senator')"""
#command = """INSERT INTO candidates (name, party, bio, state, run) VALUES ('Marco Rubio', 'Republican Party', 'Marco Rubio has represented Florida in the United States Senate since 2010, where he has one guiding objective: bring the American Dream back into the reach of those who feel it slipping away. Senator Rubios efforts have been successful and long-lasting. Non-partisan analyses by GovTrack and the Center for Effective Lawmaking ranked Rubio the Senates number two leader and most effective Republican in 2020. Senator Rubio currently serves as Vice Chairman of the Senate Select Committee on Intelligence, where he oversees our nations intelligence and national security apparatus. Senator Rubio is also a member of the Foreign Relations Committee, where he fights to promote human rights and Americas interests around the globe; the powerful Appropriations Committee, which allocates funding for the federal government; and the Special Committee on Aging, dedicated to the needs of older Americans.', 'FL', 'Senator')"""
#command = """INSERT INTO candidates (state) WHERE name = 'Marco Rubio' VALUES ('FL')"""

cursor.execute(command)
connection.commit()

#cursor.execute("INSERT INTO users VALUES (1, 'Aakriti', 'ashah@rollins.edu', 'blah')")

#connection.commit()
