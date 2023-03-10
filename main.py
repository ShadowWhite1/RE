from pprint import pprint
import csv
import re

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


header = contacts_list[0]
contacts_list_clean = [header]

for item in contacts_list[1:]:
    if item[0] != '' and item[1] != '' and item[2] != '':
        contacts_list_clean.append(item)
    else:
        full_name = ' '.join(item[0:3]).strip()
        rest_of_item = item[3:]

        full_name_divided = re.split('\s+', full_name)

        
        if len(full_name_divided) == 3:
            pass
        else:
            full_name_divided.append('')

        full_raw = full_name_divided + rest_of_item

        contacts_list_clean.append(full_raw)


for item in contacts_list_clean:
    phone_pattern = '(\+7|8)(\s*)(\(?)(\d{3})(\)?)(\s*)(\-*)(\d{3})(-*)(\d{2})(-*)(\d{2})(\s*)(\(?)(\s?(доб)?)(\.?)(\s*)(\d*)(\)?)'
    find_phone = re.findall(phone_pattern, item[5])
    clean_phone = re.sub(phone_pattern, r'+7(\4)\8-\10-\12\13\15\17\19', item[5])

    item[5] = clean_phone


contacts_list_clean_search = contacts_list_clean.copy()


contacts_list_clean_search[0].append('search_name_field')

i = 1
for item in contacts_list_clean_search[i:]:
    search_name = ' '.join(item[0:3]).strip()
    contacts_list_clean_search[i].append(search_name)
    i += 1

contacts_list_clean_no_dub = [header]

j = 0
for item in contacts_list_clean_search[1:]:
    j += 1
    k = 0
    for another_item in contacts_list_clean_no_dub:

        
        if contacts_list_clean_search[j][-1] not in contacts_list_clean_no_dub[k][-1]:
            k += 1
            if k == len(contacts_list_clean_no_dub):
                contacts_list_clean_no_dub.append(item)
                break

        
        else:
            for index, yet_another_item in enumerate(another_item[0:7]):
                if yet_another_item == '' and contacts_list_clean_search[j][index] != '':
                    another_item[index] = contacts_list_clean_search[j][index]
            break


for item in contacts_list_clean_no_dub:
    del item[7]

pprint(contacts_list_clean_no_dub)

with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list_clean_no_dub)