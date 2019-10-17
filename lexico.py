#biblioteca para entrada e saida de arquivos
import sys
import os.path
#biblioteca para string.*
import string

class Analisador_Lexico():
    #arquivo_entrada = "codigo.txt"
    #arquivo_saida = "saida_lex.txt"

    #Verifica a porra toda
    def charValido(self, entrada):
        caractere = string.printable
        if entrada in caractere:
            return True
        return False

    #Verifica se a entrada é letra
    def verLetras(self, entrada):
        letras = string.ascii_letters
        if entrada in letras:
            return True
        return False

    #Verifica se a entrada é número
    def verNumeros(self, entrada):
        numeros = string.digits
        if entrada in numeros:
            return True
        return False

    #Verifica se a entrada é operador
    def verOperadores(self, entrada):
        operadores = '. + - * / == != > >= < <= = :='.split()
        if entrada in operadores:
            return True
        return False

    #Verifica se a entrada é delimitador
    def verDelimitador(self, entrada):
        paradores = '; , ( ) [ ] { }'.split()
        if entrada in operadores:
            return True
        return False

    #Verifica se a entrada é palavra reservada
    def verReservada(self, entrada):
        palavra = 'program begin end var real integer procedure else read write while if do then'.split()
        if entrada in palavra:
            return True
        return False

    #Execução do analisador
    def analisador(self):
        #Abre o arquivo de entrada
        arquivo_entrada = open("codigo.txt", "r")
        #Abre o arquivo de saida
        arquivo_saida = open("saida_lex.txt", "w")

        #Verifica se o arquivo de entrada existe na mesma pasta
        #if not os.path.exists(arquivo_entrada):
        #    arquivo_saida.write("Arquivo de entrada inexistente")
        #    return
        
        #Lê a primeira linha
        linha_codigo = arquivo_entrada.readline()
        nLinha = 1

        while linha_codigo:
            i=0
            tam_linha = len(linha_codigo)

            #Percorre a linha inteira
            while i < linha_codigo[i]:
                char_atual = linha_codigo[i]
                prox_char = None

                if i < tam_linha:
                    prox_char = linha_codigo[i+1]
                #Delimitador
                if self.verDelimitador(char_atual):
                    arquivo_saida.write(self.char_atual+"\n")
                #Comentarios
                elif char_atual == "#":
                    i = tam_linha
                #Operador
                elif prox_char != None and self.verOperadores(char_atual+prox_char):
                    arquivo_saida.write(self.char_atual+prox_char+"\n")
                    i += 1
                elif self.verOperadores(char_atual):
                    arquivo_saida.write(self.char_atual+"\n")
                #Numero
                elif self.verNumeros(char_atual):
                    aux = char_atual
                    i += 1
                    j = 0 #Verificação de número após a vírgula
                    char_atual = linha_codigo[i]
                    
                    #Verifica se o(s) próximo(s) caractere(s) é(são) número(s)
                    while (self.verNumeros(char_atual) and (i+1 < tam_linha)):
                        aux += char_atual
                        i += 1
                        char_atual = linha_codigo[i]
                    
                    if char_atual == ".":
                        if (i+1) < tam_linha:
                            aux += char_atual
                            i += 1
                            char_atual = linha_codigo[i]

                            while self.verNumeros(char) and i+1 < tam_linha:
                                j += 1
                                aux += char_atual
                                i += 1
                                char_atual = linha_codigo[i]

                            if(caracter_atual == '.'):
                                j = 0
                                #Tratamento de erro
                                while (i+1 < tam_linha):
                                i += 1
                                char_atual = linha_codigo[i]
                                if self.verDelimitador(char_atual) or char_atual == ' ':
                                    i -= 1 #Volta um elemento da linha para que o delimitador seja reconhecido no momento certo
                                    break
                        else:
                        arquivo_saida.write('Erro Lexico - Numero mal formado - Linha: %d\n' %nLinha)

                        if (j > 0):
                        arquivo_saida.write(aux+'->'+str(nLinha)+'\n')
                        else: 
                        arquivo_saida.write('Erro Lexico - Numero mal formado - Linha: %d\n' %nLinha)
                    else:
                        arquivo_saida.write(aux+'->'+str(nLinha)+'\n')
                        if(not self.verNumeros(char_atual)):
                            i -= 1
                    