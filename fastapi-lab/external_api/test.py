import httpx, asyncio

async def main():
    async with httpx.AsyncClient() as client:

        try:
            res = await client.get('https://openlibrary.org/search.json?q=python')

            res.raise_for_status()


            docs = res.json()['docs']
            for doc in docs[:5]:
                names = doc.get('author_name', "Unknown name")
                title = doc.get('title', 'unknown title')
                print({'author_name': names, 'title': title})

        except httpx.HTTPStatusError as e:
            print('HTTP ERROR:', e.response.status_code)

        except httpx.RequestError as r:
            print(f'Request failed. {r}')




asyncio.run(main())