from fastapi import FastAPI, HTTPException
from database import Base
from pydantic import BaseModel
from contextlib import asynccontextmanager

import httpx



class BookResponse(BaseModel):
    title: str
    author : list[str]


@asynccontextmanager
async def lifeSpan(app: FastAPI):
    app.state.client = httpx.AsyncClient()
    yield

    await app.state.client.aclose()


app= FastAPI(lifespan=lifeSpan)


@app.get("/books/search", response_model=list[BookResponse])
async def get_book(q: str, limits: int):

    book_details = []
    client = app.state.client

    try:
        res = await client.get('https://openlibrary.org/search.json', params={'q':q, 'limit':limits})
        res.raise_for_status()
        docs = res.json()['docs']
        for doc in docs:
                names = doc.get('author_name', "Unknown name")
                title = doc.get('title', 'unknown title')
                book_details.append({'author': names, 'title': title})
        return book_details

    except httpx.HTTPStatusError as e:
        print('HTTP ERROR:', e.response.status_code)
        raise HTTPException(502, 'The external service is is unavailable')

    except httpx.RequestError as r:
        print(f'Request failed. {r}')

        raise HTTPException(408, 'request time out')
            
            
      
             
             
        
        

