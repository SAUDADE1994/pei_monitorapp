import urllib.request
import json
import subprocess
import os
import webbrowser
import pyautogui
import numpy

from time import sleep

from params import *

class Download:
    def __init__(self, path):
        self.path = path                # download path adress
        self.content_response = None
        self.user_reponse = None
        self.content = []
        self.trigger = False
        self.user_mode = False
        

    def start(self):
        print("Initializing...")
        self.content = os.listdir(self.path)
        webbrowser.open(FILENAME, new = 0)
        self.refresh_page()

    def run(self):
        while(True):
            connected = False
            self.content = []
            try:
                self.content_response = urllib.request.urlopen(CONTENT_ADDRESS)
                self.user_reponse = urllib.request.urlopen(USER_INPUT_ADDRESS)

                connected = True
            except urllib.error.URLError:
                print("ERROR: Could not establish connection with clouds...")  

            if connected:
                html = json.loads(self.content_response.read().decode('utf-8'))
                agent_html = json.loads(self.user_reponse.read().decode('utf-8'))

                # Checks de json for new results
                aux = []
                for res in html['results']: 
                    arr = res['downloadlink'].split('/')
                    filename = arr[4]
                    aux += [filename]


                if(not agent_html['content_confirm']):
                    sel_file = agent_html['contentname']
                    self.content += [sel_file]
                    self.content += [img for img in os.listdir(self.path) if img != sel_file]
                    self.content = numpy.roll(self.content, 1)


                    subprocess.run(["sh", "postupdatesh.sh"]) 
                    sleep(1)

                    print("User Agent Refreshing view")
                    self.refresh_page()

                else:
                    prev_content = set(os.listdir(self.path))
                    # If new content
                    if set(aux) != prev_content:
                        self.trigger = True
                        diff = prev_content - set(aux)

                        # Elimina os ficheiros que já não se apresentam na cloud 
                        for file in diff:
                            file_path = self.path+"/"+file
                            try:                            
                                print(f"Removing file {file}")
                                os.remove(file_path)
                            except:
                                print("ERROR: removing files from directory {file}")
                    
                        for res in html['results']:
                            subprocess.run(["wget", "-N", "-P", self.path, res['downloadlink']]) 
                            
                        print("Refreshing view")
                        self.content = os.listdir(self.path)
                        self.refresh_page()
                
                sleep(ESTABLISH)
            else:
                sleep(ESTABLISH)

    def refresh_page(self):

        image_div = ""
        video_div = ""

        print(self.content)        
        for elem in self.content:  
            regex = elem.split('.')
            if regex[1] == 'jpg' or regex[1] == 'png' or regex[1] == 'gif':
                image_div += IMG_TMP.format(elem)

            elif regex[1] == 'mp4':
                video_div += VIDEO_TMP.format(elem)
            
            else:
                print("ERROR: Unsupported file format")
    

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
    d = Download(PATH)
    d.start()
    d.run()

if __name__ == "__main__":
    main()