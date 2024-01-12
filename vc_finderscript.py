import requests
import random

def prev(div):
    url = f"https://codeforces.com/api/contest.list?gym=false&div={div}"
    response = requests.get(url)
    
    if response.status_code == 200:
        contests = response.json()['result']
        past_contests = [contest for contest in contests if contest['phase'] == 'FINISHED']
        return past_contests
    else:
        print("Error fetching contests. Status code:", response.status_code)
        return None

def func(usernames, div, num_results=3, skip_results=0):
    past_contests = prev(div)
    valid = []

    if past_contests:
        random.shuffle(past_contests) 

        for contest in past_contests:
            contest_id = contest['id']
            contest_name = contest['name']

            no_attempted = all(not attempt(contest_id, username) for username in usernames)

            if no_attempted:
                contest_link = f"https://codeforces.com/contest/{contest_id}"
                valid.append((contest_name, contest_id, contest_link))

                if len(valid) == num_results + skip_results:
                    break

        if valid:
            print(f"Found {len(valid)} suitable past contests in Division {div}:")
            for idx, (name, cid, link) in enumerate(valid[skip_results:], start=1):
                print(f"{idx}. {name} (Contest ID: {cid}) - Contest Link: {link}")
        else:
            print(f"No suitable past contest found for the specified conditions in Division {div}.")

def attempt(contest_id, username):
    url = f"https://codeforces.com/api/contest.status?contestId={contest_id}&handle={username}&from=1&count=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        result = response.json()['result']
        return len(result) > 0
    else:
        return True 

if __name__ == "__main__":
    usernames = ["pranav16","sujal_singh","vedantmishra69","Saket_ahlawat"]
    div = 2 
    num_results = 3
    skip_results = 1
    
    func(usernames, div, num_results, skip_results)
