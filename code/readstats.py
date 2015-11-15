import xlrd
from collections import defaultdict
import pickle

def get_code(str):
    if str.startswith("-") or str.startswith(">>"):
        return 0
    else:
      return int(str[6:10])  


def main():
    # Einkommen
    # workbook = xlrd.open_workbook('../../Statistiken/Einkommen/17745_Durchschnittliches_Reineinkommen_pro_Kopf_2011_(de).xlsx')
    # workbook = xlrd.open_workbook('../../Statistiken/Einkommen/17731_Durchschnittliches_Reineinkommen_pro_Steuerpflichtigem_r_2011_(de).xlsx')
    
    # Bevölkerung
    # workbook = xlrd.open_workbook('../../Statistiken/17024_Staendige_Wohnbevoelkerung_2013_(de).xlsx')
    # workbook= xlrd.open_workbook('../../Statistiken/Staatsangehörigkeit_Geschlecht_nach_Gemeinden.xls')
    # workbook= xlrd.open_workbook('../../Statistiken/5921_Sozialer_Status_in_der_Schweiz_2000_(de).xlsx')
    workbook= xlrd.open_workbook('../../Statistiken/5941_Individualisierung_in_der_Schweiz_2000_(de).xlsx')
    # workbook= xlrd.open_workbook('../../Statistiken/17687_Bezueger_von_Sozialhilfeleistungen_Sozialhilfeempfaenger_2013_(de).xls')
    
    # Sprache
    # workbook= xlrd.open_workbook('../../Statistiken/Sprache/3007_Vorherrschende_Landessprachen_in_den_Gemeinden_2000_(de).xlsx')
    # workbook= xlrd.open_workbook('../../Statistiken/Sprache/3013_Wohnbevoelkerung_mit_Hauptsprache_Spanisch_2000_(de).xlsx')
    # workbook= xlrd.open_workbook('../../Statistiken/Sprache/3014_Wohnbevoelkerung_mit_Hauptsprache_Portugiesisch_2000_(de).xlsx')
    # workbook= xlrd.open_workbook('../../Statistiken/Sprache/5946_Fremdsprachigkeit_in_der_Schweiz_2000_(de).xlsx')
    # workbook= xlrd.open_workbook('../../Statistiken/Sprache/3015_Fremdsprachigkeit_in_der_Schweiz_2000_(de).xlsx')

    # Alter
    # workbook= xlrd.open_workbook('../../Statistiken/Alter/5944_Alterung_in_der_Schweiz_2000_(de).xlsx')
    # workbook= xlrd.open_workbook('../../Statistiken/Alter/17044_Staendige_Wohnbevoelkerung_unter_20_Jahren_2013_(de).xlsx')
    # workbook= xlrd.open_workbook('../../Statistiken/Alter/17048_Staendige_Wohnbevoelkerung_im_Alter_von_20_bis_39_Jahren_2013_(de).xlsx')
    # workbook= xlrd.open_workbook('../../Statistiken/Alter/17051_Staendige_Wohnbevoelkerung_im_Alter_von_40_bis_64_Jahren_2013_(de).xlsx')
    # workbook= xlrd.open_workbook('../../Statistiken/Alter/17057_Staendige_Wohnbevoelkerung_im_Alter_von_65_und_mehr_Jahren_2013_(de).xlsx')
    # workbook= xlrd.open_workbook('../../Statistiken/Alter/17063_Jugendquotient_2013_(de).xlsx')
    # workbook= xlrd.open_workbook('../../Statistiken/Alter/17066_Altersquotient_2013_(de).xlsx')

    # Kriminalität
    # workbook = xlrd.open_workbook('../../Statistiken/Kriminalität/17885_Strafgesetzbuch_StGB_Haeufigkeitszahl_der_Straftaten_2014_(de).xlsx')
    # workbook = xlrd.open_workbook('../../Statistiken/Kriminalität/16548_Betaeubungsmittelgesetz_BetmG_Haeufigkeitszahl_der_Straftaten_2013_(de).xlsx')
    # workbook = xlrd.open_workbook('../../Statistiken/Kriminalität/16551_Auslaendergesetz_AuG_Haeufigkeitszahl_der_Straftaten_2013_(de).xlsx')

    # Wirtschaftssektor
    # workbook = xlrd.open_workbook('../../Statistiken/Wirtschaftssektor/16946_Beschaeftigte_im_1._Wirtschaftssektor_2012_(de).xlsx')
    # workbook = xlrd.open_workbook('../../Statistiken/Wirtschaftssektor/16949_Beschaeftigte_im_2._Wirtschaftssektor_2012_(de).xlsx')
    # workbook = xlrd.open_workbook('../../Statistiken/Wirtschaftssektor/16952_Beschaeftigte_im_3._Wirtschaftssektor_2012_(de).xlsx')
    
    
    sheet = workbook.sheet_by_index(0)

    # womandict = {}
    # mandict = {}
    # foreignerdict = {}
    dict = {}

    for i in range(6, 2402):
        code = int(sheet.cell(i,0).value)
        index = sheet.cell(i,2).value
        if index == 'X':
            index = 0
        index = int(index)
        dict[code] = index
    
    # for i in range(6, 2402):
    #     code = get_code(sheet.cell(i,0).value)
    #     if code:
    #         foreign = int(sheet.cell(i,2).value)
    #         man = int(sheet.cell(i,2).value)
    #         woman = int(sheet.cell(i,2).value)
    #         foreignerdict[code] = foreign
    #         mandict[code] = man
    #         womandict[code] = woman

    #print(dict)
    #pickle.dump(dict, open("../databases/stat[code]pop", "wb"))
    # pickle.dump(foreignerdict, open("../databases/stat[code]foreign", "wb"))
    # pickle.dump(mandict, open("../databases/stat[code]man", "wb"))
    # pickle.dump(womandict, open("../databases/stat[code]woman", "wb"))
    # pickle.dump(dict, open("../databases/stat[code]lang", "wb"))
    pickle.dump(dict, open("../databases/stat[code]sozialhilfe", "wb"))
                
if __name__ == '__main__':
    main()
