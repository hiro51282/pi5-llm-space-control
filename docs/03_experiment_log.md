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

# Phase2-A：Linear固定・Embeddingのみ学習（ノルム観測）

## なぜこの検証を行ったか（Why）

Phase1-2では、

* 意味は方向で決まる
* 出力は内積で決まる

ことを確認した。

しかし内積は

> ノルム × ノルム × cosθ

で構成される。

では、

Linearを固定し、Embeddingのみを学習させた場合、

* 方向で勝つのか？
* 長さ（ノルム）で押し切るのか？

を観測する。

---

## 実験条件

* hidden_dim: 2
* Linear: 凍結
* Embedding: 更新対象
* optimizer: Adam (lr=0.01)
* エポック数: 200
* 10epochごとに loss / ノルム / cosθ を出力

---

## 観測結果

### ① cosθ（h → e方向）

* -0.39 → 0.80
* 逆向きから整列へ
* 明確な方向最適化を確認

---

### ② ノルム変化

| token | 初期   | 最終   |
| ----- | ---- | ---- |
| h     | 1.28 | 1.57 |
| e     | 1.26 | 3.37 |
| l     | 0.96 | 1.06 |
| o     | 0.58 | 0.58 |

* eのみ大きく成長
* 頻出トークン強化を確認
* 爆発ではなく「健全成長」

---

### ③ loss

1.64 → 0.92
安定減少。収束途中。

---

## 洞察

* Linear固定でも学習は成立する
* 内積はEmbedding側のみで十分変化可能
* 学習は「方向＋強度」の両輪で進行する
* ノルムは“確信強度”として振る舞う可能性が高い

---

## 本実験での最重要発見

> ノルムは単なる長さではなく
> 意味の“強度”として機能している可能性がある。

---

## 次の問い

* ノルム固定すると何が起きるか？
* 方向のみでどこまで学習できるか？
* 強度と確信の関係は一般化できるか？

---
## 現状までのログ

``` text
=== Epoch 0 ===
loss: 1.6438908576965332
--- Norms ---
h: 1.2899
e: 1.2676
l: 0.9620
o: 0.5809
cos(h,e): -0.3988994359970093

=== Epoch 10 ===
loss: 1.5797233581542969
--- Norms ---
h: 1.1524
e: 1.4080
l: 0.8244
o: 0.5809
cos(h,e): -0.3774123191833496

=== Epoch 20 ===
loss: 1.5189850330352783
--- Norms ---
h: 1.0212
e: 1.5467
l: 0.6893
o: 0.5809
cos(h,e): -0.3472807705402374

=== Epoch 30 ===
loss: 1.4619767665863037
--- Norms ---
h: 0.9024
e: 1.6825
l: 0.5584
o: 0.5809
cos(h,e): -0.3024579882621765

=== Epoch 40 ===
loss: 1.4087615013122559
--- Norms ---
h: 0.8026
e: 1.8144
l: 0.4342
o: 0.5809
cos(h,e): -0.2356407791376114

=== Epoch 50 ===
loss: 1.3592242002487183
--- Norms ---
h: 0.7277
e: 1.9420
l: 0.3210
o: 0.5809
cos(h,e): -0.14108645915985107

=== Epoch 60 ===
loss: 1.3131632804870605
--- Norms ---
h: 0.6820
e: 2.0649
l: 0.2294
o: 0.5809
cos(h,e): -0.01974876970052719

=== Epoch 70 ===
loss: 1.2703619003295898
--- Norms ---
h: 0.6670
e: 2.1834
l: 0.1845
o: 0.5809
cos(h,e): 0.11708995699882507

=== Epoch 80 ===
loss: 1.2306175231933594
--- Norms ---
h: 0.6804
e: 2.2973
l: 0.2089
o: 0.5809
cos(h,e): 0.2519071102142334

=== Epoch 90 ===
loss: 1.1937401294708252
--- Norms ---
h: 0.7168
e: 2.4070
l: 0.2785
o: 0.5809
cos(h,e): 0.370629221200943

=== Epoch 100 ===
loss: 1.159541130065918
--- Norms ---
h: 0.7701
e: 2.5124
l: 0.3632
o: 0.5809
cos(h,e): 0.4677983224391937

=== Epoch 110 ===
loss: 1.1278256177902222
--- Norms ---
h: 0.8350
e: 2.6140
l: 0.4505
o: 0.5809
cos(h,e): 0.5445213913917542

=== Epoch 120 ===
loss: 1.0983917713165283
--- Norms ---
h: 0.9074
e: 2.7117
l: 0.5358
o: 0.5809
cos(h,e): 0.6044819951057434

=== Epoch 130 ===
loss: 1.0710355043411255
--- Norms ---
h: 0.9847
e: 2.8058
l: 0.6172
o: 0.5809
cos(h,e): 0.6515033841133118

=== Epoch 140 ===
loss: 1.0455563068389893
--- Norms ---
h: 1.0654
e: 2.8965
l: 0.6941
o: 0.5809
cos(h,e): 0.6887083649635315

=== Epoch 150 ===
loss: 1.0217626094818115
--- Norms ---
h: 1.1483
e: 2.9840
l: 0.7664
o: 0.5809
cos(h,e): 0.7184451222419739

=== Epoch 160 ===
loss: 0.999476969242096
--- Norms ---
h: 1.2329
e: 3.0685
l: 0.8341
o: 0.5809
cos(h,e): 0.7424388527870178

=== Epoch 170 ===
loss: 0.9785391688346863
--- Norms ---
h: 1.3186
e: 3.1500
l: 0.8977
o: 0.5809
cos(h,e): 0.7619613409042358

=== Epoch 180 ===
loss: 0.9588078260421753
--- Norms ---
h: 1.4052
e: 3.2289
l: 0.9576
o: 0.5809
cos(h,e): 0.7779631018638611

=== Epoch 190 ===
loss: 0.9401603937149048
--- Norms ---
h: 1.4925
e: 3.3051
l: 1.0142
o: 0.5809
cos(h,e): 0.7911637425422668

=== Embedding Movement ===
h:
  before: [-1.0756727  0.7368417]
  after : [-1.1595081 -1.0606185]
  diff  : [-0.08383536 -1.7974602 ]

e:
  before: [-0.96942395  0.7946444 ]
  after : [-2.5405831  2.2166421]
  diff  : [-1.5711591  1.4219978]

l:
  before: [ 0.5335501  -0.81705725]
  after : [-0.6325685  0.8542455]
  diff  : [-1.1661186  1.6713028]

o:
  before: [-0.14495392  0.5625342 ]
  after : [-0.14495392  0.5625342 ]
  diff  : [0. 0.]


=== Linear Weights ===
tensor([[ 0.1536, -0.2147],
        [-0.0644, -0.3381],
        [-0.5173,  0.5407],
        [ 0.3470,  0.5072]])

=== Example: h の内積分解 ===

--- Norms ---
h: 1.5714
e: 3.3717
l: 1.0630
o: 0.5809
cos(h,e): 0.8011090755462646
final loss: 0.924217700958252
```

### Table
| Epoch/token | h      | e      | cos(h,e)| l      | o      |
| ----------- | ------ | ------ | ------- | ------ | ------ |
|           0 | 1.2899 | 1.2676 | -0.3989 | 0.9620 | 0.5809 |
|          10 | 1.1524 | 1.4080 | -0.3774 | 0.8244 | 0.5809 |
|          20 | 1.0212 | 1.5467 | -0.3473 | 0.6893 | 0.5809 |
|          30 | 0.9024 | 1.6825 | -0.3025 | 0.5584 | 0.5809 |
|          40 | 0.8026 | 1.8144 | -0.2356 | 0.4342 | 0.5809 |
|          50 | 0.7277 | 1.9420 | -0.1411 | 0.3210 | 0.5809 |
|          60 | 0.6820 | 2.0649 | -0.0197 | 0.2294 | 0.5809 |
|          70 | 0.6670 | 2.1834 |  0.1171 | 0.1845 | 0.5809 |
|          80 | 0.6804 | 2.2973 |  0.2519 | 0.2089 | 0.5809 |
|          90 | 0.7168 | 2.4070 |  0.3706 | 0.2785 | 0.5809 |
|         100 | 0.7701 | 2.5124 |  0.4678 | 0.3632 | 0.5809 |
|         110 | 0.8350 | 2.6140 |  0.5445 | 0.4505 | 0.5809 |
|         120 | 0.9074 | 2.7117 |  0.6045 | 0.5358 | 0.5809 |
|         130 | 0.9847 | 2.8058 |  0.6515 | 0.6172 | 0.5809 |
|         140 | 1.0654 | 2.8965 |  0.6887 | 0.6941 | 0.5809 |
|         150 | 1.1483 | 2.9840 |  0.7184 | 0.7664 | 0.5809 |
|         160 | 1.2329 | 3.0685 |  0.7424 | 0.8341 | 0.5809 |
|         170 | 1.3186 | 3.1500 |  0.7620 | 0.8977 | 0.5809 |
|         180 | 1.4052 | 3.2289 |  0.7780 | 0.9576 | 0.5809 |
|         190 | 1.4925 | 3.3051 |  0.7912 | 1.0142 | 0.5809 |

---

## 追加考察：ノルムと方向の二段階学習挙動

### ① 一番目立つ動き：e のノルム

e のノルムは

> 1.26 → 3.30

へと、ほぼ一直線に増加した。

迷いがない。

これは

> 「e を強くしろ」という勾配が一貫して流れている

ことを示している。

爆発ではない。
構造的に整った成長である。

---

### ② cos(h,e) の変化

cos(h,e) は

> -0.39 → 0.79

へと単調増加した。

特に注目すべき点：

* epoch60付近で 0 を通過
* そこから正方向に加速

これは明確に

> 方向最適化が進行している

ことを示している。

---

### ③ h と l の挙動

#### h

一度ノルムが下がる
→ 途中から再び増加

#### l

かなり縮む
→ その後ゆっくり戻る

これは非常に興味深い。

---

## 何が起きているのか？

テーブルを観察すると、

学習は一段階ではなく、
二段階で進行しているように見える。

### 前半

* まず cosθ を改善
* 方向を合わせに行く
* h, l のノルムは一時的に縮む

👉 角度最適化が優先されている

### 後半

* 方向がある程度揃った
* 次はノルムで内積を押し上げる

👉 強度（ノルム）最適化段階へ移行

---

## 最重要ポイント

これはノルム爆発ではない。

これは

> 構造的に整った成長

である。

---

## さらに深い読み

なぜ e だけが顕著に伸び続けるのか？

hello の遷移構造は：

h → e
e → l

e は中間ノードである。

つまり、

> グラフ中心性が高い

頻出かつ接続の多いノードが強化されている。

空間構造的にも、

> 「重要ノード」が太る

という自然な挙動が観測された。

---

## 最も美しい点

o は一切動かない。

入力にも出現せず、
勾配も流れない。

> 北極星トークン

として完全な対照実験になっている。

---

## 本実験の核心的まとめ

> 学習は一段階ではなく、
> まず方向を整え、次に強度を増す二段階挙動を示した。

また、

> 最適化対象は駅間距離ではない。
> 最適化されているのは「内積（方向 × 強度）」である。
> hは単純にeへ直線移動したのではなく、
> 方向を合わせながら半径を変化させるスパイラル挙動を示した。
