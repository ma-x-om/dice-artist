#!/usr/bin/env python
# coding: utf-8

# In[1]:
print('Inicializando...\n.\n.\n.')

print('Carregando módulos...')
print('  numpy...')
import numpy as np
print('     Carregado.')
print('  rgb2gray de skimage.color...')
from skimage.color import rgb2gray
print('     Carregado.')
print('  matplotlib.pyplot...')
import matplotlib.pyplot as plt
print('     Carregado.')
print('  interactive de matplotlib.pyplot...')
from matplotlib.pyplot import interactive
print('     Carregado.')
print('  cv2...')
import cv2
print('     Carregado.')
print('  tkinter...')
import tkinter as tk
from tkinter import filedialog
print('     Carregado.\n\n\n\n')


# In[3]:


def mostrarImg(imagem,ImgTitle):
    #print('maximum grayscale value',np.max(imagem))
    #print('minimum grayscale value', np.min(imagem))
    print(f'\n-------------------------------------------\nDimensões: {np.shape(imagem)[0]} linhas e {np.shape(imagem)[1]} colunas')
    print(f'Quantidade de dados: {np.size(imagem)}\n-------------------------------------------\n')
    plt.figure(ImgTitle)
    plt.imshow(imagem,cmap='gray')
    plt.axis('off')


# In[4]:


def mostrarDice(imagem):
    plt.figure('Dice Art ~ ;)')
    plt.imshow(imagem,cmap='gray')
    plt.axis('off')
    ##plt.title()
    plt.tight_layout()
    plt.show()


# In[5]:


def carregarImg(address):
    im=cv2.imread(address)
    im=np.max(im)*rgb2gray(im)
    mostrarImg(im,'Original')
    return im


# In[6]:


def carregarResizeImg(im):
    #perguntar se quer resize manualmente ou por numero de dados
    answer=input('Deseja redimensionar a imagem a partir do numero de dados? (y/n) \n    ')
    while answer !='n' and answer!='y':
        answer=input('Insira uma resposta válida (y/n) \n    ')
    if answer=='n':
        largura, altura = input('Insira novos valores de largura e altura separados por um espaço: \n    ').split()
        largura=int(largura)
        altura=int(altura)
        imnova=cv2.resize(im, dsize=(altura, largura))
        mostrarImg(imnova, 'Redimensionada')
        return imnova
    if answer=='y':
        answer=input('Já tem um valor definido? (y/n) \n    ')
        while answer !='n' and answer!='y':
            answer=input('Insira uma resposta válida (y/n) \n    ')
        if answer=='y':
            numerodedados=int(input('----Numero de dados: '))
            altura, largura= resizeByDice(im,numerodedados)
        if answer=='n':
            conclusao='false'
            while conclusao=='false':
                tabelaDado(im)
                pergunta=input('Mais projeções? (y/n) \n    ')
                while pergunta !='n' and pergunta!='y':
                    pergunta=input('Insira uma resposta válida (y/n) \n    ')
                if pergunta=='n':
                    numerodedados=int(input('----Numero de dados: '))
                    altura, largura= resizeByDice(im,numerodedados)
                    conclusao='true'
        imnova=cv2.resize(im, dsize=(largura, altura))
        mostrarImg(imnova, 'Redimensionada')
        return imnova


# In[7]:


def resizeByDice(imagem, areaN):
    height, width = np.shape(imagem)
    #height=1024
    #width=683
    area1= height*width
    relation=areaN/area1
    heightN=int(height*np.sqrt(relation))
    widthN=int(width*np.sqrt(relation))
    
    return heightN, widthN


# In[8]:


def tabelaDado(imagem):
    mindad, maxdad = input('Insira valor minimo de dados, valor max (separados por espaço): ').split()
    mindad=int(mindad)
    maxdad=int(maxdad)
    intervalo = int(input('Intervalo: '))
    dadosnumber=np.arange(mindad,maxdad+1,intervalo,dtype=int)
    correla=np.zeros((np.size(dadosnumber),3))
    correla[:,0]=dadosnumber
    for i in range(np.size(dadosnumber)):
        correla[i,1],correla[i,2]=resizeByDice(imagem,correla[i,0])
    print('Numero de dados  |  Dimensao (HxW)')
    for i in range(np.size(dadosnumber)):
        print('          ',int(correla[i,0]),'     (',int(correla[i,1]),',',int(correla[i,2]),')')


# In[9]:


def equalizar(im,pxArt):
    nivelmax=int(np.max(im))
    numpix=np.size(im)
    Hr=np.zeros(nivelmax+1)
    linhas, colunas = np.shape(im)
    #Definindo os valores de H(r)
    for linha in range(linhas):
        for coluna in range(colunas):
            Hr[int(im[linha,coluna])] += 1
    #calcular CDF
    CDF=Hr/numpix
    for i in range(1,nivelmax):
        CDF[i]+=CDF[i-1]
    #calcular e arredondar sk
    sk=CDF*6+1
    sk=sk.astype(int)
    #nova imagem equalizada
    imnova=np.zeros((linhas,colunas))
    for linha in range(linhas):
        for coluna in range(colunas):
            imnova[linha,coluna]=sk[int(im[linha,coluna])]
    if pxArt=='y':
        mostrarImg(imnova,'Pixel Art ~ Equalizado')
    return imnova


# In[10]:


def normalizar(im,pxArt):
    nivelmax=np.max(im)
    im=im/nivelmax
    
    imnova=im*5
    imnova=imnova.astype(int)+1
    if pxArt=='y':
        mostrarImg(imnova,'Pixel Art ~ Normalizado')
    return imnova


# In[11]:


def quantidades(imagem):
    unique_elements, counts_elements = np.unique(imagem, return_counts=True)
    print('Number  |   Frequency')
    for i in range(6):
        print(int(unique_elements[i]),'      |   ',counts_elements[i])


# In[12]:


def showDice1(imagem, cor):
    linhas, colunas = np.shape(imagem)
    
    dado=1-np.array([[[0,0,0],[0,1,0],[0,0,0]],[[1,0,0],[0,0,0],[0,0,1]],[[1,0,0],[0,1,0],[0,0,1]],[[1,0,1],[0,0,0],[1,0,1]],[[1,0,1],[0,1,0],[1,0,1]],[[1,0,1],[1,0,1],[1,0,1]]])
    if cor=='black' or cor=='b':
        dado=1-dado
    imdados=np.zeros((linhas*3,colunas*3))
    
    if cor=='white':
        for linha in range(linhas):
            for coluna in range(colunas):
                imdados[linha*3:(linha*3)+3,coluna*3:(coluna*3)+3]=1-dado[7-int(imagem[linha,coluna])-1]
    else:
        for linha in range(linhas):
            for coluna in range(colunas):
                imdados[linha*3:(linha*3)+3,coluna*3:(coluna*3)+3]=dado[int(imagem[linha,coluna])-1]
            
    mostrarDice(imdados)


# In[13]:


def showDice2(imagem, cor):
    linhas, colunas = np.shape(imagem)
    
    dado2=np.array([[[0,0,0,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]],[[1,0,0,0],[0,0,0,0],[0,0,1,0],[0,0,0,0]],[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,0]],[[1,0,1,0],[0,0,0,0],[1,0,1,0],[0,0,0,0]],[[1,0,1,0],[0,1,0,0],[1,0,1,0],[0,0,0,0]],[[1,0,1,0],[1,0,1,0],[1,0,1,0],[0,0,0,0]]])
    imdados=np.zeros((linhas*4,colunas*4))
    
    if cor=='white':
        for linha in range(linhas):
            for coluna in range(colunas):
                imdados[linha*4:linha*4+4,coluna*4:coluna*4+4]=1-dado2[7-int(imagem[linha,coluna])-1]        
    else:
        for linha in range(linhas):
            for coluna in range(colunas):
                imdados[linha*4:linha*4+4,coluna*4:coluna*4+4]=dado2[int(imagem[linha,coluna])-1]
    mostrarDice(imdados)


# In[15]:


def converter2(imagem_atual,cor='black',metodo='normalizar',dice=2,pixelArt='n'):
    if metodo=='eq':
        imagem_atual=equalizar(imagem_atual,pixelArt)
    else:
        imagem_atual=normalizar(imagem_atual,pixelArt)
    if dice==1:
        showDice1(imagem_atual,cor)
    else:
        showDice2(imagem_atual,cor)


# In[16]:


def comecarContinuar():
    root = tk.Tk()
    root.withdraw()
    finalizar=False
    mudarMetodo=True
    mudarDados=True
    novaImg=True
    mudarResize=True
    while finalizar==False:
        interactive(True)
        while novaImg==True:
            #end=input('Insira o endereço da imagem: ')
            end = filedialog.askopenfilename()
            imagem_atual=carregarImg(end)
            escolha=input('Gostaria de redimensiona-la? (y/n)\n    ')
            while escolha !='y' and escolha !='n':
                escolha=input('Insira uma resposta válida (y/n)\n    ')
            novaImg=False
        while mudarResize==True:
            if escolha=='y':
                imagem_atual=carregarResizeImg(imagem_atual)
            mudarResize=False
        while mudarDados==True:
            cor=input('Insira a cor dos dados (black(padrao)/white):\n    ')
            mudarDados=False
        while mudarMetodo==True:
            method=input('Insira o metodo (normalizar(padrao)/eq(equalizado)):\n    ')
            mudarMetodo=False

        pxArt=input('Mostrar Pixel Art? (y/n)')
        converter2(imagem_atual,cor,method,pixelArt=pxArt)
        
        print('O que deseja fazer agora?\n 1. Abrir outra imagem\n 2. Redimensionar a imagem original\n 3. Mudar cor dos dados\n 4. Mudar método\n 5. Sair')
        decisao=int(input('Sua escolha: '))
        if decisao==4:
            mudarMetodo=True
        elif decisao==3:
            mudarDados=True
        elif decisao==2:
            mudarResize=True
            escolha='y'
            imagem_atual=carregarImg(end)
        elif decisao==1:
            interactive(False)
            mudarMetodo=True
            mudarDados=True
            novaImg=True
            mudarResize=True
        else:
            interactive(False)
            finalizar=True

# In[27]:

comecarContinuar()
print('Fim do programa')

