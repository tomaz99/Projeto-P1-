import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso à agenda. Um compromisso tem no mínimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):

  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    return False
  

  ################ COMPLETAR


  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


# Valida a prioridade.
def prioridadeValida(pri):
    if len(pri) != 3:
        return False
    segunda_parte = pri.split('(')
    if len(segunda_parte[0]) >= 3:
           return False
    elif len(segunda_parte[1]) == 2:
        letra1 = segunda_parte[1].split(')')
        if len(letra1[0]) != 1:
            return False
        letra = letra1[0].upper()
        if letra >= 'A' and letra <= 'Z':
            return True
        else:
            return False


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.

def DezUni(horaMin):
    horaMin = int(horaMin)
    if horaMin == 0:
        DU = 0
        return DU
    MCDU = horaMin/100
    CDU = MCDU % 10
    C = CDU // 1
    if C == 0:
        DU = CDU * 10
        return DU
    ODU = CDU % C 
    DU = ODU * 100
    if type(DU) == float:
        DU1 = DU//1
        DU = DU1 + 1
    return DU 


def horaValida(horaMin) :
    if len(horaMin) != 4:
        return False
    else:
        HoraMinInt = int(horaMin)
        hora = HoraMinInt//100
        DU = DezUni(horaMin)
        if hora <= 23 and hora >= 00 and DU >= 0 and DU <= 59: 
            return True
        else:
            return False

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 

def Dia(data):
    data = int(data)
    if data == 0:
        return False
    dia = data//1000000
    return dia
    
def Mes(data):
    data = int(data)
    if data == 0:
        return False
    DDMM = data//10000
    MM = DDMM % 100
    return MM

def Ano(data):
    data = int(data)
    if data == 0:
        return False
    ano = (data % (data//10000))
    return ano


def dataValida(data):
    if len(data) != 8:
        return False
    elif type(data) != str:
        return False
    for x in data:
        if x < '0' or x > '9':
            return False
        
    dia = Dia(data)
    MM = Mes(data)
    ano = Ano(data)        
    if dia < 1:
        return False

    elif MM == 1 and dia <= 31:
        return True
    elif MM == 3 and dia <= 31:
        return True
    elif MM == 5 and dia <= 31:
        return True
    elif MM == 7 and dia <= 31:
        return True
    elif MM == 8 and dia <= 31:
        return True
    elif MM == 10 and dia <= 31:
        return True
    elif MM == 12 and dia <= 31:
        return True
    
    elif MM == 4 and dia <= 30:
        return True
    elif MM == 6 and dia <= 30:
        return True
    elif MM == 9 and dia <= 30:
        return True
    elif MM == 11 and dia <= 30:
        return True
   
    elif MM == 2 and dia <= 29:
        return True
    else:
        return False

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
    elemento_2 = proj.split('+')
    if len(elemento_2) == 2:
        if elemento_2[0] != '':
            return False
        elemento_1 = proj.split(elemento_2[1])
        return True
    else:
        return False

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
    elemento_2 = cont.split('@')
    if len(elemento_2) == 2:
        if elemento_2[0] != '':
            return False
        elemento_1 = cont.split(elemento_2[1])
        return True
    else:
        return False

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
linhas = ['22061999 2259 (A) trabalhar no projeto @skype +casa']
def organizar(linhas):
  itens = []

  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras

    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 
    if dataValida(tokens[0]) == True:
        data = tokens.pop(0)
        if horaValida(tokens[0]) == True:
            hora = tokens.pop(0)
        if prioridadeValida(tokens[0]) == True:
            pri = tokens.pop(0)
    if dataValida(tokens[0]) == False:
        if horaValida(tokens[0]) == True:
            hora = tokens.pop(0)
        if horaValida(tokens[0]) == False:
            if prioridadeValida(tokens[0]) == True:
                pri = tokens.pop(0)

    if projetoValido(tokens[len(tokens) - 1]) == True:
        projeto = tokens.pop(len(tokens) - 1)
    if contextoValido(tokens[len(tokens) - 1]) == True:
        contexto = tokens.pop(len(tokens) - 1)
        for x in tokens:
            desc += ' ' + x
    else:
        for y in tokens:
            desc += ' ' + y

    itens.append((desc, (data, hora, pri, contexto, projeto)))

  return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():

  ################ COMPLETAR
  return 

def ordenarPorDataHora(itens):

  ################ COMPLETAR

  return itens
   
def ordenarPorPrioridade(itens):

  ################ COMPLETAR

  return itens

def fazer(num):

  ################ COMPLETAR

  return 

def remover():

  ################ COMPLETAR

  return

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):

  ################ COMPLETAR

  return 



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, prioridade, (data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
  elif comandos[1] == LISTAR:
    return    
    ################ COMPLETAR

  elif comandos[1] == REMOVER:
    return    

    ################ COMPLETAR    

  elif comandos[1] == FAZER:
    return    

    ################ COMPLETAR

  elif comandos[1] == PRIORIZAR:
    return    

    ################ COMPLETAR

  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
