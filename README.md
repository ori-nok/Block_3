# ETL проект по обработке данных

## Структура проекта
- `src/` - исходный код ETL пайплайна
- `sql/` - аналитические SQL запросы
- `ddl/` - скрипты создания DWH схемы
- `data/` - исходные данные (положить файлы сюда)

## Запуск
1. Установить зависимости: `pip install -r requirements.txt`
2. Поместить файлы данных в папку `data/`:
   - customers.csv
   - orders.json
   - payments.csv
   - events.xml
   - products.xlsx
3. Настроить подключение к PostgreSQL в файле `src/load.py`
4. Запустить: `python src/main.py`
5. Выполнить аналитические запросы из `sql/analytics.sql`

## Результат
- Очищенные данные загружаются в staging-таблицы
- Создается DWH модель (dimensions и facts)
- Лог ошибок сохраняется в `error_log.csv`
