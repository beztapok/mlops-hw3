import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import torch
import sys
from PIL import Image
from torchvision import transforms


def run_inference(image_path):
    # 1. Завантаження збереженої моделі [cite: 101]
    model = torch.jit.load("model.pt")
    model.eval()

    # 2. Підготовка зображення [cite: 16, 102]
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    try:
        input_image = Image.open(image_path).convert('RGB')
        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0) 

        # 3. Виконання передбачення
        with torch.no_grad():
            output = model(input_batch)

        # 4. Визначення топ-3 класів [cite: 33, 103]
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        top3_prob, top3_indices = torch.topk(probabilities, 3)

        print(f"--- Результати для {image_path} ---")
        for i in range(3):
            print(f"Клас #{top3_indices[i].item()}: {top3_prob[i].item():.4f}")

    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Використання: python3 inference.py <шлях_до_картинки>")
    else:
        run_inference(sys.argv[1])