import os
# 設定 Keras 3 後端引擎為 JAX
os.environ["KERAS_BACKEND"] = "jax"

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import keras

# 設定隨機種子以確保結果可重現
np.random.seed(42)
keras.utils.set_random_seed(42)

class ScratchLinearRegression:
    """
    從零開始使用梯度下降法（Gradient Descent）實現的多元線性回歸模型。
    """
    def __init__(self, learning_rate=0.05, epochs=1000):
        self.lr = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None
        self.loss_history = []

    def fit(self, X, y):
        """
        訓練模型。
        X: 形狀為 (n_samples, n_features) 的 NumPy 陣列
        y: 形狀為 (n_samples,) 的 NumPy 陣列
        """
        n_samples, n_features = X.shape
        # 初始化權重為 0，偏差為 0
        self.weights = np.zeros(n_features)
        self.bias = 0.0
        self.loss_history = []

        for epoch in range(self.epochs):
            # 預測值: y_pred = X * w + b
            y_predicted = np.dot(X, self.weights) + self.bias
            
            # 計算均方誤差 (MSE)
            loss = np.mean((y_predicted - y) ** 2)
            self.loss_history.append(loss)

            # 計算梯度
            # dw = (2/n) * X^T * (y_pred - y)
            dw = (2 / n_samples) * np.dot(X.T, (y_predicted - y))
            # db = (2/n) * sum(y_pred - y)
            db = (2 / n_samples) * np.sum(y_predicted - y)

            # 更新權重與偏差
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

            # 每 100 個 epoch 印出一次損失值
            if (epoch + 1) % 100 == 0 or epoch == 0:
                print(f"Epoch {epoch + 1:04d}/{self.epochs} - Loss (MSE): {loss:.6f}")

    def predict(self, X):
        """
        預測新數據。
        X: 形狀為 (n_samples, n_features) 的 NumPy 陣列
        """
        return np.dot(X, self.weights) + self.bias


def main():
    print("=" * 60)
    print(" 線性回歸（Linear Regression）範例展示專案（含 Keras 3） ")
    print("=" * 60)

    # 1. 生成模擬數據
    # 預設公式：y = 2.5 * x + 4.0 + 隨機雜訊
    print("\n[步驟 1] 生成隨機線性模擬數據集...")
    n_samples = 150
    X = np.random.rand(n_samples, 1) * 10  # 生成 0 到 10 之間的均勻分佈實數
    true_w = 2.5
    true_b = 4.0
    noise = np.random.randn(n_samples, 1) * 2.0  # 平均數為 0，標準差為 2.0 的常態分佈雜訊
    y = (true_w * X + true_b + noise).squeeze()  # 將 y 轉為 1D 陣列
    
    # 為了模型訓練，保持 X 為 2D 陣列 (n_samples, 1)
    print(f"生成的數據量：{n_samples} 筆")
    print(f"真實關係式：y = {true_w} * x + {true_b} + 雜訊")

    # 2. 訓練手動實現的模型 (Scratch)
    print("\n[步驟 2] 開始訓練手動梯度下降線性回歸模型 (Scratch)...")
    scratch_model = ScratchLinearRegression(learning_rate=0.01, epochs=1000)
    scratch_model.fit(X, y)
    
    # 3. 訓練 Scikit-Learn 的官方模型
    print("\n[步驟 3] 開始訓練 Scikit-Learn 內建線性回歸模型...")
    sklearn_model = LinearRegression()
    sklearn_model.fit(X, y)

    # 4. 訓練 Keras 3 模型
    print("\n[步驟 4] 開始訓練 Keras 3 模型 (JAX 後端)...")
    # 建立單層單神經元的全連接層模型 (即 y = wx + b)
    keras_model = keras.Sequential([
        keras.layers.Input(shape=(1,)),
        keras.layers.Dense(1)
    ])
    # 使用與手動實現相同的 SGD 優化器與學習率，損失函數為 MSE
    keras_model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.01), loss="mse")
    
    # 為了讓 Keras 穩定收斂，我們進行 500 個 Epoch 的訓練
    # y 需轉換成 2D 陣列 (n_samples, 1) 以符合多數深度學習庫的維度要求
    keras_history = keras_model.fit(X, y.reshape(-1, 1), epochs=500, batch_size=16, verbose=0)
    print("Keras 3 模型訓練完成。")

    # 5. 模型預測與評估
    y_pred_scratch = scratch_model.predict(X)
    y_pred_sklearn = sklearn_model.predict(X)
    y_pred_keras = keras_model.predict(X, verbose=0).squeeze()

    # 評估指標
    mse_scratch = mean_squared_error(y, y_pred_scratch)
    r2_scratch = r2_score(y, y_pred_scratch)
    
    mse_sklearn = mean_squared_error(y, y_pred_sklearn)
    r2_sklearn = r2_score(y, y_pred_sklearn)

    mse_keras = mean_squared_error(y, y_pred_keras)
    r2_keras = r2_score(y, y_pred_keras)

    # 取得 Keras 模型的權重與偏差
    keras_weights, keras_biases = keras_model.layers[0].get_weights()
    w_keras = keras_weights[0][0]
    b_keras = keras_biases[0]

    print("\n" + "=" * 60)
    print(" 三者模型訓練結果與評估比較 ")
    print("=" * 60)
    print(f"真實關係: w = {true_w:.4f}, b = {true_b:.4f}")
    print("-" * 60)
    print(f"【手動實現 (Scratch GD)】")
    print(f"  - 預估權重 (w): {scratch_model.weights[0]:.4f}")
    print(f"  - 預估偏差 (b): {scratch_model.bias:.4f}")
    print(f"  - 均方誤差 (MSE): {mse_scratch:.4f}")
    print(f"  - R² 決定係數: {r2_scratch:.4f}")
    print("-" * 60)
    print(f"【Scikit-Learn 實現】")
    print(f"  - 預估權重 (w): {sklearn_model.coef_[0]:.4f}")
    print(f"  - 預估偏差 (b): {sklearn_model.intercept_:.4f}")
    print(f"  - 均方誤差 (MSE): {mse_sklearn:.4f}")
    print(f"  - R² 決定係數: {r2_sklearn:.4f}")
    print("-" * 60)
    print(f"【Keras 3 (JAX 後端) 實現】")
    print(f"  - 預估權重 (w): {w_keras:.4f}")
    print(f"  - 預估偏差 (b): {b_keras:.4f}")
    print(f"  - 均方誤差 (MSE): {mse_keras:.4f}")
    print(f"  - R² 決定係數: {r2_keras:.4f}")
    print("=" * 60)

    # 6. 視覺化圖表繪製與儲存
    print("\n[步驟 5] 繪製並儲存高品質視覺化圖表...")
    
    # 設定畫布大小與極簡暗色質感風格
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=150)
    
    # 圖一：擬合結果對比
    ax1.scatter(X, y, color='#00e5ff', alpha=0.5, edgecolors='none', label='Data points', s=35)
    
    # 產生一組均勻分佈的 X 值來繪製平滑的擬合線
    X_line = np.linspace(0, 10, 100).reshape(-1, 1)
    y_line_scratch = scratch_model.predict(X_line)
    y_line_sklearn = sklearn_model.predict(X_line)
    y_line_keras = keras_model.predict(X_line, verbose=0).squeeze()
    
    ax1.plot(X_line, y_line_scratch, color='#ff007f', linewidth=3, label=f'Scratch GD (w={scratch_model.weights[0]:.2f}, b={scratch_model.bias:.2f})')
    ax1.plot(X_line, y_line_sklearn, color='#00ff66', linewidth=2, linestyle='--', label=f'scikit-learn (w={sklearn_model.coef_[0]:.2f}, b={sklearn_model.intercept_:.2f})')
    ax1.plot(X_line, y_line_keras, color='#ffc83d', linewidth=2, linestyle='-.', label=f'Keras 3 (w={w_keras:.2f}, b={b_keras:.2f})')
    
    ax1.set_title("Linear Regression Fits Comparison", fontsize=14, fontweight='bold', pad=15)
    ax1.set_xlabel("X (Independent Variable)", fontsize=11, labelpad=10)
    ax1.set_ylabel("y (Dependent Variable)", fontsize=11, labelpad=10)
    ax1.grid(True, color='#333333', linestyle=':', linewidth=0.8)
    ax1.legend(frameon=True, facecolor='#222222', edgecolor='none', fontsize=10)
    
    # 圖二：手動與 Keras 損失收斂曲線對比
    ax2.plot(scratch_model.loss_history, color='#ff007f', linewidth=2, label='Scratch GD Loss')
    ax2.plot(keras_history.history['loss'], color='#ffc83d', linewidth=2, linestyle='--', label='Keras 3 SGD Loss')
    ax2.set_title("Gradient Descent Loss Convergence Comparison", fontsize=14, fontweight='bold', pad=15)
    ax2.set_xlabel("Epochs", fontsize=11, labelpad=10)
    ax2.set_ylabel("Loss (MSE)", fontsize=11, labelpad=10)
    ax2.grid(True, color='#333333', linestyle=':', linewidth=0.8)
    ax2.legend(frameon=True, facecolor='#222222', edgecolor='none', fontsize=10)
    
    # 加強美化與邊框調整
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#555555')
        ax.spines['bottom'].set_color('#555555')

    plt.tight_layout()
    plot_filename = "regression_plot.png"
    plt.savefig(plot_filename, bbox_inches='tight')
    plt.close()
    
    print(f"圖表已成功生成並儲存至：{os.path.abspath(plot_filename)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
