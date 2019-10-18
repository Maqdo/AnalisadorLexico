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

                            while self.verNumeros(char_atual) and i+1 < tam_linha:
                                j += 1
                                aux += char_atual
                                i += 1
                                char_atual = linha_codigo[i]

                            if(char_atual == '.'):
								j = 0
                                #Tratamento de erro
                                while i+1 < tam_linha:
									i += 1
									char_atual = linha_codigo[i]
									if self.verDelimitador(char_atual) or char_atual == ' ':
										i -= 1 #Volta um caractere da linha para que o delimitador seja reconhecido no momento certo
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
				#Palavras reservadas
				elif self.verLetras(char_atual):
					#Caso o primeiro caractere seja uma letra, vou percorrendo o identificador até o final do identificador ou linha
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
						elif self.verDelimitador(char_atual) or char_atual == ' ' or char_atual == '\t' or char_atual == '\r':
							i -= 1 #Volta um caractere da linha para que o delimitador seja reconhecido no momento certo
							break
						elif char_seguinte != None and self.verOperadores(char_atual+prox_char) or self.verOperadores(char_atual):
							i -= 1
							break
						elif char_atual != '\n':
							arquivo_saida.write("Erro Lexico - Identificador com caracter invalido: "+caracter_atual+" - linha: %d\n" %nLinha)
							erro = True
							break
						i += 1 #Continua para o próximo caractere até o final da palavra
					

					if (erro):
						while (i+1 < tam_linha):
							i += 1
							char_atual = linha_codigo[i]
							if self.verDelimitador(char_atual) or char_atual == ' ' or char_atual == '\t' or char_atual == '\r' or char_atual == '/':
								i -= 1 #Volta um caractere da linha para que o delimitador seja reconhecido no momento certo
								break
					else: #Se nao houver erros basta verificar se o elemento é uma palavra reservada
						if (self.verReservada(aux)):
							arquivo_saida.write(self.qualTokenReservada(string_temp)+'_'+string_temp+'->'+str(nLinha)+'\n')
						else:
							arquivo_saida.write(aux+'->'+str(nLinha)+'\n') #Identificador
				#Caractere invalido
				elif char_atual != '\n' and char_atual != ' ' and char_atual != '\t' and char_atual != '\r':
					arquivo_saida.write('Erro Lexico - Caracter Invalido: ' + char_atual + ' - linha: %d\n' %nLinha)
				#Indo para o próximo caractere da linha
				i += 1
			linha_codigo = arquivo_entrada.readline() # Le a proxima linha
			nLinha += 1
		#Fim do programa
		arquivo_entrada.close()
		arquivo_saida.close

# Executando o programa
analisador_lexico = AnalisadorLexico()
analisador_lexico.analisador()
