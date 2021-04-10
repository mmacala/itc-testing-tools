import requests
import csv
from bs4 import BeautifulSoup
def main():
    #File, Line, Error
    types = {"c_w_":"01.w_Defects", "c_wo_":"02.wo_Defects", "cpp_w_":"03.w_Defects_Cpp", "cpp_wo_":"04.wo_Defects_Cpp"}
    #70px text
    #85px vulnerability criticality - done
    #95px vulnerability type
    #380px type
    #120px file:line
    #508px or 515px or 518px vulnerability count
    #488px <discard>
    #571px <discard>
    #no text - discard
    f = open(r"C:\Users\marco\OneDrive\Dokumente\GitHub\itc-testing-tools\csv-data\smartdecscan\SmartDec_html"
             r".html", "r")
    table = {}
    findings = []
    last_criticality=''
    soup = BeautifulSoup(f.read(), 'html.parser')
    all_div = soup.find_all('div')
    for tag in all_div:
        if tag.span is not None:
            if tag['style'].find('left:85px')>0:
                last_criticality = tag.span.get_text().strip()
                if last_criticality not in table:
                    table[last_criticality]={}
                    table[last_criticality]['findings']={}
            elif tag['style'].find('left:95px')>0:
                if tag.span.get_text().strip() not in table[last_criticality]['findings']:
                    table[last_criticality]['findings'][tag.span.get_text().strip()] = {}
                    table[last_criticality]['findings'][tag.span.get_text().strip()]['entries'] = {}
            elif tag['style'].find('left:120px')>0:
                findings.append(tag.span.get_text().strip())
            elif tag['style'].find('left:508px')>0 or \
                    tag['style'].find('left:518px')>0 or \
                    tag['style'].find('left:512px')>0 or \
                    tag['style'].find('left:515px')>0:
                value = tag.span.get_text().strip()
                if value.find('*')>0:
                    for key in table:
                        if 'count' not in table[key]:
                            table[key]['count'] = value.split('*')[0]
                            break
                else:
                    #debug last two entries
                    done=False
                    for key in table:
                        for subkey in table[key]['findings']:
                            if 'count' not in table[key]['findings'][subkey]:
                                table[key]['findings'][subkey]['count'] = value
                                done=True
                                break
                        if done:
                            break
            elif tag['style'].find('left:488px')>0 or tag['style'].find('left:571px')>0:
                continue
    copiedFindings = 0
    for key in table:
        for subkey in table[key]['findings']:
            fromvalue = copiedFindings
            tovalue = copiedFindings + int(table[key]['findings'][subkey]['count'])
            copiedFindings = copiedFindings + int(table[key]['findings'][subkey]['count'])
            table[key]['findings'][subkey]['entries'] = findings[fromvalue:tovalue]
    for type in types:
        with open("..\\csv-data\\smartdecscan\\temp\\"+type+"errors_per_line.csv", 'w') as csvFile:
            fieldnames = ["File", "LineStart", "LineEnd", "Error"]
            writer = csv.DictWriter(csvFile, fieldnames, lineterminator="\n")
            writer.writeheader()
            i=0
            for key in table:
                for subkey in table[key]['findings']:
                    for entry in table[key]['findings'][subkey]['entries']:
                        if(entry.find(types[type])>=0):
                            filename = entry.split("/")[-1].split(':')[0].strip()
                            linenumber = entry.split("/")[-1].split(':')[1].strip()
                            writer.writerow({'File': filename,
                                         'LineStart': linenumber,
                                         'LineEnd': linenumber,
                                         'Error':subkey})
                            i+=1
        print(type + " " + str(i))


if __name__ == "__main__":
    main()