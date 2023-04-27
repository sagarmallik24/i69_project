import time

from googletrans import Translator


translator = Translator()

def language_translate(value, source_value, output_language):
    if not value:
        time.sleep(0.22)
        value = translator.translate(source_value, dest=output_language).text
        print(output_language, source_value, value)
    return value

def language_translate_everytime(value, source_value, output_language):
    time.sleep(0.22)
    value = translator.translate(source_value, dest=output_language).text
    print(output_language, source_value, value)
    return value

def translated_field_name(user, content):
    lang = user.user_language_code
    if lang and lang != 'en':
        # Handling Exceptions for chinese language 
        # becuase in the mobile app it is "zh" and in the server it is "zh-cn"
        lang = "zh_cn" if lang == 'zh' else lang 

        return content + "_" + lang
    return content

def custom_translate(user, value):
    lang = user.user_language_code
    lang = lang if lang else "en"
    lang = 'zh-cn' if lang == 'zh' else lang
    print(lang)
    if lang != "en":
        return translator.translate(
            value,
            dest=lang
        ).text
    return value
