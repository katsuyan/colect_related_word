# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import json
import csv
import sys

class ColectRelatedWord:
    # csvを一行ごとに取得するジェネレータ
    def unfussy_reader(self, csv_reader):
        while True:
            try:
                yield next(csv_reader)
            except csv.Error:
                print("Problem with some row")
                continue

    # wikipediaAPIを利用し関連ワード取得
    def get_related_word(self, word):
        related_data = {}
        related_word_list = []
        encoded_word = urllib.parse.quote(word)
        url = 'https://ja.wikipedia.org/w/api.php?format=json&action=query&list=backlinks&bltitle=%s' % encoded_word
        get_data = urllib.request.urlopen(url)
        json_data = json.loads(get_data.read().decode('utf-8'))
        if json_data.get('query', None) != None:
            for data in json_data['query']['backlinks']:
                if data['ns'] == 0:
                    related_word_list.append(data['title'])
        related_data[word] = related_word_list
        return related_data


# json形式で'word: [related_words]'の形で収集
def main(src, dst, start, final):
    colect_related_word = ColectRelatedWord()

    count = 0 #収集した数
    with open("temp.csv", "w") as fout:
        fout.write("abc,def\nghi\x00,klm\n123,456")

    try:
        related_word_file = open(dst, 'w')
        related_word_file.write("{\"related\": [\n")

        with open(src) as fin:
            reader = colect_related_word.unfussy_reader(csv.reader(fin))
            # 指定語までスキップ
            for row in reader:
                if(row[0][0] == start):
                    break
            for n, row in enumerate(reader):
                # 指定語で終了
                if(row[0][0] == final):
                    break
                # row[4]が名詞の場合関連語収集
                if(row[4] == "名詞"):
                    keyword = row[0]
                    related_data = colect_related_word.get_related_word(keyword)
                    print("%s :  %d" % (keyword, count))
                    if len(related_data[keyword]) != 0:
                        count += 1
                        json.dump(related_data, related_word_file, ensure_ascii=False)
                        related_word_file.write(",\n")
                        related_word_file.flush()
    except Exception as e:
        print(str(e))
    else:
        related_word_file.write("]}\n")
        related_word_file.close()

if __name__ == '__main__':
    src = sys.argv[1]
    dst = sys.argv[2]
    start = sys.argv[3]
    if len(sys.argv) == 5:
        final = sys.argv[4]
    else:
        final = None
    main(src, dst, start, final)
