import sys
import os
import importlib
from threading import Thread
from pkg_resources import resource_string, resource_filename
from functools import cmp_to_key
import locale

from cardholder.cardholder import CardHolder
from cardholder.cardholder import Card
from cardholder.cardholder import CollectCardsThread

from aqfilter.aqfilter import AQFilter

from akoteka.gui.pyqt_import import *
from akoteka.gui.card_panel import CardPanel
from akoteka.gui.configuration_dialog import ConfigurationDialog
from akoteka.gui.control_buttons_holder import ControlButtonsHolder

from akoteka.accessories import collect_cards
from akoteka.accessories import filter_key
from akoteka.accessories import clearLayout
from akoteka.accessories import FlowLayout

from akoteka.constants import *
from akoteka.setup.setup import getSetupIni

from akoteka.handle_property import _
from akoteka.handle_property import re_read_config_ini
from akoteka.handle_property import config_ini
from akoteka.handle_property import get_config_ini


# =======================
#
# Advanced Filter HOLDER
#
# =======================
class AdvancedFilterHolder(QWidget):
    
    changed = pyqtSignal()
    
    def __init__(self, parent):
        super().__init__(parent)

        self_layout = QVBoxLayout(self)
        self.setLayout( self_layout )
        self_layout.setContentsMargins(0, 0, 0, 0)
        self_layout.setSpacing(0)    

        holder = QWidget(self)
        holder_layout = QGridLayout(holder)
        holder.setLayout( holder_layout )
        holder_layout.setContentsMargins(0, 0, 0, 0)
        holder_layout.setSpacing(1)

        self_layout.addWidget(QHLine())
        self_layout.addWidget(holder)
        
        filter_style_box = '''
            AQFilter { 
                max-width: 200px; min-width: 200px; border: 1px solid gray; border-radius: 5px;
            }
        '''

        combobox_short_style_box = '''
            QComboBox { 
                max-width: 150px; max-width: 150px; border: 1px solid gray; border-radius: 5px;
            }
        '''
        combobox_long_style_box = '''
            QComboBox { 
                max-width: 150px; max-width: 150px; border: 1px solid gray; border-radius: 5px;
            }
        '''
        
        dropdown_style_box ='''
            QComboBox QAbstractItemView::item { 
                color: red;
                max-height: 15px;
            }
        '''            

        # ----------
        #
        # Title
        #
        # ----------
        self.title_label = QLabel(_('title_title') + ": ")
        self.title_filter = AQFilter(holder)
        self.title_filter.setStyleSheet(filter_style_box)
        holder_layout.addWidget(self.title_label, 0, 0, 1, 1)
        holder_layout.addWidget(self.title_filter, 0, 1, 1, 1)

        # ----------
        #
        # Director
        #
        # ----------
        self.director_label = QLabel(_('title_director') + ": ")
        self.director_filter = AQFilter(holder)
        self.director_filter.setStyleSheet(filter_style_box)
        #self.director_filter.setMinCharsToShowList(0)
        holder_layout.addWidget(self.director_label, 1, 0, 1, 1)
        holder_layout.addWidget(self.director_filter, 1, 1, 1, 1)
        
        # ----------
        #
        # Actors
        #
        # ----------
        self.actor_label = QLabel(_('title_actor') + ": ")
        self.actor_filter = AQFilter(holder)
        self.actor_filter.setStyleSheet(filter_style_box)
        holder_layout.addWidget(self.actor_label, 2, 0, 1, 1)
        holder_layout.addWidget(self.actor_filter, 2, 1, 1, 1)

        # ---
     
        # ----------
        #
        # Genre
        #
        # ----------
        self.genre_label = QLabel(_('title_genre') + ": ")
        self.genre_filter = AQFilter(holder)
        self.genre_filter.setStyleSheet(filter_style_box)
        holder_layout.addWidget(self.genre_label, 0, 2, 1, 1)
        holder_layout.addWidget(self.genre_filter, 0, 3, 1, 1)
        
        # ----------
        #
        # Theme
        #
        # ----------
        self.theme_label = QLabel(_('title_theme') + ": ")
        self.theme_filter = AQFilter(holder)
        self.theme_filter.setStyleSheet(filter_style_box)
        holder_layout.addWidget(self.theme_label, 1, 2, 1, 1)
        holder_layout.addWidget(self.theme_filter, 1, 3, 1, 1)

        # ---
        
        # ----------
        #
        # Sound
        #
        # ----------
        self.sound_label = QLabel(_('title_sound') + ": ")
        self.sound_combobox = QComboBox(self)
        self.sound_combobox.setFocusPolicy(Qt.NoFocus)
        self.sound_combobox.setStyleSheet(combobox_long_style_box + dropdown_style_box)
        self.sound_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
  
        holder_layout.addWidget(self.sound_label, 0, 4, 1, 1)
        holder_layout.addWidget(self.sound_combobox, 0, 5, 1, 1)

        # ----------
        #
        # Subtitle
        #
        # ----------
        self.sub_label = QLabel(_('title_sub') + ": ")
        self.sub_combobox = QComboBox(self)
        self.sub_combobox.setFocusPolicy(Qt.NoFocus)
        self.sub_combobox.setStyleSheet(combobox_long_style_box + dropdown_style_box)
        self.sub_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
  
        holder_layout.addWidget(self.sub_label, 1, 4, 1, 1)
        holder_layout.addWidget(self.sub_combobox, 1, 5, 1, 1)
  
        # ----------
        #
        # Country
        #
        # ----------
        self.country_label = QLabel(_('title_country') + ": ")
        self.country_combobox = QComboBox(self)
        self.country_combobox.setFocusPolicy(Qt.NoFocus)
        self.country_combobox.setStyleSheet(combobox_long_style_box + dropdown_style_box)        
        self.country_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
  
        holder_layout.addWidget(self.country_label, 2, 4, 1, 1)
        holder_layout.addWidget(self.country_combobox, 2, 5, 1, 1)

        # ---
        
        # ----------
        #
        # Year
        #
        # ----------
        self.year_from_label = QLabel(_('title_year') + ": ")
        year_to_label = QLabel('-')
        self.year_from_combobox = QComboBox(self)
        self.year_from_combobox.setFocusPolicy(Qt.NoFocus)
        self.year_from_combobox.setStyleSheet(combobox_short_style_box + dropdown_style_box)
        self.year_from_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        #self.year_from_combobox.addItem("        ")

        self.year_to_combobox = QComboBox()
        self.year_to_combobox.setFocusPolicy(Qt.NoFocus)
        self.year_to_combobox.setStyleSheet(combobox_short_style_box + dropdown_style_box)
        self.year_to_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        #self.year_to_combobox.addItem("        ")
  
        holder_layout.addWidget(self.year_from_label, 0, 6, 1, 1)
        holder_layout.addWidget(self.year_from_combobox, 0, 7, 1, 1)
        holder_layout.addWidget(year_to_label, 0, 8, 1, 1)
        holder_layout.addWidget(self.year_to_combobox, 0, 9, 1, 1)

        # ----------
        #
        # Length
        #
        # ----------
        self.length_from_label = QLabel(_('title_length') + ": ")
        length_to_label = QLabel('-')
        self.length_from_combobox = QComboBox()
        self.length_from_combobox.setFocusPolicy(Qt.NoFocus)
        self.length_from_combobox.setStyleSheet(combobox_short_style_box + dropdown_style_box)
        self.length_from_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        #self.length_from_combobox.addItem("        ")

        self.length_to_combobox = QComboBox()
        self.length_to_combobox.setFocusPolicy(Qt.NoFocus)
        self.length_to_combobox.setStyleSheet(combobox_short_style_box + dropdown_style_box)        
        self.length_to_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        #self.length_to_combobox.addItem("        ")
  
        holder_layout.addWidget(self.length_from_label, 1, 6, 1, 1)
        holder_layout.addWidget(self.length_from_combobox, 1, 7, 1, 1)
        holder_layout.addWidget(length_to_label, 1, 8, 1, 1)
        holder_layout.addWidget(self.length_to_combobox, 1, 9, 1, 1)

        # ----------
        #
        # Stretch
        #
        # ----------
        holder_layout.setColumnStretch(10, 1)

    def refresh_label(self):
       self.title_label.setText(_('title_title') + ": ")
       self.director_label.setText(_('title_director') + ": ")
       self.actor_label.setText(_('title_actor') + ": ")
       self.genre_label.setText(_('title_genre') + ": ")
       self.theme_label.setText(_('title_theme') + ": ")
       self.sound_label.setText(_('title_sound') + ": ")
       self.sub_label.setText(_('title_sub') + ": ")
       self.country_label.setText(_('title_country') + ": ")
       self.year_from_label.setText(_('title_year') + ": ")
       self.length_from_label.setText(_('title_length') + ": ")
       

    def clear_title(self):
        self.title_filter.clear()

    def clear_director(self):
        self.director_filter.clear()

    def clear_actor(self):
        self.actor_filter.clear()

    def clear_genre(self):
        self.genre_filter.clear()

    def clear_theme(self):
        self.theme_filter.clear()

    def clear_sound(self):
        self.sound_combobox.clear()
        self.sound_combobox.addItem("                       ")
        
    def clear_sub(self):
        self.sub_combobox.clear()
        self.sub_combobox.addItem("                       ")
        
    def clear_country(self):
        self.country_combobox.clear()
        self.country_combobox.addItem("                       ")

    def clear_year(self):
        self.year_from_combobox.clear()
        self.year_to_combobox.clear()
        self.year_from_combobox.addItem("            ")
        self.year_to_combobox.addItem("            ")

    def clear_length(self):
        self.length_from_combobox.clear()
        self.length_to_combobox.clear()
        self.length_from_combobox.addItem("            ")
        self.length_to_combobox.addItem("            ")

    # ---
    
    def add_title(self, value):
        self.title_filter.addItemToList(value, value)
    
    def add_director(self, director):
        self.director_filter.addItemToList(director, director)

    def add_actor(self, actor):
        self.actor_filter.addItemToList(actor, actor)

    def add_genre(self, genre, index):
        self.genre_filter.addItemToList(genre, index)
    
    def add_theme(self, theme, index):
        self.theme_filter.addItemToList(theme, index)
    
    def add_sound(self, value, id):
        self.sound_combobox.addItem(value, id)

    def add_sub(self, value, id):
        self.sub_combobox.addItem(value, id)
 
    def add_country(self, value, id):
        self.country_combobox.addItem(value, id)
        
    def add_length(self, length):
        self.length_from_combobox.addItem(length)
        self.length_to_combobox.addItem(length)

    def add_year(self, year):
        self.year_from_combobox.addItem(year)
        self.year_to_combobox.addItem(year)
        pass
        


    
    

        



