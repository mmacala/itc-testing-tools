import requests
import csv
import json

token="3e6978bcbc40b5d4aa0473e986cfaf6d79d1a376"

def main():
    hits=-1
    pagenum=1
    findings = []
    full_response = []
    while hits!=0:
        payload = {'componentKeys' : 'mmacala_itc-benchmarks-test', "p" : pagenum }
        response = requests.get('https://sonarcloud.io/api/issues/search', params=payload, auth=(token, ''))
        response_json = response.json()
        full_response.append(response_json)

        hits=0
        for issue in response_json["issues"]:
            hits+=1
            if(issue["type"]!="CODE_SMELL"):
                findings.append(issue)
        pagenum+=1
    with open('..\\csv-data\\sonarcloud\\sonarcloud_results.json', 'w') as f:
        json.dump(full_response,f,indent=2)
    #File, Line, Error
    types = {"c_w_":"01.w_Defects", "c_wo_":"02.wo_Defects", "cpp_w_":"03.w_Defects_Cpp",
             "cpp_wo_":"04.wo_Defects_Cpp"}
    for type in types:
        with open("..\\csv-data\\sonarcloud\\temp\\"+type+"errors_per_line.csv", 'w') as csvFile:
            fieldnames = ["File", "LineStart", "LineEnd", "Error"]
            writer = csv.DictWriter(csvFile, fieldnames, lineterminator="\n")
            writer.writeheader()
            i=0
            for issue in findings:
                if(issue["component"].find(types[type])>0):
                    #how to include range param for fair evaluation?
                    writer.writerow({'File': issue["component"].split("/")[1].strip(), 'LineStart': issue["textRange"]["startLine"], 'LineEnd':issue["textRange"]["endLine"] ,'Error':issue["message"].strip()})
                    i+=1
            print(type + " " + str(i))
if __name__ == "__main__":
    main()