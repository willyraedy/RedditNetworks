import re
import math
import reddit_api_wrapper

def find_edges(reddit_name, reddit_type, dataframe, depth, multi_reddit_user=None):
    regex = re.compile('\/r\/\w+')
    desc = ''
    wiki = ''

    try:
        desc = dataframe.loc[reddit_name, 'description_html']
        wiki = dataframe.loc[reddit_name, 'wiki_text']
    except:
        print(f'{reddit_name}')

    if type(wiki) != str:
        wiki = ''
    if type(desc) != str:
        desc = ''

    if reddit_type == 'm':
        multi = reddit_api_wrapper.multireddit(multi_reddit_user, reddit_name)
        new_tokens = list(map(lambda sub: sub.display_name, multi.subreddits))
        return list(map(lambda token: create_edge(
                                                token=token,
                                                raw_text='',
                                                type_of_edge='multi',
                                                parent_reddit=reddit_name,
                                                type_of_parent=reddit_type,
                                                depth=depth
                                                ), new_tokens))

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


def create_edge(token, raw_text, parent_reddit, type_of_parent, type_of_edge, depth):
    idx = raw_text.index(token)
    context = raw_text[idx - 200:idx + 200]
    cleaned = token.lower()[3:]
    type_of_reddit=token.lower()[1]
    return dict(parent=parent_reddit, type_of_parent=type_of_parent, context=context, type_of_edge=type_of_edge, reddit=cleaned, type_of_reddit=type_of_reddit, depth=depth)

def fetch_network(reddit_name, dataframe, max_depth, excluded_list=[], depth=1):
    network_edges = []
    edges = find_edges(reddit_name, dataframe, depth)

    included_edges = list(filter(lambda e: e['reddit'] not in excluded_list, edges))

    network_edges = network_edges + included_edges
    if depth < max_depth:
        for edge in included_edges:
            network_edges = network_edges + fetch_network(edge['reddit'], dataframe, max_depth, excluded_list, depth + 1)
    return network_edges
