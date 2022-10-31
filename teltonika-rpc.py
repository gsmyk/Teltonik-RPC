import requests
import json
import re

stations_ip = [
        "128.0.0.1"
    ]


def getRouterToken(ip: str, login: str, passwd: str) -> str:
    url = "http://{0}/ubus".format(ip)
    result = ""
    
    headers = {'content-type': 'application/json'}    
    payload =  {
        "jsonrpc":"2.0", "id":1, "method":"call", "params": 
            [
                "00000000000000000000000000000000", "session", "login",
                { 
                 "username":"{0}".format(login), 
                 "password":"{0}".format(passwd) }
            ]
            }
    try:
        res = requests.post(url, data=json.dumps(payload), headers=headers)
        json_string = res.text
        
        start = '"ubus_rpc_session":"'
        end = '","timeout"'
    
        result = re.search('%s(.*)%s' % (start, end), json_string).group(1)
    except ConnectionError as err:
        print(err)
        
    
    return result

def runCommand(token: str, ip: str, login: str, passwd: str):
    url = "http://{0}/ubus".format(ip)
    
    if token == "":
        return ""
    
    payload = {
        "jsonrpc": "2.0", "id": 1, "method": "call", "params": 
            [
                "{0}".format(token), "file", "exec",
                {
                    "command":"gsmctl",
                    "params":
                        [
                            '-S',
                            '-l',
                            'all'
                        ]
                }
            ]
        }
    
    headers = {'content-type': 'application/json'}
    
    res = requests.post(url, data=json.dumps(payload), headers=headers)
    json_string = res.text
    
    #start = '"stdout":"'
    #end = '"'
    
    #output = re.search('%s(.*)%s' % (start, end), json_string).group(1)
    return json_string


def main():
    login = "root"
    password = "<teltonika_password>"

    for ip in stations_ip:
        try:
            token = getSesionToken(ip, login, password)
            output = runCommand(token, ip, login, password)
            parsed = json.loads(output)
            print("{0} :: {1}".format(ip, json.dumps(parsed, indent=4, sort_keys=True).replace("\\n", "\n")))
        except ValueError as err:
            print("Error: {0} - {1}".format(ip, err))
            
        

if __name__ == main():
    main()