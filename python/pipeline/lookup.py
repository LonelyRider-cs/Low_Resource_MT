
def lookup(arg):
    with open('../../supplemental_bible.com_info/bible_versions.tsv', 'r') as f:
        table_data = [['language', 'tag', 'local_name', 'iso_639_3', 'iso_639_1', 'family/subfamily/genus', 'index', 'bible_tag', 'version', 'language_version_id', 'default_version', 'text_direction']]
        for line in f.readlines():
            if arg in line:
                table_data.append(line.split('\t'))
                #print(line)
        for row in table_data:
            #print(row)
            print("{: >25} | {: >7} | {: >30} | {: >9} | {: >9} | {: >30} | {: >5} | {: >9} | {: >30} | {: >20} | {: >20} | {: >20}".format(*row))

def no_lookup(arg):
    with open('../../supplemental_bible.com_info/bible_versions.tsv', 'r') as f:
        table_data = [['language', 'tag', 'local_name', 'iso_639_3', 'iso_639_1', 'family/subfamily/genus', 'index', 'bible_tag', 'version', 'language_version_id', 'default_version', 'text_direction']]
        for line in f.readlines():
            if arg in line:
                return line.split('\t')[1]
