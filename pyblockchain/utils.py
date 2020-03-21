import collections
import hashlib

# 辞書のハッシュ化をする際に、キーの順番が同じになるように並び替えておく
# 辞書を文字列化すると、そのままの順番で文字列化されるので、実行ごとにハッシュ値が違くなっちゃう(pythonのdictは順序を保持しないから)


def sorted_dict_by_key(unsorted_dict):
    """
    辞書をキーでソートし、新しくOrderedDictを返却する関数
    """
    # sorted関数のkeyについては、公式ドキュメント参照
    # list.sort() と sorted() には key パラメータがあります。
    # これは比較を行う前にリストの各要素に対して呼び出される関数を指定するパラメータです。
    # https://docs.python.org/ja/3/howto/sorting.html
    sorted_dict = sorted(unsorted_dict.items(), key=lambda d: d[0])

    sorted_ordered_dict = collections.OrderedDict(sorted_dict)

    return sorted_ordered_dict

def pprint(chains):
    """
    ブロックチェーンのリストをわかりやすく整形して表示する関数

    chainsは、ブロックチェーンオブジェクトが入ったリスト
    """
    for i, chain in enumerate(chains):
        print(f'{"="*25} Chain {i} {"="*25}')
        for k, v in chain.items():
            # f stringの機能は下記参照　変数名の後に:をつけて表示フォーマットを指定できる
            # https://note.nkmk.me/python-f-strings/

            if k == 'transactions':
                print(k)
                for d in v:
                    print(f'{"-"*40}')
                    for kk, vv in d.items():
                        print(f' {kk:30}{vv}')
            else:
                # キー表示に15文字の幅を取っておく
                print(f'{k:15} {v}')
