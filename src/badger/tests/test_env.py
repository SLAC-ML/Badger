def test_find_env():
    from badger.factory import list_env, get_env

    assert len(list_env()) == 1

    _, configs = get_env('test')
    assert configs['name'] == 'test'
    assert configs['version'] == '1.0'
