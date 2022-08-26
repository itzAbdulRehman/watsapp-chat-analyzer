from urlextract import URLExtract
url = URLExtract()
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji




def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    messages =  df.shape[0]
    words = []
    for i in df['message']:
        words.extend(i.split())

    media = df[df['message'] == "<Media omitted>\n"].shape[0]

    links = []
    for i in df['message']:
        links.extend(url.find_urls(i))

    return messages, len(words), media, len(links)

def most_busy_user(df):
    x = df['user'].value_counts().head().reset_index()
    x.rename(columns={'index': 'Name', 'user': 'Messages'}, inplace=True)
    return x

def percentage_of_messages(df):
    y = round((df['user'].value_counts() / len(df['message'])) * 100, 2).reset_index()
    y.rename(columns={'index': 'User', 'user': 'Percentage'}, inplace=True)
    return y

def word_cloud(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    temp = df[df['message'] != '<Media omitted>\n']
    temp_df = temp[temp['user'] != 'group_notification']

    f = open('englishST.txt', 'r', encoding='utf=8')
    cm = f.read()

    def remove_cm(message):
        words = []
        for word in message.lower().split():
            if word not in cm:
                words.append(word)
        return " ".join(words)
    temp_df['message'] = temp_df['message'].apply(remove_cm)

    wc = WordCloud(width=3000,
        height=2000,
        random_state=1,
        colormap="Pastel1",
        collocations=False)
    df_wc = wc.generate(temp_df['message'].str.cat(sep=" "))
    return df_wc

def most_repeated_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    temp = df[df['message'] != '<Media omitted>\n']
    temp_df = temp[temp['user'] != 'group_notification']

    f = open('englishST.txt', 'r', encoding='utf=8')
    cm = f.read()

    words = []
    for message in temp_df['message']:
        for word in message.lower().split():
            if word not in cm:
                words.append(word)

    most_repeted_words = pd.DataFrame(Counter(words).most_common(20))
    most_repeted_words.columns = ['message', 'count']

    # a = []
    # for item in most_repeted_words['message']:
    #     a.append(item.encode('ascii', 'ignore').decode('ascii'))
    #
    # most_repeted_words['message'] = a
    # most_repeted_words = most_repeted_words[most_repeted_words['message'] != '']
    # temp_df = most_repeted_words[:20]

    return most_repeted_words

def emoji_use(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])



    emo = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emo.columns=['emoji','counter']

    return emo

def get_month(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    df['month_num'] = df['message_date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month'])['message'].count().reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append((timeline['month'][i]) + '-' + (str(timeline['year'][i])))

    timeline['month'] = time
    return timeline

def get_day(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    df['date'] = df['message_date'].dt.date
    dateline = df.groupby('date')['message'].count().reset_index()
    return dateline

def most_busy_day(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    df['day_name'] = df['message_date'].dt.day_name()
    x = df['day_name'].value_counts().reset_index()
    x.columns = ['day','message']
    return x

def most_busy_week(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    x = df['month'].value_counts().reset_index()
    x.columns = ['month','message']
    return x

def weekly_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    pt = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count')
    return pt


