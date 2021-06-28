import pandas
import pandas as pd
import src.swift_parser as sp
from datetime import datetime


startTime = datetime.now()

# # 13000
# # 42 minut
# swift_file_path = './data/SWIFT_Field_Parsing_Large.txt'
# # swift_file_path = './data/MT103_example_removed_121.txt'
# results = sp.main(file=swift_file_path, dataFrames={})
#
# print(datetime.now() - startTime)
# REF ID, SWIFT ID, FIELD, VALUE
#
# output_dict = results['103'][0]
#
# num_of_msgs_in_df = len(output_dict['1'])
# table_of_msgs = []
# for msg_index in range(num_of_msgs_in_df):
#     ref_id = output_dict['1'][msg_index]
#     transaction_id = output_dict['Transaction ID'][msg_index]
#     for key, value in output_dict.items():
#         row = []
#         row.extend([ref_id, transaction_id])
#         if key not in ['1', 'Transaction ID']:
#             row.extend([key, value[msg_index]])
#             table_of_msgs.append(row)
#
# df = pd.DataFrame(data=table_of_msgs, columns=['ref_id', 'transaction_id', 'field_name', 'field_value'])
#
# df.to_pickle('./data/output/output_dataframe.pkl')


df = pandas.read_pickle('./data/output/output_dataframe.pkl')
