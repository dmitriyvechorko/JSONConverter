import os

from src.Config import Config
from src.concept_mapper import ConceptMapper
from src.file_handler import FileHandler
from src.parser import SCSConverter
from src.scs_generator import ScsGenerator

class Parser:
    def __init__(self, input_directory: str, output_directory: str, type_mapping: dict):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.file_handler = FileHandler(input_directory)
        self.concept_mapper = ConceptMapper(type_mapping)
        self.scs_generator = ScsGenerator(output_directory)

    def process_files(self):
        """Обработка всех JSON файлов в директории и создание соответствующих SCS файлов"""
        data_list = self.file_handler.load_files()
        for data in data_list:
            name = data.get('name')
            if name:
                concept = self.concept_mapper.map_concept(name)
                scs_filename = self.get_scs_filename(name)
                self.scs_generator.generate_scs_file(data, scs_filename)

    def get_scs_filename(self, name: str) -> str:
        """Создание имени для SCS файла (по названию, транслитерированному в нижний регистр)"""
        transliterated_name = self.transliterate_name(name)
        return f"{transliterated_name}.scs"

    def transliterate_name(self, name: str) -> str:
        """Транслитерация названия для формирования имени файла"""
        return name.lower().replace(" ", "_")  # Примерная реализация

if __name__ == "__main__":
    # Указываем директории непосредственно в коде
    input_dir = Config.INPUT_DIR  # Путь к входной директории с JSON файлами
output_dir = Config.OUTPUT_DIR  # Путь к выходной директории для SCS файлов

# Проверка существования выходной директории, если нет - создать
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

scs_converter = SCSConverter(input_dir=input_dir, output_dir=output_dir)
scs_converter.process_all_json_files()
