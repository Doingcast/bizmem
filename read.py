#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import binascii
import evernote.edam.userstore.constants as UserStoreConstants
from evernote.edam.notestore.ttypes import NoteFilter
import evernote.edam.type.ttypes as Types

from evernote.api.client import EvernoteClient

# Sandbox: https://sandbox.evernote.com/api/DeveloperToken.action
# Production: https://www.evernote.com/api/DeveloperToken.action
auth_token = "S=s1:U=8f65c:E=14fa7113473:C=1484f600570:P=1cd:A=en-devtoken:V=2:H=484744fd0ffa906797416ae02ce5cd9c"

client = EvernoteClient(token=auth_token, sandbox=True)

note_store = client.get_note_store()

# GET CONTENT
noteFilter = NoteFilter()
noteFilter.order = 1 #http://dev.evernote.com/documentation/reference/Types.html#Enum_NoteSortOrder
noteFilter.ascending = False
noteList = note_store.findNotes(auth_token, noteFilter, 0, 50 )

guid = "3d958539-6cb7-4bd3-94a7-0240069ad9fb"

content = note_store.getNoteContent( auth_token, guid )

print content


sys.exit()


# Listar todos notebooks:
notebooks = note_store.listNotebooks()
print "Achei ", len(notebooks), " notebooks:"
for notebook in notebooks:
    print "  * ", notebook.name

# Criar uma nova nota:
print "\nCriando uma nova nota no notebook principal\n"

note = Types.Note()
note.title = "Evernote API Workshop @ Campus Party! Python!"

# Anexando uma imagem:
image = open('enlogo.png', 'rb').read()

md5 = hashlib.md5()
md5.update(image)
hash = md5.digest()

data = Types.Data()
data.size = len(image)
data.bodyHash = hash
data.body = image

resource = Types.Resource()
resource.mime = 'image/png'
resource.data = data

# Adicionando o novo Resource na lista de resources dessa nota
note.resources = [resource]

# Para exibir a imagem no meio da nota, soh precisamos do hash MD5 dela
hash_hex = binascii.hexlify(hash)

# ENML = Evernote Markup Language. Eh um subset do HTML, com umas tags a mais 
note.content = '<?xml version="1.0" encoding="UTF-8"?>'
note.content += '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
note.content += '<en-note>'
note.content += 'Esta eh uma nova nota, inserida direto no notebook principal :)<br/>'
note.content += 'Olha aqui o logo do Evernote:<br/>'
note.content += '<en-media type="image/png" hash="' + hash_hex + '"/>'
note.content += '</en-note>'

# Finalmente, enviando a nota
created_note = note_store.createNote(note)

print "Nota criada com sucesso! O GUID dela eh: ", created_note.guid