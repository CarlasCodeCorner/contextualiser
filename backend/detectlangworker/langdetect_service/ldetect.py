from langdetect import detect

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return 'no lang identified'
    

def detect_lang_from_paragraphs(payload:dict) -> dict:
    if type(payload) == dict:
        
        text = ''
        for i in range(len(payload['paragraphs'])):
            text = text + payload['paragraphs'][i]['text']
        
        lang = detect_language(text=text)
        payload['lang'] = lang
        return payload
    else:
        raise TypeError


