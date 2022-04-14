from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
import time
import azure.cognitiveservices.speech as speechsdk
from pywebio.output import put_text, put_scrollable, put_column, put_button, put_info, put_warning, put_markdown, put_success, put_html, put_processbar, toast, put_scope, put_buttons, put_row, put_loading, put_link, popup, clear, put_collapse
from pywebio import start_server, config

speech_key, service_region = "fb5bdd0e6eda4c919b6cd3da83360a8f", "westeurope"
canvashtml=f"""
<html lang="en" >
<head>
  <meta charset="UTF-8">
  <title>CodePen - SketchApp</title>
  <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css'><link rel="stylesheet" href="http://translation-1.com/wp-content/uploads/2021/01/style.css">

</head>
<body>
<!-- partial:index.partial.html -->
<head>


  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.6.3/css/font-awesome.min.css">
  <link href="https://fonts.googleapis.com/css?family=Arimo|Cabin+Sketch|Dancing+Script|Parisienne|Special+Elite" rel="stylesheet">
  <title>Draw Tool</title>
</head>

<body>
  <div class="container-fluid">
    <div class="row">
      <div class="col-md-12" style="height:5vh;"></div>
    </div>
    <div class="row">
      <div class="toolbar col-md-2">
        <br>

        <div class="btn-toolbar center-block" role="toolbar">
          <button type="button" class="btn btn-secondary" id="eraser" onclick="eraser()"><i class="fa fa-eraser"></i></button>
          <button type="button" class="btn btn-secondary" id="pencil" onclick="pencil()"><i class="fa fa-pencil"></i></button>
          <button type="button" class="btn btn-secondary" id="pen" onclick="pen()"><span class="glyphicon glyphicon-pencil"></span></button>
          <button type="button" class="btn btn-secondary" id="text" onclick="textBox()"><i class="fa fa-font"></i></button>
          <button type="button" class="btn btn-secondary" id="save" onclick="savePic()"><span class="glyphicon glyphicon-floppy-disk"></span></button>
          <button type="button" class="btn btn-secondary" id="clear" onclick="clearAll()"><i class="fa fa-trash"></i></button>
        </div>
        <br>
        
      </div>
      <div class="sketchPad col-md-10">
        <canvas id="sketchPad" width="650" height="600">
					Not compatible with this browser
				</canvas>
      </div>
    </div>
  </div>
  
</body>
<!-- partial -->
  <script  src="http://translation-1.com/wp-content/uploads/2021/01/script.js"></script>

</body>
</html>
        
         """



def speech_recognize_continuous_from_file():
    
    
    """performs continuous speech recognition with input from an audio file"""
    # <SpeechContinuousRecognitionWithFile>
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=speech_key, region=service_region,
        speech_recognition_language='en-US',
        target_languages=('tr',))
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
    
    def sample_recognize_entities():
        endpoint = "https://metinozetlemedeneme.cognitiveservices.azure.com/"
        key = "8382f4888efe4061a5a8740f2eab1b73"
        text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        reviews = transcriptresults
        entityresult=[]
        
        response = text_analytics_client.recognize_entities(reviews)
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
                put_text(*entityresult, sep = "\n", scope="entitypage")
                ], height=120, keep_bottom=True, scope="entitysection").style('color: black; font-size: 13px; text-align: center; background-color: white')
        
        
    

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
    
   
    
   
    put_button('Stop Recognition', onclick=speech_recognizer.stop_continuous_recognition, scope='buttonpart', color="danger", outline=False)
    put_button('Entities', onclick=sample_recognize_entities, scope='buttonpart', color="danger", outline=True, small=True)
    
    
    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    toast("Recognition Started!", position='right', color='#4eccd9', duration=2)
    while not done:
        time.sleep(1)

    

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
    
    

    put_text(*transcriptresults, sep = " ", scope="transcriptpage")
    put_text(*translationresults, sep = " ", scope="translationpage")  

                    
def main():
    # </Main layout>
    put_html(f"""
    <div class="page-header">
        <div style="text-align: center">
            <img src="https://i.ibb.co/wR535T7/Blue-and-White-Ceramics-Etsy-Banner.png" alt="logo" />
            <p class="lead">BETA</p>
        </div>
      </div>
    """)
    put_info(put_html("<h8>Press start to initate speech recognition</h8>"), closable=True)
    put_markdown("### Source Transcript")
    put_scrollable([
        put_scope('transcriptpage')], height=200, keep_bottom=True, border=True)
    
    def clearall():
        clear(scope="translationpage")
        clear(scope="transcriptpage")
        clear(scope="buttonpart")
        clear(scope="entitysection")


    
    put_row([
        put_scope('buttonpart'),
        put_button('Start Recognition', onclick=speech_recognize_continuous_from_file, color="info", outline=False).onclick(lambda: put_loading(shape='grow', color='danger', scope='transcriptpage')),
        put_button('Clear All', onclick=clearall, color="secondary", scope='cleartranscriptbutton', small=True)
    ])
    
    put_row([put_scope('cleartranscriptbutton')])  

    put_row([put_scope('cleartranslationbutton')]) 
    
    put_collapse('Entities', [put_scope("entitysection")],open=True)
    put_markdown("### Machine Translation")
    put_scrollable(put_scope('translationpage'), height=200, keep_bottom=True)
    
    
    def opencanvas():    
        put_scrollable([
            put_html("""<iframe src="http://www.translation-1.com/wp-content/uploads/sightconsecscripts/index.html" style="width: 800px; height: 1500px; border: none"></iframe>""")],
                       height=800, width=800, keep_bottom=True, border=True, scope="canvaspart")

        
    
    put_row([put_scope('canvaspart'),
             ])
            
    put_button('Canvas', onclick=opencanvas, color="primary",small=True)
    # put_button('Hide Canvas', onclick=clear(scope='canvaspart'), color="primary",small=True)
    put_warning(
        put_markdown('### Warning!'),
        "This is the demo of M-SightConsecV1, please stay tuned",
        closable=True)
    put_success("All rights reserved - Cihan Ünlü")
    put_markdown("Process")
    put_processbar('processbar', 0.8)
    def contactpopup():
        popup('Contact e-mail', 'cihan.unlu[at]yeniyuzyil.edu.tr', size='small')
    def aboutpopup():
        popup('About this project', 'M-SightConsec is for education purposes only', size='small')
        
    put_row([
        put_column([None]),
        put_button('Contact', onclick=contactpopup, color="info", link_style=True),
        put_button('About', onclick=aboutpopup, color="info", link_style=True)
    ])
                   

config(theme="sketchy")  
start_server(main, debug=True, port=8080)