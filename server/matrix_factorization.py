import pandas as pd
import numpy as np
import os
from scipy.sparse.linalg import svds

ratings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bg_ratings.csv')
info_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bg_info.csv')

ratings_df = pd.read_csv(ratings_file)
bg_df = pd.read_csv(info_file)

v = ratings_df.username.value_counts()
ratings_df = ratings_df[ratings_df.username.isin(v.index[v.gt(20)])]

R_df = ratings_df.pivot_table(index = 'username', columns = 'game_id', values = 'rating', aggfunc = 'mean').fillna(0)
R = R_df.to_numpy()
user_ratings_mean = np.mean(R, axis = 1)
#R_demeaned = R - user_ratings_mean.reshape(-1, 1)

U, sigma, Vt = svds(R, k = 50)

sigma = np.diag(sigma)

all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1,1)
preds_df = pd.DataFrame(all_user_predicted_ratings, columns = R_df.columns)
userID_dict = {}
i = 0
for user in R_df.index:
    userID_dict[user] = i
    i += 1

def recommender(username, predictions_df = preds_df, board_df = bg_df, original_ratings_df = ratings_df, num_recommendations = 10):
    if (not username in userID_dict):
        return None

    userID = userID_dict[username]

    sorted_user_predictions = predictions_df.loc[userID].sort_values(ascending = False)

    user_data = original_ratings_df[original_ratings_df.username == username]
    user_full = (user_data.merge(board_df, how = 'left', left_on = 'id', right_on = 'id').
                    sort_values(['rating'], ascending = False)
                )

    print(f'User {userID} has already rated {user_full.shape[0]} board games.')
    print(f'Recommending the highest {num_recommendations} predicted board games not already rated.')

    recommendations = (bg_df[~bg_df['id'].isin(user_full['id'])].
        merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
            left_on = 'id',
            right_on = 'id').
        rename(columns = {userID: 'Predictions'}).
        sort_values('Predictions', ascending = False).
                        iloc[:num_recommendations, :-1])

    return user_full, recommendations

already_rated, predictions = recommender('xiadow')

#print(already_rated.head(10))
print(predictions.head(10))