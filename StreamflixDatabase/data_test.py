'''
   Streamflix Database Data Generation Tests
   Script: data_test.py
   Description: Checks that the data for Streamflix was generated correctly
   Authors: Ashley Davis
'''

from data_generation import with_db_connection

# Function to check if users were inserted correctly
@with_db_connection
def check_users(conn, cursor):
    cursor.execute("SELECT * FROM User LIMIT 5;")
    users = cursor.fetchall()
    print("Users:")
    for user in users:
        print(user)
        
# Function to check if profiles were inserted correctly
@with_db_connection
def check_profiles(conn, cursor):
    cursor.execute("SELECT * FROM Profile LIMIT 5;")
    profiles = cursor.fetchall()
    print("Profiles:")
    for profile in profiles:
        print(profile)
        
# Function to check if devices were inserted correctly
@with_db_connection
def check_devices(conn, cursor):
    cursor.execute("SELECT * FROM Device LIMIT 5;")
    devices = cursor.fetchall()
    print("Devices:")
    for device in devices:
        print(device)
        
# Function to check if series were inserted correctly
@with_db_connection
def check_series(conn, cursor):
    cursor.execute("SELECT * FROM Series LIMIT 5;")
    series = cursor.fetchall()
    print("Series:")
    for s in series:
        print(s)

# Function to check if seasons were inserted correctly
@with_db_connection
def check_seasons(conn, cursor):
    cursor.execute("SELECT * FROM Season LIMIT 5;")
    seasons = cursor.fetchall()
    print("Seasons:")
    for season in seasons:
        print(season)
        
# Function to check if seasons were inserted correctly
@with_db_connection
def check_episodes(conn, cursor):
    cursor.execute("SELECT * FROM Episode LIMIT 5;")
    episodes = cursor.fetchall()
    print("Episodes:")
    for episode in episodes:
        print(episode)
        
# Function to check video content, movies, and genres
@with_db_connection
def check_video_content_and_related(conn, cursor):
    # Check Video Content table
    cursor.execute("SELECT * FROM Video_Content LIMIT 5;")
    videos = cursor.fetchall()
    print("Video Content:")
    for video in videos:
        print(video)
    
    # Check Movie table
    cursor.execute("SELECT * FROM Movie LIMIT 5;")
    movies = cursor.fetchall()
    print("\nMovies:")
    for movie in movies:
        print(movie)
    
    # Check Genre table
    cursor.execute("SELECT * FROM Genre LIMIT 5;")
    genres = cursor.fetchall()
    print("\nGenres:")
    for genre in genres:
        print(genre)
    
    # Check Movie_Genre table
    cursor.execute("SELECT * FROM Movie_Genre LIMIT 5;")
    movie_genres = cursor.fetchall()
    print("\nMovie-Genre Associations:")
    for movie_genre in movie_genres:
        print(movie_genre)
        
# Function to check if actors and directors were inserted correctly
@with_db_connection
def check_actors_and_directors(conn, cursor):
    # Check Actor table
    cursor.execute("SELECT * FROM Actor LIMIT 5;")
    actors = cursor.fetchall()
    print("\nActors:")
    for actor in actors:
        print(actor)

    # Check Director table
    cursor.execute("SELECT * FROM Director LIMIT 5;")
    directors = cursor.fetchall()
    print("\nDirectors:")
    for director in directors:
        print(director)

    # Check Movie_Actor table
    cursor.execute("SELECT * FROM Movie_Actor LIMIT 5;")
    movie_actors = cursor.fetchall()
    print("\nMovie-Actor Associations:")
    for movie_actor in movie_actors:
        print(movie_actor)
    
    # Check Movie_Director table
    cursor.execute("SELECT * FROM Movie_Director LIMIT 5;")
    movie_directors = cursor.fetchall()
    print("\nMovie-Director Associations:")
    for movie_director in movie_directors:
        print(movie_director)
        
# Function to check if reviews were inserted correctly
@with_db_connection
def check_reviews_and_content_reviews(conn, cursor):
    # Check Review table
    cursor.execute("SELECT * FROM Review LIMIT 5;")
    reviews = cursor.fetchall()
    print("Reviews:")
    for review in reviews:
        print(review)
    
    # Check Content_Review table
    cursor.execute("SELECT * FROM Content_Review LIMIT 5;")
    content_reviews = cursor.fetchall()
    print("\nContent-Review Associations:")
    for content_review in content_reviews:
        print(content_review)
        
   # Function to check if lists and listed content were inserted correctly
@with_db_connection
def check_lists_and_listed_content(conn, cursor):
    # Check My_List table
    cursor.execute("SELECT * FROM My_List LIMIT 5;")
    lists = cursor.fetchall()
    print("My Lists:")
    for list in lists:
        print(list)

    # Check Listed_Content table
    cursor.execute("SELECT * FROM Listed_Content LIMIT 5;")
    listed_contents = cursor.fetchall()
    print("\nListed Content:")
    for listed_content in listed_contents:
        print(listed_content)

# Function to check user metrics were inserted correctly
@with_db_connection
def check_user_metrics(conn, cursor):
    cursor.execute("SELECT * FROM User_Metrics LIMIT 5;")
    metrics = cursor.fetchall()
    print("User Metrics:")
    for metric in metrics:
        print(metric)

def main():
   check_users()
   check_profiles()
   check_devices()
   check_series()
   check_seasons()
   check_episodes()
   check_video_content_and_related()
   check_actors_and_directors()
   check_reviews_and_content_reviews()
   check_lists_and_listed_content()
   check_user_metrics()


if __name__ == "__main__":
   print('Testing Creation of Generated Data...\n\n')
   main()