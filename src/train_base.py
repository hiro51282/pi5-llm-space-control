import copy
import torch
import torch.nn as nn
from model import TinyModel

# --- vocab ---
vocab = list("helo")
vocab_size = len(vocab)

char_to_idx = {ch: i for i, ch in enumerate(vocab)}
idx_to_char = {i: ch for ch, i in char_to_idx.items()}

# --- data ---
text = "hello"

inputs = torch.tensor([char_to_idx[c] for c in text[:-1]])
targets = torch.tensor([char_to_idx[c] for c in text[1:]])

# --- model ---
model = TinyModel(vocab_size, hidden_dim=2)

# 学習前保存
initial_embedding = copy.deepcopy(model.embedding.weight.data)

# embedding凍結
# for param in model.embedding.parameters():
#     param.requires_grad = False

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# --- train ---
for epoch in range(200):
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = loss_fn(outputs, targets)
    loss.backward()
    optimizer.step()

# 学習後取得
final_embedding = model.embedding.weight.data

print("\n=== Embedding Movement ===")
for idx in range(vocab_size):
    token = idx_to_char[idx]
    before = initial_embedding[idx]
    after = final_embedding[idx]
    diff = after - before
    print(f"{token}:")
    print("  before:", before.numpy())
    print("  after :", after.numpy())
    print("  diff  :", diff.numpy())
    print()

print("\n=== Linear Weights ===")
print(model.linear.weight.data)

print("\n=== Example: h の内積分解 ===")

# with torch.no_grad():
#     h_idx = char_to_idx['h']
#     v = model.embedding.weight.data[h_idx]

#     W = model.linear.weight.data

#     print("embedding(h):", v.numpy())
#     print()

#     for i in range(vocab_size):
#         score = torch.dot(v, W[i])
#         token = idx_to_char[i]
#         print(f"score_{token} =", score.item())
with torch.no_grad():
    e_idx = char_to_idx['e']
    v = model.embedding.weight.data[e_idx]

    W = model.linear.weight.data

    print("embedding(e):", v.numpy())
    print()

    for i in range(vocab_size):
        score = torch.dot(v, W[i])
        token = idx_to_char[i]
        print(f"score_{token} =", score.item())

print("final loss:", loss.item())