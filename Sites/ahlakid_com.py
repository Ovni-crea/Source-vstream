#-*- coding: utf-8 -*-
#vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.gui import cGui
# from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser
from resources.sites.freebox import getHtml, showWeb, play__
from resources.lib.comaddon import progress#, VSlog
from resources.lib.comaddon import VSlog

SITE_IDENTIFIER = 'ahlakid_com'
SITE_NAME = 'Ahlakid.com'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'https://ahlakid.com/'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showPays', 'Choix du pays', 'lang.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showPays():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sHtmlContent = getHtml(sUrl)
    sHtmlContent = sHtmlContent.replace('ADULT-IPTV', '').replace('https://ahlakid.com/category/adult-iptv/', '')
    oParser = cParser()
    sPattern = '<li class=".+?"><a href="([^"]+)" *>([^<>]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(aResult)
    
    

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showDailyList', sTitle, 'tv.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showDailyList():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    sHtmlContent = getHtml(sUrl)
    sPattern = '<h2 class="entry-title"><a href="([^"]+)" title="([^<>]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showAllPlaylist', sTitle, 'tv.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showDailyList', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = ' class="last".+?href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return  aResult[1][0]

    return False

def showAllPlaylist():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    sHtmlContent = getHtml(sUrl)
    sPattern = '<a href="([^"]+)">Download ([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]
            sUrl2 = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
