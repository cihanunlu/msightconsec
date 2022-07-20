from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import time
import azure.cognitiveservices.speech as speechsdk
from pywebio.output import put_text, put_scrollable, put_column, put_button, put_info, put_warning, put_markdown, put_success, put_html, put_processbar, toast, put_scope, put_buttons, put_row, put_loading, put_link, popup, clear, put_collapse, put_buttons, scroll_to
from pywebio import start_server, config
import pywebio.platform
from pywebio.session import run_js
import flask
speech_key, service_region = "fb5bdd0e6eda4c919b6cd3da83360a8f", "westeurope"

def speech_recognize_continuous_from_file():
    
    
    """performs continuous speech recognition with input from an audio file"""
    # <SpeechContinuousRecognitionWithFile>
    transcriptlanguage = "en-US"
    targetlanguage = ('tr',)
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=speech_key, region=service_region,
        speech_recognition_language=transcriptlanguage,
        target_languages=targetlanguage)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    # Creates a translation recognizer using and audio file as input.
    speech_recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config, audio_config=audio_config)
    

    done = False

    def stop_cb(evt):
        """callback that stops continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True
    

    def keywordextraction():
        from azure.core.credentials import AzureKeyCredential
        from azure.ai.textanalytics import TextAnalyticsClient

        endpoint = "https://metinozetlemedeneme.cognitiveservices.azure.com/"
        key = "8382f4888efe4061a5a8740f2eab1b73"
        text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        put_scrollable([put_scope('phraseextractionpage')
                ], height=None, keep_bottom=True, scope="entitysection").style('color: black; font-size: 13px; text-align: left; background-color: white')
        try:
        
            response = text_analytics_client.extract_key_phrases(documents = entitybatch, language="en")

            result = [doc for doc in response if not doc.is_error]
            for doc in result:
                put_text(*doc.key_phrases, sep = "\n", scope="phraseextractionpage")

        except Exception as err:
            print("Encountered exception. {}".format(err))
        
        

    def sample_recognize_entities():
        endpoint = "https://metinozetlemedeneme.cognitiveservices.azure.com/"
        key = "8382f4888efe4061a5a8740f2eab1b73"
        text_analytics_client = TextAnalyticsClient(default_language="en",endpoint=endpoint, credential=AzureKeyCredential(key))
        showresult= ' ,'.join(transcriptresults)
        entitybatch.append(showresult)
        entityresult=[]
        response = text_analytics_client.recognize_entities(entitybatch)
        
        for result in response:
            for entity in result.entities:
                
                if entity.category == 'Organization':
                    entityresult.append("{} (Organization)".format(entity.text))
                if  entity.subcategory == 'DateRange':
                    entityresult.append("{} (Date Range)".format(entity.text))
                if  entity.subcategory == 'Number':
                    entityresult.append("{} (Number)".format(entity.text))
                if  entity.subcategory == 'Percentage':
                    entityresult.append(entity.text)
                if  entity.subcategory == 'Currency':
                    entityresult.append(entity.text)
                if  entity.subcategory == 'Ordinal numbers':
                    entityresult.append("{} (Ordinal)".format(entity.text))    
                if  entity.category == 'Person':
                    entityresult.append("{} (Person)".format(entity.text))
                if  entity.subcategory == 'GPE':
                    entityresult.append("{} (Country)".format(entity.text)) 
    
        put_scrollable([put_scope('entitypage'),
                put_text(*entityresult, sep = "\n", scope="entitypage"),
                ], height=None, keep_bottom=True, scope="entitysection").style('color: black; font-size: 12px; text-align: left; background-color: #F6F6F6')


    entitybatch=[]
    transcriptresults = []
    translationresults= []
    def handle_final_result(evt):
        transcriptresults.append(evt.result.text)
        translationresults.append(evt.result.translations['tr'])

    speech_recognizer.recognized.connect(handle_final_result)
    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)
    

    put_button('Stop Recognition', onclick=speech_recognizer.stop_continuous_recognition, scope='buttonpart', color="danger", outline=False).onclick(lambda: [sample_recognize_entities(), clear(scope="subbuttons"), toast("Recognition Stopped!", position='right', color='#4eccd9', duration=2)])
    
    put_button('Entities', onclick=sample_recognize_entities, scope='buttonpart', color="danger", outline=True, small=True).style('text-align: left;'),
    put_button('Extract Key Phrases', onclick=keywordextraction, scope='buttonpart', color="danger", outline=True, small=True).style('text-align: left;')

    
    
    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    toast("Recognition Started!", position='right', color='#4eccd9', duration=2)
    while not done:
        time.sleep(0.5)

    

    #f = open(transcript_file_path, "w")
    #for content in transcriptresults:
    #    f.write(content)
    #f.close()
    #print("Transcript Done")
    
    #f = open(translation_file_path, "w")
    #for content in translationresults:
    #    f.write(content)
    #f.close()
    #print("Translation Done.")
    
    #Displaying the transcription and translation results on the scrollable areas.
    put_text('\n\n'.join(['{} -  {}'.format(i, val) for i, val in (enumerate(transcriptresults, start=1))]), sep = "\n  • ", scope="transcriptpage")
    put_text('\n\n'.join(['{} -  {}'.format(i, val) for i, val in (enumerate(translationresults, start=1))]), sep = "\n  •  ", scope="translationpage")
      

                    
def main():
    # </Main layout>
    put_html(f"""
    <div class="page-header">
        <div style="text-align: center">
            <img src="https://iili.io/wgzx9a.jpg" alt="logo" />
            <p class="lead">BETA</p>
        </div>
      </div>
    """)
    put_info(put_html("<h8>Press start to initate speech recognition. To get transcription results, press 'Stop Recognition' button.</h8>"), closable=True)
    put_markdown("### Source Transcript")
    put_scrollable([
        put_scope('transcriptpage'),
        put_row([put_scope("subbuttons")])], height=(100,None), keep_bottom=True, border=True)
    
    def clearall():
        clear(scope="translationpage")  
        clear(scope="transcriptpage")
        clear(scope="buttonpart")
        clear(scope="entitysection")
        clear(scope="entitysection")

    def clearcanvas():
        clear(scope='canvaspart')
    
    put_row([
        put_scope('buttonpart'),
        put_button('Start Recognition', onclick=speech_recognize_continuous_from_file, color="info", outline=False).onclick(lambda: put_loading(shape='grow', color='danger', scope='subbuttons')),
        put_button('Clear All', onclick=clearall, color="secondary", scope='buttonpart', small=True).style('text-align: right;')
    ])

    
      
    
    put_collapse('Entities', [put_scope("entitysection")],open=True)
    put_collapse('Machine Translation', [put_scope("translationcollapse"),
    put_scrollable(put_scope('translationpage'), height=(5,None), keep_bottom=True, border=False)],open=False)
   
    
    def scroll_top():
        scroll_to(position='top')
        
    
    def opencanvas():    
        put_scrollable([
            put_button('Hide Notepad', onclick=clearcanvas, color="info",small=True, outline=False).style('text-align: right;'),
            put_html("<center><h4>Digital Notepad (Beta)</h4></center>"),
            put_html("""<iframe src="http://www.translation-1.com/wp-content/uploads/sightconsecscripts/2/index.html" style="width: 800px; height: 2700px; border: none"></iframe>"""),
            put_button("Scroll to top", onclick=scroll_top, link_style=True)],
                       height=2900, width=800, keep_bottom=True, border=True, scope="canvaspart")

        
    put_column([put_button('Open Notepad', onclick=opencanvas, color="info",small=True, outline=True)])

    put_row([put_scope('canvaspart'),
             ])
    
            
    
    put_warning(
        put_markdown('### Info!'),
        "This is the demo of SightTerp, ASR-enhanced CAI tool. Please stay tuned.",
        closable=True)
    put_success("Developed by Cihan Ünlü - All rights reserved.")
    put_markdown("Process")
    put_processbar('processbar', 0.8)
    def apipopup():
        popup('STT and NER API', """APIs used in this project are:
for STT: Microsoft Azure Cognitive Services Speech Translation API
https://azure.microsoft.com/en-us/services/cognitive-services/speech-translation/
for NER: Microsoft Text Analytics API
https://azure.microsoft.com/tr-tr/services/cognitive-services/text-analytics/""", size='large')
    def contactpopup():
        popup('Contact e-mail', 'cihan.unlu[at]yeniyuzyil.edu.tr', size='small')
    def aboutpopup():
        popup('About this project', """Sight-Terp is non-commercial product used for educational and/or reserach purposes only.

Sight-Terp is a prototype of a web-based ASR-supported CAI tool that initiates one-shot speech recognition and transcribes the source speech input by the speaker and automatically generates machine translated output of speech segments after the recognition is stopped by the user (interpreter).
        
The interface of the tool allows for two output contexts for interpreter to interpret from, one is the source transcription, and the other is the machine translation. Above all, a digital notepad is also implemented to allow participants carry out the note-taking practice using a stylus. The tool also incorporates Named Entity Recognition (NER), an out-sourced AI-based predictive model which identifies and categorizes named entities from the source speech and vertically displays on the interface upon retrieval of the source transcript.""", size='large')
    def researchpopup():
        popup('Research', """Sight-Terp is developed for an on-going MA Thesis at Hacettepe University by Cihan Ünlü.

The results of the research will be published soon.""", size='normal')
    
    put_row([
        put_button('Contact', onclick=contactpopup, color="info", link_style=True),
        put_button('About', onclick=aboutpopup, color="info", link_style=True),
        put_button('Used APIs', onclick=apipopup, color="info", link_style=True),
        put_button('Research', onclick=researchpopup, color="info", link_style=True)
    ])
    
                     
config(theme="default", title="SightTerp - ASR-enhanced CAI Tool", js_code="('.').highlightWithinTextarea({highlight: 'get'});", js_file="http://www.translation-1.com/wp-content/uploads/sightconsecscripts/2/mark.min.js" , css_file="http://www.translation-1.com/wp-content/uploads/sightconsecscripts/2/mark.css")
# pywebio.platform.tornado_http.start_server(main, port=8080, debug=True)
if __name__ == '__main__':
    pywebio.platform.flask.start_server(main, debug=True, port=8080)
