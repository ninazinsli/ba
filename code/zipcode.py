import xlrd
from collections import defaultdict
import pickle



def main():
    
    # workbook = xlrd.open_workbook('../../Statistiken/postleitzahlen.xls')
    # sheet = workbook.sheet_by_index(2)    

    # codetozip = defaultdict()
    # ziptocode = defaultdict()

    # for i in range(11, 4941):
    #     zip = sheet.cell(i,0).value
    #     code = sheet.cell(i,2).value
    #     zip = int(zip)
    #     code = int(code)
    #     if code in codetozip:
    #         codetozip[code].append(zip)
    #     else:
    #         codetozip[code] = [zip]
    #     if zip in ziptocode:
    #         ziptocode[zip].append(code)
    #     else:
    #         ziptocode[zip] = [code]

    
    # pickle.dump(ziptocode, open("../databases/ziptocode", "wb"))
    # pickle.dump(codetozip, open("../databases/codetozip", "wb"))

    ziptocode = pickle.load(open("../databases/ziptocode", "rb"))
    print(len(ziptocode))

    counter = 0
    for k in ziptocode.keys():
        if len(ziptocode[k]) > 1:
            print("Zip ", k)
            print(ziptocode[k])
            counter += 1
    print("counter ", counter)   
                
                
if __name__ == '__main__':
    main()
