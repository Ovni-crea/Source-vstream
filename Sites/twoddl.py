#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Votre nom ou pseudo
from resources.lib.gui.hoster import cHosterGui #systeme de recherche pour l'hote
from resources.lib.gui.gui import cGui #systeme d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler #entree des parametres
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler #sortie des parametres
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.parser import cParser #recherche de code
from resources.lib.comaddon import progress, VSlog #import du dialog progress

#from resources.lib.util import cUtil #outils pouvant etre utiles

#Si vous créez une source et la deposez dans le dossier "sites" elle sera directement visible sous xbmc

SITE_IDENTIFIER = 'twoddl' #identifant (nom de votre fichier) remplacez les espaces et les . par _ AUCUN CARACTERE SPECIAL
SITE_NAME = '2ddl' #nom que xbmc affiche
SITE_DESC = 'films en streaming, streaming hd, streaming 720p, Films/séries, récent' #description courte de votre source

URL_MAIN = 'http://2ddl.ws/' #url de votre source

#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle sera affichee.
#LA RECHERCHE GLOBAL N'UTILE PAS showSearch MAIS DIRECTEMENT LA FONCTION INSCRITE DANS LA VARIABLE URL_SEARCH_*
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
#recherche global films
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
#recherche global serie, manga
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
#recherche global divers
URL_SEARCH_MISC = (URL_MAIN + '?s=', 'showMovies')
#
FUNCTION_SEARCH = 'showMovies'

# menu films existant dans l'acceuil (Home)
MOVIE_GENRES = (True, 'showGenres') #films genres
MOVIE_1080P = (URL_MAIN + 'category/movies/1080p', 'showMovies')
MOVIE_1440P = (URL_MAIN + 'category/movies/1440p', 'showMovies')
MOVIE_2160P = (URL_MAIN + 'category/movies/2160p', 'showMovies')
MOVIE_3D = (URL_MAIN + 'category/movies/3d', 'showMovies')
MOVIE_480P = (URL_MAIN + 'category/movies/480p', 'showMovies')
MOVIE_4K = (URL_MAIN + 'category/movies/4k', 'showMovies')
MOVIE_720P = (URL_MAIN + 'category/movies/720p', 'showMovies')
MOVIE_BDRIP = (URL_MAIN + 'category/movies/bdrip', 'showMovies')
MOVIE_BRRIP = (URL_MAIN + 'category/movies/brrip', 'showMovies')
MOVIE_BLURAY = (URL_MAIN + 'category/movies/bluray', 'showMovies')
MOVIE_CBLURAY = (URL_MAIN + 'category/movies/complete-bluray', 'showMovies')
MOVIE_DVDRIP = (URL_MAIN + 'category/movies/dvdrip', 'showMovies')
MOVIE_HDRIP = (URL_MAIN + 'category/movies/hdrip', 'showMovies')
MOVIE_R6 = (URL_MAIN + 'category/movies/r6', 'showMovies')
MOVIE_REMUX = (URL_MAIN + 'category/movies/remux', 'showMovies')
MOVIE_WEBDL = (URL_MAIN + 'category/movies/web-dl', 'showMovies')
MOVIE_WEBRIP = (URL_MAIN + 'category/movies/webrip', 'showMovies')
MOVIE_WEB = (URL_MAIN + 'category/movies/web-movies', 'showMovies')
MOVIE_YIFY720 = (URL_MAIN + 'category/movies/yify/brrip-720p', 'showMovies')
MOVIE_YIFY1080P = (URL_MAIN + 'category/movies/yify/brrip-1080p', 'showMovies')
MOVIE_HEVC = (URL_MAIN + 'category/hevc-x265', 'showMovies')

SERIE_GENRES = (True, 'showGenres') #séries genres
SERIE_1080I = (URL_MAIN + 'category/tv-shows/1080i', 'showMovies')
SERIE_1080P = (URL_MAIN + 'category/tv-shows/tv-1080p', 'showMovies')
SERIE_2160P = (URL_MAIN + 'category/tv-shows/tv-2160p', 'showMovies')
SERIE_720P = (URL_MAIN + 'category/tv-shows/tv-720p', 'showMovies')
SERIE_480P = (URL_MAIN + 'category/tv-shows/tv-480p', 'showMovies')
SERIE_DVDRIP = (URL_MAIN + 'category/tv-shows/tv-dvdrip', 'showMovies')
SERIE_MOVIE = (URL_MAIN + 'category/tv-shows/tv-movies', 'showMovies')

SPORT_SPORTS = (URL_MAIN + 'category/tv-shows/sport', 'showMovies') #sport


def load(): #fonction chargee automatiquement par l'addon l'index de votre navigation.
    oGui = cGui() #ouvre l'affichage

    oOutputParameterHandler = cOutputParameterHandler() #appelle la fonction pour sortir un parametre
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') # sortie du parametres siteUrl n'oubliez pas la Majuscule
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    #Ajoute lien dossier (identifant, function a attendre, nom, icone, parametre de sortie)
    #Puisque nous ne voulons pas atteindre une url on peut mettre ce qu'on veut dans le parametre siteUrl
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Sport', 'films_news.png', oOutputParameterHandler)
    oGui.setEndOfDirectory() #ferme l'affichage

def showMenuFilms():
	oGui = cGui()
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_480P[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_480P[1], 'films en 480P', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_720P[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_720P[1], 'films en 720P', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_1080P[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_1080P[1], 'films en 1080P', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_1440P[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_1440P[1], 'films en 1440P', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_2160P[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_2160P[1], 'films en 2160P', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'films en 3D', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_1080P[1], 'films en 4K', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP[1], 'films en BDRIP', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_BRRIP[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_BRRIP[1], 'films en BRRIP', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_BLURAY[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_BLURAY[1], 'films en Bluray', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_CBLURAY[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_CBLURAY[1], 'films en Full Bluray', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_DVDRIP[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_DVDRIP[1], 'films en DVDRIP', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDRIP[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_HDRIP[1], 'films en HDRIP', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_R6[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_R6[1], 'films en R6(cinéma)', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_WEBDL[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_WEBDL[1], 'films en WEBDL', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_WEBRIP[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_WEBRIP[1], 'films en WEBRIP', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_HEVC[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_HEVC[1], 'films en HEVC', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_YIFY720[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_YIFY720[1], 'films Yify en 720P', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_YIFY1080P[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_YIFY1080P[1], 'films Yify en 1080P', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_WEB[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_WEB[1], 'Téléfilms', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
	oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'films par genre', 'genres.png', oOutputParameterHandler)
    
	oGui.setEndOfDirectory()

def showMenuSeries():
	oGui =cGui()
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', SERIE_480P[0])
	oGui.addDir(SITE_IDENTIFIER, SERIE_480P[1], 'séries en 480P', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', SERIE_720P[0])
	oGui.addDir(SITE_IDENTIFIER, SERIE_720P[1], 'séries en 720P', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', SERIE_1080P[0])
	oGui.addDir(SITE_IDENTIFIER, SERIE_1080P[1], 'séries en 1080P', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', SERIE_1080I[0])
	oGui.addDir(SITE_IDENTIFIER, SERIE_1080I[1], 'séries en 1080I', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', SERIE_2160P[0])
	oGui.addDir(SITE_IDENTIFIER, SERIE_2160P[1], 'séries en 2160P', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', SERIE_DVDRIP[0])
	oGui.addDir(SITE_IDENTIFIER, SERIE_DVDRIP[1], 'séries en DVDRIP', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', SERIE_MOVIE[0])
	oGui.addDir(SITE_IDENTIFIER, SERIE_MOVIE[1], 'Hors-Séries', 'films_news.png', oOutputParameterHandler)
	
	oOutputParameterHandler = cOutputParameterHandler()
	oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
	oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'séries  par genre', 'genres.png', oOutputParameterHandler)
	oGui.setEndOfDirectory()
		
def showSearch(): #fonction de recherche
    oGui = cGui()

    sSearchText = oGui.showKeyBoard() #appelle le clavier xbmc
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText #modifie l'url de recherche
        showMovies(sUrl) #appelle la fonction qui pourra lire la page de resultats
        oGui.setEndOfDirectory()
        return


def showGenres(): #affiche les genres
    oGui = cGui()

    #juste a entrer les categories et les liens qui vont bien
    liste = []
    liste.append( ['Action', URL_MAIN + 'action/'] )
    liste.append( ['Animation', URL_MAIN + 'animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'arts-martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'biopic/'] )
    liste.append( ['Comédie', URL_MAIN + 'comedie/'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'comedie-dramatique/'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'comedie-musicale/'] )
    liste.append( ['Documentaire', URL_MAIN + 'documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'drame/'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'epouvante-horreur/'] )
    liste.append( ['Erotique', URL_MAIN + 'erotique'] )
    liste.append( ['Espionnage', URL_MAIN + 'espionnage/'] )
    liste.append( ['Famille', URL_MAIN + 'famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'historique/'] )
    liste.append( ['Musical', URL_MAIN + 'musical/'] )
    liste.append( ['Policier', URL_MAIN + 'policier/'] )
    liste.append( ['Péplum', URL_MAIN + 'peplum/'] )
    liste.append( ['Romance', URL_MAIN + 'romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'science-fiction/'] )
    liste.append( ['Spectacle', URL_MAIN + 'spectacle/'] )
    liste.append( ['Thriller', URL_MAIN + 'thriller/'] )
    liste.append( ['Western', URL_MAIN + 'western/'] )
    liste.append( ['Divers', URL_MAIN + 'divers/'] )

    for sTitle, sUrl in liste: #boucle

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl) #sortie de l'url en parametre
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        #ajouter un dossier vers la fonction showMovies avec le titre de chaque categorie.

    oGui.setEndOfDirectory()


def showMovieYears():#creer une liste inversée d'annees
    oGui = cGui()

    for i in reversed (xrange(1913, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieYears():
    oGui = cGui()

    for i in reversed (xrange(1936, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
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

    sPattern = '<h2><a href="([^"]+)"\s*title=".+?">(.+?)</a></h2>'
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
            sThumb = str(aEntry[0])
            #sLang = str(aEntry[3])
            #sQual = str(aEntry[4])
            #sHoster = str(aEntry[5])
            sDesc = ''

            #sTitle = sTitle.replace('En streaming', '')

            #Si vous avez des information dans aEntry Qualiter lang organiser un peux vos titre exemple.
            #Si vous pouvez la langue et la Qualite en MAJ ".upper()" vostfr.upper() = VOSTFR
            sTitle = ('%s') % (sTitle)
            #mettre les information de streaming entre [] et le reste entre () vstream s'occupe de la couleur automatiquement.

        #Utile que si les liens recuperer ne commence pas par (http://www.nomdusite.com/)
            #sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2) #sortie de l'url
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) #sortie du titre
            oOutputParameterHandler.addParameter('sThumb', sThumb) #sortie du poster

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                #addTV pour sortir les series tv (identifiant, function, titre, icon, poster, description, sortie parametre)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
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


def __checkForNextPage(sHtmlContent): #cherche la page suivante
    oParser = cParser()
    sPattern = '<a class="page larger"\s*title=".+?"\s*href="([^"]+)">.+?</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False


def showHosters(): #recherche et affiche les hotes
    oGui = cGui() #ouvre l'affichage
    oInputParameterHandler = cInputParameterHandler() #apelle l'entree de parametre
    sUrl = oInputParameterHandler.getValue('siteUrl') #apelle siteUrl
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle') #appelle le titre
    sThumb = oInputParameterHandler.getValue('sThumb') #appelle le poster

    oRequestHandler = cRequestHandler(sUrl) #requete sur l'url
    sHtmlContent = oRequestHandler.request() #requete sur l'url

    oParser = cParser()
    sPattern = '<a href="([^"]+)"\s*rel="nofollow">.+?</a>'
    #ici nous cherchons toute les sources iframe

    aResult = oParser.parse(sHtmlContent, sPattern)
    VSlog(str(aResult))

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

#Pour les series, il y a generalement une etape en plus pour la selection des episodes ou saisons.
def ShowSerieSaisonEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '?????????????????????'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])

        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = sMovieTitle + str(aEntry[1])
            sUrl2 = str(aEntry[2])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def seriesHosters(): #cherche les episodes de series
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<dd><a href="([^<]+)" class="zoombox.+?" title="(.+?)"><button class="btn">.+?</button></a></dd>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry[0])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(aEntry[1])
                oHoster.setFileName(aEntry[1])
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

#Voila c'est un peux brouillon mais ça devrait aider un peu, n'hesitez pas a poser vos questions et meme a partager vos sources.
