# -*- coding: utf-8 -*-
"""Nháp of K224131549_NguyenHoMinhNguyet_Model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BMONSop_tAofsIKZ0YTMiOSlimJWKK2Y

Nháp

Thực hiện trên 1 file Google Colab + xuất ra file PDF cho Google Colab này. Trong phần đầu file Google Colab ghi rõ MSSV, Họ tên và viết code minh hoạ: Viết code minh hoạ: Học máy có giám sát có thể hiện Save best model và Load best model để dự đoán với Dataset tự chọn liên quan đến các ngành trong UEL, Dataset đọc từ Google Drive (Share anyone).
Sinh viên nộp 2 file (1 file Google Colab + 1 file PDF xuất ra từ file Google Colab) đã thực hiện theo yêu cầu trên tại đây: Quy ước đặt tên file: MSSV_HoTenKhongDau_Model.ipynb, MSSV_HoTenKhongDau_Model.pdf.
"""

import pandas as pd
import numpy as np
from sklearn import preprocessing
import urllib.parse

"""Prepocessing data"""

sheet_name = 'Preprocessing data Export 1000'
sheet_id = '1vKBpiRvp7rlvlfRh6ewL5C481PDgdI7s_3nToZO85cA'
sheet_name_encoded = urllib.parse.quote(sheet_name)
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name_encoded}"
df = pd.read_csv(url)
df

"""K-Fold Cross-Validation"""

print(df.columns.tolist())



from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, make_scorer
from sklearn.preprocessing import LabelEncoder

# Xác định các cột đặc trưng (X) và biến mục tiêu (y)
X = df[['Days for shipping (real)', 'Days for shipment (scheduled)', 'Benefit per order',
        'Sales per customer', 'Order Item Discount', 'Order Item Discount Rate',
        'Order Item Product Price', 'Order Item Profit Ratio', 'Order Item Quantity', 'Sales']]
y = df['Late_delivery_risk']

# Đảm bảo tất cả các cột trong X là kiểu số
X = X.apply(pd.to_numeric, errors='coerce')  # Chuyển các giá trị không phải số thành NaN
X = X.fillna(0)  # Thay thế NaN bằng 0 (có thể dùng chiến lược khác nếu muốn)

# Chuyển đổi biến mục tiêu thành số nếu là dạng phân loại
if y.dtype == 'object':
    le = LabelEncoder()
    y = le.fit_transform(y)

# Thiết lập K-Fold Cross-Validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)  # 5-Fold với xáo trộn để tăng tính ngẫu nhiên

# Khởi tạo mô hình (RandomForestClassifier là ví dụ, có thể thay thế mô hình khác)
model = RandomForestClassifier()

# Định nghĩa độ chính xác làm thước đo đánh giá
scorer = make_scorer(accuracy_score)

# Thực hiện Cross-Validation và lấy điểm chính xác
scores = cross_val_score(model, X, y, cv=kf, scoring=scorer)

# In độ chính xác của từng lượt gập và độ chính xác trung bình
print("Độ chính xác cho từng lượt gập:", scores)
print("Độ chính xác trung bình:", scores.mean())

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""Deep Learning & Machine Learning"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam

# Huấn luyện và đánh giá mô hình Machine Learning (Random Forest)
rf_model = RandomForestClassifier()
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
print("Độ chính xác Random Forest:", accuracy_score(y_test, y_pred_rf))
print("Báo cáo phân loại cho Random Forest:\n", classification_report(y_test, y_pred_rf))

# Xây dựng mô hình Deep Learning
# Chuyển đổi y thành dạng one-hot cho mạng neural nếu có nhiều lớp
y_train_dl = to_categorical(y_train)
y_test_dl = to_categorical(y_test)

dl_model = Sequential()
dl_model.add(Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
dl_model.add(Dense(32, activation='relu'))
dl_model.add(Dense(y_train_dl.shape[1], activation='softmax'))

# Biên dịch mô hình
dl_model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Huấn luyện mô hình Deep Learning
dl_model.fit(X_train, y_train_dl, epochs=50, batch_size=16, validation_split=0.2, verbose=1)

# Đánh giá mô hình Deep Learning trên tập kiểm tra
dl_loss, dl_accuracy = dl_model.evaluate(X_test, y_test_dl)
print("Độ chính xác mô hình Deep Learning:", dl_accuracy)

"""Choose best model"""

import joblib

# Chọn mô hình có độ chính xác cao hơn
if dl_accuracy > accuracy_score(y_test, y_pred_rf):
    best_model = dl_model  # Mô hình Deep Learning
else:
    best_model = rf_model  # Mô hình Random Forest

# In ra kết quả
print("Mô hình tốt nhất là:", "Deep Learning" if best_model == dl_model else "Random Forest")

# Lưu mô hình tốt nhất
joblib.dump(best_model, 'best_model.pkl')
print("Mô hình tốt nhất đã được lưu vào 'best_model.pkl'")

"""Save best model"""

loaded_model = joblib.load('best_model.pkl')

from google.colab import files

# Tải file best_model.pkl về máy
files.download('best_model.pkl')

"""Clustering với K-Means"""

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Áp dụng K-Means với 3 cụm
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)

# Thêm nhãn cụm vào DataFrame
df['Cluster'] = clusters

# Vẽ biểu đồ để trực quan hóa các cụm
plt.scatter(X['Sales'], X['Benefit per order'], c=clusters, cmap='viridis')
plt.xlabel('Sales')
plt.ylabel('Benefit per order')
plt.title('Clustering using K-Means')
plt.show()

"""Abnormal Analysis"""

from sklearn.ensemble import IsolationForest

# Áp dụng Isolation Forest để phát hiện điểm bất thường
iso_forest = IsolationForest(contamination=0.05, random_state=42)
outliers = iso_forest.fit_predict(X)

# Thêm nhãn bất thường vào DataFrame
df['Outlier'] = outliers
print("Điểm bất thường được phát hiện:", df[df['Outlier'] == -1].shape[0])

"""Unsupervised Machine Learning (PCA - Principal Component Analysis)"""

from sklearn.decomposition import PCA

# Giảm chiều dữ liệu xuống 2 thành phần chính
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# Vẽ biểu đồ của các thành phần chính
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap='viridis')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA of Data')
plt.show()

"""Frequent Itemset Mining và Association Rules Mining"""

from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

# Giả sử dữ liệu dạng one-hot encoding
# Only include categorical columns or those with binary values (0/1)
X_hot = pd.get_dummies(df[['Days for shipment (scheduled)', 'Order Item Discount Rate', 'Order Item Quantity']])


# Binarize the DataFrame - values greater than 0 will be converted to 1
for col in X_hot.columns:
    X_hot[col] = X_hot[col].apply(lambda x: 1 if x > 0 else 0)

# Khai thác tập mục thường xuyên với Apriori
frequent_itemsets = apriori(X_hot, min_support=0.1, use_colnames=True)
print("Tập mục thường xuyên:\n", frequent_itemsets)

# Tìm các luật kết hợp từ tập mục thường xuyên
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
print("Luật kết hợp:\n", rules)

"""Save the results of these analyses (if needed)"""

# Lưu nhãn cụm và nhãn bất thường vào file CSV
df[['Cluster', 'Outlier']].to_csv('cluster_and_outliers.csv', index=False)
print("Nhãn cụm và nhãn bất thường đã được lưu vào 'cluster_and_outliers.csv'")

# Lưu mô hình PCA
joblib.dump(pca, 'pca_model.pkl')
print("Mô hình PCA đã được lưu vào 'pca_model.pkl'")

# Lưu Frequent Itemsets và Association Rules vào file CSV
frequent_itemsets.to_csv('frequent_itemsets.csv', index=False)
rules.to_csv('association_rules.csv', index=False)
print("Frequent Itemsets và Association Rules đã được lưu vào các file 'frequent_itemsets.csv' và 'association_rules.csv'")

"""Load best *model*"""

!pip install streamlit

"""app.py file"""