#!/bin/bash

# Файл для логування 
LOG_FILE="install.log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "--- Перевірка середовища: $(date) ---"

# Функція для перевірки та встановлення через brew
check_and_install() {
    if command -v $1 &> /dev/null; then
        echo "[✅] $1 вже встановлено: $($1 --version | head -n 1)"
    else
        echo "[🚀] Встановлення $1..."
        brew install $1 || echo "[❌] Не вдалося встановити $1. Перевірте Homebrew."
    fi
}

# 1. Перевірка Docker та Docker Compose [cite: 15, 19]
check_and_install "docker"

if docker compose version &> /dev/null; then
    echo "[✅] Docker Compose доступний."
else
    echo "[🚀] Спроба встановити docker-compose..."
    brew install docker-compose
fi

# 2. Перевірка Python >= 3.9 [cite: 15, 20]
PYTHON_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null)
if [[ $(echo "$PYTHON_VER >= 3.9" | bc -l) -eq 1 ]]; then
    echo "[✅] Python $PYTHON_VER відповідає вимогам."
else
    echo "[🚀] Встановлення Python 3.9..."
    brew install python@3.9
fi

# 3. Перевірка та встановлення pip [cite: 15, 21]
check_and_install "pip3"

# 4. Встановлення Python-бібліотек (ідемпотентно) [cite: 15, 16, 22, 23]
echo "[🚀] Перевірка Python-бібліотек..."
pip3 install torch torchvision pillow Django

echo "--- Встановлення завершено: $(date) ---"