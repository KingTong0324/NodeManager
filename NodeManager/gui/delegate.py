from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class NodeListDelegate(QStyledItemDelegate):
    def paint(self,painter,option,index):
        item_type=index.data(Qt.UserRole)
        if item_type=="country":
            painter.save()
            rect=option.rect
            painter.setFont(QFont("",10,QFont.Weight.Bold))
            painter.drawText(rect.left(),rect.top()+20,index.data())
            painter.drawLine(rect.left(),rect.top()+28,rect.right(),rect.top()+28)
            painter.restore()
            return
        super().paint(painter,option,index)

    def sizeHint(self,option,index):
        if index.data(Qt.UserRole)=="country":
            size=super().sizeHint(option,index)
            size.setHeight(35)
            return size
        return super().sizeHint(option,index)