import requests;

from datetime import datetime
from .models import User, Video, Game, Channel, VersionPull, Message


class ParseTwitch:

    def __init__(self, version):
        self.version = version

    def parse_and_save(self):
        r = requests.get('https://api.twitch.tv/kraken/games/top?client_id=' + self.version.client_id)
        # update notification
        self.version.percent += 1
        self.version.save()
        # parse
        json = r.json()
        count_game = 0
        count_channel = 0
        top_game = json["top"]
        for json_game in top_game:
            count_game += 5
            if count_game > 100:
                break
            # skip if already register
            if Game.objects.filter(id_game_twitch=json_game["game"]["_id"]).first() is not None:
                continue
            game = Game(name=json_game["game"]["name"],
                        url_image=json_game["game"]["box"]["large"],
                        id_game_twitch=json_game["game"]["_id"],
                        viewers=json_game["viewers"], popularity=json_game["game"]["popularity"])
            game.save()
            r = requests.get('https://api.twitch.tv/kraken/streams/'
                             + "?client_id=" + self.version.client_id + "&game=" + game.name)
            json = r.json()
            for json_stream in json["streams"]:
                self.version.percent += 0.05
                self.version.save()
                count_channel += 1
                if count_channel > 100:
                    break
                json_channel = json_stream["channel"]
                # skip if already register
                if Channel.objects.filter(id_channel_twitch=json_channel["_id"]).first() is not None:
                    continue
                channel = Channel(id_channel_twitch=json_channel["_id"], logo=json_channel["logo"],
                                  name=json_channel["name"], url=json_channel["url"], nb_views=json_channel["views"],
                                  created_at=datetime.strptime(json_channel["created_at"], '%Y-%m-%dT%H:%M:%SZ'))
                channel.game = game
                channel.save()

                # get video
                r = requests.get(json_channel["_links"]["videos"] + "?client_id=" + self.version.client_id)
                json = r.json()
                for json_video in json["videos"]:
                    self.version.percent += 0.05
                    self.version.save()
                    # skip if already register
                    if Video.objects.filter(id_video_twitch=json_video["_id"]).first() is not None:
                        continue
                    video = Video(id_video_twitch=json_video["_id"], url=json_video["url"],
                                  title=json_video["title"], description=json_video["description"],
                                  game=game, channel=channel, nb_views=json_video["views"],
                                  created_at=datetime.strptime(json_video["created_at"], '%Y-%m-%dT%H:%M:%SZ'),
                                  recorded_at=datetime.strptime(json_video["recorded_at"], '%Y-%m-%dT%H:%M:%SZ'))
                    video.save()

                    # get messages of video
                    # first get bound
                    r = requests.get('https://rechat.twitch.tv/rechat-messages?start=0&video_id='
                                     + str(video.id_video_twitch) + "&client_id=" + self.version.client_id)
                    json = r.json()["errors"][0]
                    bounds = json["detail"]
                    bounds = [int(s) for s in bounds.split() if s.isdigit()][1::]
                    start = bounds[0]
                    end = bounds[1]
                    count_message = 0
                    while start < end:
                        self.version.percent += 0.05
                        self.version.save()
                        r = requests.get('https://rechat.twitch.tv/rechat-messages?start=' + str(start) + '&video_id='
                                         + str(video.id_video_twitch) + "&client_id=" + self.version.client_id)
                        start += 30
                        if count_message >= 1 or r.status_code == 404:
                            break
                        count_message += 1
                        json_messages = r.json()["data"]
                        for json_msg in json_messages:
                            print(json_msg)
                            if json_msg is {} or json_msg is None:
                                break
                            if Message.objects.filter(id_message_twitch=json_msg["id"]).first() is not None:
                                break
                            else:
                                # fix user no name
                                if json_msg["attributes"]["tags"]["display-name"] is None:
                                    break

                                r = requests.get('https://api.twitch.tv/kraken/users/'
                                                 + json_msg["attributes"]["tags"]["display-name"]
                                                 + '?client_id=' + self.version.client_id)
                                if r.status_code == 404 or r.status_code == 422 or r.status_code == 400:
                                    continue
                                user_json = r.json()

                                user = User.objects.filter(id_user_twitch=user_json["_id"]).first()
                                if user is None:
                                    user = User(name=user_json["name"], bio=user_json["bio"],
                                                logo=user_json["logo"], id_user_twitch=user_json["_id"])
                                user.save()
                                message = Message(
                                    id_message_twitch=json_msg["id"],
                                    body=json_msg["attributes"]["message"],
                                    timestamp=start,
                                    video=video,
                                    user=user)
                                message.save()

