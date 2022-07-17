import os
import requests
import json
import base64
import sys


class InvalidRPC(BaseException):
    def __init__(self):
        self.message = 'The provided RPC url is not valid.'
        super(InvalidRPC, self).__init__(self.message)


class NodeNotSynchronized(BaseException):
    def __init__(self):
        self.message = 'The node is not fully synchronized. Provide a different url or wait for the synchronization ' \
                       'process to finish. '
        super(NodeNotSynchronized, self).__init__(self.message)


class UnsuccessfulHttpRequest(BaseException):
    def __init__(self, url, status_code):
        self.message = 'The HTTP request for {url} failed with status code {status_code}. '\
            .format(url=url, status_code=status_code)
        super(UnsuccessfulHttpRequest, self).__init__(self.message)


# print the progress on a single line
def __update_progress__(current, total):
    progress = int(current / total * 100)
    sys.stdout.write('\r {0}/{1} [{2}] {3}%'.format(current, total, '#' * progress + ' ' * (100 - progress), progress))
    sys.stdout.flush()


# check whether the node is fully synchronized or not
def __check_sync_status__(url):
    status = requests.get(url + '/status', allow_redirects=True)

    if not status.ok:
        raise UnsuccessfulHttpRequest(status.url, status.status_code)

    try:
        json_status = json.loads(status.text)
        if json_status['result']['sync_info']['catching_up'] is not False:
            raise NodeNotSynchronized
        print('Connected to {moniker} node'.format(moniker=json_status['result']['node_info']['moniker']))
    except Exception:
        raise InvalidRPC


# download the genesis JSON file
def download_genesis(url=None):
    if url is None:
        raise InvalidRPC

    __check_sync_status__(url)

    # download the first chunk, decode it and find the total number of chunks
    chunk_index = 0
    first_chunk = requests.get(url + '/genesis_chunked?chunk=0', allow_redirects=True)
    if not first_chunk.ok:
        raise UnsuccessfulHttpRequest(first_chunk.url, first_chunk.status_code)

    txt_data = first_chunk.text
    json_data = json.loads(txt_data)
    chunk_data = base64.b64decode(json_data['result']['data'])
    total_chunks = int(json_data['result']['total'])

    print('{total_chunks} chunks'.format(total_chunks=total_chunks))
    __update_progress__(chunk_index, total_chunks - 1)

    # delete the old local genesis.json file if exists
    try:
        os.remove('../../genesis.json')
    except OSError:
        pass

    # create a new genesis.json file and write the first chunk
    genesis_file = open('../../genesis.json', 'a')
    genesis_file.write(chunk_data.decode())

    # iterate through all the chunks and append them to the file
    while chunk_index + 1 < total_chunks:
        chunk_index += 1
        __update_progress__(chunk_index, total_chunks - 1)
        chunk = requests.get('{url}/genesis_chunked?chunk={chunk_no}'.format(url=url, chunk_no=str(chunk_index)),
                             allow_redirects=True)
        if not chunk.ok:
            raise UnsuccessfulHttpRequest(chunk.url, chunk.status_code)
        txt_data = chunk.text
        json_data = json.loads(txt_data)
        chunk_data = base64.b64decode(json_data['result']['data'])
        genesis_file.write(chunk_data.decode())

    # close the genesis file
    genesis_file.close()
    print('\nFinished!\n')
