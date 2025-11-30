import pandas as pd
import pickle

def predict_cutoffs(year, reference_df, output_file='predictions.csv'):
    with open("models/scaler.pkl", 'rb') as f:
        preprocessor = pickle.load(f)
    with open("models/model.pkl", 'rb') as f:
        model = pickle.load(f)
    
    prediction_data = reference_df[['campus', 'branch']].drop_duplicates().copy()
    prediction_data['year'] = year
    
    prediction_data_scaled = preprocessor.transform(prediction_data)
    prediction_data['marks'] = model.predict(prediction_data_scaled).round().astype(int)
    
    result = prediction_data[['campus', 'branch', 'marks', 'year']].sort_values('marks', ascending=False)
    
    # Save to CSV
    result.to_csv(output_file, index=False)
    print(f"Predictions saved to {output_file}")
    
    return result

df = pd.read_csv('data/cutoff_2025.csv')
predictions_2026 = predict_cutoffs(year=2026, reference_df=df, output_file='data/predictions_2026.csv')
print(predictions_2026)

predictions_2026.to_csv('data/predictions_2026.csv', index=False)