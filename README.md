## 関連単語取得プログラム

### python
python3.5.1で動作を確認

### 使い方
#### 例
```
python colect_related_word.py ~.csv ~.json あ ん
```
#### 引数
引数1: csvのseedソースファイル  
引数2: 出力先ファイル  
引数3: 一文字(入力された文字が頭文字である単語を収集開始に)  
引数4: 一文字(入力された文字が頭文字である単語で収集終了)  
(引数4を省略した場合はcsv終了まで収集)


### ファイル説明
#### colect_related_word.py
mecabのseedCSVの単語から関連語を収集するプログラム

#### related_word.json
収集した単語のデータ

#### runtime.txt
pythonのバージョン
