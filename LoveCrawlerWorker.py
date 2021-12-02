from PyQt5.QtCore import QObject, pyqtSignal


class LCWorker(QObject):

  logger = pyqtSignal(str)
  finished = pyqtSignal()

  def __init__(self, main):
    super().__init__();
    self.MainSelf = main;

  def run(self):
    print('run...')
    self.MainSelf.LCC.getWebContent(self.MainSelf.formData['url'])
    self.finished.emit()
  