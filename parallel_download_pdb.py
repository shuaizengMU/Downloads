

import asyncio
import aiohttp
import gzip
import os


ZIPPED_PDB_DIR = "./pdb_gz/"
PDB_DIR = "./pdb"
PDB_LSIT = "pdb_list.txt"

async def download_file(url, session):
  async with session.get(url) as response:
    if response.status == 200:

      ## Download
      content = await response.read()
      # Save the content to a file or process it as needed
      filename = url.split("/")[-1]  # Extract filename from URL
      output_filename = ZIPPED_PDB_DIR + filename
      with open(output_filename, "wb") as file:
          file.write(content)
      print(f"Downloaded {url}")

      ## unzip
      # Path to the compressed .gz file
      input_file = output_filename

      pdb_id = filename.split(".")[0].replace("pdb", "")

      # Path where you want to save the decompressed file
      output_file = os.path.join(PDB_DIR, f"{pdb_id}.pdb")

      with gzip.open(input_file, 'rb') as f_in:
          with open(output_file, 'wb') as f_out:
              f_out.write(f_in.read())


def get_ids_in_folder(folder_path):
  filenames = []
  for root, dirs, files in os.walk(folder_path):
      for file in files:
          filenames.append(file.replace(".pdb", ""))
  return filenames


async def main():

  if not os.path.exists(ZIPPED_PDB_DIR):
    os.makedirs(ZIPPED_PDB_DIR)

  if not os.path.exists(PDB_DIR):
    os.makedirs(PDB_DIR)

  fp = open(PDB_LSIT)
  lines = fp.readlines()

  existing_ids = get_ids_in_folder(PDB_DIR)

  urls = []
  for line in lines:
    line = line.strip()

    if line in existing_ids:
      continue
    urls.append(f"https://files.wwpdb.org/pub/pdb/data/structures/all/pdb/pdb{line}.ent.gz")
  
  print(len(urls))
  if len(urls) < 100:
    print(urls)

  async with aiohttp.ClientSession() as session:
    tasks = [download_file(url, session) for url in urls]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
