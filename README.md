# Langchain_SQL

```python
NLP: Who are top 5 Artists and how many albums did each of them sell?
/Users/ashwjosh/modernaipro/UdemyLangchainCourse/TextToSQL/sql_agent.py:50: LangChainDeprecationWarning: The method `Chain.run` was deprecated in langchain 0.1.0 and will be removed in 1.0. Use :meth:`~invoke` instead.
  response = agent_executor.run(query)


> Entering new SQL Agent Executor chain...
Action: sql_db_list_tables
Action Input: albums, artists, customers, employees, genres, invoice_items, invoices, media_types, playlist_track, playlists, tracks I should query the schema of the artists and albums tables to see what columns I can use.
Action: sql_db_schema
Action Input: artists, albums
CREATE TABLE albums (
        "AlbumId" INTEGER NOT NULL, 
        "Title" NVARCHAR(160) NOT NULL, 
        "ArtistId" INTEGER NOT NULL, 
        PRIMARY KEY ("AlbumId"), 
        FOREIGN KEY("ArtistId") REFERENCES artists ("ArtistId")
)

/*
3 rows from albums table:
AlbumId Title   ArtistId
1       For Those About To Rock We Salute You   1
2       Balls to the Wall       2
3       Restless and Wild       2
*/


CREATE TABLE artists (
        "ArtistId" INTEGER NOT NULL, 
        "Name" NVARCHAR(120), 
        PRIMARY KEY ("ArtistId")
)

/*
3 rows from artists table:
ArtistId        Name
1       AC/DC
2       Accept
3       Aerosmith
*/ I should query the artists and albums tables to get the top 5 artists and their album sales.
Action: sql_db_query
Action Input: SELECT artists.Name, COUNT(albums.AlbumId) AS "Album Sales"
FROM artists
INNER JOIN albums ON artists.ArtistId = albums.ArtistId
GROUP BY artists.Name
ORDER BY COUNT(albums.AlbumId) DESC
LIMIT 5;[('Iron Maiden', 21), ('Led Zeppelin', 14), ('Deep Purple', 11), ('U2', 10), ('Metallica', 10)] I now know the final answer.
Final Answer: Artist Name, Album Sales
Iron Maiden, 21
Led Zeppelin, 14
Deep Purple, 11
U2, 10
Metallica, 10

> Finished chain.

import plotly.graph_objects as go

artist_names = ['Iron Maiden', 'Led Zeppelin', 'Deep Purple', 'U2', 'Metallica']
album_sales = [21, 14, 11, 10, 10]

fig = go.Figure(data=[go.Bar(x=artist_names, y=album_sales)])
fig.update_layout(title='Album Sales by Artist', xaxis_title='Artist Name', yaxis_title='Album Sales')
fig.show()

```

<img width="1719" alt="image" src="https://github.com/user-attachments/assets/8f67437a-f53d-4044-a24b-92472e1e59fc" />
