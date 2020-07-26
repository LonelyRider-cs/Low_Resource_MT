import requests
import bz2

def dump_downloader(url, tag):

    r = requests.get(url, stream = True)

    with open('../../all_wikipedia_dumps/' + str(tag) + '_latest.xml.bz2',"wb") as f:
        for chunk in r.iter_content(chunk_size=1024):

             # writing one chunk at a time to pdf file
             if chunk:
                 f.write(chunk)


def bz2_to_xml(file, tag):
    newfilepath = '../../all_wikipedia_dumps/' + str(tag) + '_latest.xml'
    with open(newfilepath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
        for data in iter(lambda : file.read(100 * 1024), b''):
            new_file.write(data)
