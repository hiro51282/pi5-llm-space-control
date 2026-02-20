# Experiment Log

本ファイルは「最小LLM空間理解」の過程を記録する。

目的は：

* 理論を実装で裏取りする
* 誤解と修正の履歴を残す
* 数ヶ月後の自分が読んで理解できるログを作る

---

# Phase1：出力層のみ学習（Embedding凍結）

## 日付
2026-02-13

## 目的

空間を固定したまま、Linear層だけで学習が成立するか確認する。

---

## 実験条件

* モデル: TinyModel (Embedding + Linear)
* hidden_dim: 8
* vocab: "helo"
* データ: "hello"
* エポック数: 200
* optimizer: Adam (lr=0.01)
* embedding: 凍結

---
## 予測

入力: "h"

Prediction: e

## 出力確率分布

h: 0.00066248  
e: 0.97796  
l: 0.014012  
o: 0.007370  

## 結果

* final loss ≈ 0.36
* h → e の予測は成立
* embeddingは更新されていない
* linear層のみ更新された

---

## 洞察

* 空間を固定しても学習は可能
* 出力射影のみで確率調整できる
* ただし自由度は制限される

---

## 現状までのログ
``` text
pi@pi:~/Documents/pi5-llm-space-control $  cd /home/pi/Documents/pi5-llm-space-control ; /usr/bin/env /home/pi/Documents/pi5-llm-space-control/venv/bin/python /home/pi/.vscode/extensions/ms-python.debugpy-2025.18.0-linux-arm64/bundled/libs/debugpy/adapter/../../debugpy/launcher 40991 -- /home/pi/Documents/pi5-llm-space-control/src/train_base.py 
final loss: 0.3504153788089752
```

``` text
pi@pi:~/Documents/pi5-llm-space-control $  cd /home/pi/Documents/pi5-llm-space-control ; /usr/bin/env /home/pi/Documents/pi5-llm-space-control/venv/bin/python /home/pi/.vscode/extensions/ms-python.debugpy-2025.18.0-linux-arm64/bundled/libs/debugpy/adapter/../../debugpy/launcher 54891 -- /home/pi/Documents/pi5-llm-space-control/src/train_base.py 
final loss: 0.3496347963809967
Prediction for 'h': e
```

``` text
pi@pi:~/Documents/pi5-llm-space-control $  cd /home/pi/Documents/pi5-llm-space-control ; /usr/bin/env /home/pi/Documents/pi5-llm-space-control/venv/bin/python /home/pi/.vscode/extensions/ms-python.debugpy-2025.18.0-linux-arm64/bundled/libs/debugpy/adapter/../../debugpy/launcher 39909 -- /home/pi/Documents/pi5-llm-space-control/src/train_base.py 
final loss: 0.3753582239151001
Prediction for 'h': e
```

``` text
pi@pi:~/Documents/pi5-llm-space-control $  cd /home/pi/Documents/pi5-llm-space-control ; /usr/bin/env /home/pi/Documents/pi5-llm-space-control/venv/bin/python /home/pi/.vscode/extensions/ms-python.debugpy-2025.18.0-linux-arm64/bundled/libs/debugpy/adapter/../../debugpy/launcher 41289 -- /home/pi/Documents/pi5-llm-space-control/src/train_base.py 
final loss: 0.3619987666606903
Prediction for 'h': e
Probabilities: tensor([[6.6248e-04, 9.7796e-01, 1.4012e-02, 7.3700e-03]])
```

# Phase1-2：Embedding（駅）とLinear（線路）の実証実験

## なぜこの検証を行ったか（Why）

理論では、

* Embeddingは座標
* 勾配は座標を動かす
* 出力は内積で決まる

と理解していた。

しかし直感では、

> h → e を学習すれば h と e は近づくのでは？

と考えていた。

この直感が正しいかを数値で検証する。

---

## 検証方針（How）

* 次元を 2 に縮小
* Embedding凍結を解除
* 学習前後の座標を保存
* 各単語の移動量を出力
* 内積を分解して出力決定プロセスを確認

---

## 実験条件

* hidden_dim: 2
* embedding: 学習対象
* エポック数: 200

---

## 結果

### ① Embedding移動

* h, e, l は大きく移動
* o は移動しなかった

→ 入力に出てこない単語には勾配が流れない

（北極星トークン）

---

### ② h と e の距離

近づいていなかった。

直感は外れた。

---

### ③ 内積分解（h入力時）

score_h = 1.13
score_e = 4.55  ← 最大
score_l = -2.21
score_o = 0.90

→ 次単語は e

決定は距離ではなく、

> embedding(h) と linear[e] の内積

で決まっている。

---

## 本質的理解

意味は

> 単語同士の距離ではない

意味は

> 単語と出力方向の一致度で決まる

---

## 比喩モデル

### 🚉 駅（Embedding）

単語は空間上の駅。

### 🚆 線路（Linear）

各出力方向は線路。

### 💡 懐中電灯（内積）

影が最も長くなる方向が選ばれる。

### 🧊 北極星

入力に出ない単語は動かない。

---

## 回転不変性

embedding と linear を同時に回転させても
出力は変わらない。

→ 絶対座標に意味はない
→ 相対構造のみが意味を持つ

---
## 現状までのログ
``` text
(venv) pi@pi:~/Documents/pi5-llm-space-control $  cd /home/pi/Documents/pi5-llm-space-control ; /usr/bin/env /home/pi/Documents/pi5-llm-space-control/venv/bin/python /home/pi/.vscode/extensions/ms-python.debugpy-2025.18.0-linux-arm64/bundled/libs/debugpy/adapter/../../debugpy/launcher 56927 -- /home/pi/Documents/pi5-llm-space-control/src/train_base.py 

=== Embedding Movement ===
h:
  before: [ 0.08503353 -1.0030769 ]
  after : [ 1.0607111 -1.9506682]
  diff  : [ 0.9756776 -0.9475913]

e:
  before: [-0.24764562  1.0446104 ]
  after : [-1.1945897  2.1180427]
  diff  : [-0.9469441  1.0734323]

l:
  before: [-1.3655794  -0.04460089]
  after : [-2.4353275   0.02118901]
  diff  : [-1.0697482   0.06578989]

o:
  before: [0.11271185 1.6435771 ]
  after : [0.11271185 1.6435771 ]
  diff  : [0. 0.]


=== Linear Weights ===
tensor([[ 1.1692,  0.0521],
        [ 1.7224, -1.3987],
        [-0.6259,  0.7975],
        [-1.1187, -1.0748]])

=== Example: h の内積分解 ===
embedding(h): [ 1.0607111 -1.9506682]

score_h = 1.138610601425171
score_e = 4.5553107261657715
score_l = -2.2195780277252197
score_o = 0.9099671840667725
final loss: 0.3588297963142395
```

``` text
(venv) pi@pi:~/Documents/pi5-llm-space-control $  cd /home/pi/Documents/pi5-llm-space-control ; /usr/bin/env /home/pi/Documents/pi5-llm-space-control/venv/bin/python /home/pi/.vscode/extensions/ms-python.debugpy-2025.18.0-linux-arm64/bundled/libs/debugpy/adapter/../../debugpy/launcher 52397 -- /home/pi/Documents/pi5-llm-space-control/src/train_base.py 

=== Embedding Movement ===
h:
  before: [-0.971792    0.01748226]
  after : [-2.2343283  1.490295 ]
  diff  : [-1.2625363  1.4728128]

e:
  before: [-0.30916807  0.22799832]
  after : [1.457043  1.2184566]
  diff  : [1.7662112 0.9904583]

l:
  before: [-0.07399309 -0.998068  ]
  after : [ 1.4252663 -0.8348193]
  diff  : [1.4992594  0.16324866]

o:
  before: [ 0.0373069  -0.29074842]
  after : [ 0.0373069  -0.29074842]
  diff  : [0. 0.]


=== Linear Weights ===
tensor([[-0.3554, -0.1877],
        [-1.4258,  0.7897],
        [ 1.5623,  0.5058],
        [ 0.9194, -1.4251]])

=== Example: e の内積分解 ===
embedding(e): [1.457043  1.2184566]

score_h = -0.7464861273765564
score_e = -1.1151466369628906
score_l = 2.8926234245300293
score_o = -0.39679673314094543
final loss: 0.37139078974723816
```

## 次フェーズ

* embedding固定 vs linear固定比較
* linearの移動量観測
* 距離と内積の関係可視化
