import pandas as pd


data={'platform':[1,2,3,4], 'title':[5,6,7,8], 'date':[1,2,3,4], 'artist':[1,2,3,4], 'url':[1,2,3,4], 'imageUrl':[1,2,3,4]}
df = pd.DataFrame(data, columns=["platform", "title", "date", "place", "artist", "url", "imageUrl"])
df.to_csv("25 ,Sep.csv", encoding='utf-8-sig')
print(df)