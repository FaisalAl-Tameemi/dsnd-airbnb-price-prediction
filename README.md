# AirBnB Price Prediction using Spark & Keras


## High-level Plan

1. Crawl the AirBnB data page and find a list of each city's data exports
2. Download each city's listing's CSV
3. Load all listings CSV files and combine them into a single file (with Spark)
4. Drop irrelevant/redundant columns
5. Save data to CSV file (or SQL database)
    - Also save a shuffled sample of the data (smaller dataset for exploration)
6. Load the previously saved CSV file (with Spark)
7. Process/Transform the data
    - numerical columns: normalizing, scaling, ...
    - categorial columns: string indexing, dummy variables
    - text data: normalize, tokenize, drop stop words, ...
    - add features: 'avg_neighbourhood_price', 'avg_city_price', ...
        - some of these features can add localization when using the entire airbnb dataset to train the models
8. Save processed data as files (CSV or otherwise)
9. Load the previously saved files
10. Train/test split
11. Run training pipeline
    - GridSearchCV with Spark
    - LSTM w. external embeddings (ex: glove)
12. Save model to disk
13. Load model
14. Run transform/predict on final test set and new data
    - Use r2 score and RMSE as metrics