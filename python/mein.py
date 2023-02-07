
import openai
import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup
import spacy


def openai_req(req):
    openai.api_key = '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'
    openai.organization = 'org-yqLTtY3xD2oElWgXAWrALhfk'
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=req,
        temperature=0,
        max_tokens=4096 - len(req),
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    result = response.choices[0].text.strip()
    return result

def netdoktor_req(req):
    # Affenpocken, Herpes, Depression, etc.
    input = req.lower()
    URL = "https://www.netdoktor.de/krankheiten/" + input
    page = None
    page = requests.get(URL)
    text = ""
    if (page):
        soup = BeautifulSoup(page.content, "html.parser")
        intro = soup.find("section", {"class": "section section-1 section-type-diseases_description"})
        test = None
        test = intro.find_all('p')
        if (test):
            for p in test:
                text = text + p.text
    return text

def sims(text1, text2):
    nlp = spacy.load("de_core_news_lg")
    netDoktor = nlp(text1)
    chatGPT = nlp(text2)
    return netDoktor.similarity(chatGPT)

def openGUI():
    sg.theme('Default1')   # Add a touch of color
    # Layout for Inputs
    input_layout = [
            [sg.Text('OpenAI Input\t'), sg.Input(key='input_ai', size=(60, 20)), sg.Text('Web Input\t'), sg.InputText(key='input_web', size=(60, 20))]
    ]
    # Layout for Output
    output_layout = [
            [sg.Text('Open AI Output\t'), sg.Multiline(key='output_ai', size=(60, 20)), sg.Text('Web Output\t'), sg.Multiline(key='output_web', size=(60, 20))]
    ]
    # Layout for Output Results
    output_result_layout = [
            [sg.Text('Output\t\t'), sg.Input(key='output', size=(60, 20))]
    ]
    # Layout for Buttons
    button_layout = [
            [sg.Button('Run', key='btn_run', size=(10, 3)), sg.Button('Exit', key='btn_exit', size=(10, 3))]
    ]
    # Layout
    layout = [
            [sg.Column(input_layout)],
            [sg.Column(output_layout)],
            [sg.Column(output_result_layout)],
            [sg.Column(button_layout)]
    ]
    # Create the Window
    window = sg.Window('Window Title', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        match event:
            case 'btn_run':
                window['output_ai'].update(openai_req(values['input_ai']))
                window['output_web'].update(netdoktor_req(values['input_web']))
                window['output'].update(sims(values['input_web'], values['input_ai']))
            case sg.WIN_CLOSED:
                break
            case 'btn_exit':
                break
            case _:
                None
    window.close()

if __name__ == '__main__':
    openGUI()
