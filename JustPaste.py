import sublime
import sublime_plugin
import urllib
import urllib2
import threading
import time
import pprint

class JustpasteCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		params = urllib.urlencode({
			'paste': self.getPaste()
		})
		response = JustPasteApiCall(params)
		response.start()
		self.check(response)



    	def getPaste(self):
    		content = '\n'.join([self.view.substr(region) for region in self.view.sel()])
    		if not content:
    			content = self.view.substr(sublime.Region(0, self.view.size()))
    		return content

	def check(self,response, i='.'):
		sublime.status_message( '[JustPaste.Me] Processing'+i)
		if(response.isAlive()):
			if(i == '...'):
				i = ''
			sublime.set_timeout(lambda: self.check(response,i+'.'), 150)
			return;
		if response.result == False:
			sublime.error_message("Can't submit to JustPaste.Me")
		else:
			sublime.set_clipboard(response.result)
    		    	sublime.status_message("[JustPaste.Me] URL has been copied to clipboard")


class JustPasteApiCall(threading.Thread):

	def __init__(self, params):
		self.params = params
		threading.Thread.__init__(self)

	def run(self):
		try:
	    		req = urllib2.Request('http://justpaste.me/api', self.params)
	    		response = urllib2.urlopen(req)
	    		self.result = response.read()
    		except (urllib2.HTTPError) as (e):
    			self.result = False
