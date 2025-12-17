#Вариант 1 
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os

def create_test_qwerty_file():
    try:
        img = Image.new('RGB', (400, 300), color='green')
        from io import BytesIO
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_data = img_bytes.getvalue()
        dummy_data = b'Some dummy data before image\n'
        jpeg_start = b'\xFF\xD8\xFF'
        jpeg_end = b'\xFF\xD9'
        full_data = dummy_data + jpeg_start + img_data + jpeg_end
        with open("qwerty.txt", 'wb') as f:
            f.write(full_data)
        print("Создан тестовый файл qwerty.txt")
        return True
    except Exception as e:
        print(f"Ошибка создания тестового файла: {e}")
        return False
if __name__ == "__main__":
    if not os.path.exists("qwerty.txt"):
        create_test_qwerty_file()
class ImageHandler:
    
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        self.loaded = False
    
    def load_image(self):
        try:
            self.image = Image.open(self.image_path)
            self.loaded = True
            print(f"Изображение загружено: {self.image_path}")
            print(f"Исходный размер: {self.image.size}")
            print(f"Исходный формат: {self.image.format}")
            return True
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            return False
    
    def save_as_png(self, save_path):
        if not self.loaded:
            print("Изображение не загружено")
            return False
        
        try:
            if not save_path.lower().endswith('.png'):
                save_path = os.path.splitext(save_path)[0] + '.png'
            folder = os.path.dirname(save_path)
            if folder and not os.path.exists(folder):
                os.makedirs(folder)
            self.image.save(save_path, 'PNG')
            print(f"Изображение сохранено в формате PNG: {save_path}")
            return True
        except Exception as e:
            print(f"Ошибка сохранения изображения в формате PNG: {e}")
            return False
    
    def resize_to_300x300(self):
        if not self.loaded:
            print("Изображение не загружено")
            return False
        
        try:
            self.image = self.image.resize((300, 300))
            print(f"Размер изменен на 300x300 пикселей")
            return True
        except Exception as e:
            print(f"Ошибка изменения размера: {e}")
            return False
    
    def get_image_for_processing(self):
        if not self.loaded:
            print("Изображение не загружено")
            return None
        return self.image.copy()

class ImageProcessor:
    def __init__(self, image):
        self.image = image
    
    def apply_filter(self, filter_type):
        try:
            if filter_type == "blur":
                self.image = self.image.filter(ImageFilter.BLUR)
                print("Применен фильтр: размытие")
            elif filter_type == "contour":
                self.image = self.image.filter(ImageFilter.CONTOUR)
                print("Применен фильтр: контур")
            elif filter_type == "sharpen":
                self.image = self.image.filter(ImageFilter.SHARPEN)
                print("Применен фильтр: резкость")
            elif filter_type == "grayscale":
                self.image = self.image.convert('L')
                print("Применен фильтр: черно-белый")
            else:
                print(f"Неизвестный фильтр: {filter_type}")
                return False
            return True
        except Exception as e:
            print(f"Ошибка применения фильтра: {e}")
            return False
    
    def add_text(self, text, position=(10, 10), color=(255, 0, 0), font_size=20):
        try:
            if self.image.mode == 'L':
                self.image = self.image.convert('RGB')
            draw = ImageDraw.Draw(self.image)
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            draw.text(position, text, fill=color, font=font)
            print(f"Добавлен текст: {text}")
            return True
        except Exception as e:
            print(f"Ошибка добавления текста: {e}")
            return False
    
    def rotate_image(self, degrees):
        try:
            self.image = self.image.rotate(degrees, expand=True)
            print(f"Изображение повернуто на {degrees} градусов")
            return True
        except Exception as e:
            print(f"Ошибка поворота изображения: {e}")
            return False
    
    def get_processed_image(self):
        return self.image
def process_lab_image():
    print("Обработка изображения")
    
    # Шаг 1: Извлекаем изображение из бинарного файла
    binary_file = "qwerty.txt"
    extracted_image = "extracted_image.jpg"
    
    if not os.path.exists(binary_file):
        print(f"Файл {binary_file} не найден!")
        return
    
    print(f"\n1. Извлечение изображения из файла: {binary_file}")
    if extract_image_from_binary(binary_file, extracted_image):
        print("Изображение успешно извлечено")
    else:
        print("Не удалось извлечь изображение")
        print("Использую тестовое изображение")
        test_img = Image.new('RGB', (400, 300), color='blue')
        test_img.save("test_image.jpg")
        extracted_image = "test_image.jpg"
    print(f"\n2. Обработка изображения: {extracted_image}")
    handler = ImageHandler(extracted_image)
    
    if handler.load_image():
        handler.resize_to_300x300()
        image_for_processing = handler.get_image_for_processing()
        processor = ImageProcessor(image_for_processing)
        processor.apply_filter("blur")
        processor.apply_filter("grayscale")
        processor.add_text("Лабораторная работа", position=(20, 20), color=(255, 255, 255), font_size=24)
        processor.add_text("Обработка изображений", position=(20, 50), color=(200, 200, 200), font_size=18)
        processor.add_text(f"Исходник: {binary_file}", position=(20, 80), color=(150, 150, 150), font_size=14)
        processor.add_text("Вариант 1", position=(280, 280), color=(256, 256, 256), font_size=15)
        processor.rotate_image(5)
        processed_image = processor.get_processed_image()
        handler.image = processed_image
        output_file = "output/lab_result.png"
        handler.save_as_png(output_file)
        
        print(f"\nОбработка завершена")
        print(f"Результат сохранен в: {output_file}")
        if os.path.exists(output_file):
            result_img = Image.open(output_file)
            print(f"Размер результата: {result_img.size}")
            print(f"Формат результата: {result_img.format}")
            result_img.show()
        if os.path.exists("test_image.jpg"):
            os.remove("test_image.jpg")
    print("\n" + "-+" * 20)
    print("Задание выполнено")
    print("+-" * 20)
if __name__ == "__main__":
    def extract_image_from_binary(binary_file_path, output_image_path):
        try:
            with open(binary_file_path, 'rb') as f:
                data = f.read()
            jpeg_start = b'\xFF\xD8\xFF'
            start_offset = data.find(jpeg_start)
            if start_offset != -1:
                print(f"Найдена сигнатура JPEG по смещению: {start_offset}")
                jpeg_end = b'\xFF\xD9'
                end_offset = data.find(jpeg_end, start_offset)
                if end_offset != -1:
                    end_offset += 2
                    jpeg_data = data[start_offset:end_offset]
                    with open(output_image_path, 'wb') as img_file:
                        img_file.write(jpeg_data)
                    print(f"Изображение извлечено и сохранено как: {output_image_path}")
                    return True
            if b'Rar!' in data[:10]:
                print("Обнаружен архив RAR. Сохраняю как .rar файл")
                rar_path = output_image_path.replace('.jpg', '.rar')
                with open(rar_path, 'wb') as rar_file:
                    rar_file.write(data)
                print(f"Архив сохранен как: {rar_path}")
                print("Используйте WinRAR или 7-Zip для извлечения изображения.")
                return False
            print("Не удалось найти изображение. Создаю тестовое")
            return False
        except Exception as e:
            print(f"Ошибка при извлечении: {e}")
            return False
    process_lab_image()

