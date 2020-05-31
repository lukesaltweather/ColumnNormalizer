import asyncpg
import asyncio

start=120000
end=125074 #last element
step=1000
uri='Database URI'
to_normalize='title' #name of column you want to normalize/edit
prim='prim' #name of column with a serial
table='table' #name of table you want to edit

async def create_con():
    conn = await asyncpg.create_pool(uri, min_size=10, max_size=100)
    return conn

async def check_chunk(start, stop, pool):
    print(f'{start}-{stop-1}')
    conn = await pool.acquire()
    await asyncio.sleep(0.2)
    try:
        rows = await conn.fetch(f'SELECT * FROM {table} WHERE $1 <= {prim} AND {prim} < $2', start, stop)
        if len(rows) == 0:
            raise RuntimeError("Empty chunk")
        for row in rows:
            #your edit
            if row.get(to_normalize)[0] == ' ':
                title = row.get(to_normalize)[1:]
                await conn.execute(f'UPDATE {table} SET {to_normalize} = $1 WHERE {prim} = $2', title, row.get(prim))
                # print(f"fixed {row.get('id')}") you can make a print here for whatever value you just edited
    except Exception as e:
        print(f'error in chunk {start} to {stop-1}: {e}')
    finally:
        await pool.release(conn)

async def chunk():
    print('Creating connection pool...')
    conn = await create_con()
    await asyncio.sleep(5)
    print('Created conn pool. Chunks:')
    await asyncio.gather(*[check_chunk(i, i+step, conn) for i in range(start, end+1, step)])

loop = asyncio.get_event_loop()
loop.run_until_complete(chunk())