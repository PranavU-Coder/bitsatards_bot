import pandas as pd
import pickle


def predict_cutoffs(year, difficulty, reference_df, output_file="predictions.csv"):
    with open("models/scaler.pkl", "rb") as f:
        preprocessor = pickle.load(f)
    with open("models/model.pkl", "rb") as f:
        model = pickle.load(f)

    # since I have dropped newer branches, I could remove this line of code and simply use itertools but this does the job so I'm letting it be.

    prediction_data = reference_df[["campus", "branch"]].drop_duplicates().copy()
    prediction_data["year"] = year
    prediction_data["difficulty"] = difficulty

    prediction_data_scaled = preprocessor.transform(prediction_data)
    prediction_data["marks"] = model.predict(prediction_data_scaled).round().astype(int)

    result = prediction_data[["campus", "branch", "marks", "year"]].sort_values(
        "marks", ascending=False
    )

    result.to_csv(output_file, index=False)
    return result


# I'm taking 0.2 -> best case, 0.5 -> most-likely and 0.8 -> worst case

# to manipulate
coefficient_of_difficulty = 0.8

df = pd.read_csv("data/model_data/cutoff_2025.csv")
predictions_2026 = predict_cutoffs(
    year=2026,
    difficulty=coefficient_of_difficulty,
    reference_df=df,
    output_file="predict/worst_case.csv",
)
print(predictions_2026)

predictions_2026.to_csv("predict/worst_case.csv", index=False)
