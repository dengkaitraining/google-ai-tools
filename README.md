## 【人工智慧工具應用實務班第01期】- 115年07月06日
## （08:00 ~ 12:00）AI 代理人概論（曾士桓）
 - [AI 協作- Antigravity 2.0/Codex](https://drive.google.com/file/d/1zw4GLvG1Rmt9jB11mS6A_TtkjwR0KUQH/view?usp=drive_link)
 - [AI 協作 - 軟體開發生命週期](https://drive.google.com/file/d/1saDyqs06lJ6ARLe2fLid_wLbJjf5T61O/view?usp=drive_link)
### Anitgravity 2.0 (Ubuntu 26.04)
 - [Antigravity 工具](https://antigravity.google/download)
 - [Anitgravity 2.0 工具](https://antigravity.google/download#antigravity-2)
 #### 1. 透過 snap 工具安裝 antigravity
 ```sh
 # 透過 snap 工具安裝 antigravity
 sudo snap install antigravity
 ```
 #### 2. ```Google``` 官網下載桌面應用軟體 (2026-07-08)
  - 建立軟體安裝位址：
  ```sh
  # create software path
  sudo mkdir /opt/google-agy
  sudo chown -R <username>:<usergroup> /opt/google-agy
  ```
  - ```Google Anitgravity``` 官網：[https://antigravity.google/](https://antigravity.google/)
  - 1. ```Anitgravity 2.0``` 下載位址：[https://antigravity.google/download#antigravity-2](https://antigravity.google/download#antigravity-2)
    - 1. ```Windows``` 版本下載位址：[https://storage.googleapis.com/antigravity-public/antigravity-hub/2.2.1-5287492581195776/windows-x64/Antigravity-x64.exe](https://storage.googleapis.com/antigravity-public/antigravity-hub/2.2.1-5287492581195776/windows-x64/Antigravity-x64.exe)
    - 2. ```Linux``` 版本下載位址：[https://storage.googleapis.com/antigravity-public/antigravity-hub/2.2.1-5287492581195776/linux-x64/Antigravity.tar.gz](https://storage.googleapis.com/antigravity-public/antigravity-hub/2.2.1-5287492581195776/linux-x64/Antigravity.tar.gz)
    ```sh
    # download Linux Anitgravity 2.0
    cd /opt/google-agy
    wget https://storage.googleapis.com/antigravity-public/antigravity-hub/2.2.1-5287492581195776/linux-x64/Antigravity.tar.gz
    ```
  - 2. ```Anitgravity CLI``` 下載位址：[https://antigravity.google/download#antigravity-cli](https://antigravity.google/download#antigravity-cli)
    - 1. ```Windows``` 版本下載位址：
    ```powershell
    irm https://antigravity.google/cli/install.ps1 | iex
    ```
    - 2. ```Linux``` 版本下載位址：
    ```sh
    curl -fsSL https://antigravity.google/cli/install.sh | bash
    ```
  - 3. ```Anitgravity IDE``` 下載位址：[https://antigravity.google/download#antigravity-ide](https://antigravity.google/download#antigravity-ide)
    - 1. ```Windows``` 版本下載位址：[https://edgedl.me.gvt1.com/edgedl/release2/j0qc3/antigravity/stable/2.1.1-6123990880747520/windows-x64/Antigravity%20IDE.exe](https://edgedl.me.gvt1.com/edgedl/release2/j0qc3/antigravity/stable/2.1.1-6123990880747520/windows-x64/Antigravity%20IDE.exe)
    - 2. ```Linux``` 版本下載位址：[https://edgedl.me.gvt1.com/edgedl/release2/j0qc3/antigravity/stable/2.1.1-6123990880747520/linux-x64/Antigravity%20IDE.tar.gz](https://edgedl.me.gvt1.com/edgedl/release2/j0qc3/antigravity/stable/2.1.1-6123990880747520/linux-x64/Antigravity%20IDE.tar.gz)
    ```sh
    # download Linux Anitgravity IDE
    cd/opt/google-agy
    wget https://edgedl.me.gvt1.com/edgedl/release2/j0qc3/antigravity/stable/2.1.1-6123990880747520/linux-x64/Antigravity%20IDE.tar.gz
    ```
### 安裝 ```Anitgravity 2.0``` (手動解壓 ```Tarball``` 並建立桌面快捷鍵) - 2026-07-08
 - 1. **解壓縮並移動至系統目錄**（以移動到 /opt 為例）：
```sh
# method 1.
sudo tar -xzf ~/Downloads/antigravity-linux-x64.tar.gz -C /opt/
# 修正內建沙盒權限問題（Electron 應用常見需求）
sudo chown root:root /opt/Antigravity-x64/chrome-sandbox
sudo chmod 4755 /opt/Antigravity-x64/chrome-sandbox

# method 2.
cd /opt/google-agy
tar -xzf Antigravity.tar.gz
# 修正內建沙盒權限問題（Electron 應用常見需求）
sudo chown root:root /opt/google-agy/Antigravity-x64/chrome-sandbox
sudo chmod 4755 /opt/google-agy/Antigravity-x64/chrome-sandbox
```
 - 2. 建立桌面圖示啟動器，方便從應用程式選單點擊啟動：
```sh
# method 1.
cat << 'EOF' > ~/.local/share/applications/antigravity-2.desktop
[Desktop Entry]
Name=Antigravity 2.0
Comment=Antigravity 2.0 - Experience liftoff
GenericName=2.0
Exec="/opt/Antigravity-x64/antigravity" %F
Icon=/opt/Antigravity-x64/resources/app/resources/icon.png
Type=Application
Terminal=false
StartupNotify=true
StartupWMClass=Antigravity
Categories=Development;2.0;TextEditor;
EOF

chmod +x ~/.local/share/applications/antigravity-2.desktop
update-desktop-database ~/.local/share/applications

# method 2.
cat << 'EOF' > ~/.local/share/applications/antigravity-2.desktop
[Desktop Entry]
Name=Antigravity 2.0
Comment=Antigravity 2.0 - Experience liftoff
GenericName=2.0
Exec="/opt/google-agy/Antigravity-x64/antigravity" %F
Icon=/opt/google-agy/Antigravity-x64/resources/app/resources/icon.png
Type=Application
Terminal=false
StartupNotify=true
StartupWMClass=Antigravity
Categories=Development;2.0;TextEditor;
EOF

chmod +x ~/.local/share/applications/antigravity-2.desktop
update-desktop-database ~/.local/share/applications
```

### 安裝 ```Anitgravity CLI``` - 2026-07-08
 - 1. 執行自動安裝腳本（會將 agy 二進位檔下載到 ```~/.local/bin/agy```）：
```sh
curl -fsSL https://antigravity.google/cli/install.sh | bash
```
 - 2. 將路徑加入環境變數（如果終端機找不到 ```agy``` 指令）：
```sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```
 - 3. 驗證安裝並登入帳戶：
```sh
agy --version
agy auth login
```
 #### 參考資料
  - [Google API Search : 'ubuntu antigravity install'](https://www.google.com/search?q=ubuntu+antigravity+install&sca_esv=a12f55507eaf5fab&sxsrf=APpeQnvIXDdjb8b5YlglxtSVhDqCZXv3mw%3A1783481111880&udm=50&source=chrome.ob&fbs=ABfTbFUhNGvvPEUFOvrsPMHwBXgOKQbaUEtApl9j-7vdAXA5KQzN1WzfUsLBMqckPdakSaEgef0W3ft7jUgHaPpSyiVNyWvj8YQdpeC6WsZG4xN-TSrNaHDwdXF_piJcndrwjHaR9gj3VZxSohG4CAJ5vRfy3cdFeqY2MIn0PdUURyQaB2syTcbieQxG7zVmkRm_dT-ggxGy&aep=1&ntc=1&sa=X&ved=2ahUKEwj2jYzxkMKVAxVQoa8BHXBXH7kQ2J8OegQIERAD&biw=1920&bih=856&dpr=1&mstk=AUtExfA13HDGE9QYTPp3SgMof_OD4YbktlNReU5nYPSeemvriB3l-ufMoq1DzKTgdfDN5_tOsTIzqyJf8KTwmPfMNtwBzvxNjJm8GQl-vYSfR15iG4fblYhKNh3D4weloK9_CyenmljGf7cMkrz1zjgwjNPDC0AOl0q4ZsOqX6MW2me9fh1c_3zS1PXVz2XFiK9mr003lquHOtPQX_K8M8u8t3mt2hE5Df3rpMh9p4NTJEuk1g0cWAII1ZpxDDhLabdIDE3_4Upa5UjEpxFQ6gYw79cdtMR-0EGxoT9oq75Z1565YCgF1nh1ou8QthGvtbVmpcb2cen3UF3gCw&csuir=1&zx=1783481117567&mtid=G8NNaoLTLfjQ1e8Pu4DhqAM)