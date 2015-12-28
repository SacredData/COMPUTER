
def magicWord(voca):
    app_key = None
    if any(substring in 'task' for substring in voca):
        print "Magic word is 'task'"
        print "App is taskwarrior"
        app_key = "task"
    if any(substring in 'music' for substring in voca):
        print "Magic word is 'music'"
        print "App is deadbeef"
        app_key = "deadbeef"
    elif any(substring in 'track' for substring in voca):
        print "Magic word is 'track'"
        print "App is deadbeef"
        app_key = "deadbeef"
    elif any(substring in 'screenshot' for substring in voca):
        print "Magic word is 'screenshot'"
        print "App is scrot"
        app_key = "scrot"
    elif any(substring in 'time' for substring in voca):
        print "Magic word is 'time'"
        print "App is talking-clock"
        app_key = "talking-clock"
    # elif any(substring in 'todo' for substring in voca):
    #     print "Magic word is todo"
    #     print "App is sh"
    elif any(substring in 'switch' for substring in voca):
        print "Magic word is 'switch'"
        print "App is i3-msg"
        app_key = "i3-msg"
    elif any(substring in 'selfie' for substring in voca):
        print "Magic word is 'selfie'"
        print "App is fswebcam"
        app_key = "fswebcam"
    elif any(substring in 'paste' for substring in voca):
        print "Magic word is 'paste'"
        print "App is copyq"
        app_key = "copyq"
    elif any(substring in 'define' for substring in voca):
        print "Magic word is 'define'"
        print "App is sh"
        app_key = "sh"
    return app_key
