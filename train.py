import sys
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))


from invoice_flagging.data_preprocessing import (
    load_invoice_data,
    apply_labels,
    split_data,
    scale_features
)

from invoice_flagging.modeling_evaluation import (
    train_random_forest,
    evaluate_classifier
)

FEATURES = [
    "invoice_quantity",
    "invoice_dollars",
    "Freight",
    "total_item_quantity",
    "total_item_dollars"
]

TARGET = "flag_invoice"


def main():

    db_path = BASE_DIR / "Data" / "inventory.db"

    # Load data
    df = load_invoice_data(db_path)

    # Apply rule based labels
    df = apply_labels(df)

    # Prepare data
    X_train, X_test, y_train, y_test = split_data(df, FEATURES, TARGET)
    X_train_scaled, X_test_scaled = scale_features(
        X_train, X_test, 'models/scaler.pkl'
    )

    # Train and evaluate models
    grid_search = train_random_forest(X_train_scaled, y_train)

    evaluate_classifier(
        grid_search.best_estimator_,
        X_test_scaled,
        y_test,
        "Random Forest Classifier"
    )

    # Save best model
    model_dir = Path(__file__).resolve().parent / "models"
    model_dir.mkdir(exist_ok=True)
    
    model_path = model_dir / "predict_flag_invoice.pkl"
    joblib.dump(grid_search.best_estimator_, model_path)
    
    print(f"Model saved to: {model_path}")
    
if __name__ == "__main__":
    main()
    