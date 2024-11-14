import requests
import os
from requests_toolbelt import MultipartEncoder

GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

class StaticAnalysis:
    def __init__(self,server,file_path,api_key) -> None:
        self.server = server
        self.path = file_path
        self.file_path = file_path+'/newapp.apk'
        self.api_key=api_key
        self.scan_hash=''

    def upload_apk(self):
        print(f'{BLUE}[*]{RESET} Uploading APK')
        multipart_data = MultipartEncoder(
            fields = {'file':(self.file_path, open(self.file_path,'rb'),'application/octet-stream')}
        )
        headers = {
            'Content-Type':multipart_data.content_type,
            'Authorization':self.api_key
        }
        response = requests.post(f'{self.server}/api/v1/upload',data=multipart_data, headers=headers)
        result = response.json()
        if 'hash' in result:
            self.scan_hash = result['hash']
            print(f'{GREEN}[+]{RESET} Upload completed')
        print(f'upload result={result}')

    def scan_apk(self):
        print(f'{BLUE}[*]{RESET} Scanning Started')
        data = {
            'hash':self.scan_hash,
            'scan_type':self.file_path.split('.')[-1],
            'file_name':os.path.basename(self.file_path)
            }
        headers = {
            'Authorization':self.api_key
        }
        response = requests.post(f'{self.server}/api/v1/scan',data=data,headers=headers)
        print(f'{GREEN}[+]{RESET} Scanning completed')
        print(response.json)

    def download_pdf(self):
        print(f'{BLUE}[*]{RESET} Downloading the pdf')
        data = {
            'hash':self.scan_hash,
        }
        headers = {
            'Authorization':self.api_key
        }
        response = requests.post(f'{self.server}/api/v1/download_pdf',data=data,headers=headers)
        with open(self.path+'/static_analysis_report.pdf','wb') as f:
            f.write(response.content)
        print(f'{GREEN}[+]{RESET} Download complete')
        print(f'{BLUE}[*]{RESET} Result of static analyze is at {YELLOW}{self.path+"/static_analysis_report.pdf"}{RESET}')

    def staticAnalysis(self):
        self.upload_apk()
        self.scan_apk()
        self.download_pdf()


