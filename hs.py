#!/usr/bin/python
# encoding: utf-8

import sys, json

from workflow import Workflow, ICON_WEB, web

sets = {
    'Basic': 'classic.png',
    'Blackrock Mountain': 'brm.png',  
    'Classic': 'classic.png',
    'Mean Streets of Gadgetzan': 'gadgetzan.png',
    'Goblins vs Gnomes': 'gvg.png',
    'Hall of Fame': 'hof.png',
    'Kobolds and Catacombs': 'kac.png',
    'One Night in Karazhan': 'kara.png',
    'Knights of the Frozen Throne': 'kotft.png',
    'The League of Explorers': 'loe.png',
    'Naxxramas': 'naxx.png',
    'The Grand Tournament': 'tgt.png',
    'Journey to Un\'Goro': 'ungoro.png',
    'Whispers of the Old Gods': 'wotog.png'
}

def singleResult(data):
    lineIcon = './icon.png'
    if(data['rarity'] != 'Free'):
        lineIcon = './icons/' + data['rarity'].lower() + '.png'
    
    wf.add_item(data['name'], data['flavor'], arg=str(data['imgGold']), quicklookurl=str(data['imgGold']), valid=True, icon=lineIcon)
    if('text' in data):
        wf.add_item(data['text'], icon='./icon.png')
    
    if('cost' in data):
            wf.add_item(str(data['cost']), icon='./icons/mana.png')
    if(data['type'] == 'Minion'):
        wf.add_item(str(data['attack']), icon='./icons/attack.png')
        wf.add_item(str(data['health']), icon='./icons/health.png')
    elif(data['type'] == 'Weapon'):
        wf.add_item(str(data['attack']), icon='./icons/attack.png')
        wf.add_item(str(data['durability']), icon='./icons/durability.png')
    elif(data['type'] == 'Hero'):
        wf.add_item(str(data['armor']), icon='./icons/durability.png')
    wf.add_item(data['playerClass'], icon='./icons/' + data['playerClass'].lower() + '.png')

    if('classes' in data and 'multiClassGroup' in data):
        gang = data['multiClassGroup'] + ': '
        for classSet in data['classes']:
            gang += classSet + '  '
        wf.add_item(gang, icon='./icons/' + data['multiClassGroup'].lower().replace(' ', '') + '.png')

    typeTribeSet = 'Type: ' + data['type']
    if('race' in data):
        typeTribeSet = typeTribeSet + ' | Subtype: ' + data['race']

    typeTribeSet = typeTribeSet + ' | Set: ' + data['cardSet']

    wf.add_item(typeTribeSet, icon='./icons/sets/white/' + sets[data['cardSet']])

def key_for_search(card):
    return '{}'.format(card['name'])

def main(wf):
    args = wf.args

    if len(args):
        query = args[0]
    else:
        query = ''

    with open('./cards.json') as data:
        data = json.load(data)

    if not data:
        wf.add_item(u'No results found. Did you setup the Workflow?', u'Think something should be here that isn\'t? Hit Enter to open an issue on Github', arg='https://github.com/gabrielrios/alfred2-hearthstone/issues/new', valid=True, icon='./icon.png')        
    else:
        searched_cards = wf.filter(query, data, key_for_search, max_results=9)

        #If there's only one result, display is as expected
        if(len(searched_cards) == 1):
            singleResult(searched_cards[0])

        else:
            for card in searched_cards:
                # There are a few cases where two cards have names that overlap, for example Alexstrasza. This puts the extra cards at the bottom of the list. 
                if card['name'] == query:
                    tempItems = wf._items
                    wf._items = []
                    singleResult(card)
                    wf._items += tempItems
                else:
                    stats = ''
                    # Leave out Heroes that aren't from Knights of the Frozen Throne
                    if(card['type'] == 'Hero' and card['rarity'] != 'Legendary'):
                        continue
                    if(card['type'] == 'Minion'):
                        stats = str(card['attack']) + '/' + str(card['health'])
                    if(card['type'] == 'Weapon'):
                        stats = str(card['attack']) + '/' + str(card['durability'])
                    title = card['name'] + ' (' + str(card['cost']) + ') ' + stats
                    text = ''
                    if('text' in card):
                        text = card['text']
                    wf.add_item(title, text, valid=False, icon='./icon.png', uid=card['cardId'], autocomplete=card['name'])
    
    wf.send_feedback()
    


if __name__ == '__main__':
    # Create a global `Workflow` object
    wf = Workflow()
    # Call your entry function via `Workflow.run()` to enable its helper
    # functions, like exception catching, ARGV normalization, magic
    # arguments etc.
    sys.exit(wf.run(main))