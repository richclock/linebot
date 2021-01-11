import boto3
import base64
import json



class rekognition():
    def __init__(self):
        self.__awsAccessKeyId = 'AKIATOREFWF7HKYBZSAH',
        self.__awsSecretAccessKey = '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',
        self.__regionName = 'ap-southeast-1'
        return

    def detect(self, path):
        

        client = boto3.client(
            'rekognition',
            aws_access_key_id=self.__awsAccessKeyId,
            aws_secret_access_key=self.__awsSecretAccessKey,
            region_name=self.__regionName
        )
        # session = boto3.Session(aws_access_key_id=self.__awsAccessKeyId,aws_secret_access_key=self.__awsSecretAccessKey)
        # s3 = session.resource('s3')
        # for bucket in s3.buckets.all():
        #     print(bucket.name)


        with open(path, 'rb') as image:
            encoded_string = base64.b64encode(image.read())
            # response = client.recognize_celebrities(Image={'Bytes': image.read()})

            kwargs = {'Bytes': image.read()}
            str =  ''.join(tup)
            response = client.recognize_celebrities(Image=str)


        print(response)

    def convert_img_to_bytes(file):
        with open(file, 'rb') as f:
            source_bytes = f.read()
        return source_bytes


if __name__ == "__main__":
    rekognition = rekognition()
    rekognition.detect('C:/Users/clock/Desktop/111.png')
    
