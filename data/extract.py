from tqdm.auto import tqdm
import requests
import zipfile
import tarfile
import argparse
import shutil
import os
import glob


argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('-u', '--url', help='Zipped data URL', required=True)
argument_parser.add_argument('-t', '--type', help='Data type', required=True)
argument_parser.add_argument('-e', '--extension', help='File extension for export', default='png')
argument_parser.add_argument('-l', '--limiter', help='File name limiter', default=None)

_current_path = os.getcwd()
_tmp = _current_path + '\\tmp\\'

def clear(path, temp=True):
    print('Cleaning up temporary files...')
    if temp and os.path.exists(_tmp):
        shutil.rmtree(_tmp)

    if os.path.exists(path):
        for folder in glob.glob(f'{path}*\\'):
            shutil.rmtree(folder)


def move(path, extension, limiter):
    print('Moving and filtering files...')
    for filename in glob.iglob(f'{path}**\\*.{extension}', recursive=True):
        if limiter in filename or limiter is None:
            os.replace(filename, path + filename.split('\\')[-1])

def extract_zip(path_zip, path_extract):
    with zipfile.ZipFile(path_zip, 'r') as _zip:
        for element in tqdm(_zip.infolist(), desc=f'Extracting {path_zip}'):
            _zip.extract(element, path_extract)

def extract_tar(path_tar, path_extract):
    with tarfile.open(path_tar, 'r:gz') as _tar:
        for element in tqdm(iterable=_tar.getmembers(), total=len(_tar.getmembers()), desc=f'Extracting {path_tar}'):
            _tar.extract(member=element, path=path_extract)

def download(url):
    if not os.path.exists(_tmp):
        os.mkdir(_tmp)

    _filename = _tmp + url.split('/')[-1]
    _response = requests.get(url, stream=True)
    with tqdm.wrapattr(open(_filename, "wb"), "write", miniters=1, total=int(_response.headers.get('content-length', 0)), desc=f'Downloading {_filename}') as _content:
        for chunk in _response.iter_content(chunk_size=4096):
            _content.write(chunk)

    return _filename

if __name__ == '__main__':
    _args = vars(argument_parser.parse_args())
    _url  = _args['url']
    _type = _args['type']
    _ext  = _args['extension']
    _lim  = _args['limiter']

    if "'" in _lim:
        _lim = _lim.replace("'", '')

    try:
        _path = f'{_current_path}\\{_type}\\'
        _zip = download(_url)
        extract_zip(_zip, _path)

        for filename in glob.iglob(f'{_path}**\\*.tar.gz', recursive=True):
            extract_tar(filename, _path)

        move(_path, _ext, _lim)
        clear(_path)
        
        print('Creation of the finished image set!')
    except Exception as e:
        print(f'Error: {e}')