import requests
import json
from math import ceil
from time import sleep
import os
import lxml
import lxml.html.clean as clean
import re

api_template_base = f"https://api.pushshift.io/reddit/search/submission"
api_template_comments = f"https://api.pushshift.io/reddit/comment/search"


def get_api_route(num_of_posts, starting_timestamp, sorting_order="desc", subreddit="writingprompts"):
    return f"{api_template_base}/?subreddit={subreddit}&sort={sorting_order}&sort_type=created_utc&after={starting_timestamp}&before={starting_timestamp+2419200}&size={num_of_posts}&num_comments=>10"


def get_api_search_route(num_of_comments, post_id):
    return f"{api_template_comments}/?link_id={post_id}&limit={num_of_comments}"


def retrieve_posts(num_of_posts, starting_timestamp, subreddit="writingprompts", recent_post=None, starting_posts=0):
    if starting_posts == 0:
        starting_posts = num_of_posts
    max_iterations = ceil(num_of_posts/starting_posts)
    print(f"posts left - {num_of_posts}")
    print(f"continue? - {max_iterations}")
    if max_iterations == 0:
        return recent_post
    else:
        route = get_api_route(num_of_posts, starting_timestamp=starting_timestamp)
        response = requests.get(route)
        if response.ok:
            response_content = response.json()
            with open(f"data/{starting_timestamp}.json", "w") as post:
                post.write(json.dumps(response_content, indent=4))
            sleep(1)
            if len(response_content['data']) > 0:
                retrieve_posts(num_of_posts-len(response.json()['data']), response.json()['data'][0]['created_utc']+2419200, recent_post=response.json()['data'][0], starting_posts=starting_posts)
        else:
            print("Request error!")


def scan_file_data():
    data_points = 0
    total_points = 0
    parsed_data = {'data': []}
    for filename in os.listdir("data"):
        print(f"Reading file: {filename}...")
        if not filename.endswith(".json"):
            continue
        with open(f"data/{filename}", "r") as json_file:
            json_content = json.loads(json_file.read())
        if not json_content:
            continue

        for i, item in enumerate(json_content['data']):
            # print(item)
            if not item.get('link_flair_text'):
                continue
            if item['link_flair_text'] != "Writing Prompt":
                continue
            if item['num_comments'] < 10:
                continue

            route = get_api_search_route(100, item['id'])
            response = requests.get(route)
            if response.ok:
                response_content = response.json()
                for x, comment in enumerate(response_content['data']):
                    total_points += 1
                    if comment.get('parent_id'):
                        if comment['parent_id'].split('_', 1)[1] != item['id']:
                            continue
                    if comment.get('allow_live_comments'):
                        continue
                    if comment.get('body'):
                        if len(comment['body']) > 50:
                            print(f"[{data_points}/{total_points}]-{comment['id']}")
                            parsed_data['data'].append(
                                {'id': comment['id'], 'text': comment['body'].strip().strip('\n')})
                            data_points += 1
    with open("parsed_data.json", "w") as json_pruned_file:
        json.dump(parsed_data, json_pruned_file, indent=4)


def clean_remaining_data():
    re_parsed = []
    item_count = 0
    total_items = 0
    with open("parsed_data.json", "r") as json_file:
        json_content = json.loads(json_file.read())
        for i, item in enumerate(json_content['data']):
            total_items += 1
            if "**Welcome to the Prompt!**" in item['text']:
                continue
            if "**Off-Topic Discussion**" in item['text']:
                continue
            if item['text'].startswith("Hi, there"):
                continue
            if item['text'].startswith("Hi there,"):
                continue
            if not item['text'][0].isalpha:
                continue
            item['text'] = item['text'].strip()
            doc = lxml.html.fromstring(item['text'])
            cleaner = clean.Cleaner(style=True)
            doc = cleaner.clean_html(doc)
            item['text'] = doc.text_content()
            item['text'] = item['text'].replace('\n', '')
            item['text'] = item['text'].replace('\\n', '')
            item['text'] = item['text'].replace('\t', '')
            item['text'] = item['text'].replace('\\t', '')
            item['text'] = item['text'].replace("\'", "'")
            item['text'] = item['text'].replace("\\'", "'")
            if re.search(r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""",
                         item['text']):
                continue
            re_parsed.append(item)
            print(f"[{item_count}/{total_items}]-{item}")
            item_count += 1
    with open("cleaned_data.json", "w") as json_file:
        json.dump({'data': re_parsed}, json_file, indent=4)
    with open("cleaned_data.txt", "w", encoding="utf-8") as txt_file:
        for i, item in enumerate(re_parsed):
            txt_file.write(f"{item['text']}\n")


if __name__ == '__main__':
    # Try to retrieve 100,000 posts from the since the given unix timestamp
    # This will most likely result in about 30,000 - 60,000 posts,
    # since there most likely isn't 100,000 posts to collect.
    retrieve_posts(100000, 1357016400)
    print("Retrieved posts!")
    scan_file_data()
    print("Scanned and parsed posts!")
    clean_remaining_data()
    print("Cleaned remaining data!")
