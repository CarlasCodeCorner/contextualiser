import pytest
import os
print(os.getcwd())
from langdetect_service.ldetect import detect_lang_from_paragraphs 

def test_base_case():
    payload ={'mongo_id':'56as5d46a5s4', 'paragraphs':['This is the first sentence.', 'This is the second sentence.']}
    
    payload =  detect_lang_from_paragraphs(payload)
    lang = payload['lang']
    assert lang == 'en'
    
def test_no_lang():
    payload ={'mongo_id':'56as5d46a5s4', 'paragraphs':[]}
    
    lang =  detect_lang_from_paragraphs(payload)
    lang = payload['lang']
    assert lang == 'no lang identified'
    
def test_input():
    payload =['56as5d46a5s4', 'paragraphs']
    
    with pytest.raises(TypeError):
        detect_lang_from_paragraphs(payload=payload)
    
if __name__ == '__main__':
    test_no_lang()
    test_base_case()
    test_input()