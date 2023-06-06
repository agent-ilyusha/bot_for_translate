import googletrans
from googletrans import Translator


def translat(text_trans: str, key_lang: str) -> str:
    translator = Translator()
    trans_message = translator.translate(text=text_trans, dest=key_lang)
    return trans_message.text


def give_key_lang(mess):
    try:
        translator = Translator()
        lang = translator.translate(text=mess, dest='en').text.lower()
        if lang in list(googletrans.LANGUAGES.values()):
            ind_lang = list(googletrans.LANGUAGES.values()).index(lang)
            return list(googletrans.LANGUAGES.keys())[ind_lang]
        elif mess == 'китайский':
            return 'zh-cn'
        else:
            for key_lang, language in googletrans.LANGUAGES.items():
                try:
                    lang = translator.translate(text=language, dest='ru')
                    if mess.lower() == lang.text.lower() or mess.lower() == lang.text.lower() + 'ский':
                        return key_lang
                except AttributeError:
                    pass
    except TypeError:
        return 0
    return 0


def process_func(mess: str, key: str or int) -> str or int:
    if key == 0:
        return 0
    return translat(mess, key)





'''
translat - переводит текст. принимает текст и ключ языка.
give_key_lang - ищет ключ языка среди доступных, если не находит, то возвращает 0. принимает сообщение.
process_func - нужна для запуска функций. принимает сообщение и ключ.
'''
