# Pi5 LLM Space Control

Raspberry Pi 5（CPUのみ）環境で、
小型言語モデルの内部ベクトル空間を操作し、
「意味がどのように形成されるのか」を観測する実験プロジェクト。

---

## 1. これは何か

* LLM内部空間（Embedding・Linearなど）の観測と制御を試みる実験プロジェクト
* 目的は「意味がどのように形成されるかを中身から理解すること」
* 実験は極小モデル（helo）から開始

---
## 2. 現在のフェーズ

* Phase 1：空間理解と用語整理（完了）
* Phase 2：空間制御実験（準備中）

---

## 3. 読み方ガイド

* 設計思想 → docs/02_design_philosophy.md
* 実験ログ → docs/03_experiment_log.md
* 用語整理 → docs/04_space_control_glossary.md
* 現在の設計状態 → PROJECT_SUMMARY.md

---

## 4. プロジェクト方針

* 小さく観測する
* 一度に1要素だけ変える
* 思考ログを残す

---

## 5. 注意

このリポジトリは「完成品」ではなく、
理解過程そのものを記録するための実験ログである。

---

## 6. 制約条件

- Raspberry Pi 5
- CPUのみ（GPUなし）
- 小型モデル（5M〜10Mパラメータ目安）
- 低電力・ローカル完結

---

## 7. 実行環境

- Python 3.11
- PyTorch (CPU)
- venv 使用

詳細なセットアップ手順は docs/SETUP.md を参照。
