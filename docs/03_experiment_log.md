# Experiment Log

本ファイルには以下を記録する：

- 実験日
- ハイパーパラメータ
- 変更点
- 観測結果
- 所感

ログは再現性確保のため詳細に記録する。

# Experiment: Output Layer Only Training

## 日付
2026-02-13

## 実験条件

- モデル: TinyModel (Embedding + Linear)
- hidden_dim: 8
- vocab: "helo"
- データ: "hello"
- エポック数: 200
- optimizer: Adam (lr=0.01)
- embedding: 凍結

---

## 学習前（未観測なら今後追加）

※今後追加予定

---

## 学習後結果

- final loss: 0.3619987666606903

### 予測

入力: "h"

Prediction: e

### 出力確率分布

h: 0.00066248  
e: 0.97796  
l: 0.014012  
o: 0.007370  

---

## 観測事実

- embeddingは更新されていない
- linear層のみ更新された
- 正解トークン(e)の確率が約97%に上昇
- lossは全層学習時よりやや高い

---

## 考察（暫定）

- 空間は固定されたまま
- 出力射影のみで学習は可能
- 自由度が制限されるため収束性能は若干低下

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