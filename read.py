#!/usr/local/bin/python
###!C:\Users\a\AppData\Local\Programs\Python\Python38

ERROR_LOG = 300
ERROR_MESSAGE = {300: "No error.", 301:"Could not open the file.", 302:"Error in content.", 303:"Searched value wasn't found.", 304:"Empty separator.", 305:"Separator must be only one char.", 306:"Begin and End cannot be empty char."}

# Read a CSV file
# - search_value: string if wanted a specific line
# - search_column: the number in which the column will be
# - search_return = n: 
#   - n > 0: how many lines with the value is wanted (from the first one to the last)
#   - n = -1: all the lines with the value
def readFile(file_name, file_directory='', search_value="", search_column=1, search_return=1):
    global ERROR_LOG
    ERROR_LOG = 300
    try:
        file_var  = open(file_directory + file_name, 'r')
    except:
        ERROR_LOG = 301
        return False
    

    table = []
    file_content = file_var.read().split('\n')
    file_var.close()
    
    separator = get_separator(file_name, file_directory) 
    if separator == False:
        return False

    if search_value == '':
        for i in file_content:
            if i != '\n' and i != '':
                table.append(i.split(separator))
    else:
        for i in file_content:
            search_line = i.split(separator)
            if len(search_line) >= search_column:
                if search_line[search_column-1] == search_value:
                    table.append(search_line)                                        
                    if search_return != -1:
                        search_return -= 1
                        if search_return == 0:
                            break
    # If not empty    
    if len(table) > 0: 
        return table
    else:
        if search_value == '':
            ERROR_LOG = 302
        else:
            ERROR_LOG = 303

        return False


def writeFile(content, file_name, file_directory='', append=True, separator=','):
    global ERROR_LOG
    ERROR_LOG = 300

    if append == True:
        open_mode = 'a'
        temp_separator = get_separator(file_name, file_directory)

        if temp_separator == False:
            if ERROR_LOG == 301:
                open_mode = 'w'
                ERROR_LOG = 300        
            else:
                return False
        else:
            separator = temp_separator
    else:
        open_mode = 'w'

    try:
        file_var = open(file_directory + file_name, open_mode)
    except:
        ERROR_LOG = 301
        return False

    if open_mode == 'w':
        file_var.write( str("separator=" + str(separator) + "\n") )
        for i in content:
            for j in range(0, len(i)):
                file_var.write(i[j])              
                if j < len(i)-1:
                    file_var.write( str(separator) )

            file_var.write('\n')
    else:
        for i in content:
            for j in range(0, len(i)):
                file_var.write(i[j])              
                if j < len(i)-1:
                    file_var.write( str(separator) )

            file_var.write('\n')

    file_var.close()
    return True

def remove_value(file_name, file_directory, value, column):

    table = readFile(file_name, file_directory)

    for i in range(0, len(table) ):
        if table[i][column] == value:
            del table[i]
            break
    
    writeFile(table, file_name, file_directory)

def get_separator(file_name, file_directory):
    global ERROR_LOG
    ERROR_LOG = 300
    try:
        file_var = open(file_directory + file_name, 'r')
    except:
        ERROR_LOG = 301
        return False

    first_line = file_var.readline()
    file_var.close()
    first_line = first_line.replace(' ', '')
    first_line = first_line.replace('\n', '')

    if "separator=" == first_line[0:10]:
        try:
            separator = str(first_line.split('=')[1])
            if len(separator) > 1:
                ERROR_LOG = 305
                file_var.close()
                return False
        except:
            ERROR_LOG = 304
            file_var.close()
            return False
    else:
        separator = ','
    
    return separator
    
if __name__ == "__main__":
    print("MAIN")
    pass
