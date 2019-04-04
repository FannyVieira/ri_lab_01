import json

def write_in_frontier(loader):
    with open('frontier/gazeta_do_povo.json', 'a') as json_file:
        _id = loader.get_output_value('_id')
        url = loader.get_output_value('url')
        data = {_id: url}
        json.dump(data, json_file)