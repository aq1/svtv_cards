import random
from ast import literal_eval

from config import db, bot, chat_id, actual_pattern
from mini_logs import log
from tgstat_helper import fetch_posts_by_word


def create_pattern(pattern_name: str):
    magic_id = random.randint(1488, 4815162342)
    pattern_id = magic_id
    db.insert_patternDB((pattern_id, pattern_name))
    while db.select_several_wordDB((magic_id, magic_id+50)):
        log("oppa, magic_id's range is not unique, retry", 'create_pattern', "WARNING")
        magic_id = random.randint(1488, 4815162342)
    for x in range(50):
        db.insert_wordDB((magic_id+x, pattern_id, " ", " "))
    return True


def set_hiding(what, value: bool):
    if what not in ["forwards", "deleted", "chats"]:
        raise Exception("what you want to hide?")
    info = {"hide_" + what: value}
    db.update_actual_patternDB(**info)
    return True


async def spin_pattern():
    log("ok, spin me right round...", "spin_pattern", "INFO")
    pattern = db.select_actual_patternDB()
    if not pattern:
        log("there is no actual pattern", "spin_pattern")
        return
    words = db.select_several_wordDB2((pattern[0],))
    words = [x for x in words if x[1] and x[1].strip()]
    if not words:
        log("there is no words for actual pattern", "spin_pattern", 'INFO')
        return
    log(f"actual words: {', '.join(x[1] for x in words)}", "spin_pattern", "INFO")
    if actual_pattern['actual_word_id'] < 0:
        actual_pattern['actual_word_id'] = words[0][0]
    next_flag = False
    for x in words:
        if x[0] != actual_pattern["actual_word_id"]:
            if next_flag:
                actual_pattern['actual_word_id'] = x[0]
                log(f"successfully spinned, next word id {x[0]}", "spin_pattern", "INFO")
                return
            continue
        if not x[1] or not x[1].strip():
            log("empty, skipping...", "spin_pattern")
            next_flag = True
            continue
        log(f"start fetching by word {x[1]} with id {x[0]}, pattern id {pattern[0]}...", "spin_pattern", "INFO")
        try:
            res = db.select_channelDB()
            if not res:
                black_list = []
            else:
                black_list = literal_eval(res)
            answer = fetch_posts_by_word(
                x[1], x[2], black_list, interval=240*len(words))
        except Exception as e:
            log(str(e), "spin_pattern")
            answer = str(e)
        next_flag = True
        if answer:
            await bot.send_message(
                chat_id,
                answer,
                disable_web_page_preview=True
            )
    if next_flag:
        actual_pattern['actual_word_id'] = words[0][0]
    else:
        log("plz check words table content, it's very shitty situation", "spin_pattern")
        return
    log(f"successfully spinned, next word id {actual_pattern['actual_word_id']}", "spin_pattern", "INFO")
