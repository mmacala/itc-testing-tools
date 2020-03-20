import json
import csv


def main():
    with open('..\\csv-data\\deepcode\\temp\\deepcode.json') as findings_json:
        results = json.load(findings_json)
        #File,LineStart,LineEnd,Error
        files = results["results"]["files"]
        categories = results["results"]["suggestions"]

        types = {"c_w_errors_":"01.w_Defects", "c_wo_errors_":"02.wo_Defects", "cpp_w_":"03.w_Defects_Cpp", "cpp_wo_":"04.wo_Defects_Cpp"}
        for type in types:
            with open("..\\csv-data\\deepcode\\temp\\"+type+"errors_per_line.csv", 'w') as csvFile:
                fieldnames = ["File", "LineStart", "LineEnd", "Error"]
                writer = csv.DictWriter(csvFile, fieldnames, lineterminator="\n")
                writer.writeheader()
                for filename in files:
                    if(filename.find(types[type])>0):
                        for issue in files[filename]:
                            for entry in files[filename][issue]:
                                file = filename.split("/")[-1].strip()
                                lineStart = entry["rows"][0]
                                lineEnd = entry["rows"][1]
                                error = categories[issue]["id"]
                                writer.writerow({'File': file, 'LineStart': lineStart, 'LineEnd':lineEnd,'Error':error})

if __name__ == "__main__":
    main()