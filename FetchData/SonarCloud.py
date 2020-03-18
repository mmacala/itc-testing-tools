import requests
import csv

token="3e6978bcbc40b5d4aa0473e986cfaf6d79d1a376"

def postSample():
    task = {"summary": "Take out trash", "description": "" }
    resp = requests.post('https://todolist.example.com/tasks/', json=task)
    print('Created task. ID: {}'.format(resp.json()["id"]))


def getSample():
    resp = requests.get('https://todolist.example.com/tasks/')
    for todo_item in resp.json():
        print('{} {}'.format(todo_item['id'], todo_item['summary']))


def main():
    hits=-1
    pagenum=1
    findings = []
    while hits!=0:
        payload = {'componentKeys' : 'mmacala_itc-benchmarks-test', "p" : pagenum }
        response = requests.get('https://sonarcloud.io/api/issues/search', params=payload, auth=(token, ''))
        response = response.json()
        hits=0
        for issue in response["issues"]:
            hits+=1
            if(issue["type"]!="CODE_SMELL"):
                findings.append(issue)
        pagenum+=1
    print(len(findings))
    #File, Line, Error
    types = {"c_w_errors_":"01.w_Defects", "c_wo_errors_":"02.wo_Defects", "cpp_w_":"03.w_Defects_Cpp", "cpp_wo_":"04.wo_Defects_Cpp"}
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