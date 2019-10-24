#biblioteca para entrada e saida de arquivos
import sys
#import os.path
#biblioteca para string.*
import string

class AnalisadorLexico():
    def __init__(self):
        self.arquivo_e = "codigo.txt"
        self.arquivo_s = "saida_lex.txt"

    def mudaEntrada(self, string):
        self.arquivo_e = string

    def getEntrada(self):
        return self.arquivo_e

    def getSaida(self):
        return self.arquivo_s

    #Verifica a porra toda
    def charValido(self, entrada):
        caractere = string.printable
        if entrada in caractere:
            return True
        return False
        
    def verEspace(self, entrada):
        espaco = string.whitespace
        if entrada in espaco:
            return True
        return False

    #Verifica se a entrada eh letra
    def verLetras(self, entrada):
        letras = string.ascii_letters
        if entrada in letras:
            return True
        return False

    #Verifica se a entrada eh numero
    def verNumeros(self, entrada):
        numeros = string.digits
        if entrada in numeros:
            return True
        return False

    #Verifica se a entrada eh operador
    def verOperadores(self, entrada):
        operadores = '. + - * / == != > >= < <= = := :'.split()
        if entrada in operadores:
            return True
        return False

    #Verifica qual token operador
    def tokenOperador(self, entrada):
        operadores = ". + - * / == != > >= < <= = := :".split()
        i = operadores.index(entrada) #posicao
        return "token "+str(i)
        
        #for x in operadores:
        #    if x == entrada:
        #        break
        #    i += 1
        #if i > 9:
        #    return "token"+str(i)
        #else:
        #    return "token"+str(i)

    #Verifica se a entrada eh delimitador
    def verDelimitador(self, entrada):
        paradores = "; , ( ) [ ] { }".split()
        if entrada in paradores:
            return True
        return False

    #Verifica token delimitador
    def tokenDelimitador(self, entrada):
        paradores = "; , ( ) [ ] { }".split()
        posicao = paradores.index(entrada)
        return "token "+str(posicao)

    #Verifica se a entrada eh palavra reservada
    def verReservada(self, entrada):
        palavra = 'program begin end var real integer procedure else read write while if do then'.split()
        if entrada in palavra:
            return True
        return False

    #Verifica Token reservada
    def tokenReservada(self, entrada):
        palavra = "program begin end var real integer procedure else read write while if do then".split()
        i = palavra.index(entrada)
        return "token "+str(i)

    #Execucao do analisador
    def analisador(self):
        #Abre o arquivo de entrada
        arquivo_entrada = open(self.arquivo_e, "r")
        #Abre o arquivo de saida
        arquivo_saida = open(self.arquivo_s, "w")

        listaTokens = []
        
        #Le a primeira linha
        linha_codigo = arquivo_entrada.readline()
        nLinha = 1

        while linha_codigo:
            i=0
            tam_linha = len(linha_codigo)

            #Percorre a linha inteira
            while i < tam_linha:
                char_atual = linha_codigo[i]
                prox_char = None

                if i+1 < tam_linha:
                    prox_char = linha_codigo[i+1]
                #Delimitador
                if self.verDelimitador(char_atual):
                    arquivo_saida.write(self.tokenDelimitador(char_atual)+' '+char_atual+'->'+str(nLinha)+'\n')
                    listaTokens.append(char_atual)
                #Comentarios
                elif char_atual == "/" and prox_char == "/":
                    i = tam_linha
                #Operador
                elif prox_char != None and self.verOperadores(char_atual+prox_char):
                    arquivo_saida.write(self.tokenOperador(char_atual+prox_char)+' '+char_atual+prox_char+'->'+str(nLinha)+'\n')
                    listaTokens.append(char_atual+prox_char)
                    i += 1
                elif self.verOperadores(char_atual):
                    arquivo_saida.write(self.tokenOperador(char_atual)+' '+char_atual+'->'+str(nLinha)+'\n')
                    listaTokens.append(char_atual)
                #Numero
                elif self.verNumeros(char_atual):
                    aux = char_atual
                    i += 1
                    j = 0 #Verificacao de numero apohs a virgula
                    char_atual = linha_codigo[i]
                    
                    #Verifica se o(s) proximo(s) caractere(s) eh(sao) numero(s)
                    while (self.verNumeros(char_atual) and (i+1 < tam_linha)):
                        aux += char_atual
                        i += 1
                        char_atual = linha_codigo[i]
                    
                    if char_atual == ".":
                        if (i+1) < tam_linha:
                            aux += char_atual
                            i += 1
                            char_atual = linha_codigo[i]

                            while self.verNumeros(char_atual) and i+1 < tam_linha:
                                j += 1
                                aux += char_atual
                                i += 1
                                char_atual = linha_codigo[i]
                            
                            if(char_atual == "."):
                                j = 0
                                #Tratamento de erro
                            while i+1 < tam_linha:
                                i += 1
                                char_atual = linha_codigo[i]
                                if self.verDelimitador(char_atual) or self.verEspace(char_atual): #char_atual == ' ':
                                    i -= 1 #Volta um caractere da linha para que o delimitador seja reconhecido no momento certo
                                    break
                        else:
                            arquivo_saida.write('Erro Lexico - Numero mal formado - Linha: %d\n' %nLinha)
                        
                        if (j > 0):
                            listaTokens.append(aux)
                            arquivo_saida.write('token '+aux+'->'+str(nLinha)+'\n')
                        else:
                            arquivo_saida.write('Erro Lexico - Numero mal formado - Linha: %d\n' %nLinha)
                    else: #Tratar quando eh letra, operador ou simbolo invalido
                        listaTokens.append(aux)
                        arquivo_saida.write('token '+aux+'->'+str(nLinha)+'\n')
                        if(not self.verNumeros(char_atual)):
                            i -= 1
				#Palavras reservadas
                elif self.verLetras(char_atual):
                    #Caso o primeiro caractere seja uma letra, vou percorrendo o identificador ate o final do identificador ou linha
                    aux = char_atual
                    i += 1
                    erro = False
                    while i < tam_linha:
                        prox_char = None
                        char_atual = linha_codigo[i]
                        if i+1 < tam_linha:
                            prox_char = linha_codigo[i+1]
                        if self.verLetras(char_atual) or self.verNumeros(char_atual) or char_atual == '_':
                            aux += char_atual
                        elif self.verDelimitador(char_atual) or self.verEspace(char_atual): #char_atual == ' ' or char_atual == '\t' or char_atual == '\r':
                            i -= 1 #Volta um caractere da linha para que o delimitador seja reconhecido no momento certo
                            break
                        elif prox_char != None and self.verOperadores(char_atual+prox_char) or self.verOperadores(char_atual) or char_atual == ':':
                            i -= 1
                            break
                        elif char_atual != '\n':
                            arquivo_saida.write("Erro Lexico - Identificador com caracter invalido: "+char_atual+" - linha: %d\n" %nLinha)
                            erro = True
                            break
                        i += 1 #Continua para o proximo caractere ate o final da palavra
					

                    if (erro):
                        while (i+1 < tam_linha):
                            i += 1
                            char_atual = linha_codigo[i]
                            if self.verDelimitador(char_atual) or self.verEspace(char_atual): #char_atual == ' ' or char_atual == '\t' or char_atual == '\r' or char_atual == '/':
                                i -= 1 #Volta um caractere da linha para que o delimitador seja reconhecido no momento certo
                                break
                    else: #Se nao houver erros basta verificar se o elemento eh uma palavra reservada
                        if (self.verReservada(aux)):
                            listaTokens.append(aux)
                            arquivo_saida.write(self.tokenReservada(aux)+" "+aux+'->'+str(nLinha)+'\n')
                        else:
                            listaTokens.append(aux)
                            arquivo_saida.write('token '+aux+'->'+str(nLinha)+'\n') #Identificador
				#Caractere invalido
                elif not self.verEspace(char_atual): #char_atual != '\n' and char_atual != ' ' and char_atual != '\t' and char_atual != '\r':
                    arquivo_saida.write('Erro Lexico - Caracter Invalido: ' + char_atual + ' - linha: %d\n' %nLinha)
                
                elif self.verEspace(char_atual):
                    arquivo_saida.write('--------------------\n')
                #Indo para o proximo caractere da linha
                i += 1
            
            linha_codigo = arquivo_entrada.readline() # Le a proxima linha
            nLinha += 1
        
        print(listaTokens)
		#Fim do programa
        arquivo_entrada.close()
        arquivo_saida.close

# Executando o programa
analisador_lexico = AnalisadorLexico()
analisador_lexico.analisador()

