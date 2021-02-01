# import xlsxwriter module 
import xlsxwriter

workbook = xlsxwriter.Workbook('Example2.xlsx')
worksheet = workbook.add_worksheet()

# Start from the first cell. 
# Rows and columns are zero indexed. 
row = 0
column = 0

content = ["ankit", "rahul", "priya", "harshita",
           "sumit", "neeraj", "shivam"]
list_2 = ['1','3','5']
# iterating through content list 
for item in content:
    # write operation perform
    worksheet.write(row, column, item)

    # incrementing the value of row by one 
    # with each iteratons. 
    row += 1
row1 = 0
for item1 in list_2:
    #row1 =0
    #column = 3
    worksheet.write(row1, 1, item1)
    row1 += 1

workbook.close() 