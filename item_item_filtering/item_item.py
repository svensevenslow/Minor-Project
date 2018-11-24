import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
import sklearn
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors

def recommender():
    movies = pd.read_csv("movies_new.csv")
    ratings = pd.read_csv("ratings_new.csv")
    users = pd.read_csv("users_new.csv")

    combine_movie_rating = pd.merge(movies, ratings, on='movie_id')
    combine_movie_rating = combine_movie_rating.drop(['serial_no_x', 'serial_no_y', 'timestamp'], axis = 1)

    combine_movie_rating = combine_movie_rating.dropna(axis = 0, subset = ['movie_title'])

    movie_ratingCount = (combine_movie_rating.
                            groupby(by = ['movie_title'])['rating'].
                            count().
                            reset_index().
                            rename(columns = {'rating': 'TotalRatingCount'})
                            [['movie_title', 'TotalRatingCount']]
                        )

    combine_movie_rating_with_rating_count = pd.merge(movie_ratingCount, combine_movie_rating, on='movie_title')

    combine_movie_rating_with_rating_count = combine_movie_rating_with_rating_count.drop(['movie_genre'], axis = 1)


    popularity_threshold = 1784
    rating_popular_movie = combine_movie_rating_with_rating_count.query('TotalRatingCount >= @popularity_threshold')

    rating_popular_movie_user_location = pd.merge(rating_popular_movie, users, on='user_id')
    rating_popular_movie_user_location = rating_popular_movie_user_location.drop(['serial_no', 'gender', 'age','occupation'], axis = 1)

    rating_popular_movie_user_location_filtered = rating_popular_movie_user_location[(rating_popular_movie_user_location['zipcode'] >= '10000') & (rating_popular_movie_user_location['zipcode'] <= '40000')]


    rating_popular_movie_user_location_filtered_pivot = rating_popular_movie_user_location_filtered.pivot(index = 'movie_title', columns = 'user_id', values = 'rating').fillna(0)
    rating_popular_movie_user_location_filtered_matrix = csr_matrix(rating_popular_movie_user_location_filtered_pivot.values)

    model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    model_knn.fit(rating_popular_movie_user_location_filtered_matrix)

    query_index = np.random.choice(rating_popular_movie_user_location_filtered_pivot.shape[0])
    distances, indices = model_knn.kneighbors(rating_popular_movie_user_location_filtered_pivot.iloc[query_index, :].values.reshape(1, -1), n_neighbors = 7)

    movie_string = ""
    recommendations = []

    for i in range(0, len(distances.flatten())):
        if i == 0:
            movie_string = 'Recommendations for {0}:\n'.format(rating_popular_movie_user_location_filtered_pivot.index[query_index])
            #print(movie_string)
        else:
            recommendation_string = '{0}: {1}:'.format(i, rating_popular_movie_user_location_filtered_pivot.index[indices.flatten()[i]])
            recommendations.append(recommendation_string)
            #print(recommendation_string)

    return movie_string, recommendations
