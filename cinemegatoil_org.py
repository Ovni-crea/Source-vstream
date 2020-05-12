#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

#07/05/20 mise en place recaptcha
#return False

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import GestionCookie
from resources.lib.recaptcha import ResolveCaptcha
from resources.lib.comaddon import progress, dialog, xbmc, xbmcgui, VSlog

import re

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

SITE_IDENTIFIER = 'cinemegatoil_org'
SITE_NAME = 'CineMegaToil'
SITE_DESC = 'Films - Films HD'

URL_MAIN = 'https://www.cinemegatoil.org/'

MOVIE_NEWS = (URL_MAIN + 'film', 'showMovies')
MOVIE_MOVIE = ('http://', 'load')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?do=search&mode=advanced&subaction=search&titleonly=3&story=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?do=search&mode=advanced&subaction=search&titleonly=3&story=', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)


    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'action'] )
    liste.append( ['Animation', URL_MAIN + 'animation'] )
    liste.append( ['Arts-martiaux', URL_MAIN + 'arts-martiaux'] )
    liste.append( ['Aventure', URL_MAIN + 'aventure'] )
    liste.append( ['Biopic', URL_MAIN + 'biopic'] )
    liste.append( ['Comédie', URL_MAIN + 'comedie'] )
    liste.append( ['Comédie musicale', URL_MAIN + 'comedie-musicale'] )#l'url sur le site n'est pas bonne
    liste.append( ['Documentaire', URL_MAIN + 'documentaire'] )
    liste.append( ['Drame', URL_MAIN + 'drame'] )
    liste.append( ['Epouvante-horreur', URL_MAIN + 'epouvante-horreur'] )
    liste.append( ['Espionnage', URL_MAIN + 'espionnage'] )
    liste.append( ['Exclu', URL_MAIN + 'exclu'] )
    liste.append( ['Famille', URL_MAIN + 'famille'] )
    liste.append( ['Fantastique', URL_MAIN + 'fantastique'] )
    liste.append( ['Guerre', URL_MAIN + 'guerre'] )
    liste.append( ['Historique', URL_MAIN + 'historique'] )
    liste.append( ['Musical', URL_MAIN + 'musical'] )
    liste.append( ['Policier', URL_MAIN + 'policier'] )
    liste.append( ['Romance', URL_MAIN + 'romance'] )
    liste.append( ['Science-fiction', URL_MAIN + 'science-fiction'] )
    liste.append( ['Thriller', URL_MAIN + 'thriller'] )
    liste.append( ['Vieux Film', URL_MAIN + 'vieux-film'] )
    liste.append( ['Western', URL_MAIN + 'western'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        if URL_SEARCH[0] in sSearch:
            sUrl = sSearch
        else:
            sUrl = URL_SEARCH[0] + sSearch
        sUrl = sUrl.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="poster.+?img src="([^"]+)".+?class="quality">([^<]+)<\/div>.+?class="title"><a href="([^"]+)".+?title="([^"]+)".+?class="label">Ann.+?<a href.+?>([^<]+)</a>.+?class="shortStory">([^<]+)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[2]
            sThumb = aEntry[0]
            if sThumb.startswith('//'):
                sThumb = 'http:' + sThumb

            sTitle = aEntry[3]
            sQual = aEntry[1]
            sYear = aEntry[4]
            sDesc = aEntry[5]
            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sYear)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="prev-next">.+?href="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return  aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #Vire les bandes annonces
    sHtmlContent = sHtmlContent.replace('src="https://www.youtube.com/', '')

    #sHtmlContent = oParser.abParse(sHtmlContent, '<div class="tcontainer video-box">', '<div class="tcontainer video-box" id=')

    sPattern = '<iframe src="([^"]+)"'
    sPattern2 = '<a.+?href="(https\:\/\/ouo.+?)"'
    sPattern3 = '<center><b> *<a href="https://www.cinemegatoil.org/xfsearch/(.+?)\/">|<a class="" rel="noreferrer" href="(https\:\/\/.+?keeplinks.org.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    aResult2 = oParser.parse(sHtmlContent, sPattern2)
    aResult3 = oParser.parse(sHtmlContent, sPattern3)
    #VSlog(aResult)
    #VSlog(aResult2)
    VSlog(aResult3)

    if (aResult2[0] == True):
        total = len(aResult2[1])
        progress_ = progress().VScreate(SITE_NAME)
        oGui.addText(SITE_IDENTIFIER, sMovieTitle)
        for aEntry2 in aResult2[1]:
            progress_.VSupdate(progress_, total)
            #oGui.addText(SITE_IDENTIFIER, aEntry2)
            sUrl = aEntry2
            #VSlog(sUrl)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addLink(SITE_IDENTIFIER, 'OUO', sUrl, sThumb, sDesc, oOutputParameterHandler)
            progress_.VSclose(progress_)
                    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                
    if (aResult3[0] == True):
        total = len(aResult3[1])
        progress_ = progress().VScreate(SITE_NAME)
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + sMovieTitle + '[/COLOR]')
        for aEntry3 in aResult3[1]:
            progress_.VSupdate(progress_, total)
            oGui.addText(SITE_IDENTIFIER, '[COLOR cyan]' + aEntry3[0] + '[/COLOR]')
            sUrl = aEntry3[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addLink(SITE_IDENTIFIER, 'KEEPLINKS', sUrl, sThumb, sDesc, oOutputParameterHandler)
            progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def OUO():# fonction pour résoudre que les liens ouo présent
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    #VSlog(sUrl)
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    if sUrl:
        sHosterUrl = DecryptOuo(sUrl)
        #VSlog(sHosterUrl)
        if (sHosterUrl):
            sTitle = sMovieTitle
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
        
        oGui.setEndOfDirectory()
        
def KEEPLINKS():# fonction pour résoudre que les liens ouo présent
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    #VSlog(sUrl)
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    if sUrl:
        sHosterUrl = DecryptKeeplinks(sUrl)
        #VSlog(sHosterUrl)
        if (sHosterUrl):
            sTitle = sMovieTitle
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
        
        oGui.setEndOfDirectory()
            
def DecryptOuo(sUrl):
    urlOuo = sUrl
    if not '/fbc/' in urlOuo:
        urlOuo = urlOuo.replace('io/', 'io/fbc/').replace('press/', 'press/fbc/')

    oRequestHandler = cRequestHandler(urlOuo)
    sHtmlContent = oRequestHandler.request()
    Cookie = oRequestHandler.GetCookies()

    key = re.search('sitekey: "(.+?)"', str(sHtmlContent)).group(1)
    OuoToken = re.search('<input name="_token" type="hidden" value="(.+?)">.+?<input id="v-token" name="v-token" type="hidden" value="(.+?)"', str(sHtmlContent), re.MULTILINE|re.DOTALL)

    gToken = ResolveCaptcha(key, urlOuo)

    url = urlOuo.replace('/fbc/', '/go/')
    params = '_token=' + OuoToken.group(1) + '&g-recaptcha-response=' + gToken + "&v-token=" + OuoToken.group(2)

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    oRequestHandler.addHeaderEntry('Referer', urlOuo)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', str(len(params)))
    oRequestHandler.addHeaderEntry('Cookie', Cookie)
    oRequestHandler.addParametersLine(params)
    sHtmlContent = oRequestHandler.request()

    final = re.search('<form method="POST" action="(.+?)" accept-charset=.+?<input name="_token" type="hidden" value="(.+?)">', str(sHtmlContent))

    url = final.group(1)
    params = '_token=' + final.group(2) + '&x-token=' + ""

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    oRequestHandler.addHeaderEntry('Referer', urlOuo)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', str(len(params)))
    oRequestHandler.addHeaderEntry('Cookie', Cookie)
    oRequestHandler.addParametersLine(params)
    sHtmlContent = oRequestHandler.request()

    return oRequestHandler.getRealUrl()

def DecryptKeeplinks(sUrl):
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    Cookie = oRequestHandler.GetCookies()

    key = re.search('<div class="g-recaptcha" data-sitekey="(.+?)"></div>', str(sHtmlContent)).group(1)
    hiddenAction = re.search('<input type="hidden" name=".+?" id="hiddenaction" value="([^"]+)"/>', str(sHtmlContent)).group(1)

    gToken = ResolveCaptcha(key, sUrl)

    data = "myhiddenpwd=&hiddenaction="+hiddenAction+"+&captchatype=Re&hiddencaptcha=1&hiddenpwd=&g-recaptcha-response="+gToken
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    oRequestHandler.addHeaderEntry('Referer', sUrl)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', len(str(data)))
    oRequestHandler.addHeaderEntry('Cookie', 'flag['+sUrl.split('/')[4]+']=1;')
    oRequestHandler.addParametersLine(data)
    sHtmlContent = oRequestHandler.request()

    sUrl = re.search('class="selecttext live">([^<]+)</a>', str(sHtmlContent)).group(1)
    return sUrl
