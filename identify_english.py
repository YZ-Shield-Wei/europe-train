#!/usr/bin/env python3
"""
Script to identify English paragraphs in Italian HTML files that need translation.
This script extracts <p> tag contents and identifies which ones are in English.
"""

import os
import re
from pathlib import Path

def is_english_text(text):
    """
    Heuristic to determine if text is English (not Italian).
    Returns True if the text appears to be English and should be translated.
    """
    text = text.strip()
    
    # Skip empty or very short text
    if len(text) < 10:
        return False
    
    # Skip text that is clearly Italian (contains common Italian words/patterns)
    italian_indicators = [
        ' il ', ' la ', ' le ', ' gli ', ' lo ', ' i ',
        ' un ', ' una ', ' uno ', ' del ', ' della ', ' dei ', ' delle ',
        ' che ', ' chi ', ' con ', ' per ', ' tra ', ' fra ',
        ' sono ', ' è ', ' sei ', ' siamo ', ' siete ', ' sono ',
        ' questo ', ' questa ', ' questi ', ' queste ',
        ' come ', ' dove ', ' quando ', ' perché ', ' perchè ', ' perche ',
        ' anche ', ' molto ', ' troppo ', ' tutto ', ' tutti ', ' ogni ',
        ' sempre ', ' mai ', ' spesso ', ' qualche ',
        ' prenotazione', ' biglietto', ' biglietti', ' treno', ' treni',
        ' viaggio', ' viaggi', ' stazione', ' stazioni',
        ' posto', ' posti', ' classe', ' tariffa', ' tariffario',
        ' guida', ' guide', ' consigli', ' risparmio',
        ' paesaggio', ' paesaggi', ' panoramico',
        ' informazioni', ' consigli', ' strutture',
        ' principali', ' popolari', ' correlati',
        ' punti chiave', ' aggiornato', ' tempo di lettura',
        ' tutti i diritti riservati',
        ' da ', ' di ', ' a ', ' in ', ' su ', ' da ', ' con ', ' per ',
    ]
    
    text_lower = text.lower()
    
    # If it contains strong Italian indicators, it's Italian
    italian_score = 0
    for indicator in italian_indicators:
        if indicator in text_lower:
            italian_score += 1
    
    # If strong Italian presence, skip
    if italian_score >= 2:
        return False
    
    # English indicators - common English words that don't exist in Italian
    english_indicators = [
        ' the ', ' and ', ' or ', ' but ', ' with ', ' from ', ' for ',
        ' you ', ' your ', ' we ', ' our ', ' they ', ' their ',
        ' can ', ' will ', ' would ', ' should ', ' could ', ' may ', ' might ',
        ' this ', ' that ', ' these ', ' those ',
        ' have ', ' has ', ' had ', ' having ',
        ' do ', ' does ', ' did ', ' doing ',
        ' get ', ' got ', ' getting ',
        ' make ', ' made ', ' making ',
        ' take ', ' took ', ' taken ', ' taking ',
        ' go ', ' went ', ' gone ', ' going ',
        ' come ', ' came ', ' coming ',
        ' see ', ' saw ', ' seen ', ' seeing ',
        ' know ', ' knew ', ' known ', ' knowing ',
        ' think ', ' thought ', ' thinking ',
        ' say ', ' said ', ' saying ',
        ' look ', ' looked ', ' looking ',
        ' use ', ' used ', ' using ',
        ' find ', ' found ', ' finding ',
        ' give ', ' gave ', ' given ', ' giving ',
        ' tell ', ' told ', ' telling ',
        ' work ', ' worked ', ' working ',
        ' call ', ' called ', ' calling ',
        ' try ', ' tried ', ' trying ',
        ' need ', ' needed ', ' needing ',
        ' feel ', ' felt ', ' feeling ',
        ' become ', ' became ', ' becoming ',
        ' leave ', ' left ', ' leaving ',
        ' put ', ' putting ',
        ' mean ', ' meant ', ' meaning ',
        ' keep ', ' kept ', ' keeping ',
        ' let ', ' letting ',
        ' begin ', ' began ', ' begun ', ' beginning ',
        ' seem ', ' seemed ', ' seeming ',
        ' help ', ' helped ', ' helping ',
        ' show ', ' showed ', ' shown ', ' showing ',
        ' hear ', ' heard ', ' hearing ',
        ' play ', ' played ', ' playing ',
        ' run ', ' ran ', ' running ',
        ' move ', ' moved ', ' moving ',
        ' live ', ' lived ', ' living ',
        ' believe ', ' believed ', ' believing ',
        ' bring ', ' brought ', ' bringing ',
        ' happen ', ' happened ', ' happening ',
        ' stand ', ' stood ', ' standing ',
        ' lose ', ' lost ', ' losing ',
        ' pay ', ' paid ', ' paying ',
        ' meet ', ' met ', ' meeting ',
        ' include ', ' included ', ' including ',
        ' continue ', ' continued ', ' continuing ',
        ' set ', ' setting ',
        ' learn ', ' learned ', ' learning ',
        ' change ', ' changed ', ' changing ',
        ' lead ', ' led ', ' leading ',
        ' understand ', ' understood ', ' understanding ',
        ' watch ', ' watched ', ' watching ',
        ' follow ', ' followed ', ' following ',
        ' stop ', ' stopped ', ' stopping ',
        ' create ', ' created ', ' creating ',
        ' speak ', ' spoke ', ' spoken ', ' speaking ',
        ' read ', ' reading ',
        ' allow ', ' allowed ', ' allowing ',
        ' add ', ' added ', ' adding ',
        ' spend ', ' spent ', ' spending ',
        ' grow ', ' grew ', ' grown ', ' growing ',
        ' open ', ' opened ', ' opening ',
        ' walk ', ' walked ', ' walking ',
        ' win ', ' won ', ' winning ',
        ' offer ', ' offered ', ' offering ',
        ' remember ', ' remembered ', ' remembering ',
        ' love ', ' loved ', ' loving ',
        ' consider ', ' considered ', ' considering ',
        ' appear ', ' appeared ', ' appearing ',
        ' buy ', ' bought ', ' buying ',
        ' wait ', ' waited ', ' waiting ',
        ' serve ', ' served ', ' serving ',
        ' die ', ' died ', ' dying ',
        ' send ', ' sent ', ' sending ',
        ' expect ', ' expected ', ' expecting ',
        ' build ', ' built ', ' building ',
        ' stay ', ' stayed ', ' staying ',
        ' fall ', ' fell ', ' fallen ', ' falling ',
        ' cut ', ' cutting ',
        ' reach ', ' reached ', ' reaching ',
        ' kill ', ' killed ', ' killing ',
        ' remain ', ' remained ',
        ' suggest ', ' suggested ',
        ' raise ', ' raised ', ' raising ',
        ' pass ', ' passed ', ' passing ',
        ' sell ', ' sold ', ' selling ',
        ' require ', ' required ', ' requiring ',
        ' report ', ' reported ', ' reporting ',
        ' decide ', ' decided ', ' deciding ',
        ' pull ', ' pulled ',
        ' return ', ' returned ', ' returning ',
    ]
    
    english_score = 0
    for indicator in english_indicators:
        if indicator in text_lower:
            english_score += 1
    
    # If it has English indicators and low Italian score, it's English
    if english_score >= 2 and italian_score == 0:
        return True
    
    # Check for common English sentence starters
    english_starters = [
        'the ', 'a ', 'an ', 'this ', 'that ', 'these ', 'those ',
        'it ', 'its ', 'there ', 'here ', 'where ', 'when ', 'why ', 'how ',
        'what ', 'who ', 'which ', 'whose ', 'whom ',
        'if ', 'unless ', 'until ', 'while ', 'although ', 'though ',
        'because ', 'since ', 'as ', 'before ', 'after ', 'once ',
        'whether ', 'either ', 'neither ', 'both ', 'all ', 'some ',
        'many ', 'much ', 'more ', 'most ', 'few ', 'little ', 'less ',
        'least ', 'several ', 'various ', 'certain ',
        'every ', 'each ', 'any ', 'no ', 'not ', 'none ',
        'only ', 'just ', 'already ', 'yet ', 'still ', 'even ',
        'also ', 'too ', 'either ', 'neither ', 'rather ', 'quite ',
        'very ', 'so ', 'such ', 'too ', 'enough ', 'almost ',
        'nearly ', 'hardly ', 'barely ', 'scarcely ',
        'perhaps ', 'maybe ', 'probably ', 'possibly ', 'likely ',
        'certainly ', 'surely ', 'definitely ', 'absolutely ',
        'actually ', 'really ', 'truly ', 'indeed ', 'obviously ',
        'clearly ', 'apparently ', 'evidently ', 'presumably ',
        'fortunately ', 'unfortunately ', 'luckily ', 'hopefully ',
        'interestingly ', 'surprisingly ', 'amazingly ', 'remarkably ',
        'notably ', 'especially ', 'particularly ', 'specifically ',
        'mainly ', 'mostly ', 'largely ', 'partly ', 'generally ',
        'usually ', 'normally ', 'typically ', 'commonly ', 'often ',
        'frequently ', 'regularly ', 'rarely ', 'seldom ', 'sometimes ',
        'occasionally ', 'eventually ', 'finally ', 'ultimately ',
        'initially ', 'originally ', 'previously ', 'formerly ',
        'recently ', 'lately ', 'currently ', 'presently ',
        'immediately ', 'instantly ', 'directly ', 'straight ',
        'slowly ', 'quickly ', 'rapidly ', 'suddenly ', 'gradually ',
        'easily ', 'difficultly ', 'hardly ', 'smoothly ',
        'carefully ', 'cautiously ', 'recklessly ', 'wildly ',
        'beautifully ', 'wonderfully ', 'perfectly ', 'completely ',
        'totally ', 'entirely ', 'fully ', 'wholly ', 'utterly ',
        'extremely ', 'highly ', 'deeply ', 'strongly ', 'weakly ',
        'slightly ', 'somewhat ', 'kind of ', 'sort of ',
        'more or less ', 'at least ', 'at most ', 'at all ',
        'in fact ', 'of course ', 'for example ', 'for instance ',
        'in other words ', 'that is ', 'i.e. ', 'e.g. ',
        'in conclusion ', 'to sum up ', 'in summary ', 'overall ',
        'on the other hand ', 'however ', 'nevertheless ',
        'nonetheless ', 'still ', 'yet ', 'though ', 'although ',
        'even though ', 'even if ', 'whether or not ',
        'in addition ', 'furthermore ', 'moreover ', 'besides ',
        'what is more ', 'apart from ', 'except for ',
        'instead ', 'rather ', 'alternatively ', 'otherwise ',
        'therefore ', 'thus ', 'hence ', 'consequently ',
        'as a result ', 'because of ', 'due to ', 'owing to ',
        'thanks to ', 'according to ', 'in accordance with ',
        'in terms of ', 'with regard to ', 'with respect to ',
        'in relation to ', 'in connection with ',
        'compared to ', 'in comparison with ', 'unlike ',
        'similarly ', 'likewise ', 'in the same way ',
        'by contrast ', 'on the contrary ', 'conversely ',
        'first ', 'firstly ', 'second ', 'secondly ', 'third ', 'thirdly ',
        'next ', 'then ', 'afterwards ', 'subsequently ',
        'finally ', 'lastly ', 'in the end ', 'at last ',
        'meanwhile ', 'at the same time ', 'simultaneously ',
        'beforehand ', 'afterwards ', 'later ', 'earlier ',
        'soon ', 'shortly ', 'recently ', 'lately ',
        'now ', 'nowadays ', 'today ', 'currently ',
        'tomorrow ', 'yesterday ', 'tonight ',
    ]
    
    for starter in english_starters:
        if text_lower.startswith(starter):
            english_score += 2
    
    # Final decision
    if english_score >= 3 and italian_score == 0:
        return True
    
    return False


def extract_p_tags(filepath):
    """Extract all <p> tag contents from an HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all <p> tags and their content
    # Match <p> or <p class="..."> or <p ...>
    pattern = r'<p[^>]*>(.*?)</p>'
    matches = re.findall(pattern, content, re.DOTALL)
    
    results = []
    for match in matches:
        # Clean up the text - remove nested HTML tags
        clean_text = re.sub(r'<[^>]+>', '', match).strip()
        # Normalize whitespace
        clean_text = ' '.join(clean_text.split())
        if clean_text:
            results.append(clean_text)
    
    return results


def main():
    articles_dir = Path('/root/.openclaw/workspace/europe-train/it/articles')
    
    all_files = sorted(articles_dir.glob('*.html'))
    
    total_files = 0
    total_english_paragraphs = 0
    
    for filepath in all_files:
        total_files += 1
        paragraphs = extract_p_tags(filepath)
        
        english_paragraphs = []
        for p in paragraphs:
            if is_english_text(p):
                english_paragraphs.append(p)
        
        if english_paragraphs:
            print(f"\n{'='*80}")
            print(f"FILE: {filepath.name}")
            print(f"{'='*80}")
            print(f"Total <p> tags: {len(paragraphs)}")
            print(f"English paragraphs: {len(english_paragraphs)}")
            print()
            for i, p in enumerate(english_paragraphs, 1):
                print(f"  [{i}] {p[:200]}{'...' if len(p) > 200 else ''}")
            total_english_paragraphs += len(english_paragraphs)
    
    print(f"\n{'='*80}")
    print(f"SUMMARY: {total_files} files, {total_english_paragraphs} English paragraphs found")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
