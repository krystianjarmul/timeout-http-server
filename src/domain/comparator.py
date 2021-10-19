import asyncio

async def something_to_wait():
    await asyncio.sleep(1)
    return "something_to_wait"

async def something_else_to_wait():
    await asyncio.sleep(2)
    return "something_else_to_wait"


async def wait_first():
    done, pending = await asyncio.wait(
        [something_to_wait(), something_else_to_wait()],
        return_when=asyncio.FIRST_COMPLETED)
    print("done", done)
    print("pending", pending)

asyncio.get_event_loop().run_until_complete(wait_first())
