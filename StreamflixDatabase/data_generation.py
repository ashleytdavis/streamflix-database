'''
   Streamflix Database Data Generation
   Script: data_generation.py
   Description: Generates the data for the Streamflix database.
   Authors: Ashley Davis, Nicole Contreras, Khanh Nguyen, and Sai Kumar Reddy
'''

from faker import Faker
from functools import wraps
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import random, os

fake = Faker()
load_dotenv()

# Decorator to ensure database connection stays open and
# only rolls back when error occurs
def with_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            port=os.getenv('MYSQL_PORT'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'), 
            database="Streamflix"
        )
        cursor = conn.cursor()
        try:
            result = func(conn, cursor, *args, **kwargs)
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            conn.rollback()
            result = None
        finally:
            cursor.close()
            conn.close()
        return result
    return wrapper


# Read the CSV data from the file into a DataFrame
def csv_to_dataframe(file_path):
    df = pd.read_csv(file_path)
    df = df.dropna()  # Exclude rows with missing values in any column
    return df


# Initializes a database at the given file path
@with_db_connection
def initialize_database(conn, cursor):
    with open('StreamflixDatabase/streamflix-db.sql', 'r') as sql_file:
        schema = sql_file.read()
    for result in cursor.execute(schema, multi=True):
        try:
            if result.with_rows:
                result.fetchall()
        except mysql.connector.Error as err:
            print(f"Error processing SQL script: {err}")
            conn.rollback()
            return
    
    print("-->  Database schema initialized")


@with_db_connection
def insert_user_data(conn, cursor):
    subscription_options = ['Family', 'Student', 'Regular']
    for i in range(100):
        username = fake.user_name()
        password = "****"
        name = fake.name()
        email = fake.email()
        phone = fake.basic_phone_number().strip("()-+")
        date_of_birth = fake.date_of_birth()
        subscription_plan = subscription_options[random.randint(0, 2)]

        cursor.execute('''
            INSERT INTO User (user_id, username, password, name, email, phone, date_of_birth, subscription_plan)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (i, username, password, name, email, phone, date_of_birth, subscription_plan))
        
        insert_profile_data(cursor, i)
        insert_device_data(cursor, i)
            
            
    print("-->  User, Profile, and Device Data Generated and Populated")


def insert_profile_data(cursor, user_id):
    num_profiles = random.randint(1,4)
    
    for i in range(num_profiles):
        name = fake.name()
    
        cursor.execute('''
            INSERT INTO Profile (name, user_id)
            VALUES (%s, %s)
        ''', (name, user_id))
 

def insert_device_data(cursor, user_id):
    num_devices = random.randint(1,3)
    
    for i in range(num_devices):
        ip_address = fake.ipv4()
    
        cursor.execute('''
            INSERT INTO Device (ip_address, user_id)
            VALUES (%s, %s)
        ''', (ip_address, user_id))


@with_db_connection
def insert_movie_genre_actor_director_data(conn, cursor):
    movies = csv_to_dataframe('StreamflixDatabase/assets/imdb_top_1000_movies.csv')
    
    for i, row in movies.iterrows():
        title = row['Series_Title']
        description = row['Overview']
        duration = int(row['Runtime'].replace(' min', ''))
        country = fake.country()
        release_year = row['Released_Year'][:4]
        thumbnail = fake.pystr(max_chars=10)
        language = fake.language_name()
        genres = row['Genre']
        director_name = row['Director']
        actors = [row['Star1'], row['Star2'], row['Star3'], row['Star4']]
        
        if isinstance(genres, str):
            genres = [genre.strip() for genre in genres.split(',')] 

        cursor.execute('''
            INSERT INTO Video_Content (title, thumbnail, country, description, release_year, language)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (title, thumbnail, country, description, release_year, language))
        
        conn.commit()
        content_id = cursor.lastrowid

        cursor.execute('''
            INSERT INTO Movie (duration, content_id)
            VALUES (%s, %s)
        ''', (duration, content_id))
        
        conn.commit()
        movie_id = cursor.lastrowid

        processed_genres = set()

        for genre_name in genres:
            if genre_name not in processed_genres:
                processed_genres.add(genre_name)
            
                cursor.execute('''
                    SELECT genre_id FROM Genre WHERE name = %s
                ''', (genre_name,))
                result = cursor.fetchone()

                if result:
                    genre_id = result[0]
                else:
                    cursor.execute('''
                        INSERT INTO Genre (name)
                        VALUES (%s)
                    ''', (genre_name,))
                    conn.commit()
                    genre_id = cursor.lastrowid

                cursor.execute('''
                    INSERT INTO Content_Genre (content_id, genre_id)
                    VALUES (%s, %s)
                ''', (movie_id, genre_id))
                conn.commit()
        
        if pd.notna(director_name):
            cursor.execute('''
                SELECT director_id FROM Director WHERE name = %s
            ''', (director_name,))
            result = cursor.fetchone()

            if result:
                director_id = result[0]
            else:
                cursor.execute('''
                    INSERT INTO Director (name, date_of_birth, biography, content_id)
                    VALUES (%s, %s, %s, %s)
                ''', (director_name, fake.date_of_birth(), fake.paragraph(), content_id))
                conn.commit()
                director_id = cursor.lastrowid
            
            cursor.execute('''
                SELECT 1 FROM Content_Director WHERE content_id = %s AND director_id = %s
            ''', (movie_id, director_id))
            if cursor.fetchone() is None:
                cursor.execute('''
                    INSERT INTO Content_Director (content_id, director_id)
                    VALUES (%s, %s)
                ''', (movie_id, director_id))
                conn.commit()

        processed_actors = set()
        for actor_name in actors:
            if pd.notna(actor_name) and actor_name not in processed_actors:
                processed_actors.add(actor_name)
                cursor.execute('''
                    SELECT actor_id FROM Actor WHERE name = %s
                ''', (actor_name,))
                result = cursor.fetchone()

                if result:
                    actor_id = result[0]
                else:
                    cursor.execute('''
                        INSERT INTO Actor (name, date_of_birth, gender, biography, content_id)
                        VALUES (%s, %s, %s, %s, %s)
                    ''', (actor_name, fake.date_of_birth(), fake.passport_gender(), fake.paragraph(), content_id))
                    conn.commit()
                    actor_id = cursor.lastrowid

                cursor.execute('''
                    SELECT 1 FROM Content_Actor WHERE content_id = %s AND actor_id = %s
                ''', (movie_id, actor_id))
                if cursor.fetchone() is None:
                    cursor.execute('''
                        INSERT INTO Content_Actor (content_id, actor_id)
                        VALUES (%s, %s)
                    ''', (movie_id, actor_id))
                    conn.commit()

    print("-->  Movie, Genre, Actor, and Director Data Generated and Populated")
    

@with_db_connection
def insert_series_data(conn, cursor):
    series_df = csv_to_dataframe('StreamflixDatabase/assets/netflix_top_series.csv')
    series_df = series_df[series_df['type'] == 'TV Show']
    
    for i, row in series_df.iterrows():
        title = row['title']
        description = row['description']
        release_year = str(int(row['release_year']))
        country = row['country']
        language = fake.language_name()
        genres = row['listed_in'].split(', ')
        director_name = row['director']
        actors = row['cast'].split(', ')

        cursor.execute('''
            INSERT INTO Video_Content (title, thumbnail, country, description, release_year, language)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (title, fake.pystr(max_chars=10), country, description, release_year, language))
        conn.commit()

        content_id = cursor.lastrowid

        cursor.execute('''
            INSERT INTO Series (content_id)
            VALUES (%s)
        ''', (content_id,))
        conn.commit()

        series_id = cursor.lastrowid
        
        for genre in genres:
            cursor.execute('SELECT genre_id FROM Genre WHERE name = %s', (genre,))
            genre_row = cursor.fetchone()
            
            if genre_row:
                genre_id = genre_row[0]
            else:
                cursor.execute('INSERT INTO Genre (name) VALUES (%s)', (genre,))
                conn.commit()
                genre_id = cursor.lastrowid
            
            cursor.execute('''
                INSERT INTO Content_Genre (content_id, genre_id)
                VALUES (%s, %s)
            ''', (content_id, genre_id))
            conn.commit()
            
            # Insert Director
            if pd.notna(director_name):
                cursor.execute('SELECT director_id FROM Director WHERE name = %s', (director_name,))
                director_row = cursor.fetchone()

                if director_row:
                    director_id = director_row[0]
                else:
                    cursor.execute('''
                        INSERT INTO Director (name, date_of_birth, biography, content_id)
                        VALUES (%s, %s, %s, %s)
                    ''', (director_name, fake.date_of_birth(), fake.paragraph(), content_id))
                    conn.commit()
                    director_id = cursor.lastrowid

                # Check for existing Content_Director entry
                cursor.execute('''
                    SELECT 1 FROM Content_Director WHERE content_id = %s AND director_id = %s
                ''', (content_id, director_id))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO Content_Director (content_id, director_id)
                        VALUES (%s, %s)
                    ''', (content_id, director_id))
                    conn.commit()

            # Insert Actors
            processed_actors = set()
            for actor_name in actors:
                if pd.notna(actor_name) and actor_name not in processed_actors:
                    processed_actors.add(actor_name)
                    
                    cursor.execute('SELECT actor_id FROM Actor WHERE name = %s', (actor_name,))
                    actor_row = cursor.fetchone()

                    if actor_row:
                        actor_id = actor_row[0]
                    else:
                        cursor.execute('''
                            INSERT INTO Actor (name, date_of_birth, gender, biography, content_id)
                            VALUES (%s, %s, %s, %s, %s)
                        ''', (actor_name, fake.date_of_birth(), fake.passport_gender(), fake.paragraph(), content_id))
                        conn.commit()
                        actor_id = cursor.lastrowid

                    # Check for existing Content_Actor entry
                    cursor.execute('''
                        SELECT 1 FROM Content_Actor WHERE content_id = %s AND actor_id = %s
                    ''', (content_id, actor_id))
                    if not cursor.fetchone():
                        cursor.execute('''
                            INSERT INTO Content_Actor (content_id, actor_id)
                            VALUES (%s, %s)
                        ''', (content_id, actor_id))
                        conn.commit()

        total_episodes = random.randint(1, 50) 
        insert_season_data(conn, cursor, series_id, total_episodes)
        
    print("-->  Series, Season, and Episode Data Generated and Populated")
    
    
def insert_season_data(conn, cursor, series_id, total_episodes):
    num_seasons = random.randint(1, 5)
    episodes_per_season = max(1, total_episodes // num_seasons)
    
    for i in range(num_seasons):
        cursor.execute('''
            INSERT INTO Season (series_id)
            VALUES (%s)
        ''', (series_id,))
        conn.commit()
        season_id = cursor.lastrowid

        insert_episode_data(conn, cursor, season_id, episodes_per_season)
        

def insert_episode_data(conn, cursor, season_id, episodes_per_season):
    for i in range(episodes_per_season):
        title = fake.sentence(nb_words=5)
        duration = random.randint(20, 60)
        
        cursor.execute('''
            INSERT INTO Episode (title, duration, season_id)
            VALUES (%s, %s, %s)
        ''', (title, duration, season_id))
        conn.commit()


@with_db_connection
def insert_review_data(conn, cursor):
    df = csv_to_dataframe('StreamflixDatabase/assets/generic_movie_series_reviews.csv')

    df['Date Posted'] = pd.to_datetime(df['Date Posted'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')
    
    cursor.execute('SELECT content_id FROM Video_Content')
    content_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT user_id FROM User')
    user_ids = [row[0] for row in cursor.fetchall()]

    for content_id in content_ids:
        num_reviews = random.randint(1, 30)
        
        sampled_reviews = df.sample(n=num_reviews, replace=True).reset_index(drop=True)
        
        for i, row in sampled_reviews.iterrows():
            user_id = random.choice(user_ids)
            
            cursor.execute('''
                INSERT INTO Review (review_content, stars, user_id, date_posted)
                VALUES (%s, %s, %s, %s)
            ''', (row['Review'], row['Stars'], user_id, row['Date Posted']))
            
            review_id = cursor.lastrowid

            cursor.execute('''
                INSERT INTO Content_Review (content_id, review_id)
                VALUES (%s, %s)
            ''', (content_id, review_id))

    print("-->  Reviews Data Generated and Populated")

    

@with_db_connection
def insert_my_list_data(conn, cursor):
    cursor.execute('SELECT user_id FROM User')
    user_ids = cursor.fetchall()

    cursor.execute('SELECT content_id FROM Video_Content')
    content_ids = cursor.fetchall()
    
    list_names = ["Favorites", "Watch Later", "Must Watch", "Classics", "Top Picks"]
    
    for user in user_ids:
        user_id = user[0]
        num_lists = random.randint(1, 3)

        for i in range(num_lists):
            list_name = random.choice(list_names)

            cursor.execute('''
                INSERT INTO My_List (name, user_id)
                VALUES (%s, %s)
            ''', (list_name, user_id))
            conn.commit()
            mylist_id = cursor.lastrowid

            num_items = random.randint(3, 10)
            selected_content_ids = random.sample(content_ids, num_items)

            for content in selected_content_ids:
                content_id = content[0]

                cursor.execute('''
                    INSERT INTO Listed_Content (content_id, mylist_id)
                    VALUES (%s, %s)
                ''', (content_id, mylist_id))
            conn.commit()

    print("-->  User Lists Data Generated and Populated")
    

@with_db_connection
def insert_user_metrics_data(conn, cursor):
    cursor.execute('SELECT user_id FROM User')
    user_ids = cursor.fetchall()

    cursor.execute('SELECT content_id FROM Video_Content')
    content_ids = cursor.fetchall()

    for i in range(800):
        user_id = random.choice(user_ids)[0]
        content_id = random.choice(content_ids)[0]
        start_time = fake.date_time_between(start_date='-1y', end_date='now')
        duration = random.randint(10, 240)
        end_time = start_time + timedelta(minutes=duration)
        completed = random.choice([True, False])

        cursor.execute('''
            INSERT INTO User_Metrics (start_time, end_time, duration, completed, content_id, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (start_time, end_time, duration, completed, content_id, user_id))
        conn.commit()

    print("-->  User Metrics Data Generated and Populated")
          

def main():  
    # Initialize the database schema
    initialize_database()
    
    # Generate and insert data
    insert_user_data()                           # User, Profile, and Device Data
    insert_movie_genre_actor_director_data()     # Video_Content, Movie, Genre, Actor, Director, Movie_Actor, Movie_Genre, Movie_Director Data
    insert_series_data()                         # Video_Content, Series, Season, and Episode Data
    insert_review_data()                         # Review and Content_Review Data
    insert_my_list_data()                        # My_List and Listed_Content Data
    insert_user_metrics_data()                   # User_Metrics Data
    
    print('\n\n-->  Data Generation Complete!\n\n')


if __name__ == "__main__":
    main()
