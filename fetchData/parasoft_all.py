import csv
import xml.etree.ElementTree as ET

def main():
    #File, Line, Error
    types = {"c_w_":"01.w_Defects", "c_wo_":"02.wo_Defects", "cpp_w_":"03.w_Defects_Cpp", "cpp_wo_":"04.wo_Defects_Cpp"}
    for type in types:
        with open("..\\csv-data\\parasoft_all\\temp\\"+type+"errors_per_line.csv", 'w') as csvFile:
            fieldnames = ["File", "LineStart", "LineEnd", "Error"]
            writer = csv.DictWriter(csvFile, fieldnames, lineterminator="\n")
            writer.writeheader()
            i=0

            tree = ET.parse('..\\csv-data\\parasoft_all\\report.xml')
            root = tree.getroot()
            standards = root.find('CodingStandards')
            stdviols = standards.find('StdViols')
            for child in stdviols:
                if(child.attrib["locFile"].find(types[type])>0):
                    writer.writerow({'File': child.attrib["locFile"].split("/")[-1].strip(),
                                     'LineStart': child.attrib["locStartln"],
                                     'LineEnd':child.attrib["locEndLn"],
                                     'Error':child.attrib["msg"]})
                    i+=1
        print(type + " " + str(i))


if __name__ == "__main__":
    main()