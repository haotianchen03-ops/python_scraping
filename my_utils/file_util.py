def print_file_info(file_name):
    f = None
    content = list()
    try:
        f = open(file_name,"r",encoding="utf-8")
        for line in f:
            content.append(line.strip())
        print(content)
    except Exception as e:
        print(e)
    finally:
        if f:
            f.close()

def append_to_file(file_name,content):
    try:
        f = open(file_name,"a",encoding="utf-8")
        f.write(content+"\n")
    except Exception as e:
        print(e)
    finally:
        f.close()


