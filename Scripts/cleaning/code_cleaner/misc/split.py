# split the code file into mulitple files based on the number of lines
import asyncio
import aiofiles
import os

async def read_file(file_path, chunk_size):
    
    out = []
    async with aiofiles.open(file_path, 'r') as file:
        
        while True:
            line = await file.readline()
            if not line:
                break
            out.append(line)
            if len(out)== chunk_size:
                yield out
                out = []

    if out:
        yield out

async def write_file(file_path, data):
    async with aiofiles.open(file_path, 'a') as file:
        for line in data:
            await file.write(line)

async def process_chunk(chunk, file_names):
    file_chunks = { name: [] for name in file_names}
    step_size = len(chunk) // len(file_names)
    tasks = []
    for i in range(len(file_names)):
        tasks.append(write_file(file_names[i], chunk[i*step_size:(i+1)*step_size]))
    await asyncio.gather(*tasks)
# use asynchronous processing to split the code file into multiple files
async def main(file_path, num_files, prefix):

    
    file_names = [f"{prefix}_{i}.jsonl" for i in range(num_files)]
    chunk_size = num_files * 5000 
    data_generator = read_file(file_path, chunk_size)
    async for chunk in data_generator:
        await process_chunk(chunk, file_names)


if __name__ == '__main__':
    asyncio.run(main('new-python-dataset/code.jsonl', 8, 'new-python-dataset/data/code'))