# Ubuntu 安裝 Antigravity IDE 指南

為了在 Ubuntu 26.04 上順利安裝並執行 **Antigravity IDE**，我們必須在安裝時主動避開兩個核心痛點：**Linux 核心對 Electron 沙盒（User Namespaces）的嚴格限制**，以及**檔案路徑中帶有空格**所導致的參數失效問題。

以下為彙整上述除錯經驗後，最安全、流暢且保證能成功啟動的完整安裝指南：

---

## 步驟 1：安裝系統基礎組件

打開終端機，先更新系統套件清單，並安裝後續解壓縮與環境配置所需的工具：

```bash
sudo apt update
sudo apt install curl tar desktop-file-utils python3 -y

```

## 步驟 2：下載與手動解包（移除路徑空格）

為了避免 Electron 底層程序對路徑空格相容性差的問題，建議將目標資料夾命名為不含空格的 `antigravity-ide`。

1. 請至官網下載 Linux 版本的 `Antigravity IDE.tar.gz` 壓縮包。
2. 建立系統安裝目錄，並將檔案解壓至 `/opt/google-agy/Antigravity-IDE`：
```bash
sudo mkdir -p /opt/google-agy/Antigravity-IDE
sudo tar -zxvf ~/Downloads/Antigravity\ IDE.tar.gz -C /opt/google-agy/Antigravity-IDE --strip-components=1

```



## 步驟 3：建立強制關閉沙盒的啟動腳本（關鍵步驟）

由於 Ubuntu 26.04 的安全機制會直接阻擋 Chromium 的 Zygote 程序，我們必須透過一個 Wrapper（包裝）腳本，強制將環境變數與 `--no-sandbox` 參數注入最底層。

1. **將原始二進位執行檔改名備用：**
```bash
sudo mv /opt/google-agy/Antigravity-IDE/antigravity-ide /opt/google-agy/Antigravity-IDE/antigravity-ide.real

```


2. **建立一個全新同名的啟動腳本：**
```bash
sudo nano /opt/google-agy/Antigravity-IDE/antigravity-ide

```


3. **將以下內容完整貼入編輯器中：**
```bash
#!/bin/bash
# 強制關閉 Electron 沙盒與防止顯示伺服器衝突
export ELECTRON_DISABLE_SANDBOX=1
export DISABLE_WAYLAND=1

# 執行真實程式並強行注入除錯參數
exec "/opt/google-agy/Antigravity-IDE/antigravity-ide.real" --no-sandbox --disable-gpu-sandbox "$@"

```


*(儲存並離開：按下 `Ctrl+O` 儲存，再按下 `Ctrl+X` 離開。)*
4. **賦予該腳本可執行權限：**
```bash
sudo chmod +x /opt/google-agy/Antigravity-IDE/antigravity-ide

```



## 步驟 4：建立全域軟連結（Symlink）

讓你隨時可以在終端機的任何路徑下，直接輸入命令啟動 IDE：

```bash
sudo ln -sf /opt/google-agy/Antigravity-IDE/antigravity-ide /usr/local/bin/Antigravity-IDE

```

## 步驟 5：新增桌面捷徑（應用程式選單圖示）

為了能從 Ubuntu 的選單（Activities）或 Dock 點擊啟動，我們需要建立一個系統捷徑檔：

```bash
sudo tee /usr/share/applications/Antigravity-IDE.desktop > /dev/null <<'EOF'
[Desktop Entry]
Name=Antigravity IDE
Comment=An agentic development platform from Google
Exec=/opt/google-agy/Antigravity-IDE/antigravity-ide
Icon=/opt/google-agy/Antigravity-IDE/resources/app/resources/icon.png
Terminal=false
Type=Application
Categories=Development;IDE;
EOF

```

*(備註：`Icon` 圖示路徑若因軟體版本更新有變動，請改至實際存放 `icon.png` 的資料夾路徑。)*

最後，更新系統桌面圖示資料庫以即時生效：

```bash
sudo update-desktop-database

```

---

## 🛠️ 疑難排解備忘（全面防禦）

如果依照上述步驟啟動，系統仍因為 AppArmor 殘留規則噴出 `拒絕不符權限的操作 (13)`，請直接執行以下指令，徹底解除 AppArmor 對該執行檔的監控：

```bash
sudo aa-disable /opt/google-agy/Antigravity-IDE/antigravity-ide.real 2>/dev/null
sudo aa-disable /opt/google-agy/Antigravity-IDE/antigravity-ide 2>/dev/null

```

現在，你可以按下鍵盤的 `Super` 鍵（Windows 鍵），搜尋 **Antigravity IDE** 並順利點擊開啟，開始享受 Google AI Agent 帶來的開發體驗了！