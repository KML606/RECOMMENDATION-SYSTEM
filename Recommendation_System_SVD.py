from surprise import SVD, Dataset, Reader
from surprise.model_selection import cross_validate, train_test_split
import pandas as pd

# Step 1: Load dataset 
data = Dataset.load_builtin('ml-100k')
trainset, testset = train_test_split(data, test_size=0.2)

# Step 2: Define model
model = SVD()

# Step 3: Train the model
model.fit(trainset)

# Step 4: Make predictions
predictions = model.test(testset)

# Step 5: Evaluate performance
from surprise import accuracy
rmse = accuracy.rmse(predictions)
mae = accuracy.mae(predictions)

# Step 6: Show top-N recommendations for a given user
from collections import defaultdict

def get_top_n(predictions, n=5):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    return top_n

top_n = get_top_n(predictions, n=5)

# Example: Print top 5 recommendations for first 3 users
for uid, user_ratings in list(top_n.items())[:3]:
    print(f"\nTop recommendations for User {uid}:")
    for iid, rating in user_ratings:
        print(f"  Item {iid} with predicted rating {rating:.2f}")
