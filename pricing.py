import boto3
import json


def get_s3_pricing():
    pricing = boto3.client('pricing')
    print('Fetching current S3 pricing')
    print()
    response = pricing.get_products(
         ServiceCode='AmazonS3',
         Filters = [
             {'Type' :'TERM_MATCH', 'Field':'storageClass',        'Value':'General Purpose'}
         ],
         MaxResults=100
    )

    costs = {
        "eu-west-1": 0,
        "eu-west-2": 0,
        "us-east-1": 0,
        "us-west-2": 0,
        "ca-central-1": 0,
        "eu-central-1": 0,
        "EU": 0
    }

    for price in response['PriceList']:
        parsed_json = json.loads(price)
        if parsed_json['product']['attributes']['usagetype'] == 'EU-TimedStorage-ByteHrs':
            costs["eu-west-1"] = float(parsed_json['terms']['OnDemand']['4AJHPB29ZPVFADXP.JRTCKXETXF']['priceDimensions'][
                '4AJHPB29ZPVFADXP.JRTCKXETXF.PGHJ3S3EYE']['pricePerUnit']['USD'])
        if parsed_json['product']['attributes']['usagetype'] == 'EUW2-TimedStorage-ByteHrs':
            costs["eu-west-2"] = float(parsed_json['terms']['OnDemand']['DV3FSFEQ3QM4J6VP.JRTCKXETXF']['priceDimensions'][
                'DV3FSFEQ3QM4J6VP.JRTCKXETXF.PGHJ3S3EYE']['pricePerUnit']['USD'])
        if parsed_json['product']['attributes']['usagetype'] == 'EUC1-TimedStorage-ByteHrs':
            costs["eu-central-1"] = float(parsed_json['terms']['OnDemand']['NRYRNCXF5TWHB476.JRTCKXETXF']['priceDimensions'][
                'NRYRNCXF5TWHB476.JRTCKXETXF.PGHJ3S3EYE']['pricePerUnit']['USD'])
        if parsed_json['product']['attributes']['usagetype'] == 'TimedStorage-ByteHrs':
            costs["us-east-1"] = float(parsed_json['terms']['OnDemand']['WP9ANXZGBYYSGJEA.JRTCKXETXF']['priceDimensions'][
                'WP9ANXZGBYYSGJEA.JRTCKXETXF.PGHJ3S3EYE']['pricePerUnit']['USD'])
        if parsed_json['product']['attributes']['usagetype'] == 'USW2-TimedStorage-ByteHrs':
            costs["us-west-2"] = float(parsed_json['terms']['OnDemand']['Z3FQZG73HYSPVABR.JRTCKXETXF']['priceDimensions'][
                'Z3FQZG73HYSPVABR.JRTCKXETXF.PGHJ3S3EYE']['pricePerUnit']['USD'])
        if parsed_json['product']['attributes']['usagetype'] == 'CAN1-TimedStorage-ByteHrs':
            costs["ca-central-1"] = float(parsed_json['terms']['OnDemand']['9MDYGCA9S4SXXTJF.JRTCKXETXF']['priceDimensions'][
                '9MDYGCA9S4SXXTJF.JRTCKXETXF.PGHJ3S3EYE']['pricePerUnit']['USD'])
    return costs

