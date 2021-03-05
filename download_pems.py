import pems_api as pems
import pandas as pd
import gzip
import shutil
from progress.bar import Bar
from os import listdir,mkdir,path
import argparse
# Initiate the parser
parser = argparse.ArgumentParser()
# Add long and short argument
parser.add_argument("--username", "-u", help="PeMS username to initialize session")
parser.add_argument("--password", "-p", help="PeMS password to initialize session")
parser.add_argument("--start_date", "-s", help="set start date to download from PeMS eg. 2020-01-12")
parser.add_argument("--end_date", "-e", help="set end date to download from PeMS eg. 2020-02-12")
parser.add_argument("--data_type", "-t", help="set data type eg. station_5min , station_raw ,metadata")
parser.add_argument("--district", "-d", help="set district number eg. 1,2..")
parser.add_argument("--unzip", "-z", help="set True to unzip downloaded files ")
args = parser.parse_args()

print(args)
def unzip_files(dirname):
    compressed_data=listdir(f'./{dirname}')
    bar = Bar('Processing', max=len(compressed_data))
    unprocessed=[]
    mkdir(f"./{dirname}/txt/") 
    for file in compressed_data:
        # print(file[0:-3])
        try:
            with gzip.open(f'./{dirname}/{file}', 'rb') as f_in:
                with open( f'./{dirname}/txt/{file[0:-3]}', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            bar.next()
        except:
            unprocessed.append(file[0:-3])
    bar.finish()
    print(f"\n Failed to process {len(unprocessed)} files",unprocessed)
def download_data(start_date,end_date,data_type:str='station_5min',district:int=None,unzip:bool=False):
    links={}
    dir_name=f'pems_station_5min_{start_date}_{end_date}_{district or "all" }'
    dates=pd.date_range(start=start_date,end=end_date)
    if data_type=="station_5min":
        handerl=pems.Station5MinDataHandler()
        url_parser=handerl._url_parser
    elif data_type=="station_raw":
        handerl=pems.StationRawDataHandler()
        url_parser=handerl._url_parser
    elif data_type=="metadata":
        handerl=pems.StationMetaDataHandler()
        url_parser=handerl._url_parser
    for date in dates:
        links[date.date()]=session.get_url(data_type,date.date(),url_parser,district)
    # print(links)
    if path.isdir(dir_name):
        print(f"Directory {dir_name} already exists => update content\n")
    else:
        print("Create new directory => ",dir_name,"\n")
        mkdir(dir_name)
    count=0

    for date,link in links.items():
        count+=1
        print("Downloading ... ",link)
        print("--------------------- \n")
        session.download(link,f"{dir_name}/{str(date)}.txt.gz")
        print(f"downloaded  {count}/{len(links.keys())} \n")
        print("---------------------\n")
    if unzip:
        print("unzipping files")
        unzip_files(dir_name)

session=pems.PeMSConnection()
if args.username and args.password:
    # try:
    print("initializing ... \n")
    # session.initialize("hatemhunish@gmail.com","~r5trickS")
    credentials={
        'username':str(args.username),
        'password':str(args.password)} 
    # print(credentials)
    session.initialize(credentials['username'],credentials['password'])
    if session.initialized:
        print("Session initialized!")
        print("--------------------- \n")
        parameters={
            'start_date':args.start_date,
            'end_date':args.end_date,
            'data_type':args.data_type,
            'district':args.district,
            'unzip':args.unzip
        }
        download_data(**parameters)
    else:
        print("Session hasn't been initialized! \n")
 