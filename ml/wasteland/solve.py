import requests
import pandas as pd

df = pd.read_csv('Ashen_Outpost_Records.csv')
df.to_csv("Ashen_Outpost_Records.csv", index=False)

print("Initial")
with open(f"Ashen_Outpost_Records.csv", "r") as f:
    r = requests.post("http://94.237.51.163:53461/score", files={"csv_file": f})
    print(line := r.text)
    prev = float(line.split("[")[1].split("]")[0])

# Dragonfire_Resistance,Shadow_Crimes,Corruption_Mutations,Reputation
for _ in range(1000):
    for feature, amt in zip(
            ["Dragonfire_Resistance", "Dragonfire_Resistance", "Shadow_Crimes", "Shadow_Crimes", "Corruption_Mutations",
             "Corruption_Mutations"], [10 ** 9, 10 ** 9, 1, -1, 1, -1]):
        # for feature, amt in zip(["Dragonfire_Resistance", "Shadow_Crimes", "Corruption_Mutations"], [5 * 10 ** 8, 1, 1]):
        # for feature, amt in zip(["Dragonfire_Resistance", "Dragonfire_Resistance"], [10 ** 9, -10 ** 9]):
        for i in range(len(df) - 1):
            print("Climbing", feature, i)
            prev_feature = df[feature][i]
            df.loc[i, feature] += amt
            if feature in ("Shadow_Crimes", "Corruption_Mutations"):
                df.loc[i, feature] = max(df.loc[i, feature], 0)
                df.loc[i, feature] = min(df.loc[i, feature], 9)

            df.to_csv("Ashen_Outpost_Records.csv", index=False)
            with open(f"Ashen_Outpost_Records.csv", "r") as f:
                r = requests.post("http://94.237.51.163:53461/score", files={"csv_file": f})
                print(line := r.text)
                if feature != prev_feature:
                    df.loc[i, feature] = prev_feature

                score = float(line.split("[")[1].split("]")[0])
                if score >= prev:
                    df.loc[i, feature] += amt
                    prev = score

                if feature in ("Shadow_Crimes", "Corruption_Mutations"):
                    df.loc[i, feature] = max(df.loc[i, feature], 0)
                    df.loc[i, feature] = min(df.loc[i, feature], 9)

# Flag: HTB{4sh3n_D4t4_M4st3r}
