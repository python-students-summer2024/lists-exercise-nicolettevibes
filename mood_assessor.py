def assess_mood():
    import datetime
    date_today = str(datetime.date.today())

    if check_today_entry(date_today):
        print("Sorry, you have already entered your mood today.")
        return

    while True:
        mood = input("What's your current mood?").strip().lower()
        accepted_mood = ('happy', 'relaxed', 'apathetic', 'sad', 'angry')
        if mood in accepted_mood:
            mood_int = translate_mood(mood)
            save_mood(date_today, mood_int)
            diagnose_mood()
            break
        else:
            print("Please enter a valid mood.")

def translate_mood(mood):
    mood_to_int = {
        'happy': 2,
        'relaxed': 1,
        'apathetic': 0,
        'sad': -1,
        'angry': -2
    }
    return mood_to_int[mood]

from pathlib import Path

def check_today_entry(date_today):
    mood_file = Path('data/mood_diary.txt')
    if mood_file.exists():
        f = mood_file.open('r')
        try:
            for line in f:
                if date_today in line:
                    f.close()
                    return True
        except:
            f.close()
    else:
        return False

def save_mood(date_today, mood_int):
    data_subdir = Path('data')
    mood_file = data_subdir / 'mood_diary.txt'

    if not data_subdir.exists():
        data_subdir.mkdir()

    f = open(mood_file, 'a')
    f.write(f"{date_today} {mood_int}\n")
    f.close()

def diagnose_mood():
    mood_file = Path('data/mood_diary.txt')
    file = open(mood_file, 'r')
    lines = file.readlines()
    file.close()

    if len(lines) >= 7:
        last_seven_entries = lines[-7:]
    else:
        last_seven_entries = lines
        print("Not enough data for diagnosis.")
        return
    
    moods = []
    for line in last_seven_entries:
        parts = line.strip().split()
        mood_value = int(parts[-1])
        moods.append(mood_value)
    if moods:
        average_mood = round(sum(moods) / len(moods))
    else:
        average_mood = None

    mood_count = {'happy': 0, 'relaxed': 0, 'apathetic': 0, 'sad': 0, 'angry': 0}
    for mood in moods:
        if mood == 2:
            mood_count['happy'] += 1
        elif mood == 1:
            mood_count['relaxed'] += 1
        elif mood == 0:
            mood_count['apathetic'] += 1
        elif mood == -1:
            mood_count['sad'] += 1
        elif mood == -2:
            mood_count['angry'] += 1

    if mood_count['happy'] >= 5:
        diagnosis = 'manic'
    elif mood_count['sad'] >= 4:
        diagnosis = 'depressive'
    elif mood_count['apathetic'] >= 6:
        diagnosis = 'schizoid'
    else:
        mood_int = {2: 'happy', 1: 'relaxed', 0: 'apathetic', -1: 'sad', -2: 'angry'}
        diagnosis = mood_int[average_mood]

    print(f"Your diagnosis: {diagnosis}!")
