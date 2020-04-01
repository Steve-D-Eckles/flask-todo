import pytest

def test_todo_list(client, auth):
    auth.login()
    # View the home page and check to see the header and a to-do item
    response = client.get('/')
    assert b'<h1>A simple to-do application</h1>' in response.data
    assert b'clean room' in response.data

    # Mock data should show three to-do items, one of which is complete
    assert response.data.count(b'<li class="">') == 2
    assert response.data.count(b'<li class="completed">') == 1

def test_new_item(client, auth):
    auth.login()
    # Should be able to post a new, uncompleted item with the route new-todo
    response = client.post('/new-todo', data={'new-item': 'sweep'})

    # User should be redirected to index after new-item is complete
    assert 'http://localhost/' == response.headers['Location']

    response = client.get('/')
    # Number of uncompleted items on index page should be incremented
    assert response.data.count(b'<li class="">') == 3
    assert b'sweep' in response.data

def test_toggle(client, auth):
    auth.login()
    # User should be able to post checked boxes to toggle completed status
    response = client.post('/toggle', data={'1': '1'})

    # User should be redirected to index after toggle is complete
    assert 'http://localhost/' == response.headers['Location']

    # Number of completed items on index page should be incremented
    response = client.get('/')
    assert response.data.count(b'<li class="completed">') == 2

def test_remove(client,auth):
    auth.login()
    # Clicking remove button should post to remove endpoint and redirect to index
    response = client.post('/remove', data={'1': '1'})
    assert 'http://localhost/' == response.headers['Location']

    # 'clean room' task should have been removed
    response = client.get('/')
    assert b'clean room' not in response.data

def test_filter(client, auth):
    auth.login()
    # View the home page and check to see a button with a value of completed
    response = client.get('/')
    assert b'<button name="filter" value="completed" type="submit">Completed</button>' in response.data
    # Go to home page and filter the items to just show completed
    response = client.post('/', data={'filter': 'completed'})

    # Show that the data only has completed items
    assert response.data.count(b'<li class="completed">') == 1
    assert response.data.count(b'<li class="">') == 0
