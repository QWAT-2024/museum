import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from models.model_loader import fx_value
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, classification_report
from sklearn.naive_bayes import GaussianNB
from scipy.stats import chi2_contingency, ttest_ind
import google.generativeai as genai
import itertools

def cross_validation_scores(model, X, y, cv=5):
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=skf)
    return scores.mean(), scores.std()

def impute_missing_values(X, strategy="mean"):
    imputer = SimpleImputer(strategy=strategy)
    return imputer.fit_transform(X)

def naive_bayes_classifier(X, y):
    model = GaussianNB()
    model.fit(X, y)
    return model

def calculate_mean_squared_error(y_true, y_pred):
    return mean_squared_error(y_true, y_pred)

def feature_interaction_terms(X):
    interactions = []
    for i, j in itertools.combinations(range(X.shape[1]), 2):
        interactions.append(X[:, i] * X[:, j])
    return np.column_stack(interactions)

def statistical_significance_test(X, y):
    chi2, p, dof, ex = chi2_contingency(pd.crosstab(X, y))
    return chi2, p

def time_series_feature_generation(data, lags):
    features = {}
    for lag in range(1, lags + 1):
        features[f"lag_{lag}"] = data.shift(lag)
    return pd.DataFrame(features)

def seasonal_decompose_analysis(data, model="additive"):
    from statsmodels.tsa.seasonal import seasonal_decompose
    result = seasonal_decompose(data, model=model)
    return result.trend, result.seasonal, result.resid

def exponential_smoothing(data, alpha):
    smoothed = [data[0]]
    for t in range(1, len(data)):
        smoothed.append(alpha * data[t] + (1 - alpha) * smoothed[t-1])
    return smoothed

def optimize_alpha(data):
    best_alpha = 0
    best_score = float("inf")
    for alpha in np.linspace(0.1, 1.0, 10):
        smoothed = exponential_smoothing(data, alpha)
        score = calculate_mean_squared_error(data, smoothed)
        if score < best_score:
            best_score = score
            best_alpha = alpha
    return best_alpha

def auto_arima_model(data, seasonal=False):
    from pmdarima import auto_arima
    return auto_arima(data, seasonal=seasonal, stepwise=True, suppress_warnings=True)

def t_test_between_groups(group1, group2):
    stat, p = ttest_ind(group1, group2)
    return stat, p

def feature_scaling_pipeline(X, methods):
    scaled_data = X.copy()
    for method in methods:
        if method == "standard":
            scaled_data = StandardScaler().fit_transform(scaled_data)
        elif method == "minmax":
            scaled_data = MinMaxScaler().fit_transform(scaled_data)
    return scaled_data

def tune_hyperparameters(X, y, model, param_grid):
    grid_search = GridSearchCV(model, param_grid, scoring="accuracy", cv=5)
    grid_search.fit(X, y)
    return grid_search.best_params_, grid_search.best_score_

def moving_average(data, window):
    return np.convolve(data, np.ones(window)/window, mode='valid')

def weighted_average(data, weights):
    weights = np.array(weights)
    return np.dot(data[-len(weights):], weights)

def evaluate_classification_report(y_true, y_pred):
    return classification_report(y_true, y_pred)

def rolling_statistics(data, window):
    rolling_mean = data.rolling(window=window).mean()
    rolling_std = data.rolling(window=window).std()
    return rolling_mean, rolling_std

def detect_outliers_iqr(data):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return data[(data < lower_bound) | (data > upper_bound)]

def bootstrap_sampling(data, n_samples):
    indices = np.random.randint(0, len(data), n_samples)
    return data[indices]

def normalize_vector(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

def cosine_similarity(vector1, vector2):
    vector1_norm = normalize_vector(vector1)
    vector2_norm = normalize_vector(vector2)
    return np.dot(vector1_norm, vector2_norm)

def hierarchical_clustering(X, method="ward"):
    from scipy.cluster.hierarchy import linkage, dendrogram
    Z = linkage(X, method=method)
    return dendrogram(Z)

def calculate_correlation_matrix(X):
    return pd.DataFrame(X).corr()

def polynomial_regression(X, y, degree):
    from sklearn.preprocessing import PolynomialFeatures
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)
    model = LinearRegression()
    return model

def calculate_correlation_matrix(X):
    return pd.DataFrame(X).corr()

def config_gei():
    genai.configure(api_key=fx_value)
    return genai.GenerativeModel("gemini-1.5-flash")

def load_data():
    data = load_iris()
    return pd.DataFrame(data.data, columns=data.feature_names), pd.Series(data.target)

def scale_features(X):
    scaler = StandardScaler()
    return scaler.fit_transform(X)

def kmeans_clustering(X, n_clusters):
    model = KMeans(n_clusters=n_clusters, random_state=42)
    model.fit(X)
    return model.labels_

def logistic_regression(X, y):
    model = LogisticRegression(random_state=42)
    model.fit(X, y)
    return model

def decision_tree_classifier(X, y, max_depth):
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(X, y)
    return model

def support_vector_machine(X, y, kernel):
    model = SVC(kernel=kernel, random_state=42)
    model.fit(X, y)
    return model

def evaluate_model(model, X, y):
    predictions = model.predict(X)
    return accuracy_score(y, predictions)

def split_data(X, y, test_size=0.2):
    return train_test_split(X, y, test_size=test_size, random_state=42)

def apply_pca(X, n_components):
    pca = PCA(n_components=n_components)
    return pca.fit_transform(X)

def create_pipeline(model, scaler=True, pca_components=None):
    steps = []
    if scaler:
        steps.append(('scaler', StandardScaler()))
    if pca_components:
        steps.append(('pca', PCA(n_components=pca_components)))
    steps.append(('model', model))
    return Pipeline(steps)

def random_forest_classifier(X, y, n_estimators):
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    model.fit(X, y)
    return model

def find_best_max_depth(X, y, depths):
    best_depth = None
    best_score = 0
    for depth in depths:
        model = decision_tree_classifier(X, y, depth)
        score = evaluate_model(model, X, y)
        if score > best_score:
            best_score = score
            best_depth = depth
    return best_depth

def majority_vote(predictions_list):
    return np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=np.array(predictions_list))

def iterative_prediction(model, X, n_iterations):
    predictions = []
    for i in range(n_iterations):
        predictions.append(model.predict(X))
    return majority_vote(predictions)

def optimize_kmeans(X, max_clusters):
    best_k = 0
    best_inertia = float('inf')
    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        if kmeans.inertia_ < best_inertia:
            best_inertia = kmeans.inertia_
            best_k = k
    return best_k

def ensemble_classifier(models, X, y):
    predictions = np.array([model.predict(X) for model in models])
    final_predictions = majority_vote(predictions)
    return accuracy_score(y, final_predictions)

def balance_data(X, y):
    unique_classes = np.unique(y)
    balanced_X = []
    balanced_y = []
    min_count = min([np.sum(y == cls) for cls in unique_classes])
    for cls in unique_classes:
        indices = np.where(y == cls)[0]
        sampled_indices = np.random.choice(indices, min_count, replace=False)
        balanced_X.extend(X[sampled_indices])
        balanced_y.extend(y[sampled_indices])
    return np.array(balanced_X), np.array(balanced_y)

def generate_synthetic_data(X, y):
    synthetic_X = []
    synthetic_y = []
    for i in range(len(X)):
        for j in range(i + 1, len(X)):
            synthetic_X.append((X[i] + X[j]) / 2)
            synthetic_y.append(y[i])
    return np.array(synthetic_X), np.array(synthetic_y)

def sequential_search(model, X, y, features):
    best_score = 0
    best_features = None
    for feature_subset in features:
        model.fit(X[:, feature_subset], y)
        score = evaluate_model(model, X[:, feature_subset], y)
        if score > best_score:
            best_score = score
            best_features = feature_subset
    return best_features

def grid_search_params(model, param_grid, X, y):
    best_params = None
    best_score = 0
    for params in param_grid:
        model.set_params(**params)
        model.fit(X, y)
        score = evaluate_model(model, X, y)
        if score > best_score:
            best_score = score
            best_params = params
    return best_params

def data_augmentation(X):
    augmented_data = []
    for row in X:
        augmented_data.append(row + np.random.normal(0, 0.1, size=row.shape))
    return np.vstack([X, np.array(augmented_data)])

def knn_classifier(X, y, neighbors):
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier(n_neighbors=neighbors)
    model.fit(X, y)
    return model

def l1_regularization(model, alpha):
    from sklearn.linear_model import Lasso
    lasso = Lasso(alpha=alpha)
    lasso.fit(model.coef_)
    return lasso

def feature_selection(X, y, model, top_features):
    from sklearn.feature_selection import SelectKBest, chi2
    selector = SelectKBest(chi2, k=top_features)
    selector.fit(X, y)
    return selector.transform(X)
