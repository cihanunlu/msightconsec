from cgitb import html
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from pywebio.output import put_text, put_scrollable, put_column, put_button, put_info, put_markdown, put_success, put_html, put_processbar, toast, put_scope, put_buttons, put_row, clear, put_tabs, put_buttons, scroll_to
from pywebio import start_server, config
import pywebio.platform
from pywebio.session import run_js, set_env
from pywebio.input import *





                    
def main():
    
    set_env(output_max_width="1000px")
    

    # </Main layout>
    put_html(f"""
    <div class="page-header">
        <div style="text-align: center">
            <img src="https://iili.io/wgzx9a.jpg" alt="logo" />
            <p class="lead">BETA</p>
        </div>
      </div>
    """)
    hide_footer_css = """
    <style>
        .footer {
            display: none;
        }
        .custom-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 0.8em;
            padding: 1em 0;
            background-color: #f8f9fa;
            border-top: 1px solid #dee2e6;
            z-index: 999;
        }
    </style>
    <div class="custom-footer">
       <strong> Developed by <a href='https://www.linkedin.com/in/cihan-%C3%BCnl%C3%BC-a82448109' target="_blank">Cihan Ünlü</a></strong>
    </div>
    """
    put_html(hide_footer_css)


    put_info(put_html("<p>Press 'Start Recognition' to initiate speech translation. Allow your browser to use your microphone input.</p>").style("font-family: Poppins;white-space: pre-line; font-size: 14px; text-align: center"), closable=True)


 


    put_html("""<iframe id="inneriframe" src="https://translation-1.com/wp-content/uploads/sightconsecscripts/speech/new/index.html" allow="microphone *" 
    style="border: none; min-width: 100%; height: 400px"></iframe>""")
    



    def clearcanvas():
        clear(scope='canvaspart')
    

   # put_collapse('Entities', [put_scope("entitysection")],open=True)
   
    
    def scroll_top():
        scroll_to(position='top')
        
    
    def opencanvas():    
        put_scrollable([
            put_button('Hide Notepad', onclick=clearcanvas, color="info",small=True, outline=False).style('text-align: right;'),
            put_html("<center><h4>Digital Notepad (Beta)</h4></center> <center> <h6>Powered by Myscript</h6></center>").style("font-family: Poppins"),
            put_html("""<iframe src="https://www.translation-1.com/wp-content/uploads/sightconsecscripts/2/index.html" style="min-width: 100%; height: 2700px; border: none"></iframe>"""),
            put_button("Scroll to top", onclick=scroll_top, link_style=True)],
                       height=(None,None), keep_bottom=True, border=True, scope="canvaspart")

    run_js("""
    $(document).ready(function(){
        $(document).on("click","#SuperWebF1",function(){
            $('#inneriframe', window.parent.document).css({"height":"1400px"});
            });
      });
    
    """)
    put_column([put_button('Open Notepad', onclick=opencanvas, color="info",small=True, outline=True).style('text-align: center; font-family: Poppins')])
    put_html("""<center><div><button type="button" id="SuperWebF1">Enlarge</button> </div></center>""")
    
    put_column()
    put_row([put_scope('canvaspart'),
             ])
    

    put_html(f"""
    <div class="page-footer">
        <div style="text-align: center">
            <img src="https://iili.io/iIfSZ7.png" alt="logo" />
        </div>
      </div>
    """)


    

    
    
    put_tabs([{'title': 'About', 'content': """Sight-Terp is a web-based ASR-supported CAI tool designed for consecutive interpreting modality. The tool initates continuous speech recognition which transcribes the source speech and simultaneously generates machine translated output of speech segments in a vertically enumerated form and layout.

Sight-Terp is non-commercial product used for educational and/or reserach purposes only.
        
The interface of the tool shows two automatically-generated reference texts: (1) the source transcription through ASR and (2) the machine translation through Speech Translation.

The "Open Notepad" button opens the digital notepad. It is an optional third-party digital note-taking application. This application offers features like scratch-out erasing and the ability to draw lines by underlining or circling text. Designed to emulate the traditional pen-and-paper experience in consecutive interpreting, the digital notepad seeks to provide a familiar and comfortable environment for interpreters as they navigate the digital landscape.

The tool also incorporates Named Entity Recognition (NER), an out-sourced AI-based predictive model which identifies the named entities in the source speech and higlights them on the source text upon retrieval of the source transcript. As the recognition process unfolds, named entities within the text are dynamically highlighted in real-time, courtesy of named entity recognition technology. This feature allows interpreters to quickly identify and focus on key information as it appears throughout the text."""},
{'title': 'How to use', 'content': """To begin, click the "Start Recognition" button to initiate the speech translation session. When browser wants to use the system microphone, click "Allow".  As the speaker speaks, the ASR technology transcribes your words and generates machine-translated output, displayed in two adjacent text boxes for both source and target languages.
As the recognition runs, named entities in the text will be automatically highlighted in real-time to help you identify critical information.
If you prefer to take notes, utilize the optional digital notepad feature located at the bottom of the interface.
After the speech is completed, you can click on "Stop Recognition" and scroll up to see the translations/transcriptions and begin interpreting.

For faster and reliable results, use the application in a silent enviroment and make sure the internet connection is strong."""},
    {'title': 'Research', 'content': """Sight-Terp is developed for an on-going MA Thesis at Hacettepe University by Cihan Ünlü.
The results of the research will be published soon."""},
    {'title': 'Used APIs', 'content': """APIs used in this project are:
for STT: Microsoft Azure Cognitive Services Speech Translation API
https://azure.microsoft.com/en-us/services/cognitive-services/speech-translation/
for NER: Microsoft Text Analytics API
https://azure.microsoft.com/tr-tr/services/cognitive-services/text-analytics/"""},
    {'title': 'Contact', 'content': 'cihan.unlu[at]yeniyuzyil.edu.tr'}]).style('font-family: Poppins; padding-top: 5px; padding-right: 20px; padding-bottom: 0px; padding-left: 20px; height:%100 ;width: %100; border-radius: 20px; font-size: 12px; box-sizing: none; border-color: #4fccda; position: relative; text-align: justify')
                     
config(theme="default", title="SightTerp - ASR-enhanced CAI Tool",  js_file="https://code.jquery.com/jquery-1.10.2.js",css_file=["https://fonts.googleapis.com/css?family=Poppins","https://translation-1.com/wp-content/uploads/sightconsecscripts/speech/resizer.css"])
# pywebio.platform.flask.start_server(main, debug=True, port=8080)
if __name__ == '__main__':
    pywebio.platform.tornado_http.start_server(main, debug=True, session_expire_seconds=1500, session_cleanup_interval=360, allowed_origins="*")


