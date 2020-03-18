import csv

def main():
    #File, Line, Error
    types = {"c_w_errors_":"01.w_Defects", "c_wo_errors_":"02.wo_Defects", "cpp_w_":"03.w_Defects_Cpp", "cpp_wo_":"04.wo_Defects_Cpp"}
    for type in types:
        with open("..\\csv-data\\checkmarx\\temp\\"+type+"errors_per_line.csv", 'w') as csvFile:
            fieldnames = ["File", "LineStart", "LineEnd", "Error"]
            writer = csv.DictWriter(csvFile, fieldnames, lineterminator="\n")
            writer.writeheader()
            i=0
            with open("..\\csv-data\\checkmarx\\temp\\itc-benchmarks-test.csv", "r") as resultsCSV:
                resultsCSV = csv.DictReader(resultsCSV, delimiter=',', quotechar="\"")
                for row in resultsCSV:
                    if(row["DestFileName"].find(types[type])>0):
                        writer.writerow({'File': row["DestFileName"].split("/")[-1].strip(), 'LineStart': row["Line"],'LineEnd': row["DestLine"], 'Error':row["ï»¿\"Query\""].strip()})
                        i+=1
        print(type + " " + str(i))


if __name__ == "__main__":
    main()