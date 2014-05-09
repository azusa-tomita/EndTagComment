# endtagcomment
# こういうHTMLがあったときに
# <div id="hoge" class="fuga foo">
# ...
# </div>
#
# 実行するとこうなる
# <div id="hoge" class="fuga foo">
# ...
# <!--/div#hoge.fuga.foo--></div>
#
# ctrl+e,ctrl+i でidのみを出力
# ctrl+e,ctrl+c でclassのみを出力
# ctrl+e,ctrl+e でidとclassを出力
# ctrl+e,ctrl+t でtagとidとclassを出力
#
# ctrl+e,ctrl+s でコメント内のテキストの前後の空白をトグル
# <!--/hoge-->  <->  <!-- /hoge -->
# ctrl+e,ctrl+y でクラス名の最初の.をトグル
# <!--/hoge.fuga-->  <->  <!--/.hoge.fuga-->
#
# 参考
# https://gist.github.com/kosei27/734448
# https://gist.github.com/hokaccha/411828

import sublime
import sublime_plugin

if sublime.version().startswith('2'):
	from HTMLParser import HTMLParser
else:
	from html.parser import HTMLParser

EndTagCommentSpace = ''
EndTagCommentFirstclassSymbol = ''

class EndTagComment:
	def __init__(self, view,edit,type):
		self.view = view
		self.edit = edit
		self.type = type
		self.region = []
		self.source = ''

	def InsertComment(self):
		self.view.run_command('expand_selection', {'to': 'tag'})
		self.view.run_command('expand_selection', {'to': 'tag'})
		self.region = self.view.sel()[0]
		self.source = self.view.substr(self.region)
		self.space = EndTagCommentSpace
		self.fcs = EndTagCommentFirstclassSymbol

		class Parser(HTMLParser):
			is_getFirstTag = False
			attrVals = {}

			def __init__(self):
				HTMLParser.__init__(self)

			def handle_starttag(self, tag, attrs):
				if self.is_getFirstTag == False:
					attrs = dict(attrs)
					self.is_getFirstTag = True

					self.attrVals.setdefault('tag',tag)
					for i in attrs:
						self.attrVals.setdefault(i,attrs[i])

		HTML = Parser()
		HTML.feed(self.source)
		HTML.close()
		attr = HTML.attrVals

		comment = {'tag':'','class':'','id':''}
		if 'tag' in attr:
			comment['tag'] = attr['tag']
		if 'class' in attr:
			comment['class'] = attr['class'].replace(' ','.')
		if 'id' in attr:
			comment['id'] = attr['id'].replace(' ','#')

		if self.type == 'id':
			closeComment = '<!--' + self.space + '/' + comment['id'] + self.space + '-->'
		elif self.type == 'class':
			closeComment = '<!--' + self.space + '/' + self.fcs + comment['class'] + self.space + '-->'
		elif self.type == 'id_class':
			closeComment = '<!--' + self.space + '/' + comment['id'] + '.' + comment['class'] + self.space + '-->'
		elif self.type == 'tag_id_class':
			symbole_id = '#' if comment['id'] else ''
			symbole_class = '.' if comment['class'] else ''
			closeComment = '<!--' + self.space + '/' + comment['tag'] + symbole_id + comment['id'] + symbole_class + comment['class'] + self.space + '-->'
		insertPoint = self.region.end()- (self.region.size() - self.source.rfind('</'))
		self.view.insert(self.edit,insertPoint,closeComment)

def SpaceToggle(self):
	global EndTagCommentSpace
	if EndTagCommentSpace == '':
		EndTagCommentSpace = ' '
	else:
		EndTagCommentSpace = ''

def FirstClassSymbolToggle(self):
	global EndTagCommentFirstclassSymbol
	if EndTagCommentFirstclassSymbol == '':
		EndTagCommentFirstclassSymbol = '.'
	else:
		EndTagCommentFirstclassSymbol = ''

class EndTagCommentSpaceToggle(sublime_plugin.TextCommand):
	def run(self, edit):
		SpaceToggle(self)

class EndTagCommentFirstClassSymbolToggle(sublime_plugin.TextCommand):
	def run(self, edit):
		FirstClassSymbolToggle(self)

class EndTagCommentId(sublime_plugin.TextCommand):
	def run(self, edit):
		EndTagComment(self.view,edit,'id').InsertComment()

class EndTagCommentClass(sublime_plugin.TextCommand):
	def run(self, edit):
		EndTagComment(self.view,edit,'class').InsertComment()

class EndTagCommentIdClass(sublime_plugin.TextCommand):
	def run(self, edit):
		EndTagComment(self.view,edit,'id_class').InsertComment()

class EndTagCommentTagIdClass(sublime_plugin.TextCommand):
	def run(self, edit):
		EndTagComment(self.view,edit,'tag_id_class').InsertComment()
