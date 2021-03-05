# PeMS_Traffic_Downloader
This is a simple script for downloading PeMS traffic data from PeMS data source 
## Example of use

* username   | PeMS username to initialize session.                 
* password   | PeMS password to initialize session.                  
* start_date | set start date to download from PeMS eg. 2020-01-12. 
* end_date   | set end date to download from PeMS eg. 2020-02-12.     
* data_type  | set data type eg. station_5min , station_raw ,metadata.
* district", | set district number eg. 1,2..                         
* unzip      | set True to unzip downloaded files.                        
```
python download_pems.py -u [username|email] -p [password]  -s [startdate] -e [enddate] -d [district] -t [data_type] -z [True| False]
```
Example :
```
python download_pems.py -u example@gmail.com -p example  -s 2020-01-01 -e 2020-01-01 -d '3' -t station_5min -z True
```
