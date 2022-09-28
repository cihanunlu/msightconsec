from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from pywebio.output import put_text, put_scrollable, put_column, put_button, put_info, put_markdown, put_success, put_html, put_processbar, toast, put_scope, put_buttons, put_row, clear, put_tabs, put_buttons, scroll_to
from pywebio import start_server, config
import pywebio.platform
from pywebio.session import run_js, set_env
from pywebio.input import *





                    
def main():
    
    set_env(output_max_width="1000px")
    def login(data):
        if data['username'] == 'sightterp' and data['password'] == 'sightterp':
            return
        else:
            return ('password', 'Username or password is wrong')
            
    data = input_group("Sight-Terp Log-In",[
        input('Username', name='username', placeholder='Subscription Username', required=True),
        input('Password', name='password', type=PASSWORD, required=True)
    ], validate=login)
    

    toast('Authorization Successful!', color='success')
    # </Main layout>
    put_html(f"""
    <div class="page-header">
        <div style="text-align: center">
            <img src="https://iili.io/wgzx9a.jpg" alt="logo" />
            <p class="lead">BETA</p>
        </div>
      </div>
    """)

    
    put_info(put_html("<p>Press 'Start Recognition' to initiate speech translation. Allow your browser to use your microphone input.</p>").style("font-family: Poppins;white-space: pre-line; font-size: 14px; text-align: center"), closable=True)

     
 


    put_html("""<iframe src="https://translation-1.com/wp-content/uploads/sightconsecscripts/speech/new/index.html" allow="microphone *" 
    style="border: none; width: 100%; height: 230px"></iframe>""")
    



    def clearcanvas():
        clear(scope='canvaspart')
    

    
      
    
   # put_collapse('Entities', [put_scope("entitysection")],open=True)
   
    
    def scroll_top():
        scroll_to(position='top')
        
    
    def opencanvas():    
        put_scrollable([
            put_button('Hide Notepad', onclick=clearcanvas, color="info",small=True, outline=False).style('text-align: right;'),
            put_html("<center><h4>Digital Notepad (Beta)</h4></center>"),
            put_html("""<iframe src="https://www.translation-1.com/wp-content/uploads/sightconsecscripts/2/index.html" style="width: 720px; height: 2700px; border: none"></iframe>"""),
            put_button("Scroll to top", onclick=scroll_top, link_style=True)],
                       height=(200,0), width=0, keep_bottom=True, border=True, scope="canvaspart")

        
    put_column([put_button('Open Notepad', onclick=opencanvas, color="info",small=True, outline=True).style('text-align: center; font-family: Poppins')])

    put_row([put_scope('canvaspart'),
             ])
    
         
    put_html(f"""
    <div class="page-footer">
        <div style="text-align: center">
            <img src="https://iili.io/iIfSZ7.png" alt="logo" />
        </div>
      </div>
    """)


    put_success("Developed by Cihan Ünlü - All rights reserved.").style("font-family: Poppins; font-size: 13px; margin-top: 15px; text-align: center")

    
    
    put_tabs([{'title': 'About', 'content': """Sight-Terp is a prototype of a web-based ASR-supported CAI tool designed for consecutive interpreting modality. The tool initates continuous speech recognition which transcribes the source speech and simultaneously generates machine translated output of speech segments in vertically enumerated form.

Sight-Terp is non-commercial product used for educational and/or reserach purposes only.
        
The interface of the tool allows for two output contexts: the source transcription and the machine translation. The "Open Notepad" button opens the digital notepad which is implemented to allow the user carry out the note-taking practice using a stylus. The tool also incorporates Named Entity Recognition (NER), an out-sourced AI-based predictive model which identifies the named entities in the source speech and higlights them on the source text upon retrieval of the source transcript."""},
{'title': 'How to use', 'content': """Press "Start Recognition" button to start speech recognition. When browser wants to use the system microphone, click "Allow". The speech recognition model will listen to the audio input from your default microphone and simultaneously display the results on the adjacent boxes.  To stop the recognition, press "Stop Recognition.

For faster and reliable results, use the application in a silent enviroment and make sure the internet connection is strong."""},
    {'title': 'Research', 'content': """Sight-Terp is developed for an on-going MA Thesis at Hacettepe University by Cihan Ünlü.
The results of the research will be published soon."""},
    {'title': 'Used APIs', 'content': """APIs used in this project are:
for STT: Microsoft Azure Cognitive Services Speech Translation API
https://azure.microsoft.com/en-us/services/cognitive-services/speech-translation/
for NER: Microsoft Text Analytics API
https://azure.microsoft.com/tr-tr/services/cognitive-services/text-analytics/"""},
    {'title': 'Contact', 'content': 'cihan.unlu[at]yeniyuzyil.edu.tr'}]).style('font-family: Poppins; padding-top: 5px; padding-right: 20px; padding-bottom: 0px; padding-left: 20px; height:%100 ;width: %100; border-radius: 20px; font-size: 14px; box-sizing: none; border-color: #4fccda; position: relative; text-align: justify')
                     
config(theme="default", title="SightTerp - ASR-enhanced CAI Tool", css_file=["https://fonts.googleapis.com/css?family=Poppins","https://www.translation-1.com/wp-content/uploads/sightconsecscripts/2/highlight.css"])
# pywebio.platform.flask.start_server(main, debug=True, port=8080)
if __name__ == '__main__':
    pywebio.platform.tornado_http.start_server(main, debug=True, session_expire_seconds=3600, session_cleanup_interval=3600)
