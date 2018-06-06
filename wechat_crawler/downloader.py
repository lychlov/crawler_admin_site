# from threading import Thread
#
#
# class DownloadWorker(Thread):
#     def __init__(self, queue, proxies=None):
#         Thread.__init__(self)
#         self.queue = queue
#         self.proxies = proxies
#         self._register_regex_match_rules()
#
#     def run(self):
#         while True:
#             medium_type, post, target_folder = self.queue.get()
#             self.download(medium_type, post, target_folder)
#             self.queue.task_done()
#
#     def download(self, medium_type, post, target_folder):
#         try:
#             medium_url = self._handle_medium_url(medium_type, post)
#             if medium_url is not None:
#                 self._download(medium_type, medium_url, target_folder)
#         except TypeError:
#             pass
#
#     # can register differnet regex match rules
#     def _register_regex_match_rules(self):
#         # will iterate all the rules
#         # the first matched result will be returned
#         self.regex_rules = [video_hd_match(), video_default_match()]
#
#     def _handle_medium_url(self, medium_type, post):
#         try:
#             if medium_type == "photo":
#                 return post["photo-url"][0]["#text"]
#
#             if medium_type == "video":
#                 video_player = post["video-player"][1]["#text"]
#                 for regex_rule in self.regex_rules:
#                     matched_url = regex_rule(video_player)
#                     if matched_url is not None:
#                         return matched_url
#                 else:
#                     raise Exception
#         except:
#             raise TypeError("Unable to find the right url for downloading. "
#                             "Please open a new issue on "
#                             "https://github.com/dixudx/tumblr-crawler/"
#                             "issues/new attached with below information:\n\n"
#                             "%s" % post)
#
#     def _download(self, medium_type, medium_url, target_folder):
#         medium_name = medium_url.split("/")[-1].split("?")[0]
#         if medium_type == "video":
#             if not medium_name.startswith("tumblr"):
#                 medium_name = "_".join([medium_url.split("/")[-2],
#                                         medium_name])
#
#             medium_name += ".mp4"
#
#         file_path = os.path.join(target_folder, medium_name)
#         if not os.path.isfile(file_path):
#             print("Downloading %s from %s.\n" % (medium_name,
#                                                  medium_url))
#             retry_times = 0
#             while retry_times < RETRY:
#                 try:
#                     resp = requests.get(medium_url,
#                                         stream=True,
#                                         proxies=self.proxies,
#                                         timeout=TIMEOUT)
#                     if resp.status_code == 403:
#                         retry_times = RETRY
#                         print("Access Denied when retrieve %s.\n" % medium_url)
#                         raise Exception("Access Denied")
#                     with open(file_path, 'wb') as fh:
#                         for chunk in resp.iter_content(chunk_size=1024):
#                             fh.write(chunk)
#                     break
#                 except:
#                     # try again
#                     pass
#                 retry_times += 1
#             else:
#                 try:
#                     os.remove(file_path)
#                 except OSError:
#                     pass
#                 print("Failed to retrieve %s from %s.\n" % (medium_type,
#                                                             medium_url))
