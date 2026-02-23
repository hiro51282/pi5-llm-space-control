# SETUP.md

# 🛠 実行環境セットアップ

本プロジェクトは Raspberry Pi 5（CPUのみ）前提。

Python 3.11 を想定。

---

## 1️⃣ venv を作成（推奨）

理由：

- 再現性の確保
- 将来のPi環境差異回避
- GitHub上での信頼性向上

### 作成

```bash
python -m venv venv
````

### 有効化

```bash
source venv/bin/activate
```

### 無効化

```bash
deactivate
```

※ プロンプトに `(venv)` が付いていれば成功。

---

## 2️⃣ PyTorch（CPU版）をインストール

Pi5（GPUなし）のためCPU版を使用。

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

確認：

```bash
python -c "import torch; print(torch.__version__)"
```

バージョンが表示されればOK。

---

## 3️⃣ numpy をインストール

```bash
pip install numpy
```

※ PyTorchの警告回避のため推奨。

---

## 4️⃣ 実行確認

例：

```bash
python src/train_base.py
```

エラーが出なければ環境構築完了。
