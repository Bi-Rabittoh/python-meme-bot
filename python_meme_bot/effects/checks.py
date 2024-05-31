
def tt_check(info):
    reply = info['reply']['text']
    content = info['content']['text']

    input_text = f"{reply} {content}".replace("\n", " ")

    if input_text.strip() == "":
        return None

    return input_text


def ttbt_check(info):
    reply = info['reply']['text'].strip()
    content = info['content']['text'].strip()

    if len(content.split("\n")) > 1:
        input_text = content
    else:
        input_text = f"{reply}\n{content}"

    if input_text.strip() == "":
        return None

    return input_text


def splash_check(info):
    reply = info['reply']['text']
    content = info['content']['text']

    if content.strip() == "":
        author = info['reply']['author']
        input_text = f"{author}\n{reply}"
    else:
        author = info['content']['author']
        input_text = f"{author}\n{content}"

    if len(input_text.strip().split("\n")) < 2:
        return None

    return input_text


def wot_check(info):
    reply = info['reply']['text']
    content = info['content']['text']

    input_text = f"{reply}\n{content}"

    if input_text.strip() == "":
        return None

    return input_text
