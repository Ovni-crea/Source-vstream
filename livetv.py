#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea
from resources.lib.gui.hoster import cHosterGui #systeme de recherche pour l'hote
from resources.lib.gui.gui import cGui #systeme d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler #entree des parametres
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler #sortie des parametres
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.parser import cParser #recherche de code
from resources.lib.comaddon import progress, VSlog #import du dialog progress
from resources.lib.util import cUtil #import du plugin cUtil
import re,sys,xbmcgui,os
import urllib

SITE_IDENTIFIER = 'livetv'
SITE_NAME = 'Livetv.sx'
SITE_DESC = 'Site pour regarder du sport en direct gratuitement'

URL_MAIN = 'http://livetv.sx/'
URL_MAIN2 = 'http://cdn.livetvcdn.net/'
URL_SEARCH = (URL_MAIN + '/frx/fanclubs/?q=', 'showMovies4')
FUNCTION_SEARCH = 'showMovies4'

SPORT_SPORTS = (URL_MAIN + 'frx/allupcoming/', 'showMovies') #Les matchs en directs
NETS_GENRES = (True, 'showGenres') #Les clubs de football
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher l équipe', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Les matchs en direct', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', NETS_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_GENRES[1], 'Les genres musicaux', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch(): 
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies4(sUrl) #showMovies4 car c'est pour afficher le club recherché'
        oGui.setEndOfDirectory()
        return


def showGenres(): #affiche les clubs de foot
    oGui = cGui()

    liste = []
    liste.append( ['PSG', URL_MAIN + 'frx/team/1_4_216_psg/fanclub/'] )
    liste.append( ['Marseille (OM)', URL_MAIN + 'frx/team/1_310_383_marseille/fanclub/'] )
    liste.append( ['Barcelone', URL_MAIN + 'frx/team/1_3_227_barcelona/fanclub/'] )
    liste.append( ['Real-Madrid', URL_MAIN + 'frx/team/1_163_317_real_madrid/fanclub/'] )
    liste.append( ['Marchester Utd', URL_MAIN + 'frx/team/1_350_421_manchester_utd/fanclub/'] )
    liste.append( ['Chelsea', URL_MAIN + 'frx/team/1_351_397_chelsea/fanclub/'] )
    liste.append( ['Bayern Munich', URL_MAIN + 'frx/team/1_5_227_bayern/fanclub/'] )
    liste.append( ['Juventus', URL_MAIN + 'frx/team/1_244_365_juventus/fanclub/'] )
    liste.append( ['Arsenal', URL_MAIN + 'frx/team/1_353_406_arsenal/fanclub/'] )
    liste.append( ['Liverpool', URL_MAIN + 'frx/team/1_352_412_liverpool/fanclub/'] )
    liste.append( ['Manchester City', URL_MAIN + 'frx/team/1_363_446_manchester_city/fanclub/'] )
    liste.append( ['France', URL_MAIN + 'frx/team/1_77_258_france/fanclub/'] )
    liste.append( ['Dortmund', URL_MAIN + 'frx/team/1_136_296_dortmund/fanclub/'] )
    liste.append( ['Monaco', URL_MAIN + 'frx/team/1_319_383_monaco/fanclub/'] )
    liste.append( ['Portugal', URL_MAIN + 'frx/team/1_79_269_portugal/fanclub/'] )
    liste.append( ['Argentine', URL_MAIN + 'frx/team/1_62_253_argentina/fanclub/'] )
    liste.append( ['Belgique', URL_MAIN + 'frx/team/1_83_270_belgium/fanclub//'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMenu', sTitle, 'genres.png', oOutputParameterHandler)
        #showMenu car c'est pour afficher les infos du club seul resultat est fonctionnel pour l'instant''

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):#affiche les catégories qui on des lives'
    oGui = cGui()
    if sSearch: 
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') 

    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request() 

    sPattern = '<a class="main"\s*href="([^"]+)"><b>(.+?)</b></a>\s*</td>\s*<td width=44\s*align="center">\s*<a class="small"\s*href=".+?"><b>\+(.+?)</b></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(str(aResult))

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = str(aEntry[1])
            sUrl2 = str(aEntry[0])
            sThumb = ''
            #sLang = str(aEntry[3])
            #sQual = str(aEntry[4])
            sHoster = str(aEntry[2])
            sDesc = ''

            sTitle = sTitle.decode("iso-8859-1", 'ignore')
            sTitle = sTitle.encode("utf-8", 'ignore')
            sTitle = ('%s (%s)') % (sTitle, sHoster) 
            sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl2', sUrl2) 
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) 
            oOutputParameterHandler.addParameter('sThumb', sThumb) 

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMovies2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_) 

    if not sSearch:
        oGui.setEndOfDirectory() 

def showMovies2(sSearch = ''): #affiche les matchs en direct depuis la section showMovie
    oGui = cGui() 
    if sSearch: 
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl2 = oInputParameterHandler.getValue('siteUrl2') 

    oRequestHandler = cRequestHandler(sUrl2)
    sHtmlContent = oRequestHandler.request() 

    sPattern = '<td>\s*<a class=".+?"\s*href="([^"]+)">([^<>]+)</a>\s*.+?<br>\s*<span class="evdesc">([^<>]+)<br>\s*([^<>]+)</span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(str(aResult)) 

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle2 = str(aEntry[1])
            sUrl3 = str(aEntry[0])
            sThumb = ''
            #sLang = str(aEntry[3])
            sQual = str(aEntry[3])
            sHoster = str(aEntry[2])
            sDesc = ''

            sTitle2 = sTitle2.decode("iso-8859-1", 'ignore')
            sTitle2 = cUtil().unescape(sTitle2)
            sTitle2 = sTitle2.encode("utf-8")

            sHoster = sHoster.decode("iso-8859-1", 'ignore')
            sHoster = cUtil().unescape(sHoster)
            sHoster = sHoster.encode("utf-8")
            
            sQual = sQual.decode("iso-8859-1", 'ignore')
            sQual = cUtil().unescape(sQual)
            sQual = sQual.encode("utf-8", 'ignore')
            
            sTitle2 = ('%s (%s) [COLOR yellow]%s[/COLOR]') % (sTitle2, sHoster, sQual)

            sUrl3 = URL_MAIN + sUrl3

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl3', sUrl3) 
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle2) 
            oOutputParameterHandler.addParameter('sThumb', sThumb) 

            if '/series' in sUrl3:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle2, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMovies3', sTitle2, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

def showMovies3(sSearch = ''): #affiche les videos disponible du live
    oGui = cGui()
    if sSearch: 
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl3 = oInputParameterHandler.getValue('siteUrl3') 

    oRequestHandler = cRequestHandler(sUrl3) 
    sHtmlContent = oRequestHandler.request() 
    #sHtmlContent = sHtmlContent.decode("iso-8859-1", 'ignore')
    #sHtmlContent = cUtil().unescape(sHtmlContent)
    #sHtmlContent = sHtmlContent.encode("utf-8", 'ignore')
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')

    sPattern = '<a title=".+?" *href="//cdn.livetvcdn.net/([^>]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(str(aResult))

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total) 
            if progress_.iscanceled():
                break

            sTitle = sMovieTitle2
            sUrl4 = str(aEntry[0])
            #sUrl4 = sUrl4.decode("iso-8859-1", 'ignore')
            #sUrl4 = cUtil().unescape(sUrl4)
            #sUrl4 = sUrl4.encode("utf-8")
            sThumb = ''
            #sLang = str(aEntry[3])
            #sQual = str(aEntry[3])
            #sHoster = str(aEntry[2])
            sDesc = ''
            
            sTitle = ('%s') % (sMovieTitle2)
            sUrl4 = URL_MAIN2 + sUrl4

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl4', sUrl4) 
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle) 
            oOutputParameterHandler.addParameter('sThumb', sThumb) 

            if '/series' in sUrl4:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_) 

    if not sSearch:
        oGui.setEndOfDirectory() 

def showHosters(sSearch = ''): #affiche les videos disponible du live
    oGui = cGui()
    if sSearch: 
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl4 = oInputParameterHandler.getValue('siteUrl4') 

    oRequestHandler = cRequestHandler(sUrl4) 
    #oRequestHandler.addHeaderEntry('User-agent', UA)
    sHtmlContent = oRequestHandler.request() 
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')
    #sHtmlContent = sHtmlContent.replace('frameborder="0 "', '')
    #sHtmlContent = sHtmlContent.replace('<iframe', '')
    #sHtmlContent = sHtmlContent.replace('allowFullScreen="true"', '')
    #sHtmlContent = sHtmlContent.replace('scrolling=no', '')
    #sHtmlContent = sHtmlContent.replace('height=".+?"', '')
    #sHtmlContent = sHtmlContent.replace('width=".+?"', '')

    sPattern = '.+?src="([^"]+)".+?'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(str(aResult))

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total) 
            if progress_.iscanceled():
                break

            sTitle = sMovieTitle2
            sUrl5 = str(aEntry[0])
            sThumb = ''
            #sLang = str(aEntry[3])
            #sQual = str(aEntry[3])
            #sHoster = str(aEntry[2])
            sDesc = ''
            sUrl5 = sUrl5.decode("iso-8859-1", 'ignore')
            sUrl5 = cUtil().unescape(sUrl5)
            sUrl5 = sUrl5.encode("utf-8")
            sTitle = ('%s') % (sMovieTitle2)
            #sUrl2 = URL_MAIN2 + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl5', sUrl5) 
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle) 
            oOutputParameterHandler.addParameter('sThumb', sThumb) 

            if '/series' in sUrl5:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_) 

    if not sSearch:
        oGui.setEndOfDirectory()

def showMovies4(sSearch = ''):#Afficher le club recherché
    oGui = cGui() 
    if sSearch: 
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') 

    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request() 

    sPattern = '<a href="([^"]+)"><span class="sltitle">([^<>]+)</span></a>\s*<br>\s*<font color=".+?">([^<>]+)</font>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(str(aResult))
    
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total) 
            if progress_.iscanceled():
                break

            sTitle = str(aEntry[1])
            sUrl2 = str(aEntry[0])
            sThumb = ''
            #sLang = str(aEntry[3])
            #sQual = str(aEntry[4])
            sHoster = str(aEntry[2])
            sDesc = ''

            sTitle = sTitle.decode("iso-8859-1", 'ignore')
            sTitle = sTitle.encode("utf-8", 'ignore')
            sTitle = ('%s (%s)') % (sTitle, sHoster) 

            sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2) 
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) 
            oOutputParameterHandler.addParameter('sThumb', sThumb) 

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMenu', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_) 

    if not sSearch:
        oGui.setEndOfDirectory() 

def showMenu(sSearch = ''):#affiche le menu du club
    oGui = cGui() 
    if sSearch: 
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') 

    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request() 

    sPattern = '<a href="([^"]+)" *class="white">(.+?)</a></td>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(str(aResult)) 

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total) 
            if progress_.iscanceled():
                break

            sTitle = str(aEntry[1])
            sUrl2 = str(aEntry[0])
            sThumb = ''
            #sLang = str(aEntry[3])
            #sQual = str(aEntry[4])
            #sHoster = str(aEntry[2])
            sDesc = ''

            sTitle = sTitle.decode("iso-8859-1", 'ignore')
            sTitle = sTitle.encode("utf-8", 'ignore')
            sTitle = ('%s') % (sTitle) 

            sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2) 
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) 
            oOutputParameterHandler.addParameter('sThumb', sThumb) 

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showResult', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_) 

    if not sSearch:
        oGui.setEndOfDirectory() 

def showResult(sSearch = ''):# le menu resultat quand on a choisi le club
    oGui = cGui() 
    if sSearch: 
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') 

    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request() 

    sPattern = '<span class="date">([^<>]+)</span>.+?<span class="graydesc">([^<>]+)</span>.+?<td align="right">([^<>]+).+?<td align="center">\s*<b>([^<>]+)</b>.+?<td>([^<>]+)</td>.+?<font color=".+?">.+?</font>.+?<a class="small" *href="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(str(aResult)) 

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total) 
            if progress_.iscanceled():
                break

            sTitle = str(aEntry[2])  + str(aEntry[4])
            sUrl2 = str(aEntry[5])
            sDate = str(aEntry[0])
            sComp = str(aEntry[1])
            sEquip = str(aEntry[2])
            sScore = str(aEntry[3])
            sEquipe = str(aEntry[4])
            sThumb = ''
            #sLang = str(aEntry[3])
            #sQual = str(aEntry[4])
            #sHoster = str(aEntry[2])
            sDesc = ''

            sTitle = sTitle.decode("iso-8859-1", 'ignore')
            sTitle = cUtil().unescape(sTitle)
            sTitle = sTitle.encode("utf-8", 'ignore')
            
            sDate = sDate.decode("iso-8859-1", 'ignore')
            sDate = cUtil().unescape(sDate)
            sDate = sDate.encode("utf-8", 'ignore')
            
            sScore = sScore.decode("iso-8859-1", 'ignore')
            sScore = cUtil().unescape(sScore)
            sScore = sScore.encode("utf-8", 'ignore')
            
            sComp = sComp.decode("iso-8859-1", 'ignore')
            sComp = cUtil().unescape(sComp)
            sComp = sComp.encode("utf-8", 'ignore')
            sTitle = ('%s  [%s] (%s) [COLOR]%s[/COLOR]]') % (sTitle, sScore, sDate, sComp) 
            sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2) 
            oOutputParameterHandler.addParameter('sMovieTitlebis', sTitle) 
            oOutputParameterHandler.addParameter('sThumb', sThumb) 

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_) 

    if not sSearch:
        oGui.setEndOfDirectory() 

def showDecode(): #les hosters des lives celui que je suis bloqué
    oGui = cGui() 
    oInputParameterHandler = cInputParameterHandler() 
    sUrl = oInputParameterHandler.getValue('siteUrl') 
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2') 
    sThumb = oInputParameterHandler.getValue('sThumb') 

    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request() 

    oParser = cParser()
    sPattern = '<iframe.+?src="(.+?)".+?</iframe>'
    #urllib.unquote(sPattern)

    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(str(aResult))

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)
            #sHosterUrl = sHosterUrl.decode("iso-8859-1", 'ignore')
            #sHosterUrl = cUtil().unescape(sHosterUrl)
            #sHosterUrl = sHosterUrl.encode("utf-8", 'ignore')
            oHoster = cHosterGui().checkHoster(sHosterUrl) 
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle2) 
                oHoster.setFileName(sMovieTitle2) 
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory() 

def showHosters2(): #Les hosters des videos (pas des lives attentions)
    oGui = cGui() 
    oInputParameterHandler = cInputParameterHandler() 
    sUrl = oInputParameterHandler.getValue('siteUrl') 
    sMovieTitlebis = oInputParameterHandler.getValue('sMovieTitlebis') 
    sThumb = oInputParameterHandler.getValue('sThumb') 

    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request() 

    oParser = cParser()
    sPattern = '<iframe.+?src="(http.+?)".+?</iframe>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(str(aResult))

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)
            #sHosterUrl = sHosterUrl.decode("iso-8859-1", 'ignore')
            #sHosterUrl = cUtil().unescape(sHosterUrl)
            #sHosterUrl = sHosterUrl.encode("utf-8", 'ignore')
            oHoster = cHosterGui().checkHoster(sHosterUrl) 
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitlebis) 
                oHoster.setFileName(sMovieTitlebis) 
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory() 

#def showVideo(sSearch = ''):# pas utilisé pour l'instant c'est pour afficher les videos disponibles sur le résumé du match et les melleurs moment ''
    oGui = cGui() #ouvre l'affichage
    if sSearch: #si une url et envoyer directement grace a la fonction showSearch
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') #recupere l'url sortie en parametre

    oRequestHandler = cRequestHandler(sUrl) #envoye une requete a l'url
    sHtmlContent = oRequestHandler.request() #requete aussi

    #sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>', '')
    #la fonction replace est pratique pour supprimer un code du resultat

    sPattern = '<a class="small" *href="([^"]+)">([^<>]+)</a>.+?</tr>'
    #pour faire simple recherche ce bout de code dans le code source de l'url
    #- "([^"]+)" je veux cette partie de code qui se trouve entre guillemets mais pas de guillemets dans la chaine
    #- .+? je ne veux pas cette partie et peux importe ceux qu'elle contient
    #- >(.+?)< je veux cette partie de code qui se trouve entre < et > mais il peut y avoir n'inporte quoi entre les 2.
    #- (https*://[^"]) je veux l'adresse qui commence par https ou http jusqu'au prochain guillemet.
    #
    #Pour tester vos Regex, vous pouvez utiliser le site https://regex101.com/ en mettant dans les modifiers "gmis"

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #le plus simple et de faire un  VSlog(str(aResult))
    #dans le fichier log d'xbmc vous pourrez voir un array de ce que recupere le script
    #et modifier sPattern si besoin
    VSlog(str(aResult)) #Commenter ou supprimer cette ligne une fois fini

    #affiche une information si aucun resulat
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        #dialog barre de progression
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total) #dialog update
            if progress_.iscanceled():
                break

            #L'array affiche vos info dans l'orde de sPattern en commencant a 0, attention dans ce cas la on recupere 6 information
            #Mais selon votre regex il ne peut y en avoir que 2 ou 3.
            sTitle = str(aEntry[1])
            sUrl2 = str(aEntry[0])
            sThumb = ''
            #sLang = str(aEntry[3])
            #sQual = str(aEntry[4])
            #sHoster = str(aEntry[2])
            sDesc = ''

            #sTitle = sTitle.replace('En streaming', '')

            #Si vous avez des information dans aEntry Qualiter lang organiser un peux vos titre exemple.
            #Si vous pouvez la langue et la Qualite en MAJ ".upper()" vostfr.upper() = VOSTFR
            sTitle = sTitle.decode("iso-8859-1", 'ignore')
            sTitle = cUtil().unescape(sTitle)
            sTitle = sTitle.encode("utf-8", 'ignore')
            sTitle = ('%s') % (sTitle) 
            #mettre les information de streaming entre [] et le reste entre () vstream s'occupe de la couleur automatiquement.

        #Utile que si les liens recuperer ne commence pas par (http://www.nomdusite.com/)
            sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2) #sortie de l'url
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) #sortie du titre
            oOutputParameterHandler.addParameter('sThumb', sThumb) #sortie du poster

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                #addTV pour sortir les series tv (identifiant, function, titre, icon, poster, description, sortie parametre)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                #addMovies pour sortir les films (identifiant, function, titre, icon, poster, description, sortie parametre)

            #il existe aussi addMisc(identifiant, function, titre, icon, poster, description, sortie parametre)
            #la difference et pour les metadonner serie, films ou sans

        progress_.VSclose(progress_) #fin du dialog

        sNextPage = __checkForNextPage(sHtmlContent) #cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)
            #Ajoute une entree pour le lien Next | pas de addMisc pas de poster et de description inutile donc

    if not sSearch:
        oGui.setEndOfDirectory() #ferme l'affichage

 
