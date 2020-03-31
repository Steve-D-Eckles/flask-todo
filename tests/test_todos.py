import pytest

def test_todo_list(client):
    # View the home page and check to see the header and a to-do item
    response = client.get('/')
    assert b'<h1>A simple to-do application</h1>' in response.data
    assert b'clean room' in response.data

    # Mock data should show three to-do items, one of which is complete
    assert response.data.count(b'<li class="">') == 2
    assert response.data.count(b'<li class="completed">') == 1

    # Should be able to post a new, uncompleted item to the list
    response = client.post('/', data={'new-item': 'sweep'})
    assert response.data.count(b'<li class="">') == 3
    assert b'sweep' in response.data

def test_toggle(client):
    # User should be able to post checked boxes to toggle completed status
    response = client.post('/toggle', data={'1': '1'})

    # User should be redirected to index after toggle is complete
    assert 'http://localhost/' == response.headers['Location']

    # Number of completed items on index page should be incremented
    response = client.get('/')
    assert response.data.count(b'<li class="completed">') == 2

def test_remove(client):
    # Clicking remove button should post to remove endpoint and redirect to index
    response = client.post('/remove', data={'1': '1'})
    assert 'http://localhost/' == response.headers['Location']

    # 'clean room' task should have been removed
    response = client.get('/')
    assert b'clean room' not in response.data
