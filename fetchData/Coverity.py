import csv

def main():
    #File, Line, Error
    types = {"c_w_":"01.w_Defects", "c_wo_":"02.wo_Defects", "cpp_w_":"03.w_Defects_Cpp", "cpp_wo_":"04.wo_Defects_Cpp"}
    for type in types:
        with open("..\\csv-data\\coverity\\temp\\"+type+"errors_per_line.csv", 'w') as csvFile:
            fieldnames = ["File", "LineStart", "LineEnd", "Error"]
            writer = csv.DictWriter(csvFile, fieldnames, lineterminator="\n")
            writer.writeheader()
            i=0
            with open("..\\csv-data\\coverity\\Coverity_Export.csv", "r") as resultsCSV:
                resultsCSV = csv.DictReader(resultsCSV, delimiter=',', quotechar="\"")
                for row in resultsCSV:
                    if(row["File"].find(types[type])>0):
                        writer.writerow({'File': row["File"].split("/")[-1].strip(), 'LineStart': row["Line Number"],
                                         'LineEnd': row["Line Number"], 'Error':row["Type"].strip()})
                        i+=1
        print(type + " " + str(i))


if __name__ == "__main__":
    main()