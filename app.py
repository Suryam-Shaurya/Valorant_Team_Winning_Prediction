import streamlit as st
import pickle
import requests
from bs4 import BeautifulSoup
import pandas as pd

file = open('Valo_pred/model_without_agent.pkl', 'rb')
model = pickle.load(file)
file.close()

file = open('Valo_pred/scaler_no_agent', 'rb')
scaler_no_agent = pickle.load(file)
file.close()

file = open('Valo_pred/valo_dataset.pkl', 'rb')
valo_df = pickle.load(file)
file.close()

file = open('Valo_pred/pipe_with_agent.pkl', 'rb')
pipe_with_agent = pickle.load(file)
file.close()

valo_df.drop(['index'], axis = 1, inplace = True)
valo_df.drop_duplicates(keep = False, inplace = True)
valo_df.dropna(inplace = True)

st.title("Valorant Winning Prediction")

st.markdown('## :green[Map]')
map_ = st.selectbox(
    '''Map''',
    ('Lotus', 'Haven', 'Ascent', 'Icebox', 'Fracture', 'Split', 'Pearl', 'Bind'), label_visibility = 'collapsed')

col1, col2 = st.columns(2)

with col1:
    st.write("## :red[Team A]")
    A_player_1 = st.text_input('Player 1', placeholder='for example, Curator#7777', key = 'A_player_1')
    A_player_2 = st.text_input('Player 2', key = 'A_player_2')
    A_player_3 = st.text_input('Player 3', key = 'A_player_3')
    A_player_4 = st.text_input('Player 4', key = 'A_player_4')
    A_player_5 = st.text_input('Player 5', key = 'A_player_5')

with col2:
    st.write("## :orange[Team B]")
    B_player_1 = st.text_input('Player 1', placeholder='for example, Curator#7777', key = 'B_player_1')
    B_player_2 = st.text_input('Player 2', key = 'B_player_2')
    B_player_3 = st.text_input('Player 3', key = 'B_player_3')
    B_player_4 = st.text_input('Player 4', key = 'B_player_4')
    B_player_5 = st.text_input('Player 5', key = 'B_player_5')

player_id = [A_player_1, A_player_2, A_player_3, A_player_4, A_player_5,
             B_player_1, B_player_2, B_player_3, B_player_4, B_player_5]

riot_id = []
tagline = []
valid_data = True
for plar in player_id:
    cnt = player_id.count(plar)
    if cnt > 1 and plar != '':
        st.markdown('### :blue[Player ID must be unique]')
        valid_data = False
        break
    if '#' in plar:
        plar_ = plar.split('#')
        riot_id.append(plar_[0])
        tagline.append(plar_[1])
    else:
        if len(plar)==0:
            st.markdown('### :blue[Please enter player ID for all players]')
            valid_data = False
        else:
            st.markdown('### :red[Some player ID are not valid]')
            st.markdown(':red[Format: riot_id#tagline]')
            st.markdown(':red[Example: Curator#7777]')
            valid_data = False
        break


agent = ['reyna', 'sova', 'jett', 'omen', 'cypher',
         'sova', 'jett', 'breach', 'omen', 'killjoy']



def predict_output(riot_id = riot_id, tagline = tagline):
    def get_players_url(riot_id: [], tagline: [], ep = 7, act = 1):
        players_url = []
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
        for i in range(10):
            riot_id[i] = riot_id[i].replace(' ', '%20')
            url = f'https://blitz.gg/valorant/profile/{riot_id[i]}-{tagline[i]}?actName=e{ep}act{act}'
            players_url.append(url)
        return players_url

    def get_match_data(plr_, ser_rec=True, dta_rec=True):
        player_stat_lst = []
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

        url = plr_
        try:
            ser_rec = True
            webpage = requests.get(url, headers=headers).text
            soup = BeautifulSoup(webpage, 'html.parser')
        except:
            ser_rec = False

        if ser_rec:
            try:
                dta_rec = True
                player_stat = soup.find_all('div', class_ = 'â¡6b4dc2a9')[0].find_all('div', class_ = 'â¡196c999c')
            except:
                dta_rec = False

            if dta_rec:
                KD = float(player_stat[0].find_all('p', class_ = 'stat-data-point')[0].text.strip())
                Econ = float(player_stat[4].find_all('p', class_ = 'stat-data-point')[0].text.strip())
                avg_score = float(player_stat[3].find_all('p', class_ = 'stat-data-point')[0].text.strip())

                player_stat_lst.append(KD)
                player_stat_lst.append(Econ)
                player_stat_lst.append(avg_score)
                return player_stat_lst, ser_rec, dta_rec
            else:
                print("DATA NOT FOUND....!!!!")
                return 'DATA NOT FOUND....!!!!', ser_rec, dta_rec

        else:
            print('Server Not Reachable...:(')
            return 'Server Not Reachable...:(', ser_rec, dta_rec



    players_url = get_players_url(riot_id, tagline, 7, 1)

    all_plr_data = []
    for i, player in enumerate(players_url):
        faulty_plr = i
        print(player)
        to_add, server_reach, data_found = get_match_data(player)
        if not server_reach or not data_found:
            break
        else:
            all_plr_data.append(to_add)

    if server_reach & data_found:
        print('in................................................', server_reach, data_found)
        in_data = pd.DataFrame(columns = list(valo_df.columns))
        in_data['map'] = [map_]
        valo_agent_col = ['A_player_1_agent', 'A_player_2_agent', 'A_player_3_agent', 'A_player_4_agent', 'A_player_5_agent',
                          'B_player_1_agent', 'B_player_2_agent', 'B_player_3_agent', 'B_player_4_agent', 'B_player_5_agent']
        for i in range(1, 6):
            in_data[f'A_player_{i}_agent'] = [agent[i-1]]
            in_data[f'A_player_{i}_KD'] = all_plr_data[i-1][0]
            in_data[f'A_player_{i}_Econ'] = all_plr_data[i-1][1]
            in_data[f'A_player_{i}_avg_score'] = all_plr_data[i-1][2]

        for i in range(6, 11):
            in_data[f'B_player_{5 if i%5 == 0 else i%5}_agent'] = [agent[i-1]]
            in_data[f'B_player_{5 if i%5 == 0 else i%5}_KD'] = all_plr_data[i-1][0]
            in_data[f'B_player_{5 if i%5 == 0 else i%5}_Econ'] = all_plr_data[i-1][1]
            in_data[f'B_player_{5 if i%5 == 0 else i%5}_avg_score'] = all_plr_data[i-1][2]


        prediction = model.predict_proba(scaler_no_agent.transform(in_data.drop(valo_agent_col+['map']+['A_outcome'], axis=1)))

        win_per = str(round(prediction[0][1]*100, 2)) + '%'
        win_per_B = str(round(100.00 - round(prediction[0][1]*100, 2), 2)) + '%'
        st.write('## :blue[RESULT]')
        if round(prediction[0][1]*100, 2) > 50:
            st.write(f'## Winning chance of :red[Team A] is :green[{win_per}]:trophy:')
            st.write(f'## Winning chance of :orange[Team B] is :red[{win_per_B}]')
        else:
            st.write(f'## Winning chance of :red[Team A] is :red[{win_per}]')
            st.write(f'## Winning chance of :orange[Team B] is :green[{win_per_B}]:trophy:')

    else:
        if not server_reach:
            st.write('### :red[Server Not Reachable...:(:construction:]')
        elif not data_found:
            if faulty_plr < 5:
                st.write(f"### :red[DATA NOT FOUND for Team A's Player {faulty_plr+1}]:sneezing_face:")
            else:
                st.write(f"### :red[DATA NOT FOUND for] :orange[Team B's] :red[Player {faulty_plr-4}]:sneezing_face:")


if valid_data:
    st.markdown('### :green[All good! You can proceed to prediction...:wink:]')
    if st.button('Predict'):
        predict_output()
else:
    st.button('Predict', disabled=True)
