import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from django.db.models import Count
import logging
from bread_management.models import Bread
from user_management.models import Profile

# 用户偏好中可能的前缀
PREFERENCE_PREFIXES = ["喜欢吃", "最爱", "常吃", "讨厌", "不喜欢", "推荐", "尝试"]


def clean_preference(pref):
    """ 去掉用户偏好中的前缀，提取关键字 """
    for prefix in PREFERENCE_PREFIXES:
        if pref.startswith(prefix):
            pref = pref[len(prefix):]
            break
    return pref.strip()


def build_bread_feature_matrix():
    """
    构造所有面包的特征矩阵。
    对每个面包，将名称和描述拼接起来，利用 TfidfVectorizer 转换为向量（15 维），
    然后在前面添加一列年龄占位符（填 0），使得总特征维度为 16。
    """
    bread_list = list(Bread.objects.all())
    # 拼接面包名称和描述
    bread_texts = [f"{bread.name} {bread.description}" for bread in bread_list]
    vectorizer = TfidfVectorizer(max_features=15)
    tfidf_matrix = vectorizer.fit_transform(bread_texts).toarray()  # shape: (n_bread, 15)
    # 为每个面包增加一列年龄占位符（面包没有年龄，统一填 0）
    age_placeholder = np.zeros((tfidf_matrix.shape[0], 1))
    bread_features = np.concatenate((age_placeholder, tfidf_matrix), axis=1)  # shape: (n_bread, 16)
    return bread_list, bread_features, vectorizer


def build_user_feature(user_preferences, user_age, vectorizer):
    """
    构造用户特征向量：
    - 将用户偏好（清洗后拼接的文本）转换为 TF-IDF 向量（15 维），
    - 将用户年龄归一化（除以 100），得到 1 维特征，
    - 最后拼接成 16 维向量。
    """
    cleaned_prefs = [clean_preference(p) for p in user_preferences]
    pref_text = " ".join(cleaned_prefs)
    user_tfidf = vectorizer.transform([pref_text]).toarray()  # shape: (1, 15)
    normalized_age = np.array([[user_age / 100.0]])  # shape: (1, 1)
    user_feature = np.concatenate((normalized_age, user_tfidf), axis=1)  # shape: (1, 16)
    return user_feature


def recommend_bread_knn(user_id, k=3):
    """
    利用 KNN 进行面包推荐：
    1. 构造面包特征矩阵（包括名称和描述的 TF-IDF 以及年龄占位符）
    2. 构造当前用户特征向量（基于用户偏好和归一化年龄）
    3. 利用 NearestNeighbors（余弦距离）找出与用户特征最接近的 k 个面包
    4. 如果没有推荐结果，则返回销量最高的面包
    """
    try:
        profile = Profile.objects.get(user_id=user_id)
        user_age = profile.age if profile.age is not None else 30
        user_preferences = profile.preferences.split(',') if profile.preferences else []

        # 构造面包特征矩阵
        bread_list, bread_features, vectorizer = build_bread_feature_matrix()
        if len(bread_list) == 0:
            return Bread.objects.annotate(sales_count=Count('order')).order_by('-sales_count')[:k]

        # 构造当前用户特征向量（16 维）
        user_feature = build_user_feature(user_preferences, user_age, vectorizer)

        # 使用 KNN 计算余弦距离
        nbrs = NearestNeighbors(n_neighbors=k, metric='cosine').fit(bread_features)
        distances, indices = nbrs.kneighbors(user_feature)

        # 确保索引为 Python int 类型，并过滤掉超出范围的索引
        indices = [int(i) for i in indices[0] if int(i) < len(bread_list)]
        recommended_breads = [bread_list[i] for i in indices]

        # 如果推荐为空，则按销量最高返回
        if not recommended_breads:
            recommended_breads = Bread.objects.annotate(sales_count=Count('order')).order_by('-sales_count')[:k]

        return recommended_breads

    except Exception as e:
        logging.error(f"🚨 推荐函数异常: {str(e)}")
        return Bread.objects.annotate(sales_count=Count('order')).order_by('-sales_count')[:k]

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Count
import logging
from bread_management.models import Bread
from user_management.models import Profile
def preprocess_data(user_ages, user_preferences, bread_categories, bread_descriptions):
    """ 数据预处理 """
    scaler = StandardScaler()
    ages_normalized = scaler.fit_transform(np.array(user_ages).reshape(-1, 1))

    encoder = OneHotEncoder(handle_unknown="ignore")
    encoder.fit(np.array(bread_categories).reshape(-1, 1))
    preferences_encoded = np.array([
        encoder.transform(np.array(pref).reshape(-1, 1)).toarray().sum(axis=0) if pref else np.zeros(len(bread_categories))
        for pref in user_preferences
    ])

    vectorizer = TfidfVectorizer(max_features=50)
    bread_descriptions_encoded = vectorizer.fit_transform(bread_descriptions).toarray()

    # **数据增强：复制少数类别的数据**
    max_length = max(len(ages_normalized), len(preferences_encoded), len(bread_descriptions_encoded))
    ages_normalized = np.resize(ages_normalized, (max_length, ages_normalized.shape[1]))
    preferences_encoded = np.resize(preferences_encoded, (max_length, preferences_encoded.shape[1]))
    bread_descriptions_encoded = np.resize(bread_descriptions_encoded, (max_length, bread_descriptions_encoded.shape[1]))

    return ages_normalized, preferences_encoded, bread_descriptions_encoded, encoder, vectorizer

def build_dnn_model(input_dim, output_dim):
    """ 构建神经网络模型 """
    model = Sequential([
        Dense(128, input_dim=input_dim, activation='relu'),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(output_dim, activation='softmax')
    ])
    model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])
    return model

def train_model(model, X, y):
    """ 训练神经网络模型 """
    y_unique = np.unique(y.argmax(axis=1))
    if len(y_unique) < y.shape[1]:
        missing_classes = set(range(y.shape[1])) - set(y_unique)
        print(f"⚠️ 训练数据缺少类别 {missing_classes}，补充数据")
        for cls in missing_classes:
            y = np.vstack([y, np.eye(y.shape[1])[cls]])
            X = np.vstack([X, np.zeros((1, X.shape[1]))])

    model.fit(X, y, epochs=50, batch_size=16, verbose=1)
    return model

def recommend_bread_dnn(user_id):
    try:
        profile = Profile.objects.get(user_id=user_id)
        age = profile.age if profile.age is not None else 30
        preferences = profile.preferences.split(',') if profile.preferences else []

        all_profiles = Profile.objects.all()
        user_ages = [p.age if p.age is not None else 30 for p in all_profiles]
        user_preferences = [p.preferences.split(',') if p.preferences else [] for p in all_profiles]
        bread_list = Bread.objects.all()

        bread_categories = list(set(cat.name for bread in bread_list for cat in bread.categories.all()))
        bread_descriptions = [bread.description if bread.description else "" for bread in bread_list]

        # **预处理数据**
        ages_normalized, preferences_encoded, bread_descriptions_encoded, encoder, vectorizer = preprocess_data(
            user_ages, user_preferences, bread_categories, bread_descriptions
        )

        input_dim = ages_normalized.shape[1] + preferences_encoded.shape[1] + bread_descriptions_encoded.shape[1]
        output_dim = len(bread_categories)

        # **修正 `y` 目标类别**
        y = np.array([
            encoder.transform(np.array(pref).reshape(-1, 1)).toarray().sum(axis=0) if pref else
            np.eye(len(bread_categories))[np.random.randint(0, len(bread_categories))]
            for pref in user_preferences
        ])

        model = build_dnn_model(input_dim, output_dim)
        X = np.concatenate((ages_normalized, preferences_encoded, bread_descriptions_encoded), axis=1)
        model = train_model(model, X, y)

        # **TF-IDF 计算 `用户偏好` 与 `面包描述` 的相似度**
        user_pref_vector = vectorizer.transform([" ".join(preferences)]).toarray()
        similarity_scores = cosine_similarity(user_pref_vector, bread_descriptions_encoded)

        # **取相似度最高的 3 个面包**
        top_indices = similarity_scores.argsort()[0][-3:][::-1]
        top_indices = [i for i in top_indices if i < len(bread_list)]
        recommended_breads = [bread_list[int(i)] for i in top_indices]  # ✅ 转换为 Python `int`

        if not recommended_breads:
            print("按照销量推荐")
            recommended_breads = Bread.objects.annotate(sales_count=Count('order')).order_by('-sales_count')[:3]

        # **计算准确率**
        correct_predictions = sum(1 for bread in recommended_breads if any(pref.lower() in bread.description.lower() for pref in preferences))
        accuracy = correct_predictions / len(recommended_breads) if recommended_breads else 0
        print(f"🎯 预测准确率: {accuracy * 100:.2f}%")

        return recommended_breads

    except Exception as e:
        logging.error(f"🚨 推荐函数异常: {str(e)}")
        return Bread.objects.annotate(sales_count=Count('order')).order_by('-sales_count')[:3]
