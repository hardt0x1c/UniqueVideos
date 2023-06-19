import cv2
import numpy as np


# Функция для добавления шума в кадр видео
def add_noise(frame, noise_type='gaussian', intensity=0.1):
    if noise_type == 'gaussian':
        # Генерация шума Гаусса
        h, w, _ = frame.shape
        noise = np.random.normal(0, intensity, (h, w, 3)) * 255
        noisy_frame = np.clip(frame + noise, 0, 255).astype(np.uint8)
    elif noise_type == 'salt_and_pepper':
        # Генерация шума "соль и перец"
        h, w, _ = frame.shape
        noise = np.random.choice([0, 255], size=(h, w, 3), p=[intensity, 1 - intensity])
        noisy_frame = np.clip(frame + noise, 0, 255).astype(np.uint8)
    else:
        noisy_frame = frame

    return noisy_frame


# Функция для наложения невидимых элементов
def overlay_invisible_elements(frame):
    # Пример: добавление прямоугольника с прозрачностью
    overlay = np.zeros(frame.shape, dtype=np.uint8)
    x, y, w, h = 100, 100, 200, 200
    alpha = 1  # Прозрачность элемента (от 0 до 1)
    cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 0, 255), -1)
    overlay = (overlay * alpha).astype(np.uint8)
    overlayed_frame = cv2.addWeighted(frame, 1, overlay, 1 - alpha, 0)
    return overlayed_frame


# Функция для удаления метаданных
def remove_metadata(video_path, output_path, noise_type='gaussian', intensity=0.02):
    # Загрузка видео
    video_capture = cv2.VideoCapture(video_path)

    # Создание объекта для записи видео
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(output_path, fourcc, 30.0, (int(video_capture.get(3)), int(video_capture.get(4))))

    # Чтение и обработка кадров видео
    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if not ret:
            break

        # Изменение исходного кода видео
        modified_frame = add_noise(frame, noise_type, intensity)

        # Наложение невидимых элементов
        overlayed_frame = overlay_invisible_elements(modified_frame)

        # Запись кадра в выходное видео
        output_video.write(overlayed_frame)

    # Освобождение ресурсов
    video_capture.release()
    output_video.release()


# Путь до исходного и итогового видео
video_path = 'video.mp4'
output_path = 'video_unique.mp4'


# Запуск основной функции
if __name__ == '__main__':
    remove_metadata(video_path, output_path)
