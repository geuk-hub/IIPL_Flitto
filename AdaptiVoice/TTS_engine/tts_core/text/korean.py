import re
import unicodedata

from transformers import AutoTokenizer

from . import punctuation, symbols


from num2words import num2words
from TTS_engine.tts_core.text.ko_dictionary import english_dictionary, etc_dictionary
from anyascii import anyascii
from jamo import hangul_to_jamo

def normalize(text):
    text = text.strip()
    text = re.sub("[⺀-⺙⺛-⻳⼀-⿕々〇〡-〩〸-〺〻㐀-䶵一-鿃豈-鶴侮-頻並-龎]", "", text)
    text = normalize_with_dictionary(text, etc_dictionary)
    text = normalize_english(text)
    text = text.lower()
    return text


def normalize_with_dictionary(text, dic):
    if any(key in text for key in dic.keys()):
        pattern = re.compile("|".join(re.escape(key) for key in dic.keys()))
        return pattern.sub(lambda x: dic[x.group()], text)
    return text


def normalize_english(text):
    def fn(m):
        word = m.group()
        if word in english_dictionary:
            return english_dictionary.get(word)
        return word

    text = re.sub("([A-Za-z]+)", fn, text)
    return text


g2p_kr = None
def korean_text_to_phonemes(text, character: str = "hangeul") -> str:
    global g2p_kr
    if g2p_kr is None:
        from g2pkk import G2p

        g2p_kr = G2p()

    if character == "english":
        from anyascii import anyascii
        text = normalize(text)
        text = g2p_kr(text)
        text = anyascii(text)
        return text

    text = normalize(text)
    text = g2p_kr(text)
    text = list(hangul_to_jamo(text))
    return "".join(text)

def text_normalize(text):
    text = normalize(text)
    return text


def distribute_phone(n_phone, n_word):
    phones_per_word = [0] * n_word
    for task in range(n_phone):
        min_tasks = min(phones_per_word)
        min_index = phones_per_word.index(min_tasks)
        phones_per_word[min_index] += 1
    return phones_per_word

model_id = 'kykim/bert-kor-base'
tokenizer = AutoTokenizer.from_pretrained(model_id)

def g2p(norm_text):
    tokenized = tokenizer.tokenize(norm_text)
    phs = []
    ph_groups = []
    for t in tokenized:
        if not t.startswith("#"):
            ph_groups.append([t])
        else:
            ph_groups[-1].append(t.replace("#", ""))
    word2ph = []
    for group in ph_groups:
        text = ""
        for ch in group:
            text += ch
        if text == '[UNK]':
            phs += ['_']
            word2ph += [1]
            continue
        elif text in punctuation:
            phs += [text]
            word2ph += [1]
            continue
        phonemes = korean_text_to_phonemes(text)
        phone_len = len(phonemes)
        word_len = len(group)

        aaa = distribute_phone(phone_len, word_len)
        assert len(aaa) == word_len
        word2ph += aaa

        phs += phonemes
    phones = ["_"] + phs + ["_"]
    tones = [0 for i in phones]
    word2ph =  [1] + word2ph + [1]
    assert len(word2ph) == len(tokenized) + 2
    return phones, tones, word2ph

def get_bert_feature(text, word2ph, device='cuda'):
    from . import japanese_bert
    return japanese_bert.get_bert_feature(text, word2ph, device=device, model_id=model_id)


if __name__ == "__main__":
    from text.symbols import symbols
    text = "전 제 일의 가치와 폰타인 대중들이 한 일의 의미를 잘 압니다. 앞으로도 전 제 일에 자부심을 갖고 살아갈 겁니다"
    import json

    genshin_data = json.load(open('/data/zwl/workspace/Genshin_Datasets/Index & Script/AI Hobbyist Version/Index/4.1/KR_output.json'))
    from tqdm import tqdm
    new_symbols = []
    for key, item in tqdm(genshin_data.items()):
        texts = item.get('voiceContent', '')
        if isinstance(texts, list):
            texts = ','.join(texts)
        if texts is None:
            continue
        if len(texts) == 0:
            continue

        text = text_normalize(text)
        phones, tones, word2ph = g2p(text)
        bert = get_bert_feature(text, word2ph)
        import  pdb; pdb.set_trace()
        for ph in phones:
            if ph not in symbols and ph not in new_symbols:
                new_symbols.append(ph)
                print('update!, now symbols:')
                print(new_symbols)
                with open('korean_symbol.txt', 'w') as f:
                    f.write(f'{new_symbols}')