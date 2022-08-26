import streamlit as st
import perprocessing
import pandas as pd
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go





st.sidebar.title("Watsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
     # To read file as bytes:\
     bytes_data = uploaded_file.getvalue()
     data = bytes_data.decode('utf-8')
     df = perprocessing.preprocessing(data)
     # st.dataframe(df)

     user_list = df['user'].unique().tolist()
     user_list.sort()
     user_list.insert(0,'Overall')
     seleted_user = st.sidebar.selectbox('Show Analysis wrt', user_list)

     st.success('Your chat uploaded successfully, Click on Show Analysis')
     if st.sidebar.button("Show Analysis"):
          st.title('Top Statistics')
          # st.title('--------------------------------------------')
          col1, col2, col3, col4 = st.columns(4)
          total_messeges, total_words, media, links = helper.fetch_stats(seleted_user, df)
          with col1:
               st.header('Total Messages')
               st.title(total_messeges)

          with col2:
               st.header('Total Words')
               st.title(total_words)

          with col3:
               st.header('Media Shared')
               st.title(media)

          with col4:
               st.header('Links Shared')
               st.title(links)


          st.title("Monthly Timeline")
          timeline = helper.get_month(seleted_user,df)
          fig = px.line(timeline, y='message', x='month',  width=785,height=600, template='plotly_dark', markers=True)
          st.plotly_chart(fig)

          st.title('Daily Timeline')
          dayline = helper.get_day(seleted_user,df)
          fig = px.line(dayline, y='message', x='date',  width=785,height=600, template='plotly_dark', markers=True)
          st.plotly_chart(fig)


          st.title("Activity Map")
          col1, col2 = st.columns(2)
          with col1:
               busyday = helper.most_busy_day(seleted_user, df)
               fig = px.bar(busyday, y='message', x='day', height=400,width=420, template='plotly_dark')
               st.plotly_chart(fig)
          with col2:
               busymonth = helper.most_busy_week(seleted_user,df)
               fig = px.bar(busymonth, y='message', x='month', height=400,width=420, template='plotly_dark')
               st.plotly_chart(fig)

          pivt = helper.weekly_activity_map(seleted_user,df)
          fig,ax = plt.subplots()
          sns.set(rc={'figure.facecolor': '7F5283'})
          ax = sns.heatmap(pivt.fillna(0),cmap="BuPu")
          st.pyplot(fig)


          if seleted_user=='Overall':
               most_busy_user = helper.most_busy_user(df)
               percentage_of_messages = helper.percentage_of_messages(df)
               col1, col2 = st.columns(2)
               with col1:
                    st.header("Messages Precentage")
                    st.dataframe(percentage_of_messages)
               with col2:
                    st.header('Most Busy Users')
                    fig = px.bar(most_busy_user, x='Name', y='Messages', template='plotly_dark', height=400,width=420)
                    st.plotly_chart(fig)




          st.title('Word Cloud')
          df_wc = helper.word_cloud(seleted_user, df)
          fig, ax = plt.subplots()
          ax.imshow(df_wc)
          st.pyplot(fig)

          st.title('Most Repeated Words')
          most_repeted_words = helper.most_repeated_words(seleted_user,df)
          fig = px.bar(most_repeted_words, y='message', x='count', width=785,height=600, template='plotly_dark')
          st.plotly_chart(fig)

          emoji = helper.emoji_use(seleted_user,df)

          col1, col2, col3, col4 = st.columns(4)

          with col1:
               st.header('Emoji used')
               st.dataframe(emoji)
          with col2:
               st.header('Most Repeated')
               fig, ax = plt.subplots()
               emoji_head=emoji.head(5)
               fig = px.pie(emoji_head, values='counter', names='emoji',color_discrete_sequence=px.colors.sequential.Teal_r,height=409,width=500)
               st.plotly_chart(fig)


else:
     st.subheader('Instructions:')
     st.caption("Export your chat from Watsapp")
     st.caption("Your Exported chat must be WITHOUT MEDIA")
     st.caption('Download or save your chat file and upload here to see the Magic!')
     st.image("https://fs.npstatic.com/userfiles/7715851/image/NextPit-Export-WhatsApp-Chat-1-w782.png")










