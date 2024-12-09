import os
import json

class FileHandler:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.ensure_output_directory_exists()

    def ensure_output_directory_exists(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Выходная директория {self.output_dir} была создана.")
        else:
            print(f"Выходная директория {self.output_dir} уже существует.")

    def load_json_files(self):
        """Загружает все JSON файлы из входной директории."""
        json_data = []
        for filename in os.listdir(self.input_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.input_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    json_data.extend(json.load(file))  # Добавляем все объекты в список
        return json_data
