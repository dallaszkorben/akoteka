import sys
import math
from akoteka.gui.pyqt_import import *
from itertools import cycle

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Card selector'
        self.left = 10
        self.top = 10
        self.width = 420
        self.height = 300
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height) 
        self.setStyleSheet('background: gray')
 
        self.scroll_layout = QVBoxLayout(self)
        self.scroll_layout.setContentsMargins(15, 15, 15, 15)
        self.scroll_layout.setSpacing(0)
        self.setLayout(self.scroll_layout)

        self.actual_card_holder = CardHolder(            
            self, 
            [],
            "Kezdocim",
            self.get_new_card
        )
        
        self.actual_card_holder.set_background_color(QColor(Qt.yellow))
        self.actual_card_holder.set_border_width(10)
        self.scroll_layout.addWidget(self.actual_card_holder)
        
        cdl = []        
        cdl.append("Elso")
        cdl.append("Masodik")
        cdl.append("Harmadik")
        cdl.append("Negyedik")
        cdl.append("Otodik")
        cdl.append("6")
        cdl.append("7")
        cdl.append("8")
        cdl.append("9")
        cdl.append("10")
        self.actual_card_holder.refresh(cdl)
        
        
        next_button = QPushButton("next",self)
        next_button.clicked.connect(self.actual_card_holder.animated_move_to_next)
        
        previous_button = QPushButton("prev",self)
        previous_button.clicked.connect(self.actual_card_holder.animated_move_to_previous)
        
        self.scroll_layout.addStretch(1)
        self.scroll_layout.addWidget(previous_button)
        self.scroll_layout.addWidget(next_button)
        
        self.show()
 
    def get_new_card(self, card_data, local_index, index):
        card = Card(card_data, self.actual_card_holder, local_index, index)
        #card.set_border_color(QColor(Qt.blue))
        #card.set_background_color(QColor(Qt.green))
        #card.set_border_radius( 15 )
        #card.set_border_width(8)
        
        panel = card.get_panel()
        layout = panel.get_layout()
        
        # Construct the Card
        label=QLabel(card_data + "\n\n\n\n\n\n\n\n\n\nHello")
        layout.addWidget(label)
        layout.addWidget(QPushButton("hello"))
        
        return card

import time 
 
 
 
class AnimateRoll(QThread):
    positionChanged = pyqtSignal(int)

    def __init__(self, loop, value, sleep=0.05):
        QThread.__init__(self)
        self.loop = loop
        self.value = value
        self.sleep = sleep
            
        print('animation: ', loop, value, sleep)

    def __del__(self):
        self.wait()
    
    def run(self): 
        for i in range(self.loop):
            time.sleep(self.sleep)
            #self.sleep(2)
            self.positionChanged.emit(self.value)
            
        print('finished')


 
# =========================
#
# Card Holder
#
# =========================
class CardHolder( QWidget ):
    
    resized = QtCore.pyqtSignal(int,int)
    moved_to_front = QtCore.pyqtSignal(int)

    DEFAULT_MAX_OVERLAPPED_CARDS = 4    
    DEFAULT_BORDER_WIDTH = 5
    DEFAULT_BACKGROUND_COLOR = QColor(Qt.red)
    DEFAULT_BORDER_RADIUS = 10
    
    def __init__(self, parent, recent_card_structure, title_hierarchy, get_new_card):
        super().__init__()

        self.get_new_card = get_new_card
        self.parent = parent
        self.title_hierarchy = title_hierarchy
        self.recent_card_structure = recent_card_structure
        
        self.shown_card_list = []
        self.card_descriptor_list = []

        self.set_max_overlapped_cards(CardHolder.DEFAULT_MAX_OVERLAPPED_CARDS, False)        
        self.set_border_width(CardHolder.DEFAULT_BORDER_WIDTH, False)
        self.set_border_radius(CardHolder.DEFAULT_BORDER_RADIUS, False)
        self.set_background_color(CardHolder.DEFAULT_BACKGROUND_COLOR, False)
        
        self.self_layout = QVBoxLayout(self)
        self.setLayout(self.self_layout)

        self.actual_card_index = 0
        self.rate_of_movement =0
        
        self.show()

    def refresh(self, filtered_card_list): 
        self.fill_up_card_descriptor_list(filtered_card_list)
        self.select_actual_card()        

    def set_border_width(self, width, update=True):
        self.border_width = width
        if update:
            self.update()
        
    def get_border_width(self):
        return self.border_width

    def set_background_color(self, color, update=True):
        self.background_color = color
        ## without this line it wont paint the background, but the children get the background color info
        ## with this line, the rounded corners will be ruined
        #self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        #self.setStyleSheet('background-color: ' + self.background_color.name())
        if update:
            self.update()
        
    def set_max_overlapped_cards(self, number, update=True):
        self.max_overlapped_cards = number
        if update:
            self.select_index(self.actual_card_index)
        
    def set_border_radius(self, radius, update=True):
        self.border_radius = radius
        if update:
            self.update()
        
    def get_max_overlapped_cards(self):
        return self.max_overlapped_cards
  
    def resizeEvent(self, event):
        self.resized.emit(event.size().width(),event.size().height())
        return super(CardHolder, self).resizeEvent(event)
     
    def fill_up_card_descriptor_list(self, filtered_card_list = []):
        
        self.card_descriptor_list = []
        for c in filtered_card_list:
            self.card_descriptor_list.append(c)
 
    def remove_all_cards(self):
        for card in self.shown_card_list:
            card.setParent(None)
            card = None

    def remove_card(self, card):
        card.setParent(None)
        card = None

    def get_rate_of_movement(self):
        return self.rate_of_movement
    

    def animated_move_to_next(self):
        rate = self.get_rate_of_movement()
        
        if rate > 0:
            loop = 10 - rate
        elif rate < 0:
            loop = -rate
        else:
            loop = 10
            
        self.animate = AnimateRoll(int(loop), 1, 0.05)
        self.animate.positionChanged.connect(self.rolling)
        self.animate.start()
        
    def animated_move_to_previous(self):
        rate = self.get_rate_of_movement()
        
        if rate > 0:
            loop = rate
        elif rate < 0:
            loop = 10+rate
        else:
            loop = 10
            
        self.animate = AnimateRoll(int(loop), -1, 0.05)
        self.animate.positionChanged.connect(self.rolling)
        self.animate.start()        
        
    
    def animated_move_to_closest_descreet_position(self):
        rate = self.get_rate_of_movement()
        
        if rate != 0:
            if rate > 0:
                if rate >= 6:
                    value = 1
                    loop = 10 - rate                    
                else:
                    value = -1
                    loop = rate
        
            elif rate < 0:
                if rate <= -6:
                    value = -1
                    loop = 10 + rate
                else:
                    value = 1
                    loop = -rate
            
            self.animate = AnimateRoll(int(loop), value, 0.01)
            self.animate.positionChanged.connect(self.rolling)
            self.animate.start()
            
        
        





    def select_next_card(self):
        self.select_index(self.actual_card_index + 1)

    def select_previous_card(self):
        self.select_index(self.actual_card_index - 1)
        
    def select_actual_card(self):
        self.select_index(self.actual_card_index)
    
    def select_index(self, index):
        index_corr = self.index_correction(index)
        
        self.actual_card_index = index_corr
        self.remove_all_cards()
        position = None
        self.shown_card_list = [None for i in range(index_corr + min(self.max_overlapped_cards, len(self.card_descriptor_list)-1), index_corr - 1, -1) ]
        
        for i in range( index_corr + min(self.max_overlapped_cards, len(self.card_descriptor_list)-1), index_corr - 1, -1):
            i_corr = self.index_correction(i)
            
            if( i_corr < len(self.card_descriptor_list)):

                local_index = i-index_corr
                card = self.get_new_card(self.card_descriptor_list[i_corr], local_index, i_corr )                                
                position = card.place(local_index)
                
                self.shown_card_list[local_index] = card

        # Control the Height of the CardHolder
        self.setMinimumHeight(position[0].y() + position[1].y() + self.border_width )











    # ------------------------------
    #
    # ROLLING
    #
    # ------------------------------
    def rolling(self, delta_rate):
        if self.rate_of_movement >= 10 or self.rate_of_movement <= -10:
            self.rate_of_movement = 0

        self.rate_of_movement = self.rate_of_movement + delta_rate

#        print(self.rate_of_movement)
        
        # Did not start to roll
        if len(self.shown_card_list) <= self.get_max_overlapped_cards() + 1:
            
            # add new card to the beginning
            first_card = self.shown_card_list[0]                
            first_card_index = self.index_correction(first_card.index - 1)
            card = self.get_new_card(self.card_descriptor_list[first_card_index], -1, first_card_index ) 
            self.shown_card_list.insert(0, card)
            
            # add a new card to the end
            last_card = self.shown_card_list[len(self.shown_card_list)-1]                
            last_card_index = self.index_correction(last_card.index + 1)
            card = self.get_new_card(self.card_descriptor_list[last_card_index], self.get_max_overlapped_cards() + 1, last_card_index ) 
            self.shown_card_list.append(card)
            
            # Re-print to avoid the wrong-overlapping
            for card in self.shown_card_list[::-1]:
                card.setParent(None)
                card.setParent(self)
                card.show()        

#        print( "after add: ", [(c.local_index, c.card_data) for c in self.shown_card_list])
            
        # adjust the 
        rate = self.rate_of_movement / 10
        if self.rate_of_movement >= 0:
            self.rolling_adjust_forward(rate)
        else:
            self.rolling_adjust_backward(rate)

        # show the cards in the right position
        rate = self.rate_of_movement / 10
        for i, card in enumerate(self.shown_card_list):
            virtual_index = card.local_index - rate
            card.place(virtual_index, True)
        print( [(c.local_index, c.card_data) for c in self.shown_card_list])
#        print()

    def rolling_adjust_forward(self,rate):
        
        if rate >= 1.0:
            self.rate_of_movement = 0
            
            # remove the first 2 cards from the list and from CardHolder
            for i in range(2):
                card_to_remove = self.shown_card_list.pop(0)
                card_to_remove.setParent(None)

            # re-index
            for i, card in enumerate(self.shown_card_list):
                card.local_index = i
                
        elif rate == 0:
            # remove the first card from the list and from CardHolder
            card_to_remove = self.shown_card_list.pop(0)
            card_to_remove.setParent(None)
            
            # remove the last card from the list and from CardHolder
            card_to_remove = self.shown_card_list.pop(len(self.shown_card_list) - 1)
            card_to_remove.setParent(None)
            

    def rolling_adjust_backward(self,rate):
        
        if rate <= -1.0:
            self.rate_of_movement = 0
        
            # remove the 2 last cards from the list and from CardHolder
            for i in range(2):
                card_to_remove = self.shown_card_list.pop(len(self.shown_card_list) - 1)
                card_to_remove.setParent(None)
#            print( "after remove:", [(c.local_index, c.card_data) for c in self.shown_card_list])
            
            # re-index
            for i, card in enumerate(self.shown_card_list):
                card.local_index = i





















        
#    def enterEvent(self, event):
#        self.rate_of_movement = 0

    # Mouse Hover out
#    def leaveEvent(self, event):
#        self.rate_of_movement = 0

    def index_correction(self, index):
        return (len(self.card_descriptor_list) - abs(index) if index < 0 else index) % len(self.card_descriptor_list)

    def paintEvent(self, event):
        s = self.size()
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setBrush( self.background_color )

        qp.drawRoundedRect(0, 0, s.width(), s.height(), self.border_radius, self.border_radius)
        qp.end()  

    def wheelEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        value = event.angleDelta().y()/8/15
        self.rolling(value)
        #if value > 0:
            #self.select_next_card()            
        #else:
            #self.select_previous_card()
  
  #---
  
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            self.card_start_position = self.geometry().topLeft()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        delta_y = self.get_delta_y(event.pos().y())        
        
        self.drag_card(delta_y)        
        
#        #self.move( tl.x(), tl.y() +  (event.pos().y() - self.drag_start_position.y()) )

#    def mouseReleaseEvent(self, event):
#        self.parent.drop_card(self.local_index, self.index)
#        self.drag_start_position = None
#        self.card_start_position = None
        
        return QWidget.mouseMoveEvent(self, event)

    def get_delta_y(self, y):
        tl=self.geometry().topLeft()
        return tl.y() +  (y - self.drag_start_position.y()) - self.card_start_position.y()



        
  
  
  
  
  
# ==================
#
# Panel
#
# ==================
class Panel(QWidget):
    DEFAULT_BORDER_WIDTH = 5
    DEFAULT_BACKGROUND_COLOR = QColor(Qt.lightGray)
    
    def __init__(self):
        super().__init__()
        
        self.self_layout = QVBoxLayout()
        self.self_layout.setSpacing(1)
        self.setLayout(self.self_layout)

        self.set_background_color(Panel.DEFAULT_BACKGROUND_COLOR, False)        
        self.set_border_width(Panel.DEFAULT_BORDER_WIDTH, False)
        #self.set_border_radius(border_radius, False)

    def get_layout(self):
        return self.self_layout
    
    def set_border_radius(self, radius, update=True):
        self.border_radius = radius
        if update:
            self.update()
        
    def set_border_width(self, width, update=True):
        self.border_width = width
        self.self_layout.setContentsMargins( self.border_width, self.border_width, self.border_width, self.border_width )
        if update:
            self.update()

    def set_background_color(self, color, update=True):
        self.background_color = color
        
        ## without this line it wont paint the background, but the children get the background color info
        ## with this line, the rounded corners will be ruined
        #self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: ' + self.background_color.name())
        
        if update:            
            self.update()
    
    def paintEvent(self, event):
        s = self.size()
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setBrush( self.background_color )

        qp.drawRoundedRect(0, 0, s.width(), s.height(), self.border_radius, self.border_radius)
        qp.end()    
    

# ==================
#
# Card
#
# ==================
class Card(QWidget):
    
    DEFAULT_RATE_OF_WIDTH_DECLINE = 10
    DEFAULT_BORDER_WIDTH = 2
    DEFAULT_BORDER_RADIUS = 10    
    DEFAULT_BORDER_COLOR = QColor(Qt.green)
    
    def __init__(self, card_data, card_holder, local_index, index):
        super().__init__(card_holder)

        self.card_data = card_data
        self.index = index
        self.local_index = local_index
        self.card_holder = card_holder
        self.actual_position = 0
        
        self.self_layout = QVBoxLayout(self)
        self.setLayout(self.self_layout)
        #self.self_layout.setContentsMargins(self.border_width,self.border_width,self.border_width,self.border_width)
        self.self_layout.setSpacing(0)
        
        ## without this line it wont paint the background, but the children get the background color info
        ## with this line, the rounded corners will be ruined
        #self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        #self.setStyleSheet('background-color: ' + "yellow")  

        # Panel where the content could be placed
        self.panel = Panel()
        self.panel_layout = self.panel.get_layout()
        self.self_layout.addWidget(self.panel)
        
        self.border_radius = Card.DEFAULT_BORDER_RADIUS
        self.set_border_width(Card.DEFAULT_BORDER_WIDTH, False)
        self.set_border_radius(Card.DEFAULT_BORDER_RADIUS, False)        
        self.set_rate_of_width_decline(Card.DEFAULT_RATE_OF_WIDTH_DECLINE, False)
        self.set_border_color(Card.DEFAULT_BORDER_COLOR, False)
        
        # Connect the widget to the Container's Resize-Event
        self.card_holder.resized.connect(self.resized)
        
        self.drag_start_position = None
        #self.setDragEnabled(True)
#        self.setAcceptDrops(True)
 
 
    def set_background_color(self, color):
        #self.background_color = color
        #self.setStyleSheet('background-color: ' + self.background_color.name())
        #self.update()
        self.panel.set_background_color(color)

    def set_border_color(self,color, update=True):
        self.border_color = color
        if update:
            self.update()      

    def set_border_width(self, width, update=True):
        self.border_width = width
        self.self_layout.setContentsMargins(self.border_width,self.border_width,self.border_width,self.border_width)
        self.panel.set_border_radius(self.border_radius - self.border_width, update)
        if update:
            self.update()

    def set_border_radius(self, radius, update=True):
        self.border_radius = radius
        self.panel.set_border_radius(self.border_radius - self.border_width, update)
        if update:
            self.update()

    def set_rate_of_width_decline(self, rate, update=True):
        self.rate_of_width_decline = rate
    
    
    def get_panel(self):
        return self.panel
 
    def paintEvent(self, event):
        s = self.size()
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setBrush( self.border_color)

        qp.drawRoundedRect(0, 0, s.width(), s.height(), self.border_radius, self.border_radius)
        qp.end()
 
 
 
 
 
#    def mousePressEvent(self, event):
#        if event.button() == Qt.LeftButton:
#            self.drag_start_position = event.pos()
#            self.card_start_position = self.geometry().topLeft()
#
#    def mouseMoveEvent(self, event):
#        if not (event.buttons() & Qt.LeftButton):
#            return
#        delta_y = self.get_delta_y(event.pos().y())        
#        self.parent.drag_card(self.local_index, self.index, delta_y)        
#        
#        #self.move( tl.x(), tl.y() +  (event.pos().y() - self.drag_start_position.y()) )
#
#    def mouseReleaseEvent(self, event):
#        #delta_y = self.get_delta_y(event.pos().y())
#        self.parent.drop_card(self.local_index, self.index)
#        self.drag_start_position = None
#        self.card_start_position = None
#        
#
#    def get_delta_y(self, y):
#        tl=self.geometry().topLeft()
#        return tl.y() +  (y - self.drag_start_position.y()) - self.card_start_position.y()














        
 
#    def mouseMoveEvent(self, event):
#        if not (event.buttons() & Qt.LeftButton):
#            return
#        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
#            return
#        drag = QDrag(self)
#        mimedata = QMimeData()
#        
#        #mimedata.setText(self.text())
#        mimedata.setText(str(self.index))
#        
#        drag.setMimeData(mimedata)
#        pixmap = QPixmap(self.size())
#        painter = QPainter(pixmap)
##        painter.drawPixmap(self.rect(), self.grab())
#        painter.end()
#        drag.setPixmap(pixmap)
#        drag.setHotSpot(event.pos())
#        drag.exec_(Qt.CopyAction | Qt.MoveAction)

 
#    def mousePressEvent(self, event):
#        if event.button() == Qt.LeftButton:
#            self.drag_start_position = event.pos()
#        #self.parent.resized.connect(self.resized)
#        #self.parent.moved_to_front.emit(self.index)
#        
#        if self.local_index != 0:
#            self.parent.select_index(self.index)
        
#    def dragEnterEvent(self, e):
           
   
    # ---------------------------------------------
    # The offset of the Card from the left side as 
    # 'The farther the card is the narrower it is'
    # ---------------------------------------------
    def get_x_offset(self, local_index):
        return  local_index * self.rate_of_width_decline
 
    # ----------------------------------------
    #
    # Resize the width of the Card
    #
    # It is called when:
    # 1. CardHolder emits a resize event
    # 2. The Card is created and Placed
    #
    # ----------------------------------------
    def resized(self, width, height, local_index=None):
        # The farther the card is the narrower it is
        if local_index==None:
            local_index = self.local_index
        standard_width = width - 2*self.card_holder.get_border_width() - 2*self.get_x_offset(local_index)
        self.resize( standard_width, self.sizeHint().height() )

    # ---------------------------------------
    #
    # Place the Card into the given position
    #
    # 0. position means the card is in front
    # 1. position is behind the 0. position
    # and so on
    # ---------------------------------------
    def place(self, local_index, front_remove=False):
        
        # Need to resize and reposition the Car as 'The farther the card is the narrower it is'
        self.resized(self.card_holder.width(), self.card_holder.height(), local_index)
        x_position = self.card_holder.get_border_width() + self.get_x_offset(local_index)
        y_position = self.card_holder.get_border_width() + self.get_y_position(local_index)
        
        if front_remove:
            y_position = y_position - local_index * (math.exp(5 - 5 * local_index) / 2000) * self.height()
            
        self.move( x_position, y_position )
        
        self.show()
        
        return(QPoint(x_position, y_position), QPoint(self.width(),self.height()))

    def get_y_position(self, local_index):
        max_card = self.card_holder.get_max_overlapped_cards()
        return ( max_card - min(local_index, max_card) ) * ( self.card_holder.get_max_overlapped_cards() - local_index ) * 6







        

  
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    #ex.start_card_holder()
    sys.exit(app.exec_())