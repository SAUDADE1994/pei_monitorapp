import urllib.request
import json
import subprocess
import os
import webbrowser
import pyautogui

from time import sleep

from params import *

class Download:
    def __init__(self, path, address):
        self.path = path                # download path
        self.address = address          # downlaod adress
        self.response = None
        self.map = []
        self.trigger = False
        #self.driver = webdriver.Firefox()
        

    def start(self):
        print("Initializing...")
        #self.driver.get(FILENAME)
        webbrowser.open(FILENAME, new = 0)
        self.refresh_page()

    def run(self):
        while(True):
            connected = False
            try:
                self.response = urllib.request.urlopen(self.address)  
                connected = True
            except urllib.error.URLError:
                print("ERROR: Could not establish connection with cloud...")  

            if connected:
                html = json.loads(self.response.read().decode('utf-8'))
                # Checks de json for new results
                aux = []
                for res in html['results']: 
                    arr = res['downloadlink'].split('/')
                    filename = arr[4]
                    aux += [filename]

                prev_content = set(os.listdir(self.path))
                if set(aux) != prev_content:
                    print(set(aux))
                    print(prev_content)
                    self.trigger = True
                    diff = prev_content - set(aux)
                    print(diff)

                    for file in diff:
                        file_path = self.path+"/"+file
                        print(file_path)
                        try:                            
                            print(f"Removing file {file}")
                            os.remove(file_path)
                        except:
                            print("ERROR: removing files from directory {file}")
                
                    for res in html['results']:
                        subprocess.run(["wget", "-N", "-P", self.path, res['downloadlink']]) 
                        
                    print("Refreshing view")
                    self.refresh_page()
                    sleep(SLEEP_TIME)
            else:
                sleep(ESTABLISH)

    def refresh_page(self):
        content = os.listdir(self.path)

        image_div = ""
        video_div = ""

        
        for elem in content:  
            regex = elem.split('.')
            if regex[1] == 'jpg' or regex[1] == 'png' or regex[1] == 'gif':
                image_div += IMG_TMP.format(elem)

            elif regex[1] == 'mp4':
                video_div += VIDEO_TMP.format(elem)
            
            else:
                print("ERROR: Unsupported format")
    

        params = {
            'img_template' : image_div,
            'video_template' : video_div
        }

        body = BODY_TMP.format(**params)
        html = HOME_TMP + body

        with(open(FILENAME, 'w')) as fp:
            fp.write(html)

        
        pyautogui.hotkey('ctrl', 'r')
        #self.driver.refresh()
        self.trigger = False



def main():
    d = Download(PATH, ADDRESS)
    d.start()
    d.run()

if __name__ == "__main__":
    main()