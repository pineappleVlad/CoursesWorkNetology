import requests
import json

class GetVkUrl:
    url = "https://api.vk.com/method/"
    def __init__(self, token):
        self.params = {
            "access_token" : token,
            "v" : "5.131"
        }

    def get_photos(self, user_id):
        photos_url = self.url + "photos.get"
        photos_params = {
            "owner_id" : user_id,
            "album_id" : "profile",
            "rev" : "0",
            "extended" : "1",
            "count" : "10"
        }
        res = requests.get(photos_url, params={**self.params, **photos_params})
        url_list = []
        photos_list = []
        for i in res.json()["response"]["items"]:
            photos_list.append(i["sizes"][-1])
            url_list.append(i["sizes"][-1]["url"])
        with open("photos_info.json", "w", encoding="utf-8") as file:
            dict_list = []
            for i in range(len(url_list)):
                information_dict = {}
                information_dict["url"] = url_list[i]
                likes = res.json()["response"]["items"][i]["likes"]["count"]
                information_dict["likes"] = likes
                information_dict["file_name"] = str(likes) + ".jpg"
                information_dict["size"] = res.json()["response"]["items"][i]["sizes"][-1]["type"]
                information_dict["date"] = res.json()["response"]["items"][i]["date"]
                dict_list.append(information_dict)
            json.dump(dict_list, file, indent=1)
        return res.json()

class YandexUpload:
    def __init__(self, token):
        self.token = token

    def upload(self, folder_name):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        api_base_url = "https://cloud-api.yandex.net/"

        with open("photos_info.json", encoding="utf-8") as file:
            requests.put(api_base_url + 'v1/disk/resources', params={'path': folder_name}, headers=headers)
            list_photos = []
            progress_count = 0
            for i in json.load(file):
                upload_url = api_base_url + 'v1/disk/resources/upload'
                if str(i["file_name"]) in list_photos:
                    r = requests.post(upload_url, headers=headers, params={
                        "path": folder_name + "/" + i["file_name"] + "_" + i["date"],
                        "url": i["url"]
                    })
                else:
                    r = requests.post(upload_url, headers=headers, params={
                        "path": folder_name + "/" + i["file_name"],
                        "url": i["url"]
                    })
                list_photos.append(i["file_name"])
                progress_count += 1
                print(f"Фото номер {progress_count} успешно загружено")
            return





if __name__ == "__main__":
    token_1 = ""
    vk_client = GetVkUrl(token_1)
    dict__ = vk_client.get_photos("")
    token_2 = ""
    ya_client = YandexUpload(token_2)
    ya_client.upload("my_vk_photos")

