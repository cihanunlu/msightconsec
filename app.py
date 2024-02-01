from pywebio.output import *
from pywebio import config
from pywebio.session import run_js, set_env
from pywebio.input import *
from pywebio.session import set_env, run_js
from flask import Flask, session, redirect, request
from pywebio.platform.flask import webio_view
import requests
import os
import time


app = Flask(__name__)
app.secret_key = 'abc123'  # Set a secret key for session management
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

AUTH0_DOMAIN = "sight-terp.eu.auth0.com"
CLIENT_ID = "UHCEijykX5f9YAuKhM0lltQ8LdkBk8JJ"
CLIENT_SECRET = "10msQMo7kZqrV-S81QdYJuI0FfTmVKmi7ud4yuoAOnSA_c_sVQT8f_qPoQzUApfo"
REDIRECT_URI = "https://www.sightterp.net/callback"  # Adjust this to your actual redirect URI

def generate_auth0_url():
    return f"https://{AUTH0_DOMAIN}/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=openid"

def exchange_code_for_token(code):
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(url, json=data)
    return response.json()


def the_trial_expired():
    put_html(f"""
    <div class="page-header">
        <div style="text-align: center">
            <img src="https://iili.io/wgzx9a.jpg" alt="logo" />
        </div>
      </div>
    """).style("font-family: Poppins;white-space: pre-line; font-size: 6px; text-align: center; margin-top: 100px")
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
       Developed by <a href='https://www.linkedin.com/in/cihan-%C3%BCnl%C3%BC-a82448109' target="_blank">Cihan Ünlü</a> © 2024. All rights reserved</strong>
    </div>
    """
    put_html(hide_footer_css)
    # Display a header
    put_html("<h1>Trial Period Expired</h1>")

    # Informative message about trial expiration
    put_text("Your trial period has ended. We hope you enjoyed experiencing our services.")

    # Optionally, you can include an image that matches the context
    # put_image('url_to_some_relevant_image.png')

    # Add more descriptive text or instructions
    put_text("To continue enjoying full access, consider subscribing to one of our plans.")
    def show_subscribe_link():
        popup("Donate and get subscription", [
            put_markdown("Please [click here](http://www.practiceai.app/subscribe) to subscribe.")
        ])

    def contact_support():
        popup("Contact Us", [
            put_text("Interested in uninterrupted access? Opt for a one-time subscription."),
            put_html('For more details, reach out to us at: <a href="mailto:contact.practiceai@gmail.com">contact.practiceai@gmail.com</a>')
        ])

    put_buttons(['Subscribe', 'Contact Support'], onclick=[show_subscribe_link, contact_support], outline=True, link_style=True,)


@app.route('/', methods = ['GET', 'POST'])
def index():
    if 'authenticated' in session:
        return webio_view(main)()
    else:
        return redirect(generate_auth0_url())

@app.route('/callback', methods = ['GET', 'POST'])
def callback():
    error = request.args.get('error')
    error_description = request.args.get('error_description')

    if error == 'access_denied' and 'trial_expiration' in error_description:
        return redirect('/trial-expired')
    code = request.args.get('code')
    if code:
        token_info = exchange_code_for_token(code)
        if 'access_token' in token_info:
            session['authenticated'] = True
            return redirect('/')
    return 'Authentication failed', 401

@app.route('/trial-expired', methods = ['GET', 'POST'])
def trial_expired():
    return webio_view(the_trial_expired)()


                    
def main():
    
    set_env(output_max_width="1000px")
    

    # </Main layout>
    put_html(f"""
    <div class="page-header">
        <div style="text-align: center">
            <img src="https://iili.io/wgzx9a.jpg" alt="logo" />
            <p class="lead">v2</p>
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
       Developed by <a href='https://www.linkedin.com/in/cihan-%C3%BCnl%C3%BC-a82448109' target="_blank">Cihan Ünlü</a> © 2024. All rights reserved</strong>
    </div>"""
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


    

    
    
    put_tabs([{'title': 'About', 'content': """Sight-Terp is an innovative web-based tool designed to support interpreters by enhancing consecutive interpreting with advanced speech recognition technology. Developed as part of a thesis project, Sight-Terp seamlessly transcribes spoken language and provides real-time, machine-translated text in a clear, vertically arranged format. Compatible with various devices, including tablets, mobile phones, and computers, it offers a highly interactive and user-friendly interface.

Key features include:

Automatic Speech Recognition (ASR) for live transcription of source speech.
Neural Machine Translation (NMT/ST) for immediate, parallel translation of text.
Named Entity Recognition (NER) for real-time highlighting of important text elements.
An embedded third-party digital notepad designed to replicate the tactile experience of pen and paper, complete with scratch-out erasing and the ability to underline or circle key information.
Sight-Terp is particularly valuable in scenarios requiring consecutive interpreting, aiding interpreters with quick access to both source and translated text, as well as efficient note-taking capabilities. The incorporation of NER ensures interpreters can easily identify and emphasize critical data during sessions."""},
{'title': 'How to use', 'content': """
• Device Compatibility: Ensure your device—be it a tablet, mobile phone, or computer—is connected to the internet and has a functioning microphone. For faster and reliable results, use the application in a silent enviroment and make sure the internet connection is strong.
• Start Recognition: Begin your interpreting session by clicking the “Start Recognition” button. This activates the ASR feature, which starts transcribing the spoken language in real time.
• View Transcriptions and Translations: Observe the source speech transcription and the machine translation appearing side by side in two adjacent text boxes. The ASR provides the transcription, and the neural machine translation offers the translated text.
• Named Entity Recognition (NER): As the speech is being transcribed, named entities such as places, names, and organizations are automatically highlighted in the text, making it easier to identify key information quickly.
• Digital Notepad: For traditional note-taking, click the “Open Notepad” button to access the digital notepad. It’s a third-party application that integrates with Sight-Terp, allowing you to take notes using scratch-out erasing and line drawing for underlining or circling text.
• Annotation with a Stylus: If you’re using a tablet, employ a stylus for natural handwriting and annotation, which enhances the digital notepad experience to closely resemble writing on paper.
 """},
    {'title': 'Research', 'content': """Sight-Terp is developed for a unpublished MA Thesis at Hacettepe University by Cihan Ünlü.
    
You can cite Sight-Terp as :
     
Unlu, C. (2023). Automatic Speech Recognition in Consecutive Interpreter Workstation: Computer-Aided Interpreting Tool ‘Sight-Terp’[Unpublished MA Thesis, Hacettepe University]
     
Access the thesis: https://tez.yok.gov.tr/UlusalTezMerkezi/tezDetay.jsp?id=xXjvte8qjvnTCyLGLB6Juw&no=uUDKocNfltgRbUmPH5W3PA"""},
    {'title': 'Used APIs', 'content': """APIs used in this project are:
for STT: Microsoft Azure Cognitive Services Speech Translation API
https://azure.microsoft.com/en-us/services/cognitive-services/speech-translation/
for NER: Microsoft Text Analytics API
https://azure.microsoft.com/tr-tr/services/cognitive-services/text-analytics/"""},
{'title': 'Terms of Service', 'content': """Acceptance of Terms
By accessing and using the Sight-Terp tool, you acknowledge that you have read, understood, and agree to be bound by these terms of service. If you do not agree with any part of these terms, you must not use this tool.

Usage Guidelines
Sight-Terp is provided as a non-commercial prototype for educational and research purposes only. Any commercial use of the software without prior written permission from the author is strictly prohibited.

Intellectual Property Rights
The software, including its interface, source code, design, and associated documentation, is the intellectual property of the author of the thesis project under which Sight-Terp was developed.

User Responsibilities
Users are expected to utilize Sight-Terp responsibly and ethically. Users must not use the tool to transcribe or translate any content that is illegal, offensive, or infringes on the intellectual property rights of others.

Privacy Policy
Sight-Terp adheres to strict privacy standards. Users must consent to the collection and processing of any personal data as required for the functioning of the ASR and NMT features in accordance with our privacy policy.

Limitation of Liability
The author of Sight-Terp shall not be liable for any direct, indirect, incidental, special, or consequential damages resulting from the use or the inability to use the tool.
Please be aware that all audio inputs captured through the Sight-Terp tool's microphone feature are processed by Microsoft's speech recognition services. We do not retain control over the data once it is sent to Microsoft for processing. Sight-Terp is not responsible for the data handling practices of Microsoft. Users should review Microsoft’s terms of service and privacy policy to understand their data processing procedures before using the speech recognition features of Sight-Terp.

Modifications to Terms of Service
The author reserves the right to update or change these terms of service at any time without prior notice. Users are encouraged to review these terms periodically for any changes.

Governing Law
These terms of service are governed by the laws of the jurisdiction in which the author resides, without regard to its conflict of law provisions.

Contact Information
For any questions or concerns regarding these terms of service, users may contact the author via the provided contact information on the Sight-Terp platform.

By using Sight-Terp, you agree to adhere to the aforementioned terms of service.                                                                                                  

"""},
{'title': 'Contact', 'content': """All rights reserved. Cihan Ünlü.
 
cihan.unlu[at]yeniyuzyil.edu.tr"""}]).style('font-family: Poppins; padding-top: 5px; padding-right: 20px; padding-bottom: 0px; padding-left: 20px; height:%100 ;width: %100; border-radius: 20px; font-size: 12px; box-sizing: none; border-color: #4fccda; position: relative; text-align: justify')
                     
config(theme="default", title="SightTerp - ASR-enhanced CAI Tool",  js_file="https://code.jquery.com/jquery-1.10.2.js",css_file=["https://fonts.googleapis.com/css?family=Poppins","https://translation-1.com/wp-content/uploads/sightconsecscripts/speech/resizer.css"], css_style="""body {font-family: 'Poppins', sans-serif;}
       
       .webio-tabs > input[type=radio]:checked + label {
       
       border-bottom: 2px solid #2baecb;
        }
       
       ..markdown-body img {
       
       margin-top: 20px;
        }
       
       """)

if __name__ == '__main__':
    app.run(debug=True)

