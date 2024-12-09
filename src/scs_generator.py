import os


class ScsGenerator:
    def __init__(self, output_directory: str):
        self.output_directory = output_directory

    def generate_scs_file(self, data, scs_filename):
        """Генерация SCS файла для конкретных данных"""
        scs_data = self.create_scs_content(data)
        with open(os.path.join(self.output_directory, scs_filename), 'w', encoding='utf-8') as scs_file:
            scs_file.write(scs_data)

    def create_scs_content(self, data):
        """Создание содержимого для SCS файла"""
        scs_content = f"nrel_main_idtf:\n    [{data['name']}] (* <- lang_ru;; *);\n"
        scs_content += f"nrel_reference_link:\n    [{data['url']}] (* <- uri;; *);\n"
        scs_content += f"nrel_address:\n    [{data['address']}] (* <- lang_ru;; *);\n"
        return scs_content
