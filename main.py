import boto3
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from utils import human_readable_size
from datetime import datetime
import time

client = boto3.client(
    's3'
    # Hard coded strings as credentials, not recommended.
    #aws_access_key_id='',
    #aws_secret_access_key=''
)
bucketsList = client.list_buckets()
# Get a list of all bucket names from the response
i = 0
print('0 - ALL BUCKETS')
buckets = bucketsList['Buckets']
for bucket in buckets:
    i += 1
    name = bucket['Name']
    print(str(i)+' - '+name)
while True:
    try:
        bucketSelection = int(input("Which bucket would you like details for? "))
        if int(bucketSelection) >= 0 and int(bucketSelection) <= i:
            break
        else:
            raise Exception('')
    except:
        print("Invalid option")

#TODO enumerate over all buckets for option 0 - done
#TODO Py2exe???
#TODO Paging for buckets with over 1000 objects
#TODO Fix last updated date on summary


def process_bucket(bucketName, counter=1):
    bucketLocation = client.get_bucket_location(Bucket=bucketName)
    truncatedBucketName = (bucketName[:28] + '..') if len(bucketName) > 30 else bucketName

    s3objects = client.list_objects_v2(Bucket=bucketName)
    bucketTotal = 0

    if s3objects['KeyCount'] > 0:
        ws2 = wb.create_sheet(title=truncatedBucketName)
        ws2.append(["Object Key", "Storage Class", "Size", "Size in Bytes", "Last Modified"])
        firstObject = s3objects['Contents'][0]
        lastModifiedDate = datetime(1970, 1, 1, tzinfo=firstObject["LastModified"].tzinfo)
        for s3object in s3objects['Contents']:
            objectLastModified = s3object["LastModified"]
            if objectLastModified > lastModifiedDate:
                lastModifiedDate = objectLastModified
            objectSize = s3object['Size']
            bucketTotal += objectSize
            dataRow = [s3object["Key"], s3object["StorageClass"], human_readable_size(objectSize), objectSize,
                       objectLastModified]
            ws2.append(dataRow)
        buckettableref = 'A1:E' + str(s3objects['KeyCount'] + 1)
        buckettablename = 'table' + str(counter)
        bucketTab = Table(displayName=buckettablename, ref=buckettableref)
        bucketTab.tableStyleInfo = style
        ws2.add_table(bucketTab)
    else:
        lastModifiedDate = ''
    bucketData = [bucketName, bucketLocation['LocationConstraint'], bucket['CreationDate'], lastModifiedDate,
                  s3objects['KeyCount'], human_readable_size(bucketTotal)]
    ws1.append(bucketData)


wb = Workbook()
ws1 = wb.active
ws1.title = "Bucket Summary"
ws1.append(["Name", "Region", "Created Date", "Last Updated", "Total Objects", "Total Size"])
# Add a default style with striped rows
style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                       showLastColumn=False, showRowStripes=True, showColumnStripes=False)
if bucketSelection == 0:
    x = len(buckets)
    y = 0
    for bucket in buckets:
        y += 1
        process_bucket(bucket['Name'], y)
else:
    x = 1
    bucket = buckets[int(bucketSelection) - 1]
    process_bucket(bucket['Name'])

tableRef = 'A1:F'+str(x+1)
summaryTab = Table(displayName="Summary", ref=tableRef)
summaryTab.tableStyleInfo = style
ws1.add_table(summaryTab)

#bucketName = bucket['Name']
#process_bucket(bucketName)
outputFilename = 'output/s3report-'+time.strftime("%Y%m%d-%H%M%S")+'.xlsx'
wb.save(filename=outputFilename)



