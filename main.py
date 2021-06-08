# Imported Libraries
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FallOutTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.config import Config
from kivy.graphics import Color

Window.clearcolor = (0.03, 0.15, 0.03, 1)

BtnColor = Color(148, 100, 47, 1, mode='hsv')

from sys import exit

# Dictionary definition 
tp = {}
file = open('file.csv', 'r', encoding='latin-1')
i = 1
for x in file:
    items = x.split(';')
    if(items[3] == '-\n'):
        tp[items[0].upper()] = [items[1], i, float(items[2]), '-']
    else:
        tp[items[0].upper()] = [items[1], i, float(items[2]), float(items[3])]
    i += 1

# Load Kivy file, all screens defined there
Builder.load_file('fef0.kv')
        
# Define Main Screen
class MainScreen(Screen):
    pass

# Define methods for screen 'Function 1'. Searches the dictionary for the element data.
class Function1(Screen):
    datos = StringProperty()
    def data(self, elemento):
        elemento = elemento.upper()
        if(elemento in tp):
            elec = ''
            if(str(tp[elemento][3]) == '-'):
                elec = '. Su electronatividad es nula, no genera enlaces fuera de su elemento.'
            else:
                elec = '. Su electronegatividad es ' + str(tp[elemento][3]) + '.'
            self.datos = 'El nombre del elemento es ' + tp[elemento][0] + '. Su número atómico es ' + str(tp[elemento][1]) + '. Su masa atómica es ' + str(tp[elemento][2]) + elec
        else:
            self.datos = 'El elemento ingresado no existe'
    pass

# Define methods for screen 'Function 2'. Searches electronegativity of both inserted elements and calculates the difference.
class Function2(Screen):
    Diferencia = StringProperty()
    def difEn(self, S1, S2):
        S1 = S1.upper()
        S2 = S2.upper()
        if S1 in tp:
            if S2 in tp:
                if tp[S1][3] != '-':
                    if tp[S2][3] != '-':
                        difResultado = abs(tp[S1][3] - tp[S2][3])
                        difResultado = round(difResultado, 2)
                        difResultado = str(difResultado)
                        self.Diferencia = 'La diferencia de electronegatividad es ' + difResultado
                    else:
                        self.Diferencia = 'El segundo elemento ingresado no tiene electronegatividad.'    
                else:
                    self.Diferencia = 'El primer elemento ingresado no tiene electronegatividad.'
            else:
                self.Diferencia = 'El segundo simbolo fue incorrectamente ingresado.'
        else:
            self.Diferencia = 'El primer simbolo fue incorrectamente ingresado.'
        pass
    pass

# Define the methods for screen 'Function 3'. Divides the inserted molecule. Searches the molar mass. Add them up.
class Function3(Screen):
    datos = StringProperty()


    def calcMasa(self, formula):
        sirve = self.compVal(formula)
        
        if(sirve == False):
            self.datos = 'Añadiste símbolos innecesarios o nada.'
            return ''

        elementos = self.formToArr(formula)
        
        if(elementos == False):
            self.datos = 'Los datos fueron ingresados de forma incorrecta.'
            return ''
        
        masaM = self.masa(elementos)

        if(masaM == False):
            self.datos = 'Los datos fueron ingresados de forma incorrecta.'
            return ''

        self.datos = 'La masa molar de la molécula es ' + str(masaM) + 'g/mol.'


    def compVal(self, form):
        #Comprobar que solo sean símbolos válidos en una fórmula.
        abre = 0
        cierra = 0
        compArr = list(form)
        for j in range(len(compArr)):
            if(compArr[j] == '('):
                abre += 1
            if(compArr[j] == ')'):
                cierra += 1

        for j in range(abre):
            compArr.remove('(')
        for j in range(cierra):
            compArr.remove(')')

        compStr = ''
        for j in compArr:
            compStr = compStr + j
        sirve = compStr.isalnum()

        return sirve


    def formToArr(self, form):
        elementos = []
        lista = list(form)

        #Una vez comprobada la funcionalidad del texto introducido se toma de nuevo el original para analizar su contenido.
        x = 0
        while x < len(lista):
            letra = lista[x]

            #Para las letras las añade dependiendo de sin son mayúsculas o minúsculas.
            if(letra.isalpha()):
                if(letra == letra.upper()):
                    elementos.append(letra)
                elif(letra == letra.lower()):
                    if(x > 0):
                        if(lista[x-1].isalpha() and lista[x-1] == lista[x-1].upper()):
                            elementos[len(elementos)-1] = elementos[len(elementos)-1] + letra.upper()
                        else:
                            return False
                    else:
                        return False
                        
                x += 1

            #Para los números comprueba cuantos son y multiplica el último elemento esa cantidad de veces.
            elif(letra.isdecimal()):
                if(x == 0):
                    return False
                    
                nume = str(letra)
                numb = True
                k = 1
                while numb and (x+k) < (len(lista)):
                    if(lista[x+k].isdecimal()):
                        nume = nume + str(lista[x+k])
                        k += 1
                    else:
                        numb = False
                        break
                    
                for j in range(int(nume)-1):
                    elementos.append(elementos[len(elementos)-1])
                x += k

            #Ahora los parentesis.
            elif(letra == '('):
                k = x
                nume = ''
                inForm = ''
                while lista[k] != ')':
                    k += 1
                dif = k-x
                for j in range(dif-1):
                    letter = lista[x+j+1]
                    inForm = inForm + letter

                inList = self.formToArr(inForm)

                numb = True
                p = k+1
                while numb and p < (len(lista)):
                    if(lista[p].isdecimal):
                        nume = nume + lista[p]
                        p += 1
                    else:
                        numb = False
                if(nume == ''):
                    nume = '1'
                for t in range(int(nume)):
                    for h in inList:
                        elementos.append(h)

                x = p+1

            else:
                return False

        return elementos


    def masa(self, arr):
        masaM = 0
        for j in arr:
            if(j in tp):
                masaM += tp[j][2]
            else:
                return False
        return round(masaM, 3)

                
        pass

# Define methods for screen 'Function 5'. Show all of the elements in a scroll page.
class Function5(Screen):
    final = StringProperty()
    def main(self):
        root.manager.current = 'main'
    def  fillIn(self, where, hecho):
        final = ''
        if(hecho == False):
            file = open('file.csv', 'r', encoding='latin-1')
            n = 0
            for x in file:
                items = x.split(';')
                n += 1
                i = str(n) + '. ' + items[0] + ': ' + str(items[1])
                self.final = self.final + i + ' \n'
            #where.add_widget(Label(size_hint_y=None, text=y, size=texture_size))
        hecho = True
    pass

# Add screens to ScreenManager
sm = ScreenManager(transition=FallOutTransition())
sm.add_widget(MainScreen(name='main'))
sm.add_widget(Function1(name='funct1'))
sm.add_widget(Function2(name='funct2'))
sm.add_widget(Function3(name='funct3'))
sm.add_widget(Function5(name='funct5'))
    

# Define App
class PruebaApp(App):
        
    def build(self):
        self.icon = 'luc4.png'
        return sm

# Run
if __name__ == "__main__":
	PruebaApp().run()
