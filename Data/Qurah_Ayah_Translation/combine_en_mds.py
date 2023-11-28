
import pandas as pd
import os


def parse_markdown_quran(file_name):
    """
    Parses a markdown file containing Quranic verses and returns a dictionary with ayah numbers as keys and text as values.

    Parameters:
    - file_name (str): The name of the markdown file.

    Returns:
    - dict: A dictionary with ayah numbers as keys and text as values.
    """
    # Extracting the actual name of the file without the extension
    file_actual_name = file_name.split('.')[0]
    # Initializing an empty dictionary to store the parsed data
    data = {file_actual_name: {}}
    # Setting the encoding for reading the file
    enc = 'utf-8'
    # Opening the file using the full path
    quran_eng_1 = open(f'{folder_path}/{file_name}','r', encoding=enc)
    # Initializing variables to track line number, starting point, and ayah number
    line_start = 0
    ayah_number = 1
    # Iterating through each line in the file
    for line_number, line in enumerate(quran_eng_1.readlines()):
        line = line.strip().rstrip().lstrip()
        # Checking for the starting line of the verses
        if line == '# 1':
            line_start = line_number
        if ((line_start != 0) and (line != '') and not line.startswith('# ') and not (line.startswith('['))):
            # Adding the ayah text to the dictionary
            data[file_actual_name][ayah_number] = line
            ayah_number += 1
    # Closing the file
    quran_eng_1.close()
    return(data)

def combine_markdown(list_ayah_markdowns):
    """
    Combines multiple Quranic translations from markdown files into a single DataFrame.

    Parameters:
    - list_ayah_markdowns (list): List of markdown file names.

    Returns:
    - pd.DataFrame: Combined DataFrame with each translation as a column.
    """
    # Iterating through each file in the list
    for file_number, file_name in enumerate(list_ayah_markdowns):
        file_name = str(file_name.strip())
        # Checking if it's the first file
        if file_number == 0:
            # Parsing the data from the first file
            master_dict = parse_markdown_quran(file_name)
            # Creating a DataFrame from the parsed data
            master_df = pd.DataFrame.from_dict(master_dict)
            # Deleting the dictionary to free up memory
            del master_dict
        else:
            # Parsing the data from subsequent files
            temp_data = parse_markdown_quran(file_name)
            # Creating a DataFrame from the parsed data
            temp_data = pd.DataFrame.from_dict(temp_data)
            # Concatenating the new DataFrame to the master DataFrame
            master_df = pd.concat([master_df,temp_data],axis=1)
    # Deleting the temporary data DataFrame to free up memory
    del temp_data
    return(master_df)

def main():
    # Find the folder where the file is located
    current_file_path = os.path.abspath(__file__)
    global folder_path
    # Find and set the folder path
    folder_path = os.path.dirname(current_file_path)
    # List of Quranic translations in markdown files

    eng_ayah_md = ['en-ahmedali-tanzil.md'
    ,'en-ahmedraza-tanzil.md'
    ,'en-arberry-tanzil.md'
    ,'en-daryabadi-tanzil.md'
    ,'en-hilali-khan-quranenc.md'
    ,'en-hilali-tanzil.md'
    ,'en-itani-tanzil.md'
    ,'en-maududi-tanzil.md'
    ,'en-mubarakpuri-tanzil.md'
    ,'en-pickthall-tanzil.md'
    ,'en-qarai-tanzil.md'
    ,'en-qaribullah-tanzil.md'
    ,'en-rwwad-quranenc.md'
    ,'en-saheeh-quranenc.md'
    ,'en-sahih-tanzil.md'
    ,'en-sarwar-tanzil.md'
    ,'en-shakir-tanzil.md'
    ,'en-wahiduddin-tanzil.md'
    ,'en-yusufali-tanzil.md']
    
    # Combine translations into a master DataFrame and remove unwanted column
    master_df = combine_markdown(eng_ayah_md).drop(['en-hilali-khan-quranenc'], axis= 1).dropna()
    # Cleanse special characters from the DataFrame
    for column in master_df.columns:
        master_df[column] = master_df[column].str.replace("“","")
        master_df[column] = master_df[column].str.replace("”","")
        master_df[column] = master_df[column].str.replace('"',"")
    
    #Set Index to Ayah Number
    master_df = master_df.reset_index().rename(columns = {'index':'Ayah_Number'})
    #Export CSV
    master_df.to_csv(f'{folder_path}/en-all-translations-tanzil.csv',index=None)

    master_df.set_index('Ayah_Number').to_json(
        f'{folder_path}/en-all-translations-tanzil.json'
        , orient='index'
    )

if __name__ == "__main__":
    main()