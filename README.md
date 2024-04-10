# Simpsons Quotes

Do you have a Simpsons quote that you just can't quite place? Then you've found the right tool. Provide your quote, 
and be provided (probably) with its season number, episode number, and a frame from the scene where the quote has been said. Allows for meme generation too. 

## How use?


```
$ ./quotes_data_retriever <quote>
Season: X
Episode: X
img_url: X
```

## How work?

[Frinkiac](https://frinkiac.com/) does much of the heavy lifting. It lets you fuzzy search for simpsons quotes, and provides you a series of stills for potential matches. This script simply takes the first one (best match from the fuzzy search), assumes it's right, and then scrapes the data from the associated still. The site also has a meme generator function, which we exploit, to generate high quality Simpsons memes.