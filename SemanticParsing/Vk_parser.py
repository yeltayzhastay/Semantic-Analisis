import vk
import csv
import time

class Vk_parser:
    def __init__(self, token):
        session = vk.Session(access_token=token)
        self.vk_api = vk.API(session)
        self.result = []

    def parsing(self, group_urls, limit=100):
        results = [['group_url', 'user_id', 'first_name', 'last_name', 'sex', 'bdate', 'interests', 'books', 'tv', 'quotes', 'about', 'games', 'movies', 'music', 'status', 'followers_count', 'relation',
        'city', 'country', 
        'alcohol', 'life_main', 'people_main', 'political', 'smoking', 'religion',
        'langs', 'inspired_by',
        'text', 'comments', 'likes', 'reposts', 'views']]

        for group_url in group_urls:
            members = self.get_members(group_url)
            for member in members[:limit]:
                row = [group_url] + self.get_person_info(member)
                try:
                    row += self.get_posts(member)
                except:
                    row += ''
                results.append(row)
        self.result = results

    def parsing_info(self, urls, limit=100):
        results = [['group_url', 'user_id', 'first_name', 'last_name', 'sex', 'bdate', 'interests', 'books', 'tv', 'quotes', 'about', 'games', 'movies', 'music', 'status', 'followers_count', 'relation',
        'city', 'country', 
        'alcohol', 'life_main', 'people_main', 'political', 'smoking', 'religion',
        'langs', 'inspired_by']]

        for group_url in group_urls:
            members = self.get_members(group_url)
            for member in members[:limit]:
                results.append([group_url] + self.get_person_info(member))
        self.result = results

    def get_members(self, groupid):
        first = self.vk_api.groups.getMembers(group_id=groupid, v=5.92)
        data = first["items"]
        count = first["count"] // 1000
        for i in range(1, count+1):  
            data = data + self.vk_api.groups.getMembers(group_id=groupid, v=5.92, offset=i*1000)["items"]
        return data
    
    def get_person_info(self, user_id):
        user_features = ['id', 'first_name', 'last_name', 'sex', 'bdate', 'interests', 'books', 'tv', 'quotes', 'about', 'games', 'movies', 'music', 'status', 'followers_count', 'relation',
        'city', 'country', 
        'personal']
        personal_features = ['alcohol', 'life_main', 'people_main', 'political', 'smoking', 'religion',
        'langs', 'inspired_by']

        post_info = self.vk_api.users.get(user_id=user_id, v=5.92, fields='sex, bdate, city, country, status, followers_count, occupation, relatives, relation, personal, interests, music, movies, tv, books, games, about, quotes')[0]
        
        results = []
        for i in user_features:
            try:
                if i in ['city', 'country']:
                    results.append(post_info[i]['title'])
                elif i != 'personal':
                    results.append(post_info[i])
            except:
                results.append('')
            if i == 'personal':
                for j in personal_features:
                    try:
                        if j == 'langs':
                            results.append(' '.join(post_info[i][j]))
                        else:
                            results.append(post_info[i][j])
                    except:
                        results.append('')
        
        return results

    def get_posts(self, owner_id):
        post_features = ['text', 'comments', 'likes', 'reposts', 'views']

        post_info = self.vk_api.wall.get(owner_id=owner_id, v=5.92, count=1000)['items']

        iter = 0
        text = ''
        clrv = {'comments': 0, 'likes': 0, 'reposts': 0, 'views': 0}
        for post in post_info:
            try:
                for j in post_features:
                    if j in ['comments', 'likes', 'reposts', 'views']:
                        clrv[j] += post[j]['count']
                    else:
                        text += post[j] + ' '
                    iter += 1
            except:
                continue
        return [text, clrv['comments']/iter, clrv['likes']/iter, clrv['reposts']/iter, clrv['views']/iter]

    def parsing_group_post(self, group_urls, count=10):
        results = [['group_url', 'text', 'comments', 'likes', 'reposts']]
        for group_url in group_urls:
            results += self.get_group_posts(group_url, count)
        self.result = results

    def get_group_posts(self, owner_id, count=10):
        post_features = ['text', 'comments', 'likes', 'reposts']
        group_posts = []
        i = 1
        while i <= count:
            post_info = self.vk_api.wall.get(domain=owner_id, v=5.92, count=100, offset=i*100)['items']
            for post in post_info:
                try:
                    row = [owner_id]
                    for j in post_features:
                        if j in ['comments', 'likes', 'reposts']:
                            row.append(post[j]['count'])
                        else:
                            row.append(post[j])
                    group_posts.append(row)
                except:
                    continue
            i += 1
        return group_posts

    def Get_sentimental(self, group_urls, count=10):
        result = [['group_url', 'from_id', 'owner_id', 'text']]

        for group_url in group_urls:
            result += self.get_group_posts_all(group_url, count)
        self.result = result

    def get_group_posts_all(self, owner_id, count=10):
        post_features = ['from_id', 'owner_id', 'text']
        group_posts = []
        i = 1
        while i <= count:
            try:
                post_info = self.vk_api.wall.get(owner_id=-owner_id, v=5.92, count=100, offset=i*100)['items']
                time.sleep(2)
                for post in post_info:
                    try:
                        row = [owner_id]
                        for j in post_features:
                            row.append(post[j])
                        group_posts.append(row)
                    except:
                        continue
            except:
                pass
            i += 1
        return group_posts

    def SearchGroup(self, text):
        groups_ = self.vk_api.search.getHints(limit=200, v=5.126, q=text)
        result = []
        for i in groups_['items']:
            try:
                result.append(i['group']['id'])
            except:
                pass
        return result

    def to_csv(self, name):
        with open('dataset/'+name, 'w', encoding='utf8') as result_file:
            writetocsv = csv.writer(result_file, delimiter=';', lineterminator='\n')
            for i in self.result:
                writetocsv.writerow(i)
        print('Successfully finished...')