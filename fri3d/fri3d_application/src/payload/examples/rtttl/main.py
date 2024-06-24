import time

from fri3d.rtttl import songs, RTTTL

frere_jacques = "Frère Jacques:d=4,o=6,b=112:c,d,e,c,c,d,e,c,e,f,g,p,e,f,g,p,8g,8a,8g,8f,e,c,8g,8a,8g,8f,e,c,c,g5,c,p,c,g5,c"
nokia = "Nokia:d=4,o=5,b=225:8e6,8d6,f#,g#,8c#6,8b,d,e,8b,8a,c#,e,2a"

short_songs = [
    songs.macarena_s,
    songs.dump_dump_s,
    songs.take_on_me_s,
    songs.good_bad_ugly_s,
    songs.creeds_push_up_s
]

long_songs = [
    songs.macarena,
    songs.dump_dump,
    songs.william,
    songs.take_on_me,
    songs.good_bad_ugly,
    songs.creeds_push_up
]

RTTTL(nokia).play(volume=100)
RTTTL(frere_jacques).play(volume=10)

for song in short_songs:
    RTTTL(song).play()
    time.sleep(0.5)

for song in long_songs:
    RTTTL(song).play()
    time.sleep(0.5)
