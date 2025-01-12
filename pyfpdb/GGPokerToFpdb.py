#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright 2008-2011, Carl Gherardi
#    
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
########################################################################

import L10n
_ = L10n.get_translation()

# TODO: straighten out discards for draw games

import sys
from HandHistoryConverter import *
from decimal_wrapper import Decimal

# PokerStars HH Format

class GGPoker(HandHistoryConverter):

    # Class Variables

    sitename = "GGPoker"
    filetype = "text"
    codepage = ("utf8", "cp1252")
    siteId   = 27 # Needs to match id entry in Sites database
    sym = {'USD': "\$", 'T$': "", "play": "", }         # ADD Euro, Sterling, etc HERE
    substitutions = {
                     'LEGAL_ISO' : "USD|CNY",      # legal ISO currency codes
                            'LS' : u"\$|\¥|", # legal currency symbols - Euro(cp1252, utf-8)
                           'PLYR': r'\s?(?P<PNAME>.+?)',
                            'CUR': u"(\$|\¥|)",
                          'BRKTS': r'(\(button\) |\(small blind\) |\(big blind\) |\(button blind\) |\(button\) \(small blind\) |\(small blind/button\) |\(button\) \(big blind\) )?',
                    }
                    
    # translations from captured groups to fpdb info strings
    Lim_Blinds = {      '0.04': ('0.01', '0.02'),         '0.08': ('0.02', '0.04'),
                        '0.10': ('0.02', '0.05'),         '0.20': ('0.05', '0.10'),
                        '0.40': ('0.10', '0.20'),         '0.50': ('0.10', '0.25'),
                        '1.00': ('0.25', '0.50'),         '1': ('0.25', '0.50'),
                        '2.00': ('0.50', '1.00'),         '2': ('0.50', '1.00'),
                        '4.00': ('1.00', '2.00'),         '4': ('1.00', '2.00'),
                        '6.00': ('1.00', '3.00'),         '6': ('1.00', '3.00'),
                        '8.00': ('2.00', '4.00'),         '8': ('2.00', '4.00'),
                       '10.00': ('2.00', '5.00'),        '10': ('2.00', '5.00'),
                       '16.00': ('4.00', '8.00'),        '16': ('4.00', '8.00'),
                       '20.00': ('5.00', '10.00'),       '20': ('5.00', '10.00'),
                       '30.00': ('10.00', '15.00'),      '30': ('10.00', '15.00'),
                       '40.00': ('10.00', '20.00'),      '40': ('10.00', '20.00'),
                       '50.00': ('10.00', '25.00'),      '50': ('10.00', '25.00'),
                       '60.00': ('15.00', '30.00'),      '60': ('15.00', '30.00'),
                       '80.00': ('20.00', '40.00'),      '80': ('20.00', '40.00'),
                      '100.00': ('25.00', '50.00'),     '100': ('25.00', '50.00'),
                      '150.00': ('50.00', '75.00'),     '150': ('50.00', '75.00'),
                      '200.00': ('50.00', '100.00'),    '200': ('50.00', '100.00'),
                      '400.00': ('100.00', '200.00'),   '400': ('100.00', '200.00'),
                      '500.00': ('100.00', '250.00'),   '500': ('100.00', '250.00'),
                      '600.00': ('150.00', '300.00'),   '600': ('150.00', '300.00'),
                      '800.00': ('200.00', '400.00'),   '800': ('200.00', '400.00'),
                     '1000.00': ('250.00', '500.00'),  '1000': ('250.00', '500.00'),
                     '2000.00': ('500.00', '1000.00'), '2000': ('500.00', '1000.00'),
                     '4000.00': ('1000.00', '2000.00'), '4000': ('1000.00', '2000.00'),
                    '10000.00': ('2500.00', '5000.00'), '10000': ('2500.00', '5000.00'),
                    '20000.00': ('5000.00', '10000.00'),'20000': ('5000.00', '10000.00'),
                    '40000.00': ('10000.00', '20000.00'),'40000': ('10000.00', '20000.00'),
                  }

    limits = { 
              'No Limit':'nl', 
              'Pot Limit':'pl', 
              'Fixed Limit':'fl', 
              'Limit':'fl',
              '(NL postflop)': 'pn'
              }
    games = {                          # base, category
                              "Hold'em" : ('hold','holdem'),
                            "ShortDeck" : ('hold','6_holdem'),
                                'Omaha' : ('hold','omahahi'),
                          'Omaha Hi/Lo' : ('hold','omahahilo'),
                                'PLO'   : ('hold','omahahi'), 
                                'PLO-5' : ('hold', '5_omahahi'),
                                'PLO-6' : ('hold', '6_omahahi')
               }
#    mixes = {
#                                 'HORSE': 'horse',
#                                '8-Game': '8game',
#                                '8-GAME': '8game',
#                                  'HOSE': 'hose',
#                         'Mixed PLH/PLO': 'plh_plo',
#                         'Mixed NLH/PLO': 'nlh_plo',
#                       'Mixed Omaha H/L': 'plo_lo',
#                        'Mixed Hold\'em': 'mholdem',
#                           'Mixed Omaha': 'momaha',
#                           'Triple Stud': '3stud'
#               } # Legal mixed games
    currencies = { '$':'USD', '':'T$', u'¥':'CNY'}
    
    #Poker Hand #TM316262814: Tournament #9364957, WSOP #77: $5,000 No Limit Hold'em Main Event [Flight W], $25M GTD Hold'em No Limit - Level10 (1,000/2,000) - 2020/08/30 15:49:08
    #Poker Hand #TM247771977: Tournament #5259595, Daily Special $250 Hold'em No Limit - Level2 (60/120) - 2020/06/02 19:17:33
    # Static regexes
    re_GameInfo     = re.compile(u"""
          Poker\sHand\s\#[A-Z]{0,2}(?P<HID>[0-9]+):\s+
          (\{.*\}\s+)?((?P<TOUR>((Zoom|Rush)\s)?(Tournament))\s\#                # open paren of tournament info
          (?P<TOURNO>\d+),\s
          # here's how I plan to use LS
          (?P<TOURNAME>.+?)\s
          )?
          # close paren of tournament info
          (?P<GAME>Hold\'em|Hold\'em|ShortDeck|Omaha|PLO|Omaha\sHi/Lo|PLO\-(5|6))\s
          (?P<LIMIT>No\sLimit|Fixed\sLimit|Limit|Pot\sLimit|\(NL\spostflop\))?,?\s*
          (-\s)?
          (?P<SHOOTOUT>Match.*,\s)?
          (Level(?P<LEVEL>[IVXLC\d]+)\s?)?
          \(?                            # open paren of the stakes
          (?P<CURRENCY>%(LS)s|)?
          (ante\s\d+,\s)?
          ((?P<SB>[,.0-9]+)/(%(LS)s)?(?P<BB>[,.0-9]+)|(?P<BUB>[,.0-9]+))
          (?P<CAP>\s-\s[%(LS)s]?(?P<CAPAMT>[,.0-9]+)\sCap\s-\s)?        # Optional Cap part
          \s?(?P<ISO>%(LEGAL_ISO)s)?
          \)                        # close paren of the stakes
          (?P<BLAH2>\s\[AAMS\sID:\s[A-Z0-9]+\])?         # AAMS ID: in .it HH's
          \s-\s
          (?P<DATETIME>.*$)
        """ % substitutions, re.MULTILINE|re.VERBOSE)

    re_PlayerInfo   = re.compile(u"""
          ^\s?Seat\s(?P<SEAT>[0-9]+):\s
          (?P<PNAME>.*)\s
          \((%(LS)s)?(?P<CASH>[,.0-9]+)\sin\schips
          (,\s(%(LS)s)?(?P<BOUNTY>[,.0-9]+)\sbounty)?
          \)
          (?P<SITOUT>\sis\ssitting\sout)?""" % substitutions, 
          re.MULTILINE|re.VERBOSE)

    re_HandInfo     = re.compile("""
          ^\s?Table\s(ID\s)?\'(?P<TABLE>.+?)\'\s
          ((?P<MAX>\d+)-max\s)?
          (?P<PLAY>\(Play\sMoney\)\s)?
          (Seat\s\#(?P<BUTTON>\d+)\sis\sthe\sbutton)?""", 
          re.MULTILINE|re.VERBOSE)

    re_Identify     = re.compile(u'Poker\sHand\s\#[A-Z]{0,2}?\d+:')
    re_SplitHands   = re.compile('(?:\s?\n){2,}')
    re_TailSplitHands   = re.compile('(\n\n\n+)')
    re_Button       = re.compile('Seat #(?P<BUTTON>\d+) is the button', re.MULTILINE)
    re_Board        = re.compile(r"\[(?P<CARDS>.+)\]")
    re_Board2       = re.compile(r"\[(?P<C1>\S\S)\] \[(\S\S)?(?P<C2>\S\S) (?P<C3>\S\S)\]")
    re_Board3       = re.compile(r"Board\s\[(?P<FLOP>\S\S \S\S \S\S) (?P<TURN>\S\S) (?P<RIVER>\S\S)\]")
    re_DateTime1     = re.compile("""(?P<Y>[0-9]{4})\/(?P<M>[0-9]{2})\/(?P<D>[0-9]{2})[\- ]+(?P<H>[0-9]+):(?P<MIN>[0-9]+):(?P<S>[0-9]+)""", re.MULTILINE)
    re_DateTime2     = re.compile("""(?P<Y>[0-9]{4})\/(?P<M>[0-9]{2})\/(?P<D>[0-9]{2})[\- ]+(?P<H>[0-9]+):(?P<MIN>[0-9]+)""", re.MULTILINE)
    # revised re including timezone (not currently used):
    #re_DateTime     = re.compile("""(?P<Y>[0-9]{4})\/(?P<M>[0-9]{2})\/(?P<D>[0-9]{2})[\- ]+(?P<H>[0-9]+):(?P<MIN>[0-9]+):(?P<S>[0-9]+) \(?(?P<TZ>[A-Z0-9]+)""", re.MULTILINE)

    # These used to be compiled per player, but regression tests say
    # we don't have to, and it makes life faster.
    re_PostSB           = re.compile(r"^%(PLYR)s: posts small blind %(CUR)s(?P<SB>[,.0-9]+)" %  substitutions, re.MULTILINE)
    re_PostBB           = re.compile(r"^%(PLYR)s: posts big blind %(CUR)s(?P<BB>[,.0-9]+)" %  substitutions, re.MULTILINE)
    re_PostBUB          = re.compile(r"^%(PLYR)s: posts button blind %(CUR)s(?P<BUB>[,.0-9]+)" %  substitutions, re.MULTILINE)
    re_Antes            = re.compile(r"^%(PLYR)s: posts the ante %(CUR)s(?P<ANTE>[,.0-9]+)" % substitutions, re.MULTILINE)
    re_BringIn          = re.compile(r"^%(PLYR)s: brings[- ]in( low|) for %(CUR)s(?P<BRINGIN>[,.0-9]+)" % substitutions, re.MULTILINE)
    re_PostMissed       = re.compile(r"^%(PLYR)s: posts missed blind %(CUR)s(?P<SBBB>[,.0-9]+)" %  substitutions, re.MULTILINE)
    re_PostStraddle     = re.compile(r"^%(PLYR)s: straddle %(CUR)s(?P<STRADDLE>[,.0-9]+)" %  substitutions, re.MULTILINE)
    re_Action           = re.compile(r"""
                        ^%(PLYR)s:(?P<ATYPE>\sbets|\schecks|\sraises|\scalls|\sfolds|\sdiscards|\sstands\spat)
                        (\s%(CUR)s(?P<BET>[,.\d]+))?(\sto\s%(CUR)s(?P<BETTO>[,.\d]+))?  # the number discarded goes in <BET>
                        \s*(and\sis\sall.in)?
                        (and\shas\sreached\sthe\s[%(CUR)s\d\.,]+\scap)?
                        (\son|\scards?)?
                        (\s\(disconnect\))?
                        (\s\[(?P<CARDS>.+?)\])?\s*$"""
                         %  substitutions, re.MULTILINE|re.VERBOSE)
    re_ShowdownAction   = re.compile(r"^%s: shows \[(?P<CARDS>.*)\]" % substitutions['PLYR'], re.MULTILINE)
    re_sitsOut          = re.compile("^%s sits out" %  substitutions['PLYR'], re.MULTILINE)
    #re_ShownCards       = re.compile("^Seat (?P<SEAT>[0-9]+): %(PLYR)s %(BRKTS)s(?P<SHOWED>showed|mucked) \[(?P<CARDS>.*)\]( and (lost|(won|collected) \(%(CUR)s(?P<POT>[.\d]+)\)) with (?P<STRING>.+?)(,\sand\s(won\s\(%(CUR)s[.\d]+\)|lost)\swith\s(?P<STRING2>.*))?)?$" % substitutions, re.MULTILINE)
    re_CollectPot       = re.compile(r"Seat (?P<SEAT>[0-9]+): %(PLYR)s %(BRKTS)s(collected|showed \[.*\] and (won|collected)) \(?%(CUR)s(?P<POT>[,.\d]+)\)?(, mucked| with.*|)" %  substitutions, re.MULTILINE)
    #Vinsand88 cashed out the hand for $2.19 | Cash Out Fee $0.02
    re_CollectPot2      = re.compile(r"^%(PLYR)s collected %(CUR)s(?P<POT>[,.\d]+)" %  substitutions, re.MULTILINE)
    re_CollectPot3      = re.compile(r"^%(PLYR)s: Receives Cashout \(%(CUR)s(?P<POT>[,.\d]+)\)" %  substitutions, re.MULTILINE)
    re_CollectPot4      = re.compile(r"^%(PLYR)s: Pays Cashout Risk \(%(CUR)s(?P<POT>[,.\d]+)\)" %  substitutions, re.MULTILINE)
    re_CashedOut        = re.compile(r"(Chooses\sto\sEV\sCashout|Receives\sCashout)")
    re_WinningRankOne   = re.compile(u"^%(PLYR)s wins the tournament and receives %(CUR)s(?P<AMT>[,\.0-9]+) - congratulations!$" %  substitutions, re.MULTILINE)
    re_WinningRankOther = re.compile(u"^%(PLYR)s finished the tournament in (?P<RANK>[0-9]+)(st|nd|rd|th) place and received %(CUR)s(?P<AMT>[,.0-9]+)\.$" %  substitutions, re.MULTILINE)
    re_RankOther        = re.compile(u"^%(PLYR)s finished the tournament in (?P<RANK>[0-9]+)(st|nd|rd|th) place$" %  substitutions, re.MULTILINE)
    re_Cancelled        = re.compile('Hand\scancelled', re.MULTILINE)
    re_Uncalled         = re.compile('Uncalled bet \(%(CUR)s(?P<BET>[,.\d]+)\) returned to' %  substitutions, re.MULTILINE)
    #APTEM-89 wins the $0.27 bounty for eliminating Hero
    #ChazDazzle wins the 22000 bounty for eliminating berkovich609
    #JKuzja, vecenta split the $50 bounty for eliminating ODYSSES
    re_Bounty           = re.compile(u"^%(PLYR)s (?P<SPLIT>split|wins) the %(CUR)s(?P<AMT>[,\.0-9]+) bounty for eliminating (?P<ELIMINATED>.+?)$" %  substitutions, re.MULTILINE)
    #Amsterdam71 wins $19.90 for eliminating MuKoJla and their own bounty increases by $19.89 to $155.32
    #Amsterdam71 wins $4.60 for splitting the elimination of Frimble11 and their own bounty increases by $4.59 to $41.32    
    #Amsterdam71 wins the tournament and receives $230.36 - congratulations!
    re_Progressive      = re.compile(u"""
                        ^%(PLYR)s\swins\s%(CUR)s(?P<AMT>[,\.0-9]+)\s
                        for\s(splitting\sthe\selimination\sof|eliminating)\s(?P<ELIMINATED>.+?)\s
                        and\stheir\sown\sbounty\sincreases\sby\s%(CUR)s(?P<INCREASE>[\.0-9]+)\sto\s%(CUR)s(?P<ENDAMT>[\.0-9]+)$"""
                         %  substitutions, re.MULTILINE|re.VERBOSE)
    re_Rake             = re.compile(u"""
                        Total\spot\s%(CUR)s(?P<POT>[,\.0-9]+)(.+?)?\s\|\sRake\s%(CUR)s(?P<RAKE>[,\.0-9]+)"""
                         %  substitutions, re.MULTILINE|re.VERBOSE)
    
    re_STP             = re.compile(u"""
                        Cash\sDrop\sto\sPot\s:\stotal\s%(CUR)s(?P<AMOUNT>[,\.0-9]+)"""
                         %  substitutions, re.MULTILINE|re.VERBOSE)

    def compilePlayerRegexs(self,  hand):
        players = set([player[1] for player in hand.players])
        if not players <= self.compiledPlayers: # x <= y means 'x is subset of y'
            self.compiledPlayers = players
            player_re = "(?P<PNAME>" + "|".join(map(re.escape, players)) + ")"
            subst = {
                'PLYR': player_re,
                'BRKTS': r'(\(button\) |\(small blind\) |\(big blind\) |\(button\) \(small blind\) |\(button\) \(big blind\) )?',
                'CUR': u"(\$|\xe2\x82\xac|\u20ac||\£|)"
            }
            self.re_HeroCards = re.compile(r"^Dealt to %(PLYR)s(?: \[(?P<OLDCARDS>.+?)\])?( \[(?P<NEWCARDS>.+?)\])" % subst, re.MULTILINE)
            self.re_ShownCards = re.compile("^Seat (?P<SEAT>[0-9]+): %(PLYR)s %(BRKTS)s(?P<SHOWED>showed|mucked) \[(?P<CARDS>.*)\]( and (lost|(won|collected) \(%(CUR)s(?P<POT>[,\.\d]+)\)) with (?P<STRING>.+?)(,\sand\s(won\s\(%(CUR)s[\.\d]+\)|lost)\swith\s(?P<STRING2>.*))?)?$" % subst, re.MULTILINE)   


    def readSupportedGames(self):
        return [["ring", "hold", "nl"],
                ["ring", "hold", "pl"],
                ["ring", "hold", "fl"],
                ["ring", "hold", "pn"],

                ["ring", "stud", "fl"],

                ["ring", "draw", "fl"],
                ["ring", "draw", "pl"],
                ["ring", "draw", "nl"],

                ["tour", "hold", "nl"],
                ["tour", "hold", "pl"],
                ["tour", "hold", "fl"],
                ["tour", "hold", "pn"],

                ["tour", "stud", "fl"],
                
                ["tour", "draw", "fl"],
                ["tour", "draw", "pl"],
                ["tour", "draw", "nl"],
                ]

    def determineGameType(self, handText):
        info = {}
        m = self.re_GameInfo.search(handText)
        if not m:
            tmp = handText[0:200]
            log.error(_("GGPokerToFpdb.determineGameType: '%s'") % tmp)
            raise FpdbParseError

        mg = m.groupdict()
        if 'LIMIT' in mg and mg['LIMIT'] is not None:
            info['limitType'] = self.limits[mg['LIMIT']]
        else:
            info['limitType'] = 'pl'
        if 'GAME' in mg:
            (info['base'], info['category']) = self.games[mg['GAME']]
        if 'SB' in mg and mg['SB'] is not None:
            info['sb'] = self.clearMoneyString(mg['SB'])
        if 'BB' in mg and mg['BB'] is not None:
            info['bb'] = self.clearMoneyString(mg['BB'])
        if 'BUB' in mg and mg['BUB'] is not None:
            info['sb'] = '0'
            info['bb'] = self.clearMoneyString(mg['BUB'])
        if 'CURRENCY' in mg:
            info['currency'] = self.currencies[mg['CURRENCY']]
        if 'CAP' in mg and mg['CAP'] is not None:
            info['buyinType'] = 'cap'
        else:
            info['buyinType'] = 'regular'
        if 'SPLIT' in mg and mg['SPLIT'] == 'Split':
            info['split'] = True
        else:
            info['split'] = False
        if 'TOURNO' in mg and mg['TOURNO'] is None:
            info['type'] = 'ring'
        else:
            info['type'] = 'tour'
            if 'ZOOM' in mg['TOUR']:
                info['fast'] = True
        
        if info.get('currency') in ('T$', None) and info['type']=='ring':
            info['currency'] = 'play'

        if info['limitType'] == 'fl' and info['bb'] is not None:
            if info['type'] == 'ring':
                try:
                    info['sb'] = self.Lim_Blinds[self.clearMoneyString(mg['BB'])][0]
                    info['bb'] = self.Lim_Blinds[self.clearMoneyString(mg['BB'])][1]
                except KeyError:
                    tmp = handText[0:200]
                    log.error(_("GGPokerToFpdb.determineGameType: Lim_Blinds has no lookup for '%s' - '%s'") % (mg['BB'], tmp))
                    raise FpdbParseError
            else:
                info['sb'] = str((Decimal(self.clearMoneyString(mg['SB']))/2).quantize(Decimal("0.01")))
                info['bb'] = str(Decimal(self.clearMoneyString(mg['SB'])).quantize(Decimal("0.01")))    

        return info

    def readHandInfo(self, hand):
        #First check if partial
        if hand.handText.count('*** SUMMARY ***')!=1:
            raise FpdbHandPartial(_("Hand is not cleanly split into pre and post Summary"))
        
        info = {}
        m  = self.re_HandInfo.search(hand.handText,re.DOTALL)
        m2 = self.re_GameInfo.search(hand.handText)
        if m is None or m2 is None:
            tmp = hand.handText[0:200]
            log.error(_("GGPokerToFpdb.readHandInfo: '%s'") % tmp)
            raise FpdbParseError

        info.update(m.groupdict())
        info.update(m2.groupdict())

        #log.debug("readHandInfo: %s" % info)
        for key in info:
            if key == 'DATETIME':
                #2008/11/12 10:00:48 CET [2008/11/12 4:00:48 ET] # (both dates are parsed so ET date overrides the other)
                #2008/08/17 - 01:14:43 (ET)
                #2008/09/07 06:23:14 ET                
                datetimestr = "2000/01/01 00:00:00"  # default used if time not found
                m1 = self.re_DateTime1.finditer(info[key])
                for a in m1:
                    datetimestr = "%s/%s/%s %s:%s:%s" % (a.group('Y'), a.group('M'),a.group('D'),a.group('H'),a.group('MIN'),a.group('S'))
                    #tz = a.group('TZ')  # just assume ET??
                    #print "   tz = ", tz, " datetime =", datetimestr
                hand.startTime = datetime.datetime.strptime(datetimestr, "%Y/%m/%d %H:%M:%S") # also timezone at end, e.g. " ET"
                hand.startTime = HandHistoryConverter.changeTimezone(hand.startTime, "ET", "UTC")
                    
            if key == 'HID':
                hand.handid = info[key]
            if key == 'TOURNO':
                hand.tourNo = info[key]
            if key == 'BUYIN':
                if hand.tourNo!=None:
                    #print "DEBUG: info['BUYIN']: %s" % info['BUYIN']
                    #print "DEBUG: info['BIAMT']: %s" % info['BIAMT']
                    #print "DEBUG: info['BIRAKE']: %s" % info['BIRAKE']
                    #print "DEBUG: info['BOUNTY']: %s" % info['BOUNTY']
                    if info[key].strip() == 'Freeroll':
                        hand.buyin = 0
                        hand.fee = 0
                        hand.buyinCurrency = "FREE"
                    elif info[key].strip() == '':
                        hand.buyin = 0
                        hand.fee = 0
                        hand.buyinCurrency = "NA"
                    else:
                        if info[key].find("$")!=-1:
                            hand.buyinCurrency="USD"
                        elif info[key].find(u"£")!=-1:
                            hand.buyinCurrency="GBP"
                        elif info[key].find(u"€")!=-1:
                            hand.buyinCurrency="EUR"
                        elif info[key].find(u"₹")!=-1:
                            hand.buyinCurrency="INR"
                        elif info[key].find(u"¥")!=-1:
                            hand.buyinCurrency="CNY"
                        elif info[key].find("FPP")!=-1:
                            hand.buyinCurrency="PSFP"
                        elif info[key].find("SC")!=-1:
                            hand.buyinCurrency="PSFP"
                        elif re.match("^[0-9+]*$", info[key].strip()):
                            hand.buyinCurrency="play"
                        else:
                            #FIXME: handle other currencies, play money
                            log.error(_("GGPokerToFpdb.readHandInfo: Failed to detect currency.") + " Hand ID: %s: '%s'" % (hand.handid, info[key]))
                            raise FpdbParseError

                        info['BIAMT'] = info['BIAMT'].strip(u'$€£FPPSC₹')
                        
                        if hand.buyinCurrency!="PSFP":
                            if info['BOUNTY'] != None:
                                # There is a bounty, Which means we need to switch BOUNTY and BIRAKE values
                                tmp = info['BOUNTY']
                                info['BOUNTY'] = info['BIRAKE']
                                info['BIRAKE'] = tmp
                                info['BOUNTY'] = info['BOUNTY'].strip(u'$€£₹') # Strip here where it isn't 'None'
                                hand.koBounty = int(100*Decimal(info['BOUNTY']))
                                hand.isKO = True
                            else:
                                hand.isKO = False

                            info['BIRAKE'] = info['BIRAKE'].strip(u'$€£₹')

                            hand.buyin = int(100*Decimal(info['BIAMT'])) + hand.koBounty
                            hand.fee = int(100*Decimal(info['BIRAKE']))
                        else:
                            hand.buyin = int(100*Decimal(info['BIAMT']))
                            hand.fee = 0
            if key == 'LEVEL':
                hand.level = info[key]       
            if key == 'SHOOTOUT' and info[key] != None:
                hand.isShootout = True
            if key == 'TABLE':
                tablesplit = re.split(" ", info[key])
                if hand.tourNo != None and len(tablesplit)>1:
                    hand.tablename = tablesplit[1]
                else:
                    hand.tablename = info[key]
            if key == 'TOURNAME':
                hand.tourneyName = info[key]
            if key == 'BUTTON':
                hand.buttonpos = info[key]
            if key == 'MAX' and info[key] != None:
                hand.maxseats = int(info[key])
                
        if 'Zoom' in self.in_path or 'Rush' in self.in_path:
            (hand.gametype['fast'], hand.isFast) = (True, True)
                
        if self.re_Cancelled.search(hand.handText):
            raise FpdbHandPartial(_("Hand '%s' was cancelled.") % hand.handid)
    
    def readButton(self, hand):
        m = self.re_Button.search(hand.handText)
        if m:
            hand.buttonpos = int(m.group('BUTTON'))
        else:
            log.info('readButton: ' + _('not found'))

    def readPlayerStacks(self, hand):
        pre, post = hand.handText.split('*** SUMMARY ***')
        m = self.re_PlayerInfo.finditer(pre)
        for a in m:
            hand.addPlayer(
                int(a.group('SEAT')), 
                a.group('PNAME'), 
                self.clearMoneyString(a.group('CASH')), 
                None, 
                a.group('SITOUT'),
                self.clearMoneyString(a.group('BOUNTY'))
            )

    def markStreets(self, hand):

        # There is no marker between deal and draw in Stars single draw games
        #  this upsets the accounting, incorrectly sets handsPlayers.cardxx and 
        #  in consequence the mucked-display is incorrect.
        # Attempt to fix by inserting a DRAW marker into the hand text attribute

        if hand.gametype['category'] in ('27_1draw', 'fivedraw'):
            # isolate the first discard/stand pat line (thanks Carl for the regex)
            discard_split = re.split(r"(?:(.+(?: stands pat|: discards).+))", hand.handText,re.DOTALL)
            if len(hand.handText) == len(discard_split[0]):
                # handText was not split, no DRAW street occurred
                pass
            else:
                # DRAW street found, reassemble, with DRAW marker added
                discard_split[0] += "*** DRAW ***\r\n"
                hand.handText = ""
                for i in discard_split:
                    hand.handText += i

        # PREFLOP = ** Dealing down cards **
        # This re fails if,  say, river is missing; then we don't get the ** that starts the river.
        if hand.gametype['base'] in ("hold"):
            m =  re.search(r"\*\*\* HOLE CARDS \*\*\*(?P<PREFLOP>(.+(?P<FLOPET>\[\S\S\]))?.+(?=\*\*\* (FIRST\s)?FLOP \*\*\*)|.+)"
                       r"(\*\*\* FLOP \*\*\*(?P<FLOP>  ?(\[\S\S\] )?\[(\S\S ?)?\S\S \S\S\].+(?=\*\*\* (FIRST\s)?TURN \*\*\*)|.+))?"
                       r"(\*\*\* TURN \*\*\* \[\S\S \S\S \S\S] (?P<TURN>\[\S\S\].+(?=\*\*\* (FIRST\s)?RIVER \*\*\*)|.+))?"
                       r"(\*\*\* RIVER \*\*\* \[\S\S \S\S \S\S \S\S] (?P<RIVER>\[\S\S\].+))?"
                       r"(\*\*\* FIRST FLOP \*\*\*(?P<FLOP1>  ?(\[\S\S\] )?\[\S\S \S\S \S\S\].+(?=\*\*\* FIRST TURN \*\*\*)|.+))?"
                       r"(\*\*\* FIRST TURN \*\*\* \[\S\S \S\S \S\S] (?P<TURN1>\[\S\S\].+(?=\*\*\* FIRST RIVER \*\*\*)|.+))?"
                       r"(\*\*\* FIRST RIVER \*\*\* \[\S\S \S\S \S\S \S\S] (?P<RIVER1>\[\S\S\].+?(?=\*\*\* SECOND (FLOP|TURN|RIVER) \*\*\*)|.+))?"
                       r"(\*\*\* SECOND FLOP \*\*\*(?P<FLOP2>  ?(\[\S\S\] )?\[\S\S \S\S \S\S\].+(?=\*\*\* SECOND TURN \*\*\*)|.+))?"
                       r"(\*\*\* SECOND TURN \*\*\* \[\S\S \S\S \S\S] (?P<TURN2>\[\S\S\].+(?=\*\*\* SECOND RIVER \*\*\*)|.+))?"
                       r"(\*\*\* SECOND RIVER \*\*\* \[\S\S \S\S \S\S \S\S] (?P<RIVER2>\[\S\S\].+?(?=\*\*\* THIRD (FLOP|TURN|RIVER) \*\*\*)|.+))?"
                       r"(\*\*\* THIRD FLOP \*\*\*(?P<FLOP3>  ?(\[\S\S\] )?\[\S\S \S\S \S\S\].+(?=\*\*\* THIRD TURN \*\*\*)|.+))?"
                       r"(\*\*\* THIRD TURN \*\*\* \[\S\S \S\S \S\S] (?P<TURN3>\[\S\S\].+(?=\*\*\* THIRD RIVER \*\*\*)|.+))?"
                       r"(\*\*\* THIRD RIVER \*\*\* \[\S\S \S\S \S\S \S\S] (?P<RIVER3>\[\S\S\].+))?", hand.handText,re.DOTALL)
        hand.addStreets(m)
        if 'AFO' in hand.tablename:
            m1 = self.re_Board3.search(hand.handText)
            if m1:
                hand.streets.update({
                    'FLOP': '[%s] %s' % (m1.group('FLOP'),hand.streets['FLOP']),
                    'TURN': '[%s]' % m1.group('TURN'), 
                    'RIVER': '[%s]' % m1.group('RIVER')
                })

    def readCommunityCards(self, hand, street): # street has been matched by markStreets, so exists in this hand
        if street!='FLOPET' or hand.streets.get('FLOP')==None:   # a list of streets which get dealt community cards (i.e. all but PREFLOP)
            m = self.re_Board.search(hand.streets[street])
            hand.setCommunityCards(street, m.group('CARDS').split(' '))
        if street in ('FLOP3', 'TURN3', 'RIVER3'):
            hand.runItTimes = 3
        elif street in ('FLOP2', 'TURN2', 'RIVER2'):
            hand.runItTimes = 2
            
    def readSTP(self, hand):
        m = self.re_STP.search(hand.handText)
        if m:
            hand.addSTP(m.group('AMOUNT'))

    def readAntes(self, hand):
        log.debug(_("reading antes"))
        m = self.re_Antes.finditer(hand.handText)
        for player in m:
            #~ logging.debug("hand.addAnte(%s,%s)" %(player.group('PNAME'), player.group('ANTE')))
            hand.addAnte(player.group('PNAME'), self.clearMoneyString(player.group('ANTE')))
    
    def readBringIn(self, hand):
        m = self.re_BringIn.search(hand.handText,re.DOTALL)
        if m:
            #~ logging.debug("readBringIn: %s for %s" %(m.group('PNAME'),  m.group('BRINGIN')))
            hand.addBringIn(m.group('PNAME'),  self.clearMoneyString(m.group('BRINGIN')))
        
    def readBlinds(self, hand):
        liveBlind, straddles = True, {}
        for a in self.re_PostSB.finditer(hand.handText):
            if liveBlind:
                hand.addBlind(a.group('PNAME'), 'small blind', self.clearMoneyString(a.group('SB')))
                liveBlind = False
            else:
                names = [p[1] for p in hand.players]
                if "Big Blind" in names or "Small Blind" in names or "Dealer" in names:
                    hand.addBlind(a.group('PNAME'), 'small blind', self.clearMoneyString(a.group('SB')))
                else:
                    # Post dead blinds as ante
                    hand.addBlind(a.group('PNAME'), 'secondsb', self.clearMoneyString(a.group('SB')))
        for a in self.re_PostMissed.finditer(hand.handText):
            hand.addBlind(a.group('PNAME'), 'secondsb', self.clearMoneyString(a.group('SBBB')))
        for a in self.re_PostStraddle.finditer(hand.handText):
            if straddles.get(a.group('PNAME')) is None:
                straddles[a.group('PNAME')] = self.clearMoneyString(a.group('STRADDLE'))
            elif Decimal(straddles[a.group('PNAME')]) < Decimal(self.clearMoneyString(a.group('STRADDLE'))):
                straddles[a.group('PNAME')] = self.clearMoneyString(a.group('STRADDLE'))
        for p, amount in straddles.iteritems():
            hand.addBlind(p, 'straddle', amount)
        for a in self.re_PostBB.finditer(hand.handText):
            if straddles.get(a.group('PNAME')) is None:
                hand.addBlind(a.group('PNAME'), 'big blind', self.clearMoneyString(a.group('BB')))
        for a in self.re_PostBUB.finditer(hand.handText):
            hand.addBlind(a.group('PNAME'), 'button blind', self.clearMoneyString(a.group('BUB')))

    def readHoleCards(self, hand):
#    streets PREFLOP, PREDRAW, and THIRD are special cases beacause
#    we need to grab hero's cards
        for street in ('PREFLOP', 'DEAL'):
            if street in hand.streets.keys():
                m = self.re_HeroCards.finditer(hand.streets[street])
                for found in m:
#                    if m == None:
#                        hand.involved = False
#                    else:
                    hand.hero = found.group('PNAME')
                    if 'cards' not in found.group('NEWCARDS'):
                        newcards = found.group('NEWCARDS').split(' ')
                        hand.addHoleCards(street, hand.hero, closed=newcards, shown=False, mucked=False, dealt=True)

        for street, text in hand.streets.iteritems():
            if not text or street in ('PREFLOP', 'DEAL'): continue  # already done these
            m = self.re_HeroCards.finditer(hand.streets[street])
            for found in m:
                player = found.group('PNAME')
                if found.group('NEWCARDS') is None:
                    newcards = []
                else:
                    newcards = found.group('NEWCARDS').split(' ')
                if found.group('OLDCARDS') is None:
                    oldcards = []
                else:
                    oldcards = found.group('OLDCARDS').split(' ')

                if street == 'THIRD' and len(newcards) == 3: # hero in stud game
                    hand.hero = player
                    hand.dealt.add(player) # need this for stud??
                    hand.addHoleCards(street, player, closed=newcards[0:2], open=[newcards[2]], shown=False, mucked=False, dealt=False)
                else:
                    hand.addHoleCards(street, player, open=newcards, closed=oldcards, shown=False, mucked=False, dealt=False)


    def readAction(self, hand, street):
        if hand.gametype['split'] and street in hand.communityStreets:
            s = street + '2'
        else:
            s = street
        if not hand.streets[s]:
            return
        m = self.re_Action.finditer(hand.streets[s])
        for action in m:
            acts = action.groupdict()
            #log.error("DEBUG: %s acts: %s" % (street, acts))
            if action.group('ATYPE') == ' folds':
                hand.addFold( street, action.group('PNAME'))
            elif action.group('ATYPE') == ' checks':
                hand.addCheck( street, action.group('PNAME'))
            elif action.group('ATYPE') == ' calls':
                hand.addCall( street, action.group('PNAME'), self.clearMoneyString(action.group('BET')) )
            elif action.group('ATYPE') == ' raises':
                if action.group('BETTO') is not None:
                    hand.addRaiseTo( street, action.group('PNAME'), self.clearMoneyString(action.group('BETTO')) )
                elif action.group('BET') is not None:
                   hand.addCallandRaise( street, action.group('PNAME'), self.clearMoneyString(action.group('BET')) ) 
            elif action.group('ATYPE') == ' bets':
                hand.addBet( street, action.group('PNAME'), self.clearMoneyString(action.group('BET')) )
            elif action.group('ATYPE') == ' discards':
                hand.addDiscard(street, action.group('PNAME'), action.group('BET'), action.group('CARDS'))
            elif action.group('ATYPE') == ' stands pat':
                hand.addStandsPat( street, action.group('PNAME'), action.group('CARDS'))
            else:
                log.debug(_("DEBUG:") + " " + _("Unimplemented %s: '%s' '%s'") % ("readAction", action.group('PNAME'), action.group('ATYPE')))


    def readShowdownActions(self, hand):
# TODO: pick up mucks also??
        for shows in self.re_ShowdownAction.finditer(hand.handText):            
            cards = shows.group('CARDS').split(' ')
            hand.addShownCards(cards, shows.group('PNAME'))

    def readTourneyResults(self, hand):
        """Reads knockout bounties and add them to the koCounts dict"""
        if self.re_Bounty.search(hand.handText) == None:
            koAmounts = {}
            winner = None
            #%(PLYR)s wins %(CUR)s(?P<AMT>[\.0-9]+) for eliminating (?P<ELIMINATED>.+?) and their own bounty increases by %(CUR)s(?P<INCREASE>[\.0-9]+) to %(CUR)s(?P<ENDAMT>[\.0-9]+)
            #re_WinningRankOne   = re.compile(u"^%(PLYR)s wins the tournament and receives %(CUR)s(?P<AMT>[\.0-9]+) - congratulations!$" %  substitutions, re.MULTILINE)
            for a in self.re_Progressive.finditer(hand.handText):
                if a.group('PNAME') not in koAmounts:
                    koAmounts[a.group('PNAME')] = 0
                koAmounts[a.group('PNAME')] += 100*Decimal(a.group('AMT'))
                hand.endBounty[a.group('PNAME')] = 100*Decimal(a.group('ENDAMT'))
                hand.isProgressive = True
                
            m = self.re_WinningRankOne.search(hand.handText)
            if m: winner = m.group('PNAME')
            
            if hand.koBounty > 0:
                for pname, amount in koAmounts.iteritems():
                    if pname == winner:
                        end = (amount + hand.endBounty[pname])
                        hand.koCounts[pname] = (amount + hand.endBounty[pname]) / Decimal(hand.koBounty)
                    else:
                        end = 0
                        hand.koCounts[pname] = amount / Decimal(hand.koBounty)
        else:
            for a in self.re_Bounty.finditer(hand.handText):
                if a.group('SPLIT') == 'split':
                    pnames = a.group('PNAME').split(', ')
                    for pname in pnames:
                        if pname not in hand.koCounts:
                            hand.koCounts[pname] = 0
                        hand.koCounts[pname] += (1 / Decimal(len(pnames)))
                else:
                    if a.group('PNAME') not in hand.koCounts:
                        hand.koCounts[a.group('PNAME')] = 0
                    hand.koCounts[a.group('PNAME')] += 1        

    def readCollectPot(self,hand):
        #Bovada walks are calculated incorrectly in converted PokerStars hands
        acts, bovadaUncalled_v1, bovadaUncalled_v2, blindsantes, adjustment = hand.actions.get('PREFLOP'), False, False, 0, 0
        names = [p[1] for p in hand.players]
        i=0
        pre, post = hand.handText.split('*** SUMMARY ***')
        hand.cashedOut = self.re_CashedOut.search(pre) != None
        if hand.runItTimes==0 and hand.cashedOut == False:
            for m in self.re_CollectPot.finditer(post):
                pot = self.clearMoneyString(m.group('POT'))
                hand.addCollectPot(player=m.group('PNAME'),pot=pot)
                i+=1
        if i==0:
            for m in self.re_CollectPot2.finditer(pre):
                pot = self.clearMoneyString(m.group('POT'))
                hand.addCollectPot(player=m.group('PNAME'),pot=pot)
            if hand.cashedOut:
                for m in self.re_CollectPot3.finditer(pre):
                    pot = self.clearMoneyString(m.group('POT'))
                    hand.addCollectPot(player=m.group('PNAME'),pot=pot)
                for m in self.re_CollectPot4.finditer(pre):
                    pot = '-' + self.clearMoneyString(m.group('POT'))
                    hand.addCollectPot(player=m.group('PNAME'),pot=pot)

    def readShownCards(self,hand):                
        for m in self.re_ShownCards.finditer(hand.handText):
            if m.group('CARDS') is not None:
                cards = m.group('CARDS')
                cards = cards.split(' ') # needs to be a list, not a set--stud needs the order
                string = m.group('STRING')
                if m.group('STRING2'):
                    string += '|' + m.group('STRING2')

                (shown, mucked) = (False, False)
                if m.group('SHOWED') == "showed": shown = True
                elif m.group('SHOWED') == "mucked": mucked = True

                #print "DEBUG: hand.addShownCards(%s, %s, %s, %s)" %(cards, m.group('PNAME'), shown, mucked)
                hand.addShownCards(cards=cards, player=m.group('PNAME'), shown=shown, mucked=mucked, string=string)
            

    @staticmethod
    def getTableTitleRe(type, table_name=None, tournament = None, table_number=None):
        "Returns string to search in windows titles"
        regex = re.escape(str(table_name))
        if type=="tour":
            regex = re.escape(str(tournament)) + ".* (Table|Tisch) " + re.escape(str(table_number))
        log.info("Stars.getTableTitleRe: table_name='%s' tournament='%s' table_number='%s'" % (table_name, tournament, table_number))
        log.info("Stars.getTableTitleRe: returns: '%s'" % (regex))
        return regex

