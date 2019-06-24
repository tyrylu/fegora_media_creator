

    resp = session.get(url_for("areas/{0}/download".format(area_name)), stream=True, params={"client_id": config().client_id})
    if resp.status_code == 200:
        total = int(resp.headers.get("content-length", 0))
        chunk_size = 32*1024
        fp = open(Database.get_database_file(area_name, server_side=False), "wb")
        so_far = 0
        for chunk in resp.iter_content(chunk_size):
            so_far += len(chunk)
            fp.write(chunk)
            if progress_callback:
                progress_callback(total, so_far)
        fp.close()
        return True
    else:
        log.warn("Non 200 status code during area download: %s.", resp.status_code)
        return False
