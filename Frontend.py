from distutils.command.install_egg_info import safe_name
import json

import requests
import streamlit as st

import clip_image_search.utils as utils
from st_clickable_images import clickable_images
import pandas as pd
from streamlit_player import st_player
from streamlit_elements import media
from streamlit_elements import elements, mui, html


SERVER_URL = "https://eventretrieval.one/api/v1/submit"
SESSION_ID  = "node0kv3avq01drpu1b6n5ytha1two8"
if 'query' not in st.session_state:
    st.session_state['query'] = 'clouds at sunset'

if 'result' not in st.session_state:
    st.session_state['result'] = []

if 'resultId' not in st.session_state:
    st.session_state['resultId'] = []

if 'prev_mode' not in st.session_state:
    st.session_state['prev_mode'] = ""

if 'click' not in st.session_state:
    st.session_state['click'] = -1

if 'max_showing' not in st.session_state:
    st.session_state['max_showing'] = 100

if 'res_vid' not in st.session_state:
    st.session_state['res_vid'] = []

if 'frame_id' not in st.session_state:
    st.session_state['frame_id'] = []

if 'index_mapping' not in st.session_state:
    with open('/mmlabworkspace/Students/AIC/ALL_3batch_metadata.json', 'r') as f:
        st.session_state['index_mapping'] = json.load(f)
if 'index_mapping_ocr' not in st.session_state:
    with open('/mmlabworkspace/Students/AIC/ALL_3batch_OCR_Metadata.json', 'r') as f:
        st.session_state['index_mapping_ocr'] = json.load(f)
if 'frame_id_mapping' not in st.session_state:
    with open('/mmlabworkspace/Students/AIC/Data_Batch3/keyframe_p_batch3/keyframe_p/result_batch1_2_3.json', 'r') as fi:
        st.session_state['frame_id_mapping'] = json.load(fi)


def handle_query(query, input_type, mode, max_attempts=1):
    if not query:
        st.sidebar.error("Please enter a query.")
        return

    if input_type == "image":
        st.sidebar.image(query)

    # for i in range(max_attempts):
    #     if i == 0:
    #         message = "Wait for it..."
    #     else:
    #         message = "The server needs some time to warm up..."
    with st.spinner("Wait for it..."):
        response = make_post_request(query, input_type, mode)
        # if response.status_code != 503:
        #     break

    return response


def make_post_request(query, input_type, mode):
    headers = {
        "Content-type": "application/json",
    }
    data = json.dumps({"query": query, "input_type": input_type, "mode": mode})
    print(data)
    response = requests.post(
        "http://192.168.20.154:2022/process", data=data, headers=headers)
    # return response
    print("response via PROCESS_TUAN", response)
    st.session_state['resultId'] = response.json()
    # return data
    # tmp = ["https://images.unsplash.com/photo-1565130838609-c3a86655db61?w=300",
    #         "https://images.unsplash.com/photo-1565372195458-9de0b320ef04?w=300",
    #         "https://images.unsplash.com/photo-1582550945154-66ea8fff25e1?w=300",
    #         "https://images.unsplash.com/photo-1591797442444-039f23ddcc14?w=300",
    #         "https://images.unsplash.com/photo-1518727818782-ed5341dbd476?w=300",
    #         ]
    result = []
    for id in st.session_state['resultId'][:500]:
        # print(str(response.content[id]))
        result.append("http://localhost:2024/getImage?id=" +
                      str(id) + "&mode=" + mode)
    return result


def paginator(label, items, items_per_page=200, on_sidebar=True):
    """Lets the user paginate a set of items.
    Parameters
    ----------
    label : str
        The label to display over the pagination widget.
    items : Iterator[Any]
        The items to display in the paginator.
    items_per_page: int
        The number of items to display per page.
    on_sidebar: bool
        Whether to display the paginator widget on the sidebar.

    Returns
    -------
    Iterator[Tuple[int, Any]]
        An iterator over *only the items on that page*, including
        the item's index.
    Example
    -------
    This shows how to display a few pages of fruit.
    >>> fruit_list = [
    ...     'Kiwifruit', 'Honeydew', 'Cherry', 'Honeyberry', 'Pear',
    ...     'Apple', 'Nectarine', 'Soursop', 'Pineapple', 'Satsuma',
    ...     'Fig', 'Huckleberry', 'Coconut', 'Plantain', 'Jujube',
    ...     'Guava', 'Clementine', 'Grape', 'Tayberry', 'Salak',
    ...     'Raspberry', 'Loquat', 'Nance', 'Peach', 'Akee'
    ... ]
    ...
    ... for i, fruit in paginator("Select a fruit page", fruit_list):
    ...     st.write('%s. **%s**' % (i, fruit))
    """

    # Figure out where to display the paginator
    if on_sidebar:
        location = st.sidebar.empty()
    else:
        location = st.empty()

    # Display a pagination selectbox in the specified location.
    items = list(items)
    n_pages = len(items)
    n_pages = (len(items) - 1) // items_per_page + 1
    def page_format_func(i): return "Page %s" % i
    page_number = location.selectbox(
        label, range(n_pages), format_func=page_format_func)

    # Iterate over the items in the page to let the user display them.
    min_index = page_number * items_per_page
    max_index = min_index + items_per_page
    import itertools
    return itertools.islice(enumerate(items), min_index, max_index)


if __name__ == "__main__":

    st.markdown(
        """
              <style>
              .block-container{
                max-width: 1200px;
              }
              div.row-widget.stRadio > div{
                flex-direction:row;
                display: flex;
                justify-content: center;
              }
              div.row-widget.stRadio > div > label{
                margin-left: 5px;
                margin-right: 5px;
              }
              .row-widget {
                margin-top: -25px;
              }
              section>div:first-child {
                padding-top: 30px;
              }
              div.reportview-container > section:first-child{
                max-width: 320px;
              }
              #MainMenu {
                visibility: hidden;
              }
              footer {
                visibility: hidden;
              }
              </style>""",
        unsafe_allow_html=True,
    )

    # st.caption("Query number:")
    # query_name = st.text_input("")
    # if 'query_name' not in st.session_state:
    #     print("IN IF", query_name)
    #     st.session_state['query_name'] = query_name
    # print("NAME", st.session_state['query_name'])
    # st.text("")
    
    _, c, d = st.columns((1, 3, 1))
    st.session_state.update(st.session_state)

    # c.caption("Query number:")
    # name_query = c.text_input("Query number", on_change = None, key ='query_id')
    # name_query = 'result'


    query = c.text_input("Query", on_change=None)
    
    # d.caption("Max img showing: ")
    max_showing = d.text_input("Max img showing", value=st.session_state['max_showing'],  on_change=None)

    c.text("")
    mode = c.radio("mode", ["caption", "ocr"])

    search_clicked = c.button('Search')
    c.text("")
    if search_clicked:
        st.session_state['res_vid'] = []
        st.session_state['frame_id'] = []

    if (max_showing != st.session_state['max_showing']):
        st.session_state['max_showing'] = max_showing

    # submit_btn = c.button("Submit")
    # if submit_btn:
    #     print("Submiting")
        
        # x = requests.get(f"{server}?item={video_id}&frame={frame_id}")
        
        # df = pd.DataFrame(
        #     list(zip(st.session_state['res_vid'], st.session_state['frame_id'])))
        # print('/home/tuanld/AIC/Frontend/result/{}.csv'.format(st.session_state['query_name']))
        # df.to_csv('/home/tuanld/AIC/Frontend/result/{}.csv'.format(st.session_state['query_name']),header=False, index=False)
        # st.session_state['res_vid'] = []
        # st.session_state['frame_id'] = []

    # print(st.session_state['prev_mode'] != mode)
    if len(query) > 0 and (st.session_state['query'] != query or st.session_state['prev_mode'] != mode):
        # print("prev: " ,st.session_state['query'])
        # print("query: " , query)
        st.session_state['query'] = query
        st.session_state['prev_mode'] = mode
        st.session_state['result'] = handle_query(query, "text", mode)
        clicked = -1

    print(st.session_state['result'][:int(st.session_state['max_showing'])])
    clicked = clickable_images(
        st.session_state['result'][:int(st.session_state['max_showing'])],
        titles=[f"Image #{str(i)}" for i in range(5)],
        div_style={"display": "flex",
                   "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "150px"},
        key=query + "1",
    )

    if len(st.session_state['resultId']) > 0:
        c.caption("Total query result: " +
                  str(len(st.session_state['resultId'])))
        if clicked != -1:

            st.sidebar.title("Selected image")
            st.markdown(
                """
                    <style>
                    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
                        width: 500px;
                    }
                    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
                        width: 500px;
                        margin-left: -500px;
                    }
                    </style>
                    """,
                unsafe_allow_html=True,
            )
            print(st.session_state['result'][clicked])
            resized_image = utils.load_image_from_url(
                f"{st.session_state['result'][clicked]}")
            st.sidebar.image(resized_image)
            _, aa, _ = st.sidebar.columns((50, 5, 5))
            add_btn = aa.button("submit")

            
            
            if mode == "caption":
                vid_id = st.session_state['index_mapping'][str(st.session_state['resultId'][clicked])]['video_id']
                frame_id = st.session_state['index_mapping'][str(st.session_state['resultId'][clicked])]['image_name'][:-4]
            else:
                vid_id = st.session_state['index_mapping_ocr'][str(st.session_state['resultId'][clicked])]['video_name']
                frame_id =  st.session_state['index_mapping_ocr'][str(st.session_state['resultId'][clicked])]['image_name'][:-4]
            print(str(st.session_state['resultId'][clicked]), frame_id)
            # if int(frame_id) %5 !=0:
            try:
                new_frame_id = st.session_state['frame_id_mapping'][vid_id +".csv"][frame_id + '.jpg']
            # else:
            except:
                new_frame_id = frame_id

            st.sidebar.markdown( f"ImageId #{st.session_state['resultId'][clicked]}" + "\n" + f"Video: {vid_id}\n" + f"Frame_id: {new_frame_id}\n")

            result = (requests.get("http://192.168.20.154:2024/getClipID2",params={"id": st.session_state['resultId'][clicked], "mode": mode, "new_frame_id": new_frame_id})).json()
        #   st.sidebar.markdown(f"(ClipID: {result['clip_id']}, Timecode: {result['timecode']}, Frameids: {result['frame_idx']})")
        #   s = int(result['timecode'][0:2]) *3600 + int( result['timecode'][3:5]) * 60 + int(result['timecode'][6:8])

            #

        #   print("http://192.168.50.239:9235/" + result['image_folder'][:5] +  "videos/" + result['image_folder'][5:] + "/" + result['image_folder'][5:]  + ".mp4")
        #   video_url = "http://192.168.50.239:9235/" + result['image_folder'][:5] +  "videos/" + result['image_folder'][5:] + "/" + result['image_folder'][5:]  + ".mp4"
        #   st.sidebar.markdown(result['image_folder'][:5] +  "videos/" + result['image_folder'][5:] + "/" + result['image_folder'][5:]  + ".mp4" )

            st.sidebar.video(result['video_path'], format="video/mp4", start_time=result['timecode'])

            # with st.sidebar:
            #     # player = st_player(url="http://localhost:2023/getVideo?video_path=")
            #     # st.write(player)
            #     with elements("media_player"):
            #         from streamlit_elements import media
            #         media.Player(url="http://localhost:2023/getVideo?video_name=123", controls=True) #vid_id
                    

            if (add_btn):
                print ("Submited " + "item", vid_id, "frame",int(new_frame_id))
                # requests.get("http://192.168.20.154:5002/submit",params={"id": st.session_state['resultId'][clicked], "mode" : mode})
                st.session_state['res_vid'].append(vid_id)
                st.session_state['frame_id'].append(new_frame_id)
                # x = requests.get(SERVER_URL, params={"item": vid_id[:-4], "frame":new_frame_id, "session": SESSION_ID})
                x = requests.get(SERVER_URL, params={"item": vid_id, "frame":int(new_frame_id), "session": SESSION_ID})

                print("respond: ",x)

    else:
        c.title("No result")
