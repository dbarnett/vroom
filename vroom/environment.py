"""A vroom test execution environment.

This is an object with all of the vroom verifiers asked. Good for one file.
"""
import vroom.editor
import vroom.output
import vroom.shell


class Environment(object):
  """The environment object.

  Sets up all the verifiers and managers and communicators you'll ever need.
  """

  def __init__(self, filename, args):
    self.args = args
    self.message_strictness = args.message_strictness
    self.system_strictness = args.system_strictness
    self.filename = filename
    self.writer = vroom.output.Writer(filename, args)
    self.shell = vroom.shell.Communicator(filename, self, self.writer)
    self.editor = vroom.editor.EditorRunner(args, self)
    # These are initialized after vim communicator is initialized.
    self.vim = None
    self.buffer = None
    self.messenger = None
