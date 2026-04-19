import torch
import torchvision.models as models
import ssl

# Цей рядок виправляє помилку SSL на macOS
ssl._create_default_https_context = ssl._create_unverified_context

# 1. Завантажуємо модель [cite: 29]
print("Завантаження моделі...")
model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
model.eval()

# 2. Використовуємо TorchScript (jit.trace) [cite: 98]
example_input = torch.rand(1, 3, 224, 224)
traced_model = torch.jit.trace(model, example_input)

# 3. Зберігаємо у файл model.pt [cite: 31, 68]
traced_model.save("model.pt")

print("✅ Модель успішно збережена як model.pt")