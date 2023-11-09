import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from pyspark.sql import SparkSession
from pyspark.sql.functions import mean
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline

spark = SparkSession.builder.appName("KNNSparkAssignment").getOrCreate()

train_csv_path = '/content/drive/My Drive/Colab Notebooks/train.csv'
train_data = spark.read.csv(train_csv_path, header=True)

mean_age = train_data.select(mean('Age')).collect()[0][0]

indexers = [
    StringIndexer(inputCol=column, outputCol=f"{column}_index", handleInvalid="keep")
    for column in ["Sex", "Pclass", "Embarked"]
]
pipeline = Pipeline(stages=indexers)
train_data = pipeline.fit(train_data).transform(train_data)

selected_columns = ["Age", "Fare", "Sex_index", "Pclass_index", "SibSp", "Parch", "Embarked_index", "Survived"]
train_data = train_data.select(selected_columns)
train_data = train_data.na.fill(mean_age, ['Age'])
train_data = train_data.withColumn("Fare", train_data["Fare"].cast("float"))
X = np.array(train_data.select(["Age", "Fare", "Pclass_index", "Sex_index", "SibSp", "Parch", "Embarked_index"]).collect())
y = np.array(train_data.select("Survived").rdd.flatMap(lambda x: x).collect())

imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

best_k = 0
best_accuracy = 0

for k in range(1, 21):
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X, y, cv=5)
    accuracy = scores.mean()

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_k = k

print('Best K value:', best_k)
print('Best K accuracy:', best_accuracy)
final_knn = KNeighborsClassifier(n_neighbors=best_k)
final_knn.fit(X, y)
test_csv_path = '/content/drive/My Drive/Colab Notebooks/test.csv'
test_data = spark.read.csv(test_csv_path, header=True)
test_data = fitted_pipeline.transform(test_data)
test_data = test_data.select(["Age", "Fare", "Sex_index", "Pclass_index", "SibSp", "Parch", "Embarked_index"])
test_data = test_data.na.fill(mean_age, ['Age'])
test_data = test_data.withColumn("Fare", test_data["Fare"].cast("float"))

X_test = np.array(test_data.collect())

X_test = imputer.transform(X_test)

y_pred_test = final_knn.predict(X_test)

print("PassengerId | Predicted Survived")
for index, pred in enumerate(y_pred_test):
    print(f"{index + 1} | {pred}")

spark.stop()
