# Importing the pandas library as pd
import pandas as pd

# List of Ayah numbers with their corresponding lengths
ayah_numbers = ['01;148', '02;111', '03;126', '04;131', '05;124', '06;110', '07;149', '08;142', '09;159', '10;127', '11;151', '12;170', '13;154', '14;227', '15;185', '16;269', '17;190', '18;202', '19;339', '20;171', '21;178', '22;169', '23;357', '24;175', '25;246', '26;195', '27;399', '28;137', '29;431', '30;564']
# List of Surah numbers with their corresponding lengths
surah_numbers = ['1;7','2;286','3;200','4;176','5;120','6;165','7;206','8;75','9;129','10;109','11;123','12;111','13;43','14;52','15;99','16;128','17;111','18;110','19;98','20;135','21;112','22;78','23;118','24;64','25;77','26;227','27;93','28;88','29;69','30;60','31;34','32;30','33;73','34;54','35;45','36;83','37;182','38;88','39;75','40;85','41;54','42;53','43;89','44;59','45;37','46;35','47;38','48;29','49;18','50;45','51;60','52;49','53;62','54;55','55;78','56;96','57;29','58;22','59;24','60;13','61;14','62;11','63;11','64;18','65;12','66;12','67;30','68;52','69;52','70;44','71;28','72;28','73;20','74;56','75;40','76;31','77;50','78;40','79;46','80;42','81;29','82;19','83;36','84;25','85;22','86;17','87;19','88;26','89;30','90;20','91;15','92;21','93;11','94;8','95;8','96;19','97;5','98;8','99;8','100;11','101;11','102;8','103;3','104;9','105;5','106;4','107;7','108;3','109;6','110;3','111;5','112;4','113;5','114;6']

# CSV file containing translations data
file_name = 'en-all-translations-tanzil.csv'
#Read translation data into a DataFrame
df = pd.read_csv(file_name)

# Initialization of variables
start = 1
ayah_list = []

# Loop through each Ayah number
for idx, ayah_item in enumerate(ayah_numbers):
    # Split the Ayah item into Ayah number and length
    line_split = ayah_item.split(';')
    ayah_num = idx +1
    if idx == 0:
        # For the first Ayah, set start, end, and length
        ayah_number = int(line_split[0])
        ayah_len = int(line_split[1 ])
        line_start = start
        line_end = line_start + ayah_len
        ayah_list.append([ayah_num,line_start,line_end,ayah_len])
    else:
        # For subsequent Ayahs, update start, end, and length
        ayah_number = int(line_split[0])
        ayah_len = int(line_split[1])
        line_start = line_end
        line_end = line_start + ayah_len
        ayah_list.append([ayah_num,line_start,line_end,ayah_len])

# Create a DataFrame from the Ayah list
df_ayah = pd.DataFrame(ayah_list, columns=['Ayah_Number','Ayah_Start','Ayah_end','Juz_length'])


# Initialize a list to store Ayah-Juz associations
df_ayah_juz_list = []
for i in ayah_list:
    start_x = i[1]
    end_x = i[2]
    # Create associations between Ayahs and Juz numbers
    for ayah_number in range(start_x,end_x):
        df_ayah_juz_list.append([ayah_number, i[0], i[3]])

# Create a DataFrame from the Ayah-Juz list
df_ayah_juz_ = pd.DataFrame(df_ayah_juz_list, columns=['Ayah_Number', 'Juz_Number','Juz_length'])
# Save the Ayah-Juz DataFrame to a CSV file
df_ayah_juz_.to_csv('Ayah_Juz.csv',index=None)

# Similar process for Surahs
surah_list = []
for idx, ayah_item in enumerate(surah_numbers):
    # Split the Surah item into Surah number and length
    line_split = ayah_item.split(';')
    ayah_num = idx +1
    if idx == 0:
        # For the first Surah, set start, end, and length
        ayah_number = int(line_split[0])
        ayah_len = int(line_split[1 ])
        line_start = start
        line_end = line_start + ayah_len
        surah_list.append([ayah_num,line_start,line_end,ayah_len])
    else:
        ayah_number = int(line_split[0])
        ayah_len = int(line_split[1])
        line_start = line_end
        line_end = line_start + ayah_len
        surah_list.append([ayah_num,line_start,line_end,ayah_len])

# Create a DataFrame from the Surah list
df_surah = pd.DataFrame(surah_list, columns=['Surah_Number','Surah_Start','Surah','Surah_Length'])

# Initialize a list to store Surah-Juz associations
df_surah_juz_list = []
for i in surah_list:
    start_x = i[1]
    end_x = i[2]
    # Create associations between Ayahs and Juz numbers
    for ayah_number in range(start_x,end_x):
        df_surah_juz_list.append([ayah_number, i[0], i[3]])

# Create a DataFrame from the Surah-Juz list
df_surah_juz_ = pd.DataFrame(df_surah_juz_list, columns=['Ayah_Number', 'Surah_Number','Surah_Length'])
#Save Ayah Surah DataFrame
df_surah_juz_.to_csv('Ayah_Surah.csv',index=None)
# Merge the Surah-Juz and Ayah-Juz DataFrames on Ayah number
ayah_juz_surah = pd.merge(df_surah_juz_,df_ayah_juz_,on = 'Ayah_Number')

# Merge the Ayah-Juz-Surah DataFrame with the original Translations DataFrame
df_new = pd.merge(df,ayah_juz_surah, on='Ayah_Number')

#Save the result to a CSV file
df_new.to_csv('En-all-Ayah.csv',index=None)
df_new.set_index('Ayah_Number').to_json(f'En-all-Ayah.json', orient='index')


en_tanzil_list = ['en-ahmedali-tanzil', 'en-ahmedraza-tanzil','en-arberry-tanzil', 'en-daryabadi-tanzil', 'en-hilali-tanzil',
       'en-itani-tanzil', 'en-maududi-tanzil', 'en-mubarakpuri-tanzil','en-pickthall-tanzil', 'en-qarai-tanzil', 'en-qaribullah-tanzil',
       'en-rwwad-quranenc', 'en-saheeh-quranenc', 'en-sahih-tanzil','en-sarwar-tanzil', 'en-shakir-tanzil', 'en-wahiduddin-tanzil','en-yusufali-tanzil']
Juz_Number_list = df_new['Juz_Number'].unique().tolist()
Surah_Number_list = df_new['Surah_Number'].unique().tolist()

juz_number_dict = {}
for juz_number in Juz_Number_list:
    juz_number_dict[juz_number] = {}
    for tanzil in en_tanzil_list:
        juz_text = " ".join(df_new[df_new['Juz_Number'] == juz_number][tanzil].tolist())
        juz_number_dict[juz_number][tanzil] = juz_text

surah_number_dict = {}
for surah_number in Surah_Number_list:
    surah_number_dict[surah_number] = {}
    for tanzil in en_tanzil_list:
        surah_text = " ".join(df_new[df_new['Surah_Number'] == surah_number][tanzil].tolist())
        surah_number_dict[surah_number][tanzil] = surah_text

df_juz = pd.DataFrame.from_dict(juz_number_dict).transpose().reset_index().rename(columns={'index':'Juz_Number'})
df_surah = pd.DataFrame.from_dict(surah_number_dict).transpose().reset_index().rename(columns={'index':'Surah_Number'})

df_juz.to_csv('En-all-Juz.csv',index=None)
df_juz.set_index('Juz_Number').to_json(f'En-all-Juz.json', orient='index')

df_surah.to_csv('En-all-Surah.csv',index=None)
df_surah.set_index('Surah_Number').to_json(f'En-all-Surah.json', orient='index')