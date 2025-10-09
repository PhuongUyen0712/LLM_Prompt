import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

result = [
  {
    "dialogue_id": 1,
    "average_score": 3.0,
    "model_score": 60
  },
  {
    "dialogue_id": 2,
    "average_score": 3.25,
    "model_score": 60
  },
  {
    "dialogue_id": 3,
    "average_score": 3.0,
    "model_score": 60
  },
  {
    "dialogue_id": 7,
    "average_score": 3.25,
    "model_score": 70
  },
  {
    "dialogue_id": 9,
    "average_score": 3.33,
    "model_score": 60
  },
  {
    "dialogue_id": 10,
    "average_score": 3.67,
    "model_score": 80
  },
  {
    "dialogue_id": 13,
    "average_score": 3.5,
    "model_score": 70
  },
  {
    "dialogue_id": 14,
    "average_score": 3.75,
    "model_score": 70
  },
  {
    "dialogue_id": 15,
    "average_score": 3.33,
    "model_score": 70
  },
  {
    "dialogue_id": 16,
    "average_score": 2.75,
    "model_score": 60
  },
  {
    "dialogue_id": 18,
    "average_score": 2.25,
    "model_score": 60
  },
  {
    "dialogue_id": 20,
    "average_score": 3.67,
    "model_score": 60
  },
  {
    "dialogue_id": 24,
    "average_score": 3.6,
    "model_score": 60
  },
  {
    "dialogue_id": 29,
    "average_score": 3.5,
    "model_score": 60
  },
  {
    "dialogue_id": 32,
    "average_score": 2.8,
    "model_score": 60
  },
  {
    "dialogue_id": 35,
    "average_score": 2.67,
    "model_score": 40
  },
  {
    "dialogue_id": 37,
    "average_score": 2.4,
    "model_score": 60
  },
  {
    "dialogue_id": 40,
    "average_score": 2.8,
    "model_score": 60
  },
  {
    "dialogue_id": 41,
    "average_score": 2.75,
    "model_score": 60
  },
  {
    "dialogue_id": 46,
    "average_score": 2.67,
    "model_score": 40
  },
  {
    "dialogue_id": 53,
    "average_score": 2.2,
    "model_score": 70
  },
  {
    "dialogue_id": 70,
    "average_score": 2.25,
    "model_score": 60
  },
  {
    "dialogue_id": 78,
    "average_score": 3.2,
    "model_score": 70
  },
  {
    "dialogue_id": 93,
    "average_score": 3.2,
    "model_score": 70
  },
  {
    "dialogue_id": 115,
    "average_score": 3.75,
    "model_score": 70
  },
  {
    "dialogue_id": 136,
    "average_score": 4.0,
    "model_score": 70
  },
  {
    "dialogue_id": 138,
    "average_score": 3.4,
    "model_score": 70
  },
  {
    "dialogue_id": 150,
    "average_score": 2.5,
    "model_score": 60
  },
  {
    "dialogue_id": 152,
    "average_score": 2.5,
    "model_score": 60
  },
  {
    "dialogue_id": 163,
    "average_score": 2.6,
    "model_score": 60
  },
  {
    "dialogue_id": 169,
    "average_score": 3.4,
    "model_score": 80
  },
  {
    "dialogue_id": 191,
    "average_score": 2.33,
    "model_score": 40
  },
  {
    "dialogue_id": 202,
    "average_score": 2.0,
    "model_score": 40
  },
  {
    "dialogue_id": 213,
    "average_score": 2.4,
    "model_score": 40
  },
  {
    "dialogue_id": 254,
    "average_score": 2.33,
    "model_score": 40
  },
  {
    "dialogue_id": 273,
    "average_score": 2.6,
    "model_score": 40
  },
  {
    "dialogue_id": 326,
    "average_score": 3.6,
    "model_score": 40
  },
  {
    "dialogue_id": 407,
    "average_score": 2.2,
    "model_score": 40
  }
]

# Create result_df from result
result_df = pd.DataFrame(result)

# Assuming 'average_scores' is a typo for 'average_score' in the original snippet, and no separate 'df' is needed (data is already combined)
# Select columns and rename 'average_score' to 'average_scores' for consistency with the function
result_df = result_df[['dialogue_id', 'average_score', 'model_score']]
result_df.rename(columns={'average_score': 'average_scores'}, inplace=True)

# Scale model_score to 5-point scale
result_df['model_score_5'] = result_df['model_score'] / 20

# Drop original model_score
result_df.drop(columns=['model_score'], inplace=True)

# Drop NaN rows if any
result_df = result_df.dropna()

def calculate_all_metrics(y_true, y_pred):
    """
    Calculates MAE, MSE, RMSE, and R-squared and returns them in a dictionary.
    
    Args:
        y_true (list or np.array): True Average Scores (in dataset).
        y_pred (list or np.array): Predicted Average Scores (model generated).
    """
    mae = round(mean_absolute_error(y_true, y_pred), 4)
    mse = round(mean_squared_error(y_true, y_pred), 4)
    rmse = float(round(np.sqrt(mse), 4))
    r2 = round(r2_score(y_true, y_pred), 4)
    
    metrics = {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2
    }
    
    return metrics

metrics_list = []

metrics = calculate_all_metrics(result_df['average_scores'], result_df['model_score_5'])
metrics_list.append(metrics)

all_results = {
    'mean': {
    'MAE': float(np.mean([m['MAE'] for m in metrics_list])),
    'MSE': float(np.mean([m['MSE'] for m in metrics_list])),
    'RMSE': float(np.mean([m['RMSE'] for m in metrics_list])),
    'R2': float(np.mean([m['R2'] for m in metrics_list])),
    },
    'sd' :{
    'MAE': float(np.std([m['MAE'] for m in metrics_list])),
    'MSE': float(np.std([m['MSE'] for m in metrics_list])),
    'RMSE': float(np.std([m['RMSE'] for m in metrics_list])),
    'R2': float(np.std([m['R2'] for m in metrics_list])),
    }
}

print(all_results)