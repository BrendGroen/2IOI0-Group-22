import requests
import os
from tqdm import tqdm
import gzip
import shutil
import os


def download_and_extract_gzip(url: str, save_path: str, extract_path: str, file_name: str) -> None:
    """
    Download a zip data file form the given URL and extract its contents to the specified folder.
    param url: URL of the zip file to download
    param save_path: Path to save the downloaded zip file
    param extract_path: Path to extract the contents of the zip file
    file_name: Name of the file to save the zip file as
    return: None
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"Directory {save_path} created.")

    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
        print(f"Directory {extract_path} created.")

    # Save path for the zip file
    save_path_file = os.path.join(save_path, file_name)

    try:
        # Download the zip file
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Get the total file size
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

        # Save the downloaded zip file
        with open(save_path_file, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()
        # get the absolute path of the downloaded file
        save_path = os.path.abspath(save_path_file)
        print(f"Zip file downloaded successfully and saved to {save_path}")

        # Extract the downloaded gzip file
        with gzip.open(save_path_file, 'rb') as f_in:
            extract_file_path = os.path.join(extract_path, file_name[:-3])
            with open(extract_file_path, 'wb') as f_out:
                progress_bar_extract = tqdm(total=os.path.getsize(
                    save_path_file), unit='B', unit_scale=True, desc='Extracting')
                shutil.copyfileobj(f_in, f_out)
                progress_bar_extract.update(os.path.getsize(save_path_file))
                progress_bar_extract.close()

        # get the absolute path of the extracted file
        extract_path = os.path.abspath(extract_file_path)
        print(f"Data extracted to {extract_path}")

    # Handle exceptions
    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")


if __name__ == "__main__":
    # Adapt the following variables to the specific values you want
    # Or you could just leave them as they are and use the default values
    # 2018 BPI Challenge data
    gzip_data_url = 'https://data.4tu.nl/file/443451fd-d38a-4464-88b4-0fc641552632/cd4fd2b8-6c95-47ae-aad9-dc1a085db364'
    file_name = 'BPI_challenge_2018.xes.gz'

    # 2017 BPI Challenge data
    # gzip_data_url = 'https://data.4tu.nl/file/34c3f44b-3101-4ea9-8281-e38905c68b8d/f3aec4f7-d52c-4217-82f4-57d719a8298c'
    # file_name = 'BPI_challenge_2017.xes.gz'

    # Road Traffic Fine Management Process data
    # gzip_data_url = 'https://data.4tu.nl/file/806acd1a-2bf2-4e39-be21-69b8cad10909/b234b06c-4d4f-4055-9f14-6218e3906d82'
    # file_name = 'Road_Traffic_Fine_Management_Process.xes.gz'

    # 2012 BPI Challenge data
    # gzip_data_url = 'https://data.4tu.nl/file/533f66a4-8911-4ac7-8612-1235d65d1f37/3276db7f-8bee-4f2b-88ee-92dbffb5a893'
    # file_name = 'BPI_challenge_2012.xes.gz'

    gzip_save_path = 'data/zipped'
    extract_folder = 'data/extracted'
    
    ################################# Running the data fetcher ##################################

    download_and_extract_gzip(
        gzip_data_url, gzip_save_path, extract_folder, file_name)
