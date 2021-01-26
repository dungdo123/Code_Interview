# import json
#
# json_path = 'box_dataset_by_hand\mask_definitions.json'
#
# def renameKey(iterable, oldkey, newkey):
#     if type(iterable) is dict:
#         for key in iterable.keys():
#             if key == oldkey :
#                 iterable[newkey] = iterable.pop(key)
#     return iterable
#
# with open(json_path) as f:
#     data = json.load(f)
# # new_string = json.dumps(data, indent=2)
# # print(new_string)
# print(type(data["masks"]))
# i = 0
# for image in data["masks"]:
#     i = i + 1
#
#     new_json = json.dumps(renameKey(data["masks"], image, str(i)))
# print(new_json)
#
# # # init list
# # ini_list_1 = ["a", "b", "c", "d"]
# # ini_list_2 = ["1", "2", "3", "4"]
# # final_data_1 = dict(zip(ini_list_1, list(data["masks"].values())))
# # print(final_data_1)
#

import json

def write_json(data, filename = 'mask_definitions.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

with open('new_dataset/img_set_1/mask_definitions.json') as json_1:
    mask_1 = json.load(json_1)
    temp_1 = mask_1['masks']

with open('new_dataset/img_set_2/mask_definitions.json') as json_2:
    mask_2 = json.load(json_2)
    temp_2 = mask_2['masks']

temp_1.update(temp_2)
write_json(mask_1)