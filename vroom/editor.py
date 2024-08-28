import re
import subprocess
from enum import Enum


VimVariant = Enum('VimVariant', ['VIM', 'NEOVIM', 'NEOVIM_07'])


class EditorRunner(object):
  """Object to communicate with a vim or neovim instance."""

  def __init__(self, args, env):
    self.args = args
    self.env = env
    self._vim_variant = None

  def DetectEditor(self):
    """Determine which editor to use and version/feature info."""
    if self._vim_variant is None:
      out, err = subprocess.Popen(
          [self.args.vim_cmd, '--version'],
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
          env=self.env.shell.env,
          universal_newlines=True).communicate()
      if out.startswith('NVIM'):
        self._vim_variant = (
            VimVariant.NEOVIM_07 if re.match(r'NVIM v0\.[0-7]\b', out)
            else VimVariant.NEOVIM)
      else:
        self._vim_variant = VimVariant.VIM
    return self._vim_variant

  def Spawn(self):
    """Runs an editor."""
    variant = self.DetectEditor()
    kwargs = {}
    if variant in (VimVariant.NEOVIM, VimVariant.NEOVIM_07):
      try:
        import vroom.neovim_mod
        Communicator = vroom.neovim_mod.Communicator
        kwargs['pre_v08'] = variant == VimVariant.NEOVIM_07
      except ImportError:
        # neovim extra not available, fall back to vim mode
        Communicator = vroom.vim.Communicator
    else:
      Communicator = vroom.vim.Communicator

    editor = Communicator(
        self.args, self.env.shell.env, self.env.writer, **kwargs)
    editor.Start()
    return editor

