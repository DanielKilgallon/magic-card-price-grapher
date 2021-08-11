#  magic-card-price-grapher

A script I made to aggregate .csv files stored in S3 into one .csv file and upload it back to S3. The steps are:
* Sync local folder with S3 bucket
* Read and collect data from each file into Map
* Write aggregated data to a .csv file
* Upload single output file to S3 bucket

## Installing and Running

This project was made using Python 3.8.2

### How to run project locally

You can download or clone this repository, then navigate to this folder and run the python script. You will need your own collection of .csv files to aggregate, since this is for my personal s3 bucket :)

## Built With

* [Python 3](https://www.python.org/) - The language
* [MasterPlan](https://solarlune.itch.io/masterplan) - light-weight project management software

## Authors

* **Daniel Kilgallon** - *Creator and Maintainer*