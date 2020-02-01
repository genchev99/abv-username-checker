import random
import requests
import threading
from time import sleep

proxies_path = "proxies_bg.txt"
with open(proxies_path) as f:
    proxies_content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
proxies = [x.strip() for x in proxies_content]

output_file = open("out.txt", "a+")


def check_username(username):
    try:
        proxy_index = random.randint(0, len(proxies) - 1)
        proxy = {"http": "http://" + proxies[proxy_index], "https": "http://" + proxies[proxy_index]}
        url = "https://passport.abv.bg/app/profiles/validateename?id=%s&answ=undefined&fname=&lname=&byear=0" % username
        print(url)

        response = requests.get(url, proxies=proxy, timeout=10)
        content = str(response.content)
        print(content)
        if "occupied" in content:
            output_file.write(username + " occupied\n")
            output_file.flush()
        elif "free" in content:
            output_file.write(username + " free\n")
            output_file.flush()
        else:
            check_username(username)
    # except requests.exceptions.Timeout:
    #     # implement here what to do when there’s a connection error
    #     # for example: remove the used proxy from the pool and retry the request using another one
    #     # check_username(username)
    #     print("Timeout exception")
    #     check_username(username)
    except:
        print("Random exception")
        check_username(username)


if __name__ == '__main__':
    usernames_path = "./usernames.txt"
    with open(usernames_path) as f:
        usernames_content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    usernames = [x.strip() for x in usernames_content]

    threads = []

    for username in usernames:
        t = threading.Thread(target=check_username, args=(username,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    output_file.flush()
    output_file.close()
