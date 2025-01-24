#!/usr/bin/env python3
# Generates the *.json files in json/ from content in the sources/ dir

import json
import yaml
import os
import shutil

input_dir = "sources"
output_dir = "json"


def renderSource(path):
    db = {}
    titleslugs = []
    for file in os.scandir(path):
        if len(file.name) != 2 or file.name[len(file.name)-2:] == "md":
            pass

        sourceFile = open(file.path).read()
        parts = sourceFile.split("%=%", maxsplit=1)
        if len(parts) != 2:
            raise Exception(f"invalid format for file '{file.path}'")

        var = yaml.safe_load(parts[0])
        data = parts[1]

        if 'post' not in var:
            raise Exception(f"missing post id in file '{file.path}'")

        try:
            postid = int(var['post'])
        except Exception:
            idx = var['post']
            raise Exception(f"invalid post id in file '{file.path}': {idx}")

        postData = {}
        postData.update(var)
        postData.update({'content': data})
        db[postid] = postData

    out = []
    ids = list(db.keys())
    ids.sort()
    for i in ids:
        out.append(db[i])

    return json.dumps(out)


if __name__ == "__main__":
    if os.path.exists(output_dir) is False:
        os.mkdir(output_dir)

    for directory in os.scandir(input_dir):
        if directory.is_dir() is False:
            pass
        jsondata = renderSource(directory.path)
        path = os.path.join(output_dir, f"{directory.name}.json")
        open(path, "w").write(jsondata)
        print(f"wrote '{path}'")
    print("rendered sources")
