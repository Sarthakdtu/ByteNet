def get_track_id(url):
    track_id = None
    if "spotify:track" in url:
        track_id = url.split(":")[2]
    else:
        track_id = url.split('/')[4]
        print(track_id)
        track_id = track_id.split('?')[0]
    return track_id
