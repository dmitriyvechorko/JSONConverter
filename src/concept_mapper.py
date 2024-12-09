# импортируем стандартный модуль re
import re


class ConceptMapper:
    def __init__(self, type_mapping: dict):
        self.type_mapping = type_mapping

    def map_concept(self, name: str) -> str:
        """Определяет концепт по названию"""
        name_lower = name.lower()
        for key, concept in self.type_mapping.items():
            # Используем стандартный модуль re для поиска
            if re.search(r'\b' + re.escape(key) + r'\b', name_lower):
                return concept
        return "other"
