import sublime, sublime_plugin, threading, json, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "requests"))
import requests

class SubmitPasteCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.aliases = [
      'text', 'augeas', 'DASM16', 'puppet', 'iex', 'ceylon', 'html+evoque',
      'numpy', 'css+php', 'xml+lasso', 'vim', 'cfm', 'cfs', 'ssp',
      'smarty', 'xml+evoque', 'tea', 'redcode', 'mason', 'jags', 'dtd', 'java',
      'nemerle', 'ragel-java', 'dpatch', 'octave', 'ragel-d',
      'scilab', 'monkey', 'html+myghty', 'erl', 'css', 'io', 'cobolfree', 'vhdl',
      'fortran', 'd-objdump', 'mysql', 'rebol', 'erb', 'cbmbas', 'befunge',
      'xml+smarty', 'dylan', 'groovy', 'ahk', 'c', 'html', 'cmake', 'sp',
      'mako', 'vgl', 'velocity', 'koka', 'gnuplot', 'irc', 'prolog', 'yaml',
      'xml+mako', 'xslt', 'urbiscript', 'maql', 'sqlite3', 'boo', 'ocaml',
      'ec', 'd', 'fan', 'logos', 'jlcon', 'scss', 'bbcode', 'py3tb', 'mupad',
      'dart', 'idl', 'dg', 'evoque', 'c-objdump', 'jsp', 'registry', 'abap',
      'xml+velocity', 'html+mako', 'protobuf', 'ragel', 'glsl', 'cobol', 'ts',
      'xtend', 'logtalk', 'objdump', 'toml', 'css+mako', 'ca65', 'html+php',
      'postscript', 'kotlin', 'plpgsql', 'bro', 'lua', 'pov', 'antlr-java', 'tcl',
      'antlr-objc', 'aspectj', 'basemake', 'antlr-python', 'genshitext', 'croc',
      'gas', 'bat', 'snobol', 'pycon', 'xml', 'antlr', 'opa', 'go', 'minid',
      'ragel-c', 'erlang', 'control', 'aspx-vb', 'ragel-cpp', 'aspx-cs',
      'matlabsession', 'properties', 'modelica', 'antlr-perl', 'treetop', 'matlab',
      'myghty', 'fsharp', 'newlisp', 'scala', 'css+lasso', 'xml+php', 'stan',
      'moocode', 'shell-session', 'spec', 'newspeak', 'console', 'coq', 'raw',
      'html+lasso', 'gst', 'mxml', 'css+smarty', 'smali', 'css+myghty',
      'rd', 'llvm', 'sml', 'nginx', 'gooddata-cl', 'applescript', 'html+smarty',
      'rust', 'ragel-em', 'pytb', 'antlr-cpp', 'gosu', 'factor', 'html+velocity',
      'ooc', 'sql', 'http', 'ecl', 'ragel-objc', 'json', 'nasm', 'xml+myghty'
    ]
    self.titles = [
      'Text only', 'Augeas', 'dasm16', 'Puppet', 'Elixir iex session', 'Ceylon', 'HTML+Evoque',
      'NumPy', 'CSS+PHP', 'XML+Lasso', 'VimL', 'Coldfusion HTML', 'cfstatement',
      'Scalate Server Page', 'Smarty', 'XML+Evoque', 'Tea', 'Redcode', 'Mason',
      'JAGS', 'DTD', 'Java', 'Nemerle', 'Ragel in Java Host', 'Darcs Patch',
      'Octave', 'Ragel in D Host', 'Scilab', 'Monkey', 'HTML+Myghty', 'Erlang erl session',
      'CSS', 'Io', 'COBOLFree', 'vhdl', 'Fortran', 'd-objdump', 'MySQL', 'REBOL',
      'ERB', 'CBM BASIC V2', 'Befunge', 'XML+Smarty', 'Dylan', 'Groovy', 'autohotkey',
      'C', 'HTML', 'CMake', 'SourcePawn', 'Mako', 'VGL', 'Velocity', 'Koka',
      'Gnuplot', 'IRC logs', 'Prolog', 'YAML', 'XML+Mako', 'XSLT', 'UrbiScript',
      'MAQL', 'sqlite3con', 'Boo', 'OCaml', 'eC', 'D', 'Fantom', 'Logos', 'Julia console',
      'SCSS', 'BBCode', 'Python 3.0 Traceback', 'MuPAD', 'Dart', 'IDL', 'dg', 'Evoque',
      'c-objdump', 'Java Server Page', 'reg', 'ABAP', 'XML+Velocity', 'HTML+Mako',
      'Protocol Buffer', 'Ragel', 'GLSL', 'COBOL', 'TypeScript', 'Xtend',
      'Logtalk', 'objdump', 'TOML', 'CSS+Mako', 'ca65', 'HTML+PHP', 'PostScript',
      'Kotlin', 'PL/pgSQL', 'Bro', 'Lua', 'POVRay', 'ANTLR With Java Target', 'Tcl',
      'ANTLR With ObjectiveC Target', 'AspectJ', 'Base Makefile', 'ANTLR With Python Target',
      'Genshi Text', 'Croc', 'GAS', 'Batchfile', 'Snobol', 'Python console session',
      'XML', 'ANTLR', 'Opa', 'Go', 'MiniD', 'Ragel in C Host', 'Erlang', 'Debian Control file',
      'aspx-vb', 'Ragel in CPP Host', 'aspx-cs', 'Matlab session', 'Properties',
      'Modelica', 'ANTLR With Perl Target', 'Treetop', 'Matlab', 'Myghty', 'FSharp',
      'NewLisp', 'Scala', 'CSS+Lasso', 'XML+PHP', 'Stan', 'MOOCode', 'Shell Session',
      'RPMSpec', 'Newspeak', 'Bash Session', 'Coq', 'Raw token data', 'HTML+Lasso',
      'Gosu Template', 'MXML', 'CSS+Smarty', 'Smali', 'CSS+Myghty', 'Rd',
      'LLVM', 'Standard ML', 'Nginx configuration file', 'GoodData-CL', 'AppleScript',
      'HTML+Smarty', 'Rust', 'Embedded Ragel', 'Python Traceback',
      'ANTLR With CPP Target', 'Gosu', 'Factor', 'HTML+Velocity', 'Ooc', 'SQL',
      'HTTP', 'ECL', 'Ragel in Objective C Host', 'JSON', 'NASM', 'XML+Myghty'
    ]

    self.getContent()
    self.showPanel()

  def getContent(self):
    view = self.window.active_view()
    self.content = '\n'.join([view.substr(region) for region in view.sel()])
    if not self.content:
      self.content = view.substr(sublime.Region(0, view.size()))

  def showPanel(self):
    self.window.show_quick_panel(self.titles, self.findLang)

  def findLang(self, pos):
    if pos == -1: return
    params = {
      'content': self.content,
      'lexer': self.aliases[pos]
    }
    request = SubmitPasteRequest(params)
    request.start()
    self.check(request)
  def check(self,response, i='.'):
      sublime.status_message( '[JustPaste.Me] Processing'+i)
      if(response.isAlive()):
        if(i == '...'):
          i = ''
        sublime.set_timeout(lambda: self.check(response,i+'.'), 150)
        return;
      if response.result.status_code == requests.codes.ok:
        sublime.set_clipboard('http://justpaste.me/view/'+response.result.text)
        sublime.status_message("[JustPaste.Me] URL has been copied to clipboard")
      else:
        sublime.error_message("[JustPaste.Me] Can't submit paste :(")

class SubmitPasteRequest(threading.Thread):

  def __init__(self, params):
    self.requestUrl = 'http://justpaste.me/new'
    self.params = params
    threading.Thread.__init__(self)

  def run(self):
      self.result = requests.post(self.requestUrl, data=json.dumps(self.params))
