import os
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import time
import argparse
import gc

class KNNRecommender:
    def __init__(self):
        self.bg_rating_threshold = 0
        self.user_rating_threshold = 0

        self.model = NearestNeighbors()

    def setFilterParams(self, bg_rating_threshold, user_rating_threshold):
        self.bg_rating_threshold = bg_rating_threshold
        self.user_rating_threshold = user_rating_threshold

    def setModelParams(self, n_neighbors, algorithm, metric, n_jobs = None):
        if n_jobs and (n_jobs > 1 or n_jobs == -1):
            os.environ['JOBLIB_TEMP_FOLDER'] = '/tmp'
        self.model.set_params(**{
            'n_neighbors': n_neighbors,
            'algorithm': algorithm,
            'metric': metric,
            'n_jobs': n_jobs})

    def _prepData(self):
        df_bg_info = pd.read_csv(
            'bg_info.csv',
            usecols = ['id', 'name'],
            dtype = {'id': 'int32', 'name': 'str'}
        )

        df_ratings = pd.read_csv(
            'bg_ratings.csv',
            usecols = ['game_id', 'username', 'rating'],
            dtype = {'game_id': 'int32', 'username': 'str', 'rating': 'float64'}
        )

        bg_user_mat = df_ratings.pivot_table(index = 'game_id', columns = 'username', values = 'rating', aggfunc = 'mean').fillna(0)

        hashmap = {
            game: i for i, game in
            enumerate(list(df_bg_info.set_index('id').loc[bg_user_mat.index].name))
        }

        bg_user_mat_sparse = csr_matrix(bg_user_mat.values)

        # clean up
        del df_bg_info
        del df_ratings, bg_user_mat
        gc.collect()
        return bg_user_mat_sparse, hashmap

    def _inference(self, model, data, hashmap, fav_bg, n_recommendations):

        model.fit(data)
        print(f'input: {fav_bg}')
        print('........\n')

        t_start = time.time()
        distances, indices = model.kneighbors(
            data['Gloomhaven'],
            n_neighbors=n_recommendations+1
        )

        raw_recommends = \
            sorted(
                list(
                    zip(
                        indices.squeeze().tolist(),
                        distances.squeeze().tolist()
                    )
                ),
                key=lambda x: x[1]
            )[:0:-1]
        print('It took my system {:.2f}s to make inference \n\
              '.format(time.time() - t_start))

        return raw_recommends

    def make_recommendations(self, fav_bg, n_recommendations):
        bg_user_mat_sparse, hashmap = self._prepData()
        raw_recommends = self._inference(
            self.model, bg_user_mat_sparse, hashmap,
            fav_bg, n_recommendations
        )
        print(raw_recommends)

        reverse_hashmap = {v: k for k, v in hashmap.items()}
        print('Recommendations for {}:'.format(fav_bg))
        for i, (idx, dist) in enumerate(raw_recommends):
            print('{0}: {1}, with distance '
                  'of {2}'.format(i+1, reverse_hashmap[idx], dist))

def parse_args():
    parser = argparse.ArgumentParser(
        prog="BGG Recommender",
        description="Run KNN BGG Recommender")
    parser.add_argument('--bg_id', nargs='?', default=174430,
                        help='provide your favorite bgg id')
    parser.add_argument('--top_n', type=int, default=10,
                        help='top n board game recommendations')
    return parser.parse_args()

if __name__ == '__main__':
    # get args
    args = parse_args()
    bg_id = args.bg_id
    top_n = args.top_n
    # initial recommender system
    recommender = KNNRecommender()
    # set params
    recommender.setFilterParams(50, 50)
    recommender.setModelParams(20, 'brute', 'cosine', -1)
    # make recommendations
    recommender.make_recommendations(bg_id, top_n)
