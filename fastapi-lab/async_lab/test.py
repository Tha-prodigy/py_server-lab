import time, asyncio

async def add(a,b):
    res =  a+b
    time.sleep(2)
    return res

async def result():
    res = await add(2, 3)
    print(res)

asyncio.run(result())
