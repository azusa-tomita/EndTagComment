EndTagComment
=============

SublimeTextで閉じコメントを追加します。

こういうHTMLがあったときに

```
<div id="hoge" class="fuga foo">
...
</div>
```

実行するとこうなる

```
<div id="hoge" class="fuga foo">
...
<!--/div#hoge.fuga.foo--></div>
```

`ctrl+e`,`ctrl+i` でidのみを出力
`ctrl+e`,`ctrl+c` でclassのみを出力
`ctrl+e`,`ctrl+e` でidとclassを出力
`ctrl+e`,`ctrl+t` でtagとidとclassを出力

`ctrl+e`,`ctrl+s` でコメント内のテキストの前後の空白をトグル

```
<!--/hoge-->  <->  <!-- /hoge -->
```

`ctrl+e`,`ctrl+y` でクラス名の最初の.をトグル

```
<!--/hoge.fuga-->  <->  <!--/.hoge.fuga-->
```

参考
https://gist.github.com/kosei27/734448
https://gist.github.com/hokaccha/411828


Installing
------

package直下に `EndTagComment` ディレクトリを作って入れてください


Supported
----------------

ST2/ ST3


License
----------

wtfpl
