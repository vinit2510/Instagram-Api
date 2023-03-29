from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def base():
    return jsonify({'documentation': "https://github.com/vinit2510/Instagram-Api"})


@app.route('/instagram/', methods=['GET'])
def instagram_():
    url = request.args.get('url')
    cookie = request.args.get('cookie')

    if url and cookie:
        return get_data(url, cookie)
    elif url:
        return get_data(url)
    else:
        return jsonify({'response': False, 'error': 'No URL parameter found', 'error_code': 12, 'documentation': "https://github.com/vinit2510/Instagram-Api"}), 400


@app.route('/instagram', methods=['GET'])
def instagram():
    url = request.args.get('url')
    cookie = request.args.get('cookie')

    if url and cookie:
        return get_data(url, cookie)
    elif url:
        return get_data(url)
    else:
        return jsonify({'response': False, 'error': 'No URL parameter found', 'error_code': 12, 'documentation': "https://github.com/vinit2510/Instagram-Api"}), 400


def get_data(link, cookie=""):
    
    if "instagram" not in link:
        return jsonify({'response': False, 'error': 'Not valid url', 'error_code': 13, 'documentation': "https://github.com/vinit2510/Instagram-Api"}), 400
    
    url = link.split("?")[0] + "?__a=1&__d=dis"

    my_cookie = """replace_with_your_cookie"""

    headers = {
        "cookie": my_cookie
    }

    if cookie != "":
        headers = {
            "cookie": cookie
        }

    ig_response = requests.get(url, headers=headers)

    try:

        if ig_response.status_code == 200:

            data = ig_response.json()

            items = data["items"][0]
            username = items["user"]["username"]
            caption = ""

            try:
                caption = items["caption"]["text"]
            except:
                caption = ""

            type = items["media_type"]

            thumbUrl = []
            videoUrl = []
            is_video = []

            if type == 1:
                thumb = items["image_versions2"]["candidates"][0]["url"]
                thumbUrl.append(thumb)
                videoUrl.append("")
                is_video.append(False)

            elif type == 2:
                thumb = items["image_versions2"]["candidates"][0]["url"]
                video = items["video_versions"][0]["url"]

                thumbUrl.append(thumb)
                videoUrl.append(video)
                is_video.append(True)

            elif type == 8:
                carouselMedia = items["carousel_media"]

                for i in carouselMedia:
                    mediaType = i["media_type"]

                    if mediaType == 1:
                        thumb = i["image_versions2"]["candidates"][0]["url"]
                        thumbUrl.append(thumb)
                        videoUrl.append("")
                        is_video.append(False)

                    elif mediaType == 2:
                        thumb = i["image_versions2"]["candidates"][0]["url"]
                        video = i["video_versions"][0]["url"]
                        thumbUrl.append(thumb)
                        videoUrl.append(video)
                        is_video.append(True)
            else:
                return jsonify({
                    'response': False,
                    'error': "Media type not supported"
                })

            response = {
                'response': True,
                "media_type": type,
                "ig_username": username,
                "post_caption": caption,
                "thumbnail": thumbUrl,
                "video": videoUrl,
                "is_video": is_video,
                'documentation': "https://github.com/vinit2510/Instagram-Api"

            }

            return jsonify(response)

        else:
            return jsonify({'response': False, 'error': 'Data not found', 'error_code': 10, 'documentation': "https://github.com/vinit2510/Instagram-Api"}), 400
    except:
        return jsonify({'response': False, 'error': 'Something went wrong', 'error_code': 11, 'documentation': "https://github.com/vinit2510/Instagram-Api"}), 400


if __name__ == '__main__':
    app.run(debug=True)
