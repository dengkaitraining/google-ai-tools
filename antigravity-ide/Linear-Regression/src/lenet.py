import os
# 設定 Keras 3 後端引擎為 JAX
os.environ["KERAS_BACKEND"] = "jax"

import numpy as np
import matplotlib.pyplot as plt
import keras

# 設定隨機種子以確保結果可重現
keras.utils.set_random_seed(42)
np.random.seed(42)

def main():
    print("=" * 60)
    print("   使用 Keras 3 (JAX 後端) 實作 LeNet-5 卷積神經網路   ")
    print("=" * 60)

    # 1. 載入 MNIST 資料集
    print("\n[步驟 1] 載入 MNIST 手寫數字資料集...")
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    print(f"訓練集形狀: {x_train.shape}, 訓練標籤形狀: {y_train.shape}")
    print(f"測試集形狀: {x_test.shape}, 測試標籤形狀: {y_test.shape}")

    # 2. 資料前處理
    print("\n[步驟 2] 資料前處理與歸一化...")
    # 將像素值歸一化至 [0, 1] 之間，並轉換為 float32
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    # 擴展維度為 (height, width, channels)
    x_train = np.expand_dims(x_train, axis=-1)
    x_test = np.expand_dims(x_test, axis=-1)

    # 將標籤轉換為 One-Hot 編碼
    num_classes = 10
    y_train_cat = keras.utils.to_categorical(y_train, num_classes)
    y_test_cat = keras.utils.to_categorical(y_test, num_classes)

    # 3. 建立經典 LeNet-5 模型架構
    print("\n[步驟 3] 建立經典 LeNet-5 模型架構...")
    # 經典 LeNet-5 模型輸入為 32x32x1。
    # 由於 MNIST 為 28x28x1，我們使用 ZeroPadding2D 將其擴展至 32x32。
    model = keras.Sequential([
        keras.Input(shape=(28, 28, 1), name="Input"),
        
        # 補零層 (Zero Padding)：(28, 28, 1) -> (32, 32, 1)
        keras.layers.ZeroPadding2D(padding=((2, 2), (2, 2)), name="Padding"),
        
        # C1 卷積層：6 個 5x5 的卷積核，步長 (stride) 為 1，使用 tanh 激活函數
        # (32, 32, 1) -> (28, 28, 6)
        keras.layers.Conv2D(filters=6, kernel_size=(5, 5), strides=1, activation="tanh", name="C1"),
        
        # S2 平均池化層：池化大小 2x2，步長為 2
        # (28, 28, 6) -> (14, 14, 6)
        keras.layers.AveragePooling2D(pool_size=(2, 2), strides=2, name="S2"),
        
        # C3 卷積層：16 個 5x5 的卷積核，步長為 1，使用 tanh 激活函數
        # (14, 14, 6) -> (10, 10, 16)
        keras.layers.Conv2D(filters=16, kernel_size=(5, 5), strides=1, activation="tanh", name="C3"),
        
        # S4 平均池化層：池化大小 2x2，步長為 2
        # (10, 10, 16) -> (5, 5, 16)
        keras.layers.AveragePooling2D(pool_size=(2, 2), strides=2, name="S4"),
        
        # C5 卷積層：120 個 5x5 的卷積核，步長為 1，使用 tanh 激活函數
        # 因為輸入是 5x5，使用 5x5 卷積後輸出會是 1x1x120
        # (5, 5, 16) -> (1, 1, 120)
        keras.layers.Conv2D(filters=120, kernel_size=(5, 5), strides=1, activation="tanh", name="C5"),
        
        # 攤平層：將 3D 的 (1, 1, 120) 轉為 1D 向量 (120,)
        keras.layers.Flatten(name="Flatten"),
        
        # F6 全連接層：84 個神經元，使用 tanh 激活函數
        keras.layers.Dense(units=84, activation="tanh", name="F6"),
        
        # 輸出層：10 個神經元，對應 0~9 個類別，使用 softmax 激活函數
        keras.layers.Dense(units=num_classes, activation="softmax", name="Output")
    ], name="LeNet-5")

    # 印出模型結構摘要
    model.summary()

    # 4. 編譯與訓練模型
    print("\n[步驟 4] 編譯與訓練模型 (使用 Adam 優化器)...")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    epochs = 10
    batch_size = 128
    print(f"開始訓練，預計執行 {epochs} 個 Epoch，Batch Size 為 {batch_size}...")
    history = model.fit(
        x_train, y_train_cat,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.1,
        verbose=1
    )

    # 5. 評估模型效能
    print("\n[步驟 5] 評估測試集效能...")
    test_loss, test_acc = model.evaluate(x_test, y_test_cat, verbose=0)
    print(f"測試集損失值 (Test Loss): {test_loss:.4f}")
    print(f"測試集準確度 (Test Accuracy): {test_acc:.4f}")

    # 6. 視覺化訓練收斂曲線
    print("\n[步驟 6] 繪製訓練收斂曲線並儲存...")
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), dpi=150)
    
    # 準確度曲線 (Accuracy)
    ax1.plot(history.history["accuracy"], color="#00e5ff", linewidth=2.5, label="Train Acc")
    ax1.plot(history.history["val_accuracy"], color="#ffc83d", linewidth=2, linestyle="--", label="Val Acc")
    ax1.set_title("LeNet-5 Accuracy Convergence", fontsize=12, fontweight="bold", pad=12)
    ax1.set_xlabel("Epoch", fontsize=10)
    ax1.set_ylabel("Accuracy", fontsize=10)
    ax1.grid(True, color="#333333", linestyle=":", linewidth=0.8)
    ax1.legend(frameon=True, facecolor="#222222", edgecolor="none")
    
    # 損失值曲線 (Loss)
    ax2.plot(history.history["loss"], color="#ff007f", linewidth=2.5, label="Train Loss")
    ax2.plot(history.history["val_loss"], color="#00ff66", linewidth=2, linestyle="--", label="Val Loss")
    ax2.set_title("LeNet-5 Loss Convergence", fontsize=12, fontweight="bold", pad=12)
    ax2.set_xlabel("Epoch", fontsize=10)
    ax2.set_ylabel("Loss", fontsize=10)
    ax2.grid(True, color="#333333", linestyle=":", linewidth=0.8)
    ax2.legend(frameon=True, facecolor="#222222", edgecolor="none")
    
    # 美化邊框
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#555555')
        ax.spines['bottom'].set_color('#555555')
        
    plt.tight_layout()
    plot_filename = "lenet_training_plot.png"
    plt.savefig(plot_filename, bbox_inches="tight")
    plt.close()
    print(f"訓練曲線圖已儲存至：{os.path.abspath(plot_filename)}")

    # 7. 隨機預測展示
    print("\n[步驟 7] 執行隨機預測展示...")
    # 隨機挑選 5 張測試集影像進行預測
    indices = np.random.choice(len(x_test), 5, replace=False)
    predictions = model.predict(x_test[indices], verbose=0)
    predicted_labels = np.argmax(predictions, axis=1)
    true_labels = np.argmax(y_test_cat[indices], axis=1)
    
    print("-" * 60)
    for i, idx in enumerate(indices):
        is_correct = "✓ 正確" if predicted_labels[i] == true_labels[i] else "✗ 錯誤"
        print(f"測試樣本索引: {idx:04d} | 真實標籤: {true_labels[i]} | 預測標籤: {predicted_labels[i]} | 結果: {is_correct}")
    print("-" * 60)
    print("LeNet-5 實作範例執行完畢。")
    print("=" * 60)

if __name__ == "__main__":
    main()
