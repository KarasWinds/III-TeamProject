from pytube import Playlist
import os

urllist = ["PLGjGElTtLa4cwGe0kS_xb7VsQyOgEAJ7J",
           "PLhNOSp011_9WBBOtW_8iaMWB5hyD65fj8",
           "PLt9JOvvH4uk62ZO7tBZNxZNTM7qcLvX1F",
           "PL-osUfNyY9znWoSgJTSzBY-NIkn3PzTRY",
           "PLO3UPeBh19YCdwgMlmEq9P9z4TN8VENWV",
           "PLIqFvQrfr2oYGXX2QTSh8-eaVYzxJ3d9j",
          ]
# print(type(urllist[0]))

for u in urllist:
    url = "https://www.youtube.com/playlist?list=" + u

    pl = Playlist(url, suppress_exception=True)
    dirname = './youtube/'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    pl.downloadaudio_all(dirname)
