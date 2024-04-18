import time
from fri3d.rtttl_player import play_rtttl


macarena = 'Los del Rio - Macarena:o=5,d=8,b=180,b=180:f,f,f,4f,f,f,f,f,f,f,f,a,c,c,4f,f,f,4f,f,f,f,f,f,f,d,c,4p,4f,f,f,4f,f,f,f,f,f,f,f,a,4p,2c6.,4a,c6,a,f,4p,2p'
macarena_s = 'Los del Rio - Macarena:o=5,d=8,b=180,b=180:4f,f,f,f,f,f,f,f,a,4p,2c6.,4a,c6,a,f'

dump_dump = 'To The Dump To The Dump To The Dump Dump Dump:o=5,d=8,b=270,b=270:c,c,4c,c,c,4c,c,c,f,p,g,p,4a,c,c,4c,c,c,4c,a,a,g,p,e,p,4c,c,c,4c,c,c,4c,c,c,f,p,g,p,4a,f,a,1c6,a,g,f,p,a.,p,f'
dump_dump_s = 'To The Dump To The Dump To The Dump Dump Dump:o=5,d=8,b=270,b=270:c,c,4c,c,c,4c,c,c,f,p,g,p,4a'

william = 'Rossini - William Tell Overture Finale:d=4,o=5,b=140:16c,16c,16c,16p,16c,16c,16c,16p,16c,16c,16f,16p,8g,16a,16p,16c,16c,16c,16p,16c,16c,16f,16p,16a,16a,16g,16p,8e,16c,16p,16c,16c,16c,16p,16c,16c,16c,16p,16c,16c,16f,16p,8g,16a,16p,16f,16a,c6,16p,16a#,16a,16g,16f,16p,16a,16p,16f,16p'

take_on_me = 'a-ha - Take On Me:o=5,d=8,b=160,b=160:f#,f#,f#,d,p,b4,p,e,p,e,p,e,g#,g#,a,b,a,a,a,e,p,d,p,f#,p,f#,p,f#,e,e,f#,e,f#,f#,f#,d,p,b4,p,e,p,e,p,e,g#,g#,a,b,a,a,a,e,p,d,p,f#,p,f#,p,f#,e,e5'
take_on_me_s = 'a-ha - Take On Me:o=5,d=8,b=160,b=160:f#,f#,f#,d,p,b4,p,e,p,e,p,e,g#,g#,a,b,a,a,a,e,p,d,p,f#,p,f#,'

good_bad_ugly = 'The Good The Bad The Ugly:d=8,o=5,b=125:16a,16d6,16a,16d6,2a,4f,4g,2d,4p,16a,16d6,16a,16d6,2a,4f,4g,2c6,4p,16a,16d6,16a,2d6,4f6,e6,d6,2c6,4p,16a,16d6,16a,16d6,4a.,4g,d,2d'
good_bad_ugly_s = 'The Good The Bad The Ugly:d=8,o=5,b=125:16a,16d6,16a,16d6,2a,4f,4g,2d'

creeds_push_up = 'Creeds - Push Up:d=8,o=5,b=160:b,b,b,g,a,a,a,g,f#,f#,f#,f#,2f#,2p,b,b,b,g,a,a,a,g,f#,f#,f#,f#,2f#,2p, g,g,g,d,a,a,a,g,f#,f#,f#,f#,2f#,2p,g,g,g,d,e,e,e,g,f#,f#,f#,f#,2f#,2p, b,b,b,g,a,a,a,g,f#,f#,f#,f#,4p,b,b,b,g,a,a,a,g,f#,f#,f#,f#,4p, g,g,g,d,a,a,a,g,f#,f#,f#,f#,4p,g,g,g,d,e,e,e,g,f#,f#,f#,f#,4p'
creeds_push_up_s = 'Creeds - Push Up:d=8,o=5,b=160:b,b,b,g,a,a,a,g,f#,f#,f#,f#,2f#'


short_songs = [macarena_s, dump_dump_s, take_on_me_s, good_bad_ugly_s, creeds_push_up_s]
songs = [macarena, dump_dump, william, take_on_me, good_bad_ugly, creeds_push_up]

for song in short_songs:
    play_rtttl(song)
    time.sleep(0.5)

for song in songs:
    play_rtttl(song)
    time.sleep(0.5)
