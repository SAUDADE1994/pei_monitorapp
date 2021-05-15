SLEEP_TIME = 15
ESTABLISH = 1

PATH = "downloads"
CONTENT_ADDRESS = "http://peig2.westeurope.cloudapp.azure.com/api/documents/?format=json&fbclid=IwAR0G9JxR9jB-kRuR8oUf-L9Kgt6AQ8feoXFNC1_aan3h4Ed9ZXQSMpfwcSU"
USER_INPUT_ADDRESS = "http://peig2.westeurope.cloudapp.azure.com/api/agentupdates/3/?fbclid=IwAR2sSx1hJj7gKveB3MhrZRH0OHq37nLUMXEt8912J65e8ac3ugMOJFDz0Vc"

FILENAME = "home.html"
#FILENAME = r"C:\Users\gabri\Desktop\PEI\tests\home.html"

HOME_TMP = '''\
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: black;
            overflow: hidden;
        }

        .screen {
            height: 100%;
            width: 100%;
        }

        .slides {
            object-fit: contain;
            height: 100%;
            width: auto;
            max-width: 100%;
            margin-left: auto;
            margin-right: auto;
            display: block;
        }

        .slides-hidden {
            display: none;
        }
    </style>

    <script src="update.js"></script>
</head>
'''

BODY_TMP = '''\
    <body>
    <div>
        {img_template}
        {video_template}
    </div>
    </body>
    </html>
    '''

IMG_TMP = "<img class='slides slides-hidden' src='downloads/{}' />\n"
VIDEO_TMP = '''\
<video id="my-video" class="slides slides-hidden" autoplay>
    <source src="downloads/{}" type="video/mp4">
</video>    
'''