import pandas as pd
import os
import sys


def main(save_to_file):
    location = os.getcwd() # get present working directory location here
    counter = 0 #keep a count of all files found

    #loop through all directories within /text
    for root_file in os.listdir(location+"/text"):
        #loop through all wiki dump files in /text subdirectory
        for file in os.listdir(location+"/text/"+root_file):
            try:
                #if file is found say so in command line and proceed to convert json data
                if file.startswith("wiki_"):
                    print("wiki dump file found:\t" + str(file))
                    temp_json_file = "text/"+root_file+"/"+file
                    converter(temp_json_file, save_to_file)
                    counter = counter+1
            except Exception as e:
                raise e
                print("No files found here!")
    print("Total files found and converted:\t" + str(counter))


def converter(json_file, save_to_file):
    #open file and append what we find
    f = open(save_to_file, "a")
    #get pandas dataframe
    pd_obj = pd.read_json(json_file, lines=True)
    #iterate through pandas dataframe
    for index, row in pd_obj.iterrows():
        #print("text:\t:" + str(row['text']))
        temp_row = row['text'].split('\n')
        # after splitting by new line, iterate through all substrings
        for i in range(0,len(temp_row)):
            #if i==0 then we know we are reading the title so no checks need to be made
            if i == 0:
                f.write(str(temp_row[i])+"\n")
            #everything else needs to be cleaned
            else:
                #split sentences on periods
                temp_texts = temp_row[i].split('.')
                #strings are cleaned and appended to file
                for text in temp_texts:
                    if text == '':
                        continue
                    elif text[0] == '\xa0' or text[0] == ' ':
                        f.write(str(text[1:])+".\n")
                    else:
                        f.write(str(text)+".\n")
    print("Transfer completed")

if __name__ == '__main__':

    save_to_file = sys.argv[1][:-3]+"txt"
    #if our save_to_file already exists want to delete and start with a blank document
    if os.path.isfile(save_to_file):
        os.remove(save_to_file)

    main(save_to_file)
