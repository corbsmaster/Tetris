"""
Die Datei geht davon aus, dass eine .dat 'highscore' im Verzeichnis existiert.
-> BEIM PROGRAMMSTART PRÜFEN/ERSTELLEN (modul os: os.path.isfile('file)')) und leere liste darin speichern

{
    try:
        with open('highscore','rb') as hs:
            scorelist=pickle.load(hs)
    except:
        with open('highscore','wb') as hs: #wenn nicht, erstelle sie
            scorelist=list() #und die darin enthaltene Liste
            pickle.dump(scorelist, hs)
            pos=0 #-> Platzierung 0
}
    
"""
import pickle

def writescore(score,linescleared,name='cencored',pos=-1): #speichert Score in die Datei 'highscore'
    with open('highscore','rb') as hs: #lade Highscoreliste
        scorelist=pickle.load(hs)
    if pos==-1: #wenn keine Platzierung an die Funktion übergeben wurde, ermittle Platzierung
        pos=getpos(score,linescleared,name,scorelist)
    with open('highscore','wb') as hs:
        scorelist.insert(pos,[score,linescleared,name]) #Füge Ergebnis an richtiger Stelle ein
        pickle.dump(scorelist,hs) #und speichere
        
        
def getpos(score,linescleared,name,scorelist=-1): #ermittelt die erreichte Platzierung
    if scorelist==-1:
        with open('highscore','rb') as hs:
            scorelist=pickle.load(hs) #lade Highscoreliste
    i=0
    while i<len(scorelist): #iteriere durch die Liste, um Platzierung zu finden
        if score<scorelist[i][0]:
            i+=1
        elif score==scorelist[i][0]:
            if linescleared<scorelist[i][1]:
                i+=1
            elif linescleared==scorelist[i][1]:
                if name>scorelist[i][2]:
                    i+=1
                else:
                    return i
            else:
                return i
        else:
            return i
    return i