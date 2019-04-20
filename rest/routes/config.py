BASE_URL = '/api/v1'


def setup_routes(app, handler):
    router = app.router
    h = handler
    router.add_get(BASE_URL + '/getAll', h.get_all)
    router.add_get(BASE_URL + '/getByUrl', h.get_by_url)
    router.add_get(BASE_URL + '/getById', h.get_by_id)
    router.add_post(BASE_URL + '/add', h.insert_url)
    router.add_put(BASE_URL + '/update', h.update_url)
    router.add_delete(BASE_URL + '/deleteById', h.delete_by_id)
    router.add_delete(BASE_URL + '/deleteByUrl', h.delete_by_url)
