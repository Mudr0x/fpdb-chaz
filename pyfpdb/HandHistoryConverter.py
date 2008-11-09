#!/usr/bin/python

#Copyright 2008 Carl Gherardi
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, version 3 of the License.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.
#In the "official" distribution you can find the license in
#agpl-3.0.txt in the docs folder of the package.

import Configuration
#import FpdbRegex
import sys
import traceback
import os
import os.path
import xml.dom.minidom
from xml.dom.minidom import Node

class HandHistoryConverter:
	def __init__(self, config, file, sitename):
		print "HandHistory init called"
		self.c         = config
		self.sitename  = sitename
		self.obs       = ""             # One big string
		self.filetype  = "text"
		self.doc       = None     # For XML based HH files
		self.file      = file
		self.hhbase    = self.c.get_import_parameters().get("hhArchiveBase")
		self.hhbase    = os.path.expanduser(self.hhbase)
		self.hhdir     = os.path.join(self.hhbase,sitename)
		self.gametype  = []
#		self.ofile     = os.path.join(self.hhdir,file)

	def __str__(self):
		tmp = "HandHistoryConverter: '%s'\n" % (self.sitename)
		tmp = tmp + "\thhbase:     '%s'\n" % (self.hhbase)
		tmp = tmp + "\thhdir:      '%s'\n" % (self.hhdir)
		tmp = tmp + "\tfiletype:   '%s'\n" % (self.filetype)
		tmp = tmp + "\tinfile:     '%s'\n" % (self.file)
#		tmp = tmp + "\toutfile:    '%s'\n" % (self.ofile)
		tmp = tmp + "\tgametype:   '%s'\n" % (self.gametype[0])
		tmp = tmp + "\tgamebase:   '%s'\n" % (self.gametype[1])
		tmp = tmp + "\tlimit:      '%s'\n" % (self.gametype[2])
		tmp = tmp + "\tsb/bb:      '%s/%s'\n" % (self.gametype[3], self.gametype[4])
		return tmp

	# Functions to be implemented in the inheriting class
	def readSupportedGames(self): abstract

	# should return a list
	#   type  base limit
	# [ ring, hold, nl   , sb, bb ]
	# Valid types specified in docs/tabledesign.html in Gametypes
	def determineGameType(self): abstract
	def readPlayerStacks(self): abstract
	def readBlinds(self): abstract
	def readAction(self): abstract

	def sanityCheck(self):
		sane = False
		base_w = False
		#Check if hhbase exists and is writable
		#Note: Will not try to create the base HH directory
		if not (os.access(self.hhbase, os.W_OK) and os.path.isdir(self.hhbase)):
			print "HH Sanity Check: Directory hhbase '" + self.hhbase + "' doesn't exist or is not writable"
		else:
			#Check if hhdir exists and is writable
			if not os.path.isdir(self.hhdir):
				# In first pass, dir may not exist. Attempt to create dir
				print "Creating directory: '%s'" % (self.hhdir)
				os.mkdir(self.hhdir)
				sane = True
			elif os.access(self.hhdir, os.W_OK):
				sane = True
			else:
				print "HH Sanity Check: Directory hhdir '" + self.hhdir + "' or its parent directory are not writable"

		return sane

	# Functions not necessary to implement in sub class
	def setFileType(self, filetype = "text"):
		self.filetype = filetype

	def processFile(self):
		if not self.sanityCheck():
			print "Cowardly refusing to continue after failed sanity check"
			return
		self.readFile(self.file)
		self.gametype = self.determineGameType()

	def readFile(self, filename):
		"""Read file"""
		print "Reading file: '%s'" %(filename)
		if(self.filetype == "text"):
			infile=open(filename, "rU")
			self.obs = infile.read()
			infile.close()
		elif(self.filetype == "xml"):
			try:
				doc = xml.dom.minidom.parse(filename)
				self.doc = doc
			except:
				traceback.print_exc(file=sys.stderr)

	def writeStars(self):
		"""Write out parsed data"""
#		print sitename + " Game #" + handid + ":  " + gametype + " (" + sb + "/" + bb + " - " + starttime
#		print "Table '" + tablename + "' " + maxseats + "-max Seat #" + buttonpos + " is the button"
#
#		counter = 1
#		for player in seating:
#			print "Seat " + counter + ": " + playername + "($" + playermoney + " in chips"
#
#		print playername + ": posts small blind " + sb
#		print playername + ": posts big blind " + bb
#
#		print "*** HOLE CARDS ***"
#		print "Dealt to " + hero + " [" + holecards + "]"
#
##		ACTION STUFF
#
#		print "*** SUMMARY ***"
#		print "Total pot $" + totalpot + " | Rake $" + rake
#		print "Board [" + boardcards + "]"
#
##		SUMMARY STUFF

#takes a poker float (including , for thousand seperator and converts it to an int
	def float2int (self, string):
		pos=string.find(",")
		if (pos!=-1): #remove , the thousand seperator
			string=string[0:pos]+string[pos+1:]

		pos=string.find(".")
		if (pos!=-1): #remove decimal point
			string=string[0:pos]+string[pos+1:]

		result = int(string)
		if pos==-1: #no decimal point - was in full dollars - need to multiply with 100
			result*=100
		return result
#end def float2int
