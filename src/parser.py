import os
import json
import re
from transliterate import translit


class SCSConverter:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def transliterate_name(self, name):
        """Транслитерация названия для формирования имени файла"""
        return translit(name, language_code='ru', reversed=True).replace(' ', '_')

    def determine_concept(self, name):
        """Определяет концепт на основе ключевых слов в названии"""
        keywords = {
            "музей": "museum",
            "памятник": "monument",
            "церковь": "church",
            "отель": "hotel",
            "ресторан": "restaurant",
            "кафе": "cafe",
            "бар": "bar",
            "кинотеатр": "cinema",
            "театр": "theater",
            "галерея": "gallery",
            "парк": "park",
            "клуб": "club",
            "спа": "spa",
            "массаж": "massage",
            "казино": "casino",
            "стриптиз": "striptease",
            "сексшоп": "sex_shop",
            "спортзал": "gym",
            "библиотека": "library",
            "торговый центр": "shopping_center"
        }

        # Приводим название к нижнему регистру для поиска
        name_lower = name.lower()

        # Проверяем на наличие ключевых слов в наименовании
        for key, concept in keywords.items():
            if re.search(r'\b' + re.escape(key) + r'\b', name_lower):
                return concept

        return "other"  # Если не нашли подходящего ключевого слова, возвращаем "other"

    def convert_to_scs(self, item):
        """Конвертирует данные в формат SCS"""
        establishment_type = self.determine_concept(item['name'])  # Определяем тип заведения
        description = item.get("description", "Описание отсутствует.")
        url = item.get("url", None)
        address = item.get("address", "Адрес не указан.")
        reviews = item.get("reviews", [])

        scs_content = f"..{self.transliterate_name(item['name'])}\n"
        scs_content += "\n    => nrel_place_idtf:\n"
        scs_content += f"        [{item['name']}]\n"
        scs_content += f"        (* <- lang_ru;; *);\n"
        scs_content += f"        [{self.transliterate_name(item['name'])}] (* <- lang_en;; *);\n"

        if url:
            scs_content += f"\n    => nrel_reference_link:\n        [{url}] (* <- url;; *);\n"

        scs_content += f"\n    => nrel_place_address:\n        [{address}] (* <- lang_ru;; *);\n"

        # Добавляем отзывы, если они есть
        if reviews:
            for review in reviews:
                author = review.get("author", "Неизвестный автор")
                comment = review.get("comment", "Комментарий отсутствует")
                rating = review.get("rating", "Нет оценки")
                scs_content += f"\n    => nrel_review:\n"
                scs_content += f"        [\"{author}\"]\n"
                scs_content += f"        (* -> nrel_author: [{author}];;\n"
                scs_content += f"           -> nrel_rating: [{rating}];;\n"
                scs_content += f"           -> nrel_comment: [{comment}];; *);\n"

        scs_content += f"\n    <-concept_place;\n"
        scs_content += f"\n    <-{establishment_type};;\n"

        return scs_content

    def process_all_json_files(self):
        """Чтение всех JSON файлов в директории и создание SCS файлов"""
        json_files = [f for f in os.listdir(self.input_dir) if f.endswith('.json')]

        if not json_files:
            print(f"Нет JSON-файлов в директории {self.input_dir}.")
            return

        for json_file in json_files:
            input_filepath = os.path.join(self.input_dir, json_file)

            with open(input_filepath, 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError as e:
                    print(f"Ошибка чтения JSON из файла {json_file}: {e}")
                    continue

            if not isinstance(data, list):
                print(f"Ожидается список объектов в файле {json_file}, но получен другой формат.")
                continue

            for item in data:
                if not isinstance(item, dict):
                    print(f"Пропуск некорректного элемента в файле {json_file}: {item}")
                    continue

                filename_scs = self.transliterate_name(item['name']) + ".scs"
                scs_content = self.convert_to_scs(item)

                output_filepath = os.path.join(self.output_dir, filename_scs)
                with open(output_filepath, 'w', encoding='utf-8') as scs_file:
                    scs_file.write(scs_content)

                print(f"Файл '{filename_scs}' успешно создан из '{json_file}' в папке '{self.output_dir}'.")

