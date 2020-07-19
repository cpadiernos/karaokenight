from flask import current_app

def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    searchable_text = {}
    for field in model.__searchable__:
        searchable_text[field] = getattr(model, field)
        if isinstance(searchable_text[field], list):
            searchable_text[field] = ', '.join([str(x) for x in searchable_text[field]])
    current_app.elasticsearch.index(index=index, id=model.id, body=searchable_text)
    
def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)
    
def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
            'from': (page - 1)* per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']