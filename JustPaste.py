import sublime, sublime_plugin, threading, json, sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "requests"))
import requests

class SubmitPasteCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.languages = [
      'Text only', 'Augeas', 'dasm16', 'Puppet', 'Delphi', 'JavaScript+Mako',
      'Elixir iex session', 'PostgreSQL console (psql)', 'Brainfuck', 'Ceylon',
      'JavaScript+Django/Jinja', 'HTML+Evoque', 'NumPy', 'Modula-2',
      'LiveScript', 'Nimrod', 'Bash', 'HTML+Django/Jinja', 'CSS+PHP',
      'XML+Lasso', 'VimL', 'CSS+Genshi Text', 'Fancy', 'Coldfusion HTML',
      'cfstatement', 'Scalate Server Page', 'Smarty', 'XML+Evoque', 'haXe',
      'PowerShell', 'Tea', 'HTML+Cheetah', 'Redcode', 'Ruby irb session',
      'Mason', 'Django/Jinja', 'JAGS', 'ApacheConf', 'DTD', 'Dylan session',
      'Lighttpd configuration file', 'Java', 'JavaScript+Genshi Text',
      'Scheme', 'Nemerle', 'RHTML', 'Ragel in Java Host', 'Darcs Patch',
      'Octave', 'CoffeeScript', 'Ragel in D Host', 'Scilab', 'Monkey',
      'HTML+Myghty', 'Erlang erl session', 'CSS', 'JavaScript+Smarty',
      'Io', 'COBOLFree', 'Asymptote', 'vhdl', 'Python 3', 'CSS+Ruby',
      'Fortran', 'd-objdump', 'MySQL', 'REBOL', 'C++', 'ERB', 'CBM BASIC V2',
      'Befunge', 'Julia', 'MoonScript', 'Ruby', 'XML+Smarty', 'Dylan', 'Groovy',
      'MoinMoin/Trac Wiki markup', 'autohotkey', 'C', 'HTML', 'Felix', 'CMake',
      'NSIS', 'SourcePawn', 'Mako', 'VGL', 'Velocity', 'Koka', 'CUDA',
      'Gnuplot', 'IRC logs', 'Prolog', 'Python', 'CSS+Django/Jinja', 'verilog',
      'Smalltalk', 'JavaScript+Myghty', 'YAML',
      'ANTLR With ActionScript Target', 'XML+Mako', 'XSLT', 'UrbiScript',
      'Scaml', 'S', 'DylanLID', 'MAQL', 'sqlite3con', 'Boo', 'OCaml', 'eC',
      'ActionScript', 'VB.net', 'SquidConf', 'XQuery', 'D', 'Fantom',
      'Gettext Catalog', 'Logos', 'Julia console', 'Lasso', 'SCSS', 'BBCode',
      'Haml', 'FoxPro', 'Python 3.0 Traceback', 'MuPAD', 'XML+Ruby', 'Dart',
      'IDL', 'dg', 'Evoque', 'Jade', 'c-objdump', 'Kconfig',
      'Java Server Page', 'reg', 'ABAP', 'XML+Velocity', 'JavaScript+Cheetah',
      'HTML+Mako', 'Ragel in Ruby Host', 'RobotFramework', 'Protocol Buffer',
      'CFEngine3', 'Ragel', 'GLSL', 'COBOL', 'TypeScript', 'Ada',
      'PostgreSQL SQL dialect', 'Xtend', 'Logtalk', 'objdump', 'TOML',
      'CSS+Mako', 'ca65', 'Objective-C++', 'Gherkin', 'HTML+PHP', 'Makefile',
      'PostScript', 'Hxml', 'Kotlin', 'PL/pgSQL', 'Vala', 'Haskell', 'Bro',
      'Lua', 'POVRay', 'Sass', 'ANTLR With Java Target', 'Tcl',
      'ANTLR With ObjectiveC Target', 'JavaScript+Ruby', 'Racket', 'AspectJ',
      'Base Makefile', 'ANTLR With Python Target', 'cpp-objdump',
      'Genshi Text', 'Ioke', 'PyPy Log', 'Croc', 'Objective-J', 'GAS',
      'Batchfile', 'Snobol', 'Python console session', 'XML', 'ANTLR', 'Opa',
      'XML+Cheetah', 'Go', 'Diff', 'MiniD', 'Cython', 'Ragel in C Host',
      'Erlang', 'Debian Control file', 'aspx-vb', 'BUGS', 'Ragel in CPP Host',
      'aspx-cs', 'Matlab session', 'Properties', 'Groff', 'Clojure',
      'Modelica', 'QML', 'JavaScript+Lasso', 'ANTLR With Perl Target',
      'Genshi', 'BlitzMax', 'Treetop', 'Matlab', 'Myghty', 'HTML+Genshi',
      'Duel', 'Perl', 'FSharp', 'reStructuredText', 'NewLisp', 'Scala',
      'CSS+Lasso', 'XML+PHP', 'Stan', 'INI', 'MOOCode', 'Shell Session',
      'RPMSpec', 'Newspeak', 'Bash Session', 'Coq', 'Raw token data', 'Tcsh',
      'HTML+Lasso', 'C#', 'Gosu Template', 'RConsole', 'MXML', 'TeX',
      'CSS+Smarty', 'ANTLR With C# Target', 'OpenEdge ABL',
      'Cheetah', 'Smali', 'CSS+Myghty', 'Rd', 'LLVM', 'Standard ML', 'Elixir',
      'Nginx configuration file', 'GoodData-CL', 'AppleScript', 'HTML+Smarty',
      'Objective-C', 'JavaScript', 'Rust', 'Common Lisp', 'Embedded Ragel',
      'ActionScript 3', 'systemverilog', 'Literate Haskell',
      'Python Traceback', 'PHP', 'ANTLR With CPP Target', 'Gosu', 'Hybris',
      'JavaScript+PHP', 'Factor', 'HTML+Velocity', 'Mscgen', 'Ooc', 'SQL',
      'HTTP', 'ECL', 'Ragel in Objective C Host', 'XML+Django/Jinja', 'Awk',
      'JSON', 'NASM', 'ANTLR With Ruby Target', 'XML+Myghty'
    ]

    self.getContent()
    self.showPanel()

  def getContent(self):
    view = self.window.active_view()
    self.content = '\n'.join([view.substr(region) for region in view.sel()])
    if not self.content:
      self.content = view.substr(sublime.Region(0, view.size()))

  def showPanel(self):
    self.window.show_quick_panel(self.languages, self.findLang)

  def findLang(self, pos):
    if pos == -1: return
    params = {
      'content': self.content,
      'lexer': self.languages[pos]
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
