import pandas as pd
import re


def preprocessing(data):

    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}(?:\s[A?PM]+)?\s-\s"
    dates = re.findall(pattern, data)
    messeges = re.split(pattern, data)[1:]
    df = pd.DataFrame({'user_messege': messeges, 'message_date': dates})
#     df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M - ')
    try:
        df['message_date'] = pd.to_datetime(df['message_date'],format='%m/%d/%y, %H:%M - ')
    except:
        df['message_date'] = pd.to_datetime(df['message_date'],format='%m/%d/%y, %I:%M %p - ')
    user = []
    messeges = []

    for messege in df['user_messege']:
        entry = re.split("([\w\W]+?):\s", messege)
        if entry[1:]:
            user.append(entry[1])
            messeges.append(entry[2])
        else:
            user.append('group_notification')
            messeges.append(entry[0])

    df['user'] = user
    df['message'] = messeges
    df.drop('user_messege', axis=1, inplace=True)

    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute
    df['day_name'] = df['message_date'].dt.day_name()

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        if hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        if (hour != 0) & (hour != 23):
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period

    return df
