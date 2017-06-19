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


'----------------------------------------------------------------------------------------'


def dataCerta(data):
    dia = data[0:2]
    mes = data[2:4]
    ano = data[4:8]
    if data == '':
        return ''
    else:
        return dia + '/' + mes + '/' + ano

'----------------------------------------------------------------------------------------'


def horaCerta(horario):
    hora = horario[0:2]
    minuto = horario[2:4]
    if hora == '':
        return ''
    else:
        return hora + 'h' + minuto + 'm'




'----------------------------------------------------------------------------------------'


def printCores(texto, cor) :
  print(cor + texto + RESET)
  

'----------------------------------------------------------------------------------------'




def adicionar(descricao, extras):

  novaAtividade = '' 
  if descricao  == '' :
    return False
  if extras == ('', '', '', '', ''):
    novaAtividade += descricao
  
  
  if dataValida(extras[0]) == True:
    dat = extras[0]
    novaAtividade = dat
  if horaValida(extras[1]) == True:
    hor = extras[1]
    novaAtividade += ' ' + hor
  if prioridadeValida(extras[2]) == True:
    priori = extras[2]
    novaAtividade += ' ' + priori
  if extras != ('', '', '', '', ''):
      novaAtividade += ' ' + descricao
  if contextoValido(extras[3]) == True:
    contex = extras[3]
    novaAtividade += ' ' + contex
  if projetoValido(extras[4]) == True:
    projet = extras[4]
    novaAtividade += ' ' + projet
  
  

  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possivel escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


'----------------------------------------------------------------------------------------'



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


'----------------------------------------------------------------------------------------'

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


'----------------------------------------------------------------------------------------'


def horaValida(horaMin) :
    if horaMin > 'a' and horaMin < 'z' or horaMin > 'A' and horaMin < 'Z':
        return False
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


'----------------------------------------------------------------------------------------'


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

'----------------------------------------------------------------------------------------'


def projetoValido(proj):
    elemento_2 = proj.split('+')
    if len(elemento_2) == 2:
        if elemento_2[0] != '':
            return False
        elemento_1 = proj.split(elemento_2[1])
        return True
    else:
        return False

'----------------------------------------------------------------------------------------'


def contextoValido(cont):
    elemento_2 = cont.split('@')
    if len(elemento_2) == 2:
        if elemento_2[0] != '':
            return False
        elemento_1 = cont.split(elemento_2[1])
        return True
    else:
        return False

'----------------------------------------------------------------------------------------'


def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


'----------------------------------------------------------------------------------------'


'''info = open(TODO_FILE, 'r')
linhas = info.readlines()
info.close()'''

def organizar(linhas):
  itens = []

  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() 
    tokens = l.split() 

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
    if projetoValido(tokens[len(tokens) - 1]) == False:
      if contextoValido(tokens[len(tokens) - 2]) == True:
        contexto = tokens.pop(len(tokens) - 2)

    if contextoValido(tokens[len(tokens) - 1]) == True:
        contexto = tokens.pop(len(tokens) - 1)
        for x in tokens:
            desc += x + ' '
    else:
        for y in tokens:
            desc += ' ' + y

    itens.append((desc, (data, hora, pri, contexto, projeto)))

  return itens

'----------------------------------------------------------------------------------------'


def listar():
  info = open(TODO_FILE, 'r+')
  linhas = info.readlines()
  info.close()
  itens = (organizar(linhas))
  itens1 = [] + itens
  body = ordenarPorPrioridade(ordenarPorDataHora(itens1))
  
  
  for x in body:
        index = itens.index(x)

        datar = dataCerta(itens[index][1][0])
        horar = horaCerta(itens[index][1][1])
        prio = itens[index][1][2]
        descr = itens[index][0]
        azinho = itens[index][1][3]
        projt = itens[index][1][4]
              
        texto = str(index + 1) + ' ' + datar + ' ' + horar + ' ' + prio + ' ' + descr + ' ' + azinho + ' ' + projt

        i = 0
        lacre = ""
        while i < len(texto)-1:
            if (texto[i] == " ") and (texto[i + 1] == " "):
                lacre += texto[i]
                i += 2
            else:
                lacre += texto[i]
                i += 1
        
        if itens[index][1][2] == '(A)':
            printCores(lacre, RED + BOLD)

        elif itens[index][1][2] == '(B)':
            printCores(lacre, BLUE)

        elif itens[index][1][2] == '(C)':
            printCores(lacre, CYAN)

        elif itens[index][1][2] == '(D)':
            printCores(lacre, GREEN)

        else:
            print(lacre)

  
  return









'----------------------------------------------------------------------------------------'


'''itens = organizar(linhas)'''
def ordenarPorDataHora(itens): 
  lista_sem_impor = []
  lista_impor = []
  

  for x in itens:
    if x[1][0] == '':
      lista_sem_impor.append(x)
    else:
      lista_impor.append(x)

  if lista_impor == []:
    itens = lista_sem_impor
    return itens

  else:
    maior = lista_impor[0]
    contador = 1
    x = 0
    while (x < len(lista_impor)):
      j = contador
      while j < len(lista_impor):
          data_x = lista_impor[x][1][0][4:8] + lista_impor[x][1][0][2:4] + lista_impor[x][1][0][0:2]
          data_j = lista_impor[j][1][0][4:8] + lista_impor[j][1][0][2:4] + lista_impor[j][1][0][0:2]
          
          if (data_x) > (data_j):
              lista_impor[x], lista_impor[j] = lista_impor[j], lista_impor[x]
          elif (data_x) == (data_j):
              hora_x = lista_impor[x][1][1][0:4]
              hora_j = lista_impor[j][1][1][0:4]
              if (hora_x) > (hora_j):
                  lista_impor[x], lista_impor[j] = lista_impor[j], lista_impor[x]
          j += 1
      contador += 1
      x += 1


  itens = lista_impor + lista_sem_impor
  
  return itens

'----------------------------------------------------------------------------------------'


def ordenarPorPrioridade(itens):
    itens = sorted(itens, key = lambda x: x[1][2] if x[1][2] != '' else '(Z A)')
    return itens

'----------------------------------------------------------------------------------------'


def fazer(num):
    num = int(num)
    arquivo = open(TODO_FILE, "r+") 
    linhas = arquivo.readlines()
    arquivo.close()
    if num > len(linhas):
        raise KeyError(num)
    else:
        mensagem = linhas[num - 1]        
        del linhas[num - 1]
        arquivo = open(TODO_FILE, "w+")
        arquivo.writelines(linhas)
        arquivo.close()

        arquivo = open('done.txt', "w+")
        arquivo.write(mensagem + "\n")

    return

'----------------------------------------------------------------------------------------'


def remover(nume):
    nume = int(nume)
    arquivo = open(TODO_FILE, "r+")
    linhas = arquivo.readlines()
    arquivo.close()
    if nume > len(linhas):
        raise KeyError(nume)
    else:
        del linhas[nume - 1]
        arquivo = open(TODO_FILE, "w+")
        arquivo.writelines(linhas)
   

  
    return


'----------------------------------------------------------------------------------------'


def priorizar(num, prioridade):
    prioridade = prioridade.upper()
    num = int(num)
    arquivo = open(TODO_FILE, "r+")
    linhas = arquivo.readlines()
    arquivo.close()
    if num > len(linhas):
        raise KeyError(num) 
    else:
        itens = organizar(linhas)

    atividade = itens[num - 1]
    if prioridade == itens[num - 1][1][2][1:2]:
      return
    else:
      remover(num)
      prioridade = '(' + prioridade + ')'
      descricao = atividade[0]
      adicionar(descricao, (atividade[1][0], atividade[1][1], prioridade, atividade[1][3], atividade[1][4]))
       
        

    return  


'----------------------------------------------------------------------------------------'


def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    comandos.pop(0) 
    comandos.pop(0) 
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1])


  elif comandos[1] == LISTAR:
    listar()
    return    
    

  elif comandos[1] == REMOVER:
      remover(comandos[2])

      return    

        

  elif comandos[1] == FAZER:
      fazer(comandos[2])

      return    

    

  elif comandos[1] == PRIORIZAR:
    priorizar(comandos[2], comandos[3])
    
    return     

    
  else :
    print("Comando invalido.")
    
  

'----------------------------------------------------------------------------------------'
processarComandos(sys.argv)

