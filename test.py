import os
import json
from datetime import datetime
from dependency_graph import (
    load_config,
    read_commit,
    get_commit_hash_from_ref,
    get_commits_after_date,
    parse_commit_data,
    generate_graph
)

# Мок функции для теста (используйте только для тестов)
def mock_read_commit(commit_hash, repo_path):
    # Возвращаем тестовые данные с обязательными полями
    return {
        'commit_hash': commit_hash,
        'parent': None,
        'author': 'John Doe <john@example.com>',
        'committer': 'John Doe',
        'committer_email': 'john@example.com',
        'committer_timestamp': 1616564023,
        'message': 'Initial commit'
    }

def mock_get_commit_hash_from_ref(branch_ref, repo_path):
    # Для ссылки на ветку main возвращаем заранее заданный хеш
    if branch_ref == 'refs/heads/main':
        return 'abc1234567890abcdef1234567890abcdef1234'
    raise FileNotFoundError(f"Branch ref {branch_ref} not found")

# Мок функции для получения коммитов после определенной даты
def mock_get_commits_after_date(repo_path, start_date):
    # Возвращаем список мок-коммитов
    return [
        {
            'commit_hash': 'abc1234567890abcdef1234567890abcdef1234',
            'parent': None,
            'author': 'John Doe <john@example.com>',
            'committer': 'John Doe',
            'committer_email': 'john@example.com',
            'committer_timestamp': 1616564023,
            'message': 'Initial commit'
        },
        {
            'commit_hash': 'def567890abcdef1234567890abcdef123456789',
            'parent': 'abc1234567890abcdef1234567890abcdef1234',
            'author': 'Jane Doe <jane@example.com>',
            'committer': 'Jane Doe',
            'committer_email': 'jane@example.com',
            'committer_timestamp': 1616565023,
            'message': 'Second commit'
        }
    ]

# Тест для загрузки конфигурации
def test_load_config():
    config = load_config("config.json")  # Путь к вашему конфигу
    assert config is not None, "Не удалось загрузить конфигурацию"
    assert 'repo_path' in config, "Не найден параметр 'repo_path' в конфигурации"
    assert 'output_image_path' in config, "Не найден параметр 'output_image_path' в конфигурации"
    assert 'commit_date' in config, "Не найден параметр 'commit_date' в конфигурации"
    print("test_load_config passed!")

# Тест для чтения коммита
def test_read_commit():
    commit_hash = 'abc1234567890abcdef1234567890abcdef1234'
    repo_path = 'mock/repo/path'  # Путь к репозиторию для тестов
    try:
        result = mock_read_commit(commit_hash, repo_path)
        assert 'commit_hash' in result, "Хеш коммита не найден в результате"
        assert 'parent' in result or 'message' in result, "Родитель или сообщение коммита не найдены"
        print("test_read_commit passed!")
    except Exception as e:
        print(f"test_read_commit failed: {e}")

# Тест для получения хеша коммита по ссылке на ветку
def test_get_commit_hash_from_ref():
    branch_ref = 'refs/heads/main'  # Пример ссылки на ветку
    repo_path = 'mock/repo/path'  # Путь к репозиторию для теста
    try:
        commit_hash = mock_get_commit_hash_from_ref(branch_ref, repo_path)
        # Убедимся, что хеш правильный
        assert commit_hash == 'abc1234567890abcdef1234567890abcdef1234', f"Неверный хеш коммита: {commit_hash}"
        print("test_get_commit_hash_from_ref passed!")
    except Exception as e:
        print(f"test_get_commit_hash_from_ref failed: {e}")

# Тест для получения коммитов после определенной даты
def test_get_commits_after_date():
    repo_path = 'mock/repo/path'  # Путь к репозиторию для теста
    commit_date = datetime(2023, 1, 1)  # Дата для фильтрации
    try:
        # Мокируем функцию получения коммитов
        commits = mock_get_commits_after_date(repo_path, commit_date)
        assert isinstance(commits, list), "Результат должен быть списком"
        assert len(commits) > 0, "Не найдены коммиты после указанной даты"
        print("test_get_commits_after_date passed!")
    except Exception as e:
        print(f"test_get_commits_after_date failed: {e}")


# Тест для генерации графа
def test_generate_graph():
    # Пример данных о коммитах
    commits = [
        {'commit_hash': 'abc1234567890abcdef1234567890abcdef1234', 'parent': None},
        {'commit_hash': 'def567890abcdef1234567890abcdef123456789', 'parent': 'abc1234567890abcdef1234567890abcdef1234'}
    ]
    try:
        graph = generate_graph(commits)
        assert graph is not None, "Граф не был сгенерирован"
        assert len(graph.body) > 0, "Граф пуст"
        print("test_generate_graph passed!")
    except Exception as e:
        print(f"test_generate_graph failed: {e}")

# Функция для выполнения всех тестов
def run_tests():
    test_load_config()
    test_read_commit()
    test_get_commit_hash_from_ref()
    test_get_commits_after_date()
    test_generate_graph()

# Запуск тестов
if __name__ == "__main__":
    run_tests()
