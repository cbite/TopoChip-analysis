import re
def checkNumberChip(chip_number_file_name,data_frame,column_name):
    # first translate the chip number in a file name to an integer
    number=re.findall(r'\d+',chip_number_file_name)
    # remove the leading zero (so 01 to 1)
    leading_zero_removed=[number_chip.lstrip("0") for number_chip in number]
    leading_zero_removed=int(leading_zero_removed[0])
    print(column_name)
    chip_number_in_data_frame=data_frame[column_name][0]
    if chip_number_in_data_frame == leading_zero_removed:
        return data_frame
    else:
        print("Chip number in data is not correct")
        data_frame[column_name]=leading_zero_removed
        print("Chip number has been corrected")
        return data_frame
