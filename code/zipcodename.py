import xlrd
from collections import defaultdict
import pickle



def main():
    
    # workbook = xlrd.open_workbook('../../Statistiken/postleitzahlen.xls')
    # sheet = workbook.sheet_by_index(2)    

    # namezip = defaultdict()
    # namecode = defaultdict()
    

    # for i in range(11, 4941):
    # #for i in range(11, 15):
    #     zip = sheet.cell(i,0).value
    #     code = sheet.cell(i,2).value
    #     name = sheet.cell(i,4).value
    #     zip = int(zip)
    #     code = int(code)
    #     if code in namecode:
    #         if not name in namecode[code]: 
    #             namecode[code].append(name)
    #     else:
    #         namecode[code] = [name]
    #     if zip in namezip:
    #         if not name in namezip[zip]:
    #             namezip[zip].append(name)
    #     else:
    #         namezip[zip] = [name]

    # pickle.dump(namezip, open("../databases/namezip", "wb"))
    # pickle.dump(namecode, open("../databases/namecode", "wb")
    
    zc = 0
    cc = 0
    namezip = pickle.load(open("../databases/namezip", "rb"))
    print('namezip ', len(namezip))
    for k in namezip.keys():
        if len(namezip[k]) > 1:
            zc += 1
    print("zip count ", zc)
            
    namecode = pickle.load(open("../databases/namecode", "rb"))
    print(len(namecode))
    for k in namecode.keys():
        if len(namecode[k]) > 1:
            cc += 1
    print("code count ", cc)       
    
                
                
if __name__ == '__main__':
    main()
