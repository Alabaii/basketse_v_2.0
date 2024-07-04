import json

import pandas as pd


# Функция для преобразования Excel в JSON
def excel_to_json(excel_file, json_file):
    # Читаем Excel файл
    df = pd.read_excel(excel_file)
    
    # Преобразуем DataFrame в словарь
    data = df.to_dict(orient='records')
    
    # Записываем данные в JSON файл
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Пример использования
if __name__ == "__main__":
    excel_file = 'C:/work/basketse_v_2.0/app/api-refs.xlsx'
    json_file = 'output_file.json'
    excel_to_json(excel_file, json_file)
    