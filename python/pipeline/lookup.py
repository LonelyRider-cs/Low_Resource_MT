
def lookup(arg):
    with open('../../supplemental_bible.com_info/bible_versions.tsv', 'r') as f:
        table_data = [['language', 'tag', 'local_name', 'iso_639_3', 'iso_639_1', 'family/subfamily/genus', 'index', 'bible_tag', 'version', 'language_version_id', 'default_version', 'text_direction']]
        for line in f.readlines():
            if arg in line:
                table_data.append(line.split('\t'))
                #print(line)
        for row in table_data:
            #print(row)
            print("{: >15} | {: >7} | {: >30} | {: >9} | {: >9} | {: >30} | {: >5} | {: >9} | {: >30} | {: >20} | {: >20} | {: >20}".format(*row))
    f.close()

def no_lookup(arg):
    with open('../../supplemental_bible.com_info/bible_versions.tsv', 'r') as f:
        table_data = [['language', 'tag', 'local_name', 'iso_639_3', 'iso_639_1', 'family/subfamily/genus', 'index', 'bible_tag', 'version', 'language_version_id', 'default_version', 'text_direction']]
        for line in f.readlines():
            if arg in line:
                return line.split('\t')[1]


def wiki_lang_lookup(arg):
    with open('../../all_wikipedia_dumps/language_info/wikipedia_language_info.csv') as f:
        print('arg:' + str(arg))
        language_name = get_language_name(arg)
        print('language name:' + str(language_name))
        table_data = [['language family', 'ISO name', 'native name', '639-1', '639-2/T', '639-2/B', '639-3', 'notes']]
        for line in f.readlines():
            temp_line = line.split('\t')
            print(temp_line)
            if language_name == temp_line[1]:
                return temp_line[3]
            #if tag in line:
                #print('tag:' + str(tag))
                #print(line)
                #table_data.append(line.split('\t'))
            #for row in table_data:
                #print(row)
                #print("{: >20} | {: >15} | {: >15} | {: >2} | {: >3} | {: >3} | {: >5} | {: >50}".format(*row))
    f.close()



def get_iso_631_1(arg):
    with open('../../supplemental_bible.com_info/bible_versions.tsv', 'r') as f:
        table_data = [['language', 'tag', 'local_name', 'iso_639_3', 'iso_639_1', 'family/subfamily/genus', 'index', 'bible_tag', 'version', 'language_version_id', 'default_version', 'text_direction']]
        for line in f.readlines():
            if str(arg) in line:
                return line.split('\t')[4]

def get_language_name(arg):
    with open('../../supplemental_bible.com_info/bible_versions.tsv', 'r') as f:
        table_data = [['language', 'tag', 'local_name', 'iso_639_3', 'iso_639_1', 'family/subfamily/genus', 'index', 'bible_tag', 'version', 'language_version_id', 'default_version', 'text_direction']]
        for line in f.readlines():
            if str(arg) in line:
                return line.split('\t')[0]
