'''
   Streamflix Database Data Generation Tests
   Script: data_test.py
   Description: Checks that the data for Streamflix was generated correctly
   Authors: Ashley Davis
'''

from data_generation import with_db_connection

# According to our data, we have 40 unique genres
@with_db_connection
def test1(conn, cursor):
    cursor.execute("SELECT * FROM Genre;")
    genres = cursor.fetchall()
    if len(genres) == 40:
        print("Test 1: \033[32mPASS\033[0m")
        return
    print("Test 1: \033[31mFAIL\033[0m")
    
    
# According to our data, Jennifer Aniston has acted in 1 Series and 2 Movies
@with_db_connection
def test2(conn, cursor):
    cursor.execute('''
                   SELECT vc.title 
                   FROM Actor a 
                   JOIN Content_Actor ca ON a.actor_id = ca.actor_id 
                   JOIN Video_Content vc ON ca.content_id = vc.content_id 
                   WHERE a.name = 'Jennifer Aniston';
                   ''')
    content = cursor.fetchall()
    if len(content) == 3:
        print("Test 2: \033[32mPASS\033[0m")
        return
    print("Test 2: \033[31mFAIL\033[0m")
    

# According to our data, David Fincher has directed 8 movies
@with_db_connection
def test3(conn, cursor):
    cursor.execute('''
                   SELECT vc.title 
                   FROM Director d 
                   JOIN Content_Director cd ON d.director_id = cd.director_id 
                   JOIN Video_Content vc ON cd.content_id = vc.content_id 
                   WHERE d.name = 'David Fincher';
                   ''')
    content = cursor.fetchall()
    if len(content) == 8:
        print("Test 3: \033[32mPASS\033[0m")
        return
    print("Test 3: \033[31mFAIL\033[0m")
    

# Based on the data design, no user should have more than 4 devices linked to their account
@with_db_connection
def test4(conn, cursor):
    cursor.execute('''
                    SELECT user_id, COUNT(device_id) AS device_count
                    FROM Device
                    GROUP BY user_id
                    HAVING COUNT(device_id) > 4;
                   ''')
    content = cursor.fetchall()
    if not content:
        print("Test 4: \033[32mPASS\033[0m")
        return
    print("Test 4: \033[31mFAIL\033[0m")
    
    
# Ensuring there are no duplicate video_content entries
@with_db_connection
def test5(conn, cursor):
    cursor.execute('''
                    SELECT title, COUNT(*)
                    FROM Video_Content
                    GROUP BY title
                    HAVING COUNT(*) > 1;
                   ''')
    content = cursor.fetchall()
    if not content:
        print("Test 5: \033[32mPASS\033[0m")
        return
    print("Test 5: \033[31mFAIL\033[0m")


# Ensuring the watch duration of a user metric entry aligns with the start and end time
@with_db_connection
def test6(conn, cursor):
    cursor.execute('''
                    SELECT metric_id, TIMESTAMPDIFF(SECOND, start_time, end_time) AS calculated_duration, duration
                    FROM User_Metrics
                    WHERE TIMESTAMPDIFF(SECOND, start_time, end_time) != duration;
                   ''')
    content = cursor.fetchall()
    if not content:
        print("Test 6: \033[32mPASS\033[0m")
        return
    print("Test 6: \033[31mFAIL\033[0m")


# There is one director who has produced at least 1 movie and 1 series
# Seeing what directors have produced at least 1 movie and 1 series
@with_db_connection
def test7(conn, cursor):
    cursor.execute('''
                    SELECT DISTINCT d.name, d.director_id
                    FROM Director d
                    JOIN Content_Director cd_movie ON d.director_id = cd_movie.director_id
                    JOIN Movie m ON cd_movie.content_id = m.content_id
                    JOIN Content_Director cd_series ON d.director_id = cd_series.director_id
                    JOIN Series s ON cd_series.content_id = s.content_id;
                   ''')
    content = cursor.fetchall()
    if len(content) == 1:
        print("Test 7: \033[32mPASS\033[0m")
        return
    print("Test 7: \033[31mFAIL\033[0m")


def main():
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()


if __name__ == "__main__":
   print('Testing Creation of Generated Data...\n')
   main()