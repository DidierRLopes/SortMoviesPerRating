#!/usr/bin/python

# Import data packages
import pandas as pd
from imdb import IMDb
import os.path
import sys

filepath = sys.argv[1]

if not os.path.isfile(filepath):
    print(f"File {filepath} doesn't exist.")
    
else:
    # create an instance of the IMDb class
    ia = IMDb()

    d_movies_ratings = {}
    
    # Open file with movies list
    with open(filepath) as fp:
        
        print("Original movies list with year and IMDB rating added")
        
        # Read line from the document of the list of movies
        s_movie_title = fp.readline().strip('\n')
        
        # While there is a new movie title on the file
        while s_movie_title:
            
            # Search for movies with such title
            movies_with_title = ia.search_movie(s_movie_title)
            
            # If there is at least 1 movie with a similar title, then we're good
            if movies_with_title:
                
                # The movie that we want is usually the first one of the list, 
                #since it is the most famous / higher rating
                movie = ia.get_movie(movies_with_title[0].movieID)
                
                # Before gathering rating data, make sure that it exists
                if 'rating' in movie.data:    
                    n_rating = movie.data['rating']
                # Otherwise, attribute 0 to allow ranking, and put this movie at the bottom
                else:
                    n_rating = 0
                    
                # Before gathering year data, make sure that it exists
                if 'year' in movie.data:
                    n_year = movie.data['year']
                # Otherwise, attribute 0 which will be replaced at the end
                else:
                    n_year = 0
                
                s_year = ('????', n_year)[n_year>0]
                s_rating = ('??', n_rating)[n_rating>0]
                print(f"{s_movie_title} ({s_year}): {s_rating}")
                
                # Create dictionary with movie title as key, and values: year and rating
                d_movies_ratings[s_movie_title] = [n_year, n_rating]
                
            else:
                print(f"Error with movie: {s_movie_title}")

            # Read line from the document of the list of movies
            s_movie_title = fp.readline().strip('\n')

    # Create dataframe from dictionary
    df_movies_ratings = pd.DataFrame.from_dict(d_movies_ratings, columns=['year', 'rating'], orient='index')
    
    # Sort descending dataframe values by rating and then by year
    df_movies_ratings = df_movies_ratings.sort_values(by=['rating', 'year'], ascending=False)
    
    # Prepare dataframe to print
    df_movies_ratings.index.name = 'title'
    df_movies_ratings = df_movies_ratings.reset_index()

    # Open file to save list of movies ranked
    f = open(f"sorted_{filepath}", "w+")
        
    print("\nIMDB ranked movies")
    for rank, data in df_movies_ratings.iterrows():
        s_year = ('????', int(data['year']))[data['year'] > 0]
        s_rating = ('??', data['rating'])[data['rating'] > 0]
        s_movie = f"{1+rank:2}. {data['title']} ({s_year}): {s_rating}"
        print(s_movie)
        f.write(f"{s_movie}\n")

    # Close opened file
    f.close()