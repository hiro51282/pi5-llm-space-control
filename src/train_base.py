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
model = TinyModel(vocab_size, hidden_dim=8)

# embedding凍結
for param in model.embedding.parameters():
    param.requires_grad = False

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# --- train ---
for epoch in range(200):
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = loss_fn(outputs, targets)
    loss.backward()
    optimizer.step()

print("final loss:", loss.item())

with torch.no_grad():
    test_input = torch.tensor([char_to_idx["h"]])
    output = model(test_input)

    predicted_idx = torch.argmax(output).item()
    print("Prediction for 'h':", idx_to_char[predicted_idx])

    probs = torch.softmax(output, dim=1)
    print("Probabilities:", probs)
