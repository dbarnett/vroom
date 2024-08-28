from enum import Enum


VimVariant = Enum('VimVariant', ['VIM', 'NEOVIM'])


class EditorRunner(object):
  """Object to communicate with a vim or neovim instance."""

  def __init__(self, args, env):
    self.args = args
    self.env = env
    self._vim_variant = None

  def DetectEditor(self):
    """Determine which editor to use and version/feature info."""
    if self._vim_variant is None:
      self._vim_variant = (VimVariant.NEOVIM if self.args.neovim
                           else VimVariant.VIM)
    return self._vim_variant

  def Spawn(self):
    """Runs an editor."""
    variant = self.DetectEditor()
    if variant == VimVariant.NEOVIM:
      import vroom.neovim_mod
      Communicator = vroom.neovim_mod.Communicator
    else:
      Communicator = vroom.vim.Communicator

    editor = Communicator(self.args, self.env.shell.env, self.env.writer)
    editor.Start()
    return editor

