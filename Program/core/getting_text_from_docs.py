from googleapiclient.discovery import build
from google.oauth2 import service_account
import time
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot

class GetTextfromGoogleDocs(QObject):

    close_push = pyqtSignal()

    def __init__(self, work_with_text):
        super().__init__()
        SCOPES = ['https://www.googleapis.com/auth/documents']
        SERVICE_ACCOUNT_FILE = '../secret_data/gogAPI.json' 
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = build('docs', 'v1', credentials=creds)
        self.DOCUMENT_ID = '1jxQs9DNNV9gKY_9NvsixZlcqe_Sc-LZKlTwWkp8kYbI'
        self.work_WithText = work_with_text

        self.time_open_push = 0

        self.get_text_running = True

        self.start_rec_command = False

    # витягуємо текст
    def extract_text(self, elements):
        text = ''
        for element in elements:
            if 'paragraph' in element:
                for run in element['paragraph']['elements']:
                    if 'textRun' in run:
                        text += run['textRun']['content']
        return text

    def print_text(self):
        doc = self.service.documents().get(documentId=self.DOCUMENT_ID).execute()
        content = doc.get('body').get('content')
        self.end_index = max(el.get('endIndex', 0) for el in content if 'endIndex' in el)

        self.text = self.extract_text(content)
        time.sleep(0.5)

        self.set_text()

    def stop_GetText(self):
        self.get_text_running = False


    def clear_text(self):
        if len(self.text) == 1:
            return
        else:
            requests = [
                {
                    'deleteContentRange': {
                        'range': {
                            'startIndex': 1,
                            'endIndex': self.end_index - 1
                        }

                    }

                },
            ]
            result = self.service.documents().batchUpdate(
                documentId=self.DOCUMENT_ID, body={'requests': requests}).execute()
            

    def set_text(self):
        if self.work_WithText.start_write_text:
            self.chech_whether_isText()
        elif self.work_WithText.find_silence == True:
            print("НАДСИЛАННЯ КОМАНДИ")
            self.work_WithText.send_command(self.text)
            self.work_WithText.status_find_silence_OFF()
            self.start_rec_command = False
            self.clear_text()
            


    def chech_whether_isText(self):
        print(f"ТИША ============ {self.work_WithText.find_silence}")

        if self.start_rec_command == True:
            self.work_WithText.receive_google_docs_text(self.text)
        elif self.work_WithText.time_wait_passed == True:
            self.work_WithText.steps_if_time_passed()
            self.start_rec_command = False
            self.clear_text()
        elif len(self.text) > 1:
            self.start_rec_command = True
            self.work_WithText.status_text_ON()
            self.work_WithText.receive_google_docs_text(self.text)




    def start(self):

        self.print_text()
        self.clear_text()
        while True:
            self.print_text()
            if self.get_text_running == False:
                break

    

    





    # def start(self):
    #     self.print_text()
    #     self.clear_text()
    #     while True:
    #         if self.push_running:
    #             self.print_text()
    #             self.wait_text()
    #         if self.get_text_running == False:
    #             break
    




    # @pyqtSlot()
    # def status_Push_ON(self):
    #     self.push_running = True

    # @pyqtSlot()
    # def status_Push_OFF(self):
    #     self.push_running = False

    

if __name__ == "__main__":
    get_text_docs = GetTextfromGoogleDocs()
    get_text_docs.start()

