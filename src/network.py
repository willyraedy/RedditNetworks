import re
import math
from reddit import reddit_api_wrapper


def find_edges(reddit_name, reddit_type, dataframe, depth, multi_reddit_user=None):
    regex = re.compile('\/[r|m]\/\w+')
    desc = ''
    wiki = ''

    try:
        desc = dataframe.loc[reddit_name, 'description_html']
        wiki = dataframe.loc[reddit_name, 'wiki_text']
    except:
        b = 'c'
        # print(f'{reddit_name}')

    if type(wiki) != str:
        wiki = ''
    if type(desc) != str:
        desc = ''

    if reddit_type == 'm':
        try:
            multi = reddit_api_wrapper.multireddit(multi_reddit_user, reddit_name)
            new_tokens = list(map(lambda sub: sub.display_name, multi.subreddits))
            return list(map(lambda token: create_edge(
                token=token,
                raw_text='',
                type_of_edge='multi',
                parent_reddit=reddit_name,
                type_of_parent=reddit_type,
                depth=depth,
                parent_multi_user=multi_reddit_user
            ), new_tokens))
        except:
            return []

    raw_desc_tokens = list(map(lambda token: create_edge(
        token=token,
        raw_text=desc,
        type_of_edge='desc',
        parent_reddit=reddit_name,
        type_of_parent=reddit_type,
        depth=depth
    ), re.findall(regex, desc)))

    raw_wiki_tokens = list(map(lambda t: create_edge(token=t,
                                                     raw_text=wiki,
                                                     type_of_edge='wiki',
                                                     parent_reddit=reddit_name,
                                                     type_of_parent=reddit_type,
                                                     depth=depth
                                                     ), re.findall(regex, wiki)))

    return raw_desc_tokens + raw_wiki_tokens

def get_user_for_multi(multi, raw_text):
    rgx = re.compile('user/(\w+)/m/' + multi)
    m = re.search(rgx, raw_text)
    try:
        return m.group(1)
    except:
        return None

def create_edge(token, raw_text, parent_reddit, type_of_parent, type_of_edge, depth, parent_multi_user=None):
    if type_of_parent == 'm':
        return dict(parent=parent_reddit,
            type_of_parent=type_of_parent,
            parent_multi_user=parent_multi_user,
            reddit=token.lower(),
            type_of_reddit='r',
            context='',
            type_of_edge=type_of_edge,
            depth=depth)

    idx = raw_text.index(token)
    context = raw_text[idx - 200:idx + 200]
    cleaned = token.lower()[3:]
    type_of_reddit = token.lower()[1]

    multi_reddit_user = None if type_of_reddit == 'r' else get_user_for_multi(raw_text=raw_text, multi=cleaned)

    return dict(parent=parent_reddit,
                type_of_parent=type_of_parent,
                parent_multi_user=parent_multi_user,
                reddit=cleaned,
                type_of_reddit=type_of_reddit,
                multi_reddit_user=multi_reddit_user,
                context=context,
                type_of_edge=type_of_edge,
                depth=depth)


def fetch_network(reddit_name, dataframe, max_depth, reddit_type='r', excluded_list=[], depth=1, multi_reddit_user=None):
    network_edges = []
    edges = find_edges(reddit_name=reddit_name,
                       reddit_type=reddit_type,
                       multi_reddit_user=multi_reddit_user,
                       dataframe=dataframe,
                       depth=depth
                       )

    included_edges = list(
        filter(lambda e: e['reddit'] not in excluded_list, edges))

    network_edges = network_edges + included_edges
    if depth < max_depth:
        for edge in included_edges:
            network_edges = network_edges + fetch_network(
                edge['reddit'],
                dataframe,
                max_depth,
                edge['type_of_reddit'],
                excluded_list,
                depth + 1,
                multi_reddit_user=edge['multi_reddit_user']
            )
    return network_edges
