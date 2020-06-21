
class Gramatica():
    def __init__(self, gramatica):
        """Constructor de la clase.

        Parameters
        ----------
        gramatica : string
            Representación de las producciones de una gramática determinada.

            Ejemplo:
            "A:b A\nA:a\nA:A B c\nA:lambda\nB:b"
        """
        self.resultado = True

        def borrar_espacios(string):
            cadena = string.split(" ")
            while '' in cadena:
                cadena.remove('')
            nueva_cadena = ""
            primera = True
            for letra in cadena:
                if primera == True:
                    primera = False
                    nueva_cadena = letra
                else:
                    nueva_cadena = nueva_cadena + " " + letra
            return nueva_cadena



        self.reglas = dict()
        self.reglas = {}
        division = gramatica.split("\n")
        antecedente = ""
        consecuentes = []
        self.antecedentes = []
        n_antecedente= ""
        primera = True
        for x in division:
            expresion = x.split(":")
            if len(expresion) == 1:
                expresion.insert(0, antecedente)
            expresion[1] = borrar_espacios(expresion[1])
            n_antecedente = expresion[0]
            if n_antecedente == expresion[1][0]:
                self.resultado = False
            if n_antecedente[0].isupper():
                if n_antecedente != antecedente:
                    self.antecedentes.append(n_antecedente)
                    if primera is True:
                        primera = False
                        antecedente = n_antecedente
                    else:
                        self.reglas[antecedente] = consecuentes
                        antecedente = n_antecedente
                        consecuentes = []
                consecuentes.append(expresion[1])
            else:
                print("No es una gramatica valida")
        self.reglas[antecedente] = consecuentes



        pass

    def isLL1(self):
        """Verifica si una gramática permite realizar derivaciones utilizando
           la técnica LL1.

        Returns
        -------
        resultado : bool
            Indica si la gramática es o no LL1.
        """

        def buscar_first(noterminal):
            lista = []
            for x in self.reglas[noterminal]:
                l = x.split(" ")
                if not l[0].isupper():
                    if len(l) > 1:
                        lista.extend(l[0])
                    else:
                        lista.extend(l)
                else:
                    buscar_first(l[0])
            return lista

        if self.resultado:
            #FIRSTS

            lam = False
            self.firsts = []
            consecuentes = []
            for ant in self.antecedentes:
                consecuentes = self.reglas[ant]
                for cons in consecuentes:
                    firsts_linea = []
                    lista = cons.split(" ")
                    for c in lista:
                        lam = False
                        if not c[0].isupper():
                            if c == 'lambda':
                                firsts_linea.append(c)
                            else:
                                firsts_linea.extend(c)
                            break
                        else:
                            l = buscar_first(c)
                            for i in firsts_linea:
                                if i in l:
                                    l.remove(i)
                            if 'lambda' in l:
                                l.remove('lambda')
                                lam = True
                                firsts_linea.extend(l)
                            else:
                                firsts_linea.extend(l)
                                break
                    if lam is True:
                        firsts_linea.append('lambda')
                    self.firsts.append(firsts_linea)
            self.dicfirsts = dict()
            self.dicfirsts = {}
            cont = 0
            for ant in self.antecedentes:
                hasta = cont + len(self.reglas[ant])
                reg = self.firsts[cont:hasta]
                self.dicfirsts[ant] = reg
                cont = hasta

            #FOLLOWS

            lam = False
            self.follows = []
            primera = True
            consecuentes = []
            for a in self.antecedentes:
                consecuentes.extend(self.reglas[a])
            for ant in self.antecedentes:
                follows_ant = []
                if primera == True:
                    primera = False
                    follows_ant.append('$')
                for cons in consecuentes:
                    lista = cons.split(" ")
                    if ant in lista:
                        if ant == lista[-1] and '$' not in follows_ant:
                            follows_ant.append('$')
                        elif ant != lista[-1]:
                            idx = lista.index(ant) + 1
                            while idx < len(lista):
                                lam = False
                                if not lista[idx].isupper():
                                    follows_ant.append(lista[idx])
                                else:
                                    l = buscar_first(lista[idx])
                                    for i in follows_ant:
                                        if i in l:
                                            l.remove(i)
                                    if 'lambda' in l:
                                        l.remove('lambda')
                                        lam = True
                                        follows_ant.extend(l)
                                    else:
                                        follows_ant.extend(l)
                                        break
                                if lam is True and '$' not in follows_ant:
                                    follows_ant.append('$')
                                idx = idx + 1
                self.follows.append(follows_ant)

            # SELECTS
            lam = False
            self.selects = []

            for first in self.firsts:
                select = []
                for element in first:
                    select.append(element)
                self.selects.append(select)

            self.dicfollows = dict(zip(self.antecedentes, self.follows))
            i = -1
            for ant in self.reglas:
                consencuentes = self.reglas.get(ant)
                for cons in consencuentes:
                    i = i + 1
                    select = self.selects[i]
                    if 'lambda' in select or ['lambda'] in select:
                        if 'lambda' in select:
                            select.remove('lambda')
                        else:
                            select.remove(['lambda'])
                        for foant in self.dicfollows:
                            if ant == foant:
                                follow = self.dicfollows.get(foant)
                                for element in follow:
                                    select.append(element)

            self.dicselects = dict()
            self.dicselects = {}
            cont = 0
            for ant in self.antecedentes:
                hasta = cont + len(self.reglas[ant])
                reg = self.selects[cont:hasta]
                self.dicselects[ant] = reg
                cont = hasta
            #print('Selects: ', self.dicselects)

            for ant in self.antecedentes:
                list_sel = self.dicselects[ant]
                for sel in list_sel:
                    for x in sel:
                        cont = 0
                        for l in list_sel:
                            if x != '$':
                                cont = cont + l.count(x)
                        if cont >= 2:
                            self.resultado = False
                            break
        return self.resultado

        pass

    def parse(self, cadena):
        """Retorna la derivación para una cadena dada utilizando las
           producciones de la gramática y los conjuntos de Fi, Fo y Se
           obtenidos previamente.

        Parameters
        ----------
        cadena : string
            Cadena de entrada.

            Ejemplo:
            babc

        Returns
        -------
        devivacion : string
            Representación de las reglas a aplicar para derivar la cadena
            utilizando la gramática.
        """
        if self.resultado:

            primeraregla = self.reglas[self.antecedentes[0]]
            primeraregla = primeraregla[0]
            self.derivacion = self.antecedentes[0] + "=>" + primeraregla
            indice_cadena = 0
            band = False
            adelantamiento = 0
            while cadena[indice_cadena] != '$':
                band = False
                consecuente = ""
                lam = False
                lam2 = False
                if cadena[indice_cadena] != ' ':
                    if not primeraregla[indice_cadena+adelantamiento].isupper():
                        if primeraregla[indice_cadena+adelantamiento] != cadena[indice_cadena]:
                            if primeraregla[indice_cadena] != 'lambda':
                                break
                            else:
                                adelantamiento = adelantamiento + 1
                        else:
                            indice_cadena = indice_cadena + 1
                            band = True
                    else:
                        idx = 1
                        idx = idx + indice_cadena+adelantamiento
                        while idx < len(primeraregla) and primeraregla[idx] != ' ':
                            idx = idx + 1
                        ant = primeraregla[(indice_cadena+adelantamiento):idx]
                        axioma = primeraregla.split(" ")
                        for cons in self.dicselects[ant]:
                            if cadena[indice_cadena] in cons:
                                band = True
                                indice = self.dicselects[ant].index(cons)
                                consecuente = self.reglas[ant][indice]
                                break
                        if band == True:
                            if ('lambda' in self.dicfirsts[ant] or ['lambda'] in self.dicfirsts[ant]) and (cadena[indice_cadena] in self.dicfollows[ant]):
                                consecuente = ''
                                lam = True
                            nuevaregla = ""
                            for i in axioma:
                                if i == ant:
                                    if lam != True:
                                        nuevaregla = nuevaregla + consecuente + " "
                                    else:
                                        lam = True
                                else:
                                    nuevaregla = nuevaregla + i + " "
                            nuevaregla = nuevaregla[0:len(nuevaregla)-1]
                            self.derivacion = self.derivacion + "=>" + nuevaregla
                            primeraregla = nuevaregla
                            indice_cadena = 0
                            adelantamiento = 0
                        else:
                            break
                else:
                    indice_cadena = indice_cadena + 1
                    band = True
            if band == False:
                return 'La cadena no pertenece al lenguaje que define la gramática.'
            else:
                axioma = primeraregla.split(" ")
                for letra in axioma:

                    if letra.isupper():
                        if 'lambda' in self.dicfirsts[letra] or ['lambda'] in self.dicfirsts[letra]:
                            consecuente = ''
                            lam = True
                            nuevaregla = ""
                            for i in axioma:
                                if i == letra:
                                        nuevaregla = nuevaregla + consecuente
                                else:
                                        nuevaregla = nuevaregla + i + " "
                            nuevaregla = nuevaregla[0:len(nuevaregla)-1]
                            self.derivacion = self.derivacion + "=>" + nuevaregla
                            primeraregla = nuevaregla
                        else:
                            return 'La cadena no pertenece al lenguaje que define la gramática.'
            return self.derivacion
        else:
            return None

        pass
