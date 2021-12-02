from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, Qt
import sys
import time
import LoveCrawlerUI
from LoveCrawlerWorker import LCWorker
from LoveCrawlerCtrl import LoveCrawlerCtrl

class LoveCrawler(QtWidgets.QMainWindow,LoveCrawlerUI.Ui_Form):
  def __init__(self, parent=None):
    super(LoveCrawler, self).__init__(parent)
    self.setupUi(self)
  
  # 窗口居中
  def center(self):
    qr = self.frameGeometry()
    cp = QtWidgets.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

  def onStartClick(self):
    self.thread = QThread()
    self.LCC = LoveCrawlerCtrl(self)
    self.worker = LCWorker(self)
    self.worker.moveToThread(self.thread)
    self.worker.finished.connect(self.thread.quit)
    self.thread.started.connect(self.worker.run)
    self.thread.start()

  def onUrlCheckChanged(self):

    if self.isAllUrlChecked:
      enabled = False
    else:
      enabled = True

    self.videoCheckBox.setEnabled(enabled)
    self.musicCheckBox.setEnabled(enabled)
    self.pictureCheckBox.setEnabled(enabled)
    self.wordCheckBox.setEnabled(enabled)

  @property
  def formData(self):
    self.data = {}
    self.data["url"] = self.urlEdit.text()
    self.data["save_name"] = self.nameEdit.text()
    self.data["save_path"] = self.pathEdit.text()
    self.data["match_suffix"] = self.matchSuffix
    return self.data

  @property
  def matchSuffix(self, suffix = ""):
    if self.videoCheckBox.checkState() == Qt.CheckState.Checked:
      suffix += 'mp4|flv|'
    if self.musicCheckBox.checkState() == Qt.CheckState.Checked:
      suffix += 'mp3|'
    if self.pictureCheckBox.checkState() == Qt.CheckState.Checked:
      suffix += 'jpg|jpeg|png|webp|'
    if self.wordCheckBox.checkState() == Qt.CheckState.Checked:
      suffix += 'pdf|txt'
    return suffix.strip("|")
  
  @property
  def savePath(self):
    return self.pathEdit.text() or str(int(time.time()))
  @property
  def customRegexp(self):
    return self.customRegexpEdit.text()
  @property
  def isSaveFile(self):
    return self.isSaveCheckBox.checkState() == Qt.CheckState.Checked
  @property
  def isAllUrlChecked(self):
    return self.urlCheckBox.checkState() == Qt.CheckState.Checked
  @property
  def isTimeRandom(self):
    return self.isRandomCheckBox.checkState() == Qt.CheckState.Checked

def main():
  app = QApplication(sys.argv)
  form = LoveCrawler()
  form.show()
  form.center()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()