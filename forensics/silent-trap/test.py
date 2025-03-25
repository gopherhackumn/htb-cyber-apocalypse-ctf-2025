import requests

# for i in range(0, 10000, 100):
#     ids = list(range(i, i + 100))
# r = requests.get("https://api.telegram.org/bot7767830636:AAF5Fej3DZ44ZZQbMrkn8gf7dQdYb3eNxbc/copyMessage", params=dict(
#     chat_id="-1002695046188",
#     from_chat_id="-1002496072246",
#     message_id=5
# ))
# print(r.text)

r = requests.get("https://api.telegram.org/bot7767830636:AAF5Fej3DZ44ZZQbMrkn8gf7dQdYb3eNxbc/getUpdates", params=dict(
    # chat_id="-1002496072246",
))

import json
d = r.json()
for l in d["result"]:
    # print(json.dumps(l, indent=2))
    try: print(l["update_id"], l["message"]["from"]["username"], l["message"]["chat"]["id"], l["message"]["chat"]["type"], l["message"]["text"])
    except: pass
    try: print(l["update_id"], l["channel_post"]["from"]["username"], l["channel_post"]["chat"]["id"], l["channel_post"]["chat"]["type"], l["channel_post"]["text"])
    except: pass
