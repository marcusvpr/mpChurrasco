from django.shortcuts import render
from .models import MpTopic, MpEntry, MpUsuarioChurrasco
from .forms import MpTopicForm, MpEntryForm, MpUsuarioChurrascoForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from validate_docbr import CPF
import urllib.request
import re
import json

import math

from geopy.geocoders import Nominatim

# Create your views here.
def index(request):
    """Página Principal"""
    return render(request, 'mp_churrascos/index.html')

@login_required
def topics(request):
    """Página Topics"""
    topics = MpTopic.objects.filter(owner=request.user).order_by('date_added')
    context = { 'topics': topics }
    return render(request, 'mp_churrascos/topics.html', context)

@login_required
def topic(request, topic_id):
    """Página Topic/Entries"""
    topic = MpTopic.objects.get(id = topic_id)

    # Garante informação Usuário Logado...
    if topic.owner != request.user:
        raise Http404

    entries = topic.mpentry_set.order_by('-date_added')
    context = { 'topic': topic, 'entries': entries }
    return render(request, 'mp_churrascos/topic.html', context)

@login_required
def new_topic(request):
    """Adiciona Novo Assunto"""
    if request.method != 'POST':
        form = MpTopicForm()
    else:
        form = MpTopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit = False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))

    context = { 'form': form }
    return render(request, 'mp_churrascos/new_topic.html', context)
    
@login_required
def new_entry(request, topic_id):
    """Adiciona Nova Entrada"""
    topic = MpTopic.objects.get(id = topic_id)
        
    # Garante informação Usuário Logado...
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = MpEntryForm()
    else:
        form = MpEntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args = [topic_id]))

    context = { 'topic': topic, 'form': form }
    return render(request, 'mp_churrascos/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Altera Entrada"""
    entry = MpEntry.objects.get(id = entry_id)
    topic = entry.topic
    
    # Garante informação Usuário Logado...
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = MpEntryForm(instance = entry)
    else:
        form = MpEntryForm(instance = entry, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args = [topic.id]))

    context = { 'entry': entry, 'topic': topic, 'form': form }
    return render(request, 'mp_churrascos/edit_entry.html', context)

def churrasco(request):
    if request.method == 'POST':
        form = MpUsuarioChurrascoForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            if validar_usuario(usuario):
                # Valida No.Convidados
                if int(usuario.qtdPessoas) < 1 or int(usuario.qtdPessoas) > 100:
                    form.add_error('qtdPessoas', 'Erro No.Convidados deve ser de (001 - 100) convidados')
                else:
                    # Calcula longitude/Latidude a partir do Endereco ...
                    enderecoJson = json.loads(usuario.resultado)
                    endereco = enderecoJson['logradouro']
                    endereco = endereco + ', 100 - ' + enderecoJson['bairro']
                    endereco = endereco + ', ' + enderecoJson['localidade']
                    endereco = endereco + ' - ' + enderecoJson['uf']
                    endereco = endereco + ', ' + enderecoJson['cep']

                    latLong = captura_latLong(endereco)            
                    if latLong == 'error':
                        form.add_error('cpf', 'Erro Rotina Latitude/Longitude')
                    else:
                        usuario.endereco = endereco

                        latLongJson = json.loads(latLong)
                        usuario.latitude = latLongJson['latitude']
                        usuario.longitude = latLongJson['longitude']

                        # Calcular/Verificar distancia a partir da Latitude/Longitude ...
                        distanciaKM = calcula_distancia(usuario)
                        if distanciaKM > 50:
                            form.add_error('cpf', 'Distância excede 50 Km... não podemos atender! ( ' + str(distanciaKM))
                        else:
                            usuario.distancia = str(distanciaKM) # Em KM !

                            usuario.save()
                            
                            return HttpResponseRedirect(reverse('churrascoResult', args = [usuario.id]))
            else:
                form.add_error('cpf', 'CPF ou CEP ou No.Convidados inválidos')
    else:
        form = MpUsuarioChurrascoForm()

    return render(request, 'mp_churrascos/churrasco.html', {'form': form})

def churrascoResult(request, usuario_id):
    """Página Resultado Planejamento Churrasco"""
    usuario = MpUsuarioChurrasco.objects.get(id = usuario_id)
    context = { 'usuario': usuario }
    return render(request, 'mp_churrascos/churrascoResult.html', context)

# ==================================================================

def validar_cpf(cpf):
    if CPF().validate(cpf):
        return True

    return False
        
def validar_cep(usuario):
    cep = usuario.cep
    try:
        cep = cep.replace('-', '')
        if cep_valido(cep):
            # cepx = '01001000'
            #url = 'https://viacep.com.br/ws/%s/json/' % cep
            url = f'https://viacep.com.br/ws/{cep}/json/'
            
            headers = {'User-Agent': 'Autociencia/1.0'}
            requisicao = urllib.request.Request(url, headers=headers, method='GET')
            cliente = urllib.request.urlopen(requisicao)
            conteudo = cliente.read().decode('utf-8')
            cliente.close()
            
            usuario.resultado = conteudo
            usuario.save()
            return True

        print('Cep Inválido! ' + cep)
        return False        
    except:
        print('Houve erro acesso api Viacep')
        return False # not response.json().get('erro')

def cep_valido(cep):
    return True if re.search(r'^(\d{5}-\d{3}|\d{8})$', cep) else False

def validar_qtd(qtdPessoas):
    qtd = int(qtdPessoas)
    if not int(qtd):
        print("Esse não é um número inteiro! " + qtdPessoas)    
        return False
    return True

def validar_usuario(usuario):
    cpf_valido = validar_cpf(usuario.cpf)
    cep_valido = validar_cep(usuario)
    qtd_valido = validar_qtd(usuario.qtdPessoas)

    return cpf_valido and cep_valido and qtd_valido

def captura_latLong(endereco):
    """Captura Latitude/Longitude a partir de um endereço"""
    geolocator = Nominatim(user_agent="geolocalização")
    #location = geolocator.geocode('R. Capote Valente, 39 - Pinheiros, São Paulo - SP, 05409-000')
    location = geolocator.geocode(endereco)

    if location == None:
        return 'error'
    
    latLong = '{"latitude": "' + str(location.latitude) + '", "longitude": "' + str(location.longitude) + '"}'
    return latLong

def calcula_distancia(usuario):
    """Calcula distância"""

    #Local Origem: Niteroi - Centro
	#Latitude / Longitude: -22.89097208098677 / -43.1137931282155
    latitude_origem = -22.89097208098677
    longitude_origem = -43.1137931282155

    latitude_destino = float(usuario.latitude)
    longitude_destino = float(usuario.longitude)

    delta_latitude = latitude_destino - latitude_origem
    delta_longitude = longitude_destino - longitude_origem

    R = 6371.01 # Raio da Terra em quilômetros

    a = math.sin(delta_latitude / 2)**2 + math.cos(latitude_origem) * math.cos(latitude_destino) * math.sin(delta_longitude / 2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distanciaKM = (R * c) / 100 # Vrf.??? / 100

    return distanciaKM
