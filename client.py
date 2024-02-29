import requests
import json

def login(session, url):
    if url[-1] == "/":
        url = url + "api/login"
    else:
        url = url + "/api/login"
    username = input("Username: ")
    password = input("Password: ")
    data = {
        "username": username,
        "password": password,
    }
    response = session.post(url, data=data)
    print(response.status_code)
    print(response.text)

def logout(session, url):
    url = url + "api/logout"
    response = session.post(url)
    print(response.status_code)
    print(response.text)

def post(session, url):
    if url[-1] == "/":
        url = url + "api/stories"
    else:
        url = url + "/api/stories"
    headline = input("Headline: ")
    category = input("Category: ")
    region = input("Region: ")
    details = input("Details: ")
    headers = {"Content-Type": "application/json"}
    data = {
        'headline': headline,
        'category': category,
        'region': region,
        'details': details,
    }
    response = session.post(url, json=data, headers=headers)
    print(response.status_code)
    print(response.text)

def story(url, category, region, date):
    if "pythonanywhere" in url:
        if url[-1] == "/":
            url = url + "api/stories"
        
        if url[-1] == "m":
            url = url + "/api/stories"
    
        data = {
            "story_cat": category,
            "story_region": region,
            "story_date": date,
        }
        response = session.get(url, params=data)
        if response.status_code == 200:
            objects = response.json()
            objects = objects['stories']
            for obj in objects:
                print(f"{obj['key']} {obj['headline']} {obj['story_cat']} {obj['story_region']} {obj['author']}")
                print(f"{obj['story_date']} {obj['story_details']}")

def news(session, parameters):
    id = ""
    category = "*"
    region = "*"
    date = "*"
    for parameter in parameters:
        if "-id=" in parameter:
            id = parameter[4:]
        if "-cat=" in parameter:
            category = parameter[5:]
        if "-reg=" in parameter:
            region = parameter[5:]
        if "-date=" in parameter:
            date = parameter[6:]
            date = date.split("/")[::-1]
            date = "-".join(date)
            print(date)
    
    url = "http://newssites.pythonanywhere.com/api/directory/"
    response = session.get(url)
    if response.status_code == 200:
        objects = response.json()
        for obj in objects:
            if id in obj['agency_code']:
                story(obj['url'], category, region, date)
        
            

def list_news(session):
    url = "http://newssites.pythonanywhere.com/api/directory/"
    response = session.get(url)
    if response.status_code == 200:
        objects = response.json()
        print(f"{'Agency Name'.ljust(40)}|{'URL'.ljust(35)}|{'Code'.ljust(7)}")
        print("-" * 84)
        for obj in objects:
            print(f"{obj['agency_name'].ljust(40)} {obj['url'].ljust(35)} {obj['agency_code'].ljust(7)}")
    else:
        print(response.text)
    

def delete(session, url, pk):
    if url[-1] == "/":
        url = url + "api/stories/" + pk
    else:
        url = url + "/api/stories/" + pk
    response = session.delete(url)
    if response.status_code == 200:
        print(response.text)
    else:
        print(response.text)
    

if __name__ == "__main__":
    session = requests.Session()
    while True:
        input_string = input(">> ")
        input_list = input_string.split()
        argument = input_list[0]
        if argument == "login":
            url = input_list[1]
            login(session, url)
        elif argument == "logout":
            logout(session, url)
        elif argument == "post":
            post(session, url)
        elif argument == "news":
            news(session, input_list[1:])
        elif argument == "list":
            list_news(session)
        elif argument == "delete":
            delete(session, url, input_list[1])
        else:
            exit(0)