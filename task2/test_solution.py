import requests
from task2.solution import count_first_letters, fetch_category_members
from unittest.mock import Mock, patch


def test_count_first_letters():
    titles = ['Акула', 'Бегемот', 'Волк', 'Гепард', 'Горилла']
    result = count_first_letters(titles)
    assert result == {'А': 1, 'Б': 1, 'В': 1, 'Г': 2}


@patch('requests.Session.get')
def test_fetch_category_members(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        'query': {
            'categorymembers': [
                {'title': 'Акула'},
                {'title': 'Бегемот'},
                {'title': 'Волк'},
                {'title': 'Гепард'},
                {'title': 'Горилла'}
            ]
        }
    }
    mock_get.return_value = mock_response

    session = requests.Session()
    titles = fetch_category_members('Животные по алфавиту', session)
    assert len(titles) == 5
    assert 'Акула' in titles
