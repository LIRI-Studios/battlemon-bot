import pokebase as pb

def write(dir: str, text: str):
    f = open(dir, "w")
    f.write(text)
    f.close()

def format(text: str):
    text = 'NULL' if text is None else text
    return str('{};'.format(text)).replace('\n', ' ')

def moves():
    keys = ['attack', 'defense', 'special-attack', 'special-defense', 'speed', 'accuracy', 'evasion']
    text = '\"{}\"\n'.format('\";\"'.join(['description', 'name', 'category', 'accuracy', 'power', 'pp', 'type', 'id']))
    text2 = '\"{}\"\n'.format('\";\"'.join(['category', 'crit_rate', 'drain', 'flinch_chance', 'healing', 'stat_chance', 'min_hits', 'max_hits', 'min_turns', 'max_turns', 'st_0', 'st_1', 'st_2', 'st_3', 'st_4', 'st_5', 'st_6', 'id']))
    for i in range(1, 729):
        print('Fetching {}% --- {}/728'.format(round(100*i/728, 2), i))
        aux = pb.move(i)
        for item in aux.flavor_text_entries:
            if item.language.name == 'en' and item.version_group.name == 'ultra-sun-ultra-moon':
                text += format(str(item.flavor_text))
                break
        text += format(aux.name)
        text += format(aux.damage_class.name)
        text += format(aux.accuracy)
        text += format(aux.power)
        text += format(aux.pp)
        text += format(aux.type.name)
        text += '{}\n'.format(i)

        text2 += format(aux.meta.category.name)
        text2 += format(aux.meta.crit_rate)
        text2 += format(aux.meta.drain)
        text2 += format(aux.meta.flinch_chance)
        text2 += format(aux.meta.healing)
        text2 += format(aux.meta.stat_chance)
        text2 += format(aux.meta.min_hits)
        text2 += format(aux.meta.max_hits)
        text2 += format(aux.meta.min_turns)
        text2 += format(aux.meta.max_turns)

        stats = len(keys) * ['0']

        if len(aux.stat_changes) != 0:
            for item in aux.stat_changes:
                for idx in range(len(keys)):
                    if item.stat.name == keys[idx]:
                        stats[idx] = item.change
        text2 += str(stats)[1:-1].replace(', ', ';')
        text2 += ';{}\n'.format(i)

    write('move.csv', text)
    write('meta.csv', text2)

def cat_pokemon(text: str):
    forms = [
        'pikachu-', 'wormadam-', 'lycanroc-',
        'shaymin-', 'deoxys-', 'giratina-',
        'rotom-','-alola', 'castform-',
        'basculin-','darmanitan-','meloetta-',
        'tornadus-','thundurus-','landorus-',
        'kyurem-', 'meowstic-','aegislash-',
        'pumpkaboo-','gourgeist-','hoopa-',
        'nidoran-'
    ]
    if '-primal' in text:
        return 'MEGA'
    if '-mega' in text:
        return 'MEGA'
    legendaries = [
        'articuno','zapdos','moltres','mewtwo',
        'raikou','entei','suicune','lugia',
        'ho-oh','regirock','regice','registeel',
        'latias','latios','kyogre','groudon',
        'rayquaza','uxie','mesprit','azelf',
        'dialga','palkia','heatran','regigigas',
        'giratina','cresselia','cobalion','terrakion',
        'virizion','tornadus','thundurus','reshiram',
        'zekrom','landorus','kyurem','xerneas',
        'yveltal','zygarde','type-null','silvally',
        'tapu-', 'cosmog', 'cosmoem', 'solgaleo',
        'lunala', 'necrozma', 'zacian', 'zamazenta',
        'eternatus']
    mythicals = [
        'mew', 'celebi', 'jirachi', 'deoxys-normal',
        'phione', 'manaphy', 'darkrai', 'shaymin',
        'arceus', 'victini', 'keldeo', 'meloetta',
        'genesect', 'diancie', 'hoopa', 'volcanion',
        'magearna', 'marshadow', 'zeraora', 'meltan',
        'melmetal']
    ultrabeasts = [
        'nihilego', 'buzzwole','pheromosa','celesteela',
        'kartana','guzzlord','poipole','naganadel',
        'stakataka','blacephalon']
    for item in legendaries:
        if item in text:
            return 'LEGENDARY'
    for item in mythicals:
        if item in text:
            return 'MYTHICAL'
    for item in ultrabeasts:
        if item in text:
            return 'ULTRABEAST'
    for item in forms:
        if item in text:
            return 'FORM'
    return 'NORMAL'

def abilities():
    range_vals = range(1, 234)  # + range(10001, 10061)
    text = '\"{}\"\n'.format('\";\"'.join(
        ['description', 'name', 'special', 'id']
    ))
    text2 = '\"{}\"\n'.format('\";\"'.join(
        ['ability', 'pokemon', 'hidden', 'id']
    ))
    idx = 1
    for i in range_vals:
        print(round(100*i/len(range_vals), 2))
        aux = pb.ability(i)
        for item in aux.flavor_text_entries:
            if item.language.name == 'en' and item.version_group.name == 'ultra-sun-ultra-moon':
                text += format(str(item.flavor_text))
                break
        text += format(str(aux.name))
        text += format('FALSE')
        text += '{}\n'.format(i)
        for item in aux.pokemon:
            aux2 = pb.pokemon(str(item.pokemon.name))
            text2 += format(str(i))
            text2 += format(aux2.id)
            text2 += format(str('TRUE' if item.is_hidden else 'FALSE'))
            text2 += '{}\n'.format(idx)
            idx += 1

    write('abilities.csv', text)
    write('base_abilities.csv', text2)

def pokemon():
    init = [1, 10001]# a b
    end  = [808, 10158] # c d 
    # d - b + c - a
    text = "\"{}\"\n".format('\";\"'.join(['name', 'type1', 'type2' ,'height','weight','category','hp','atk','def','sp_atk','sp_def','speed','id']))
    text2 = "\"{}\"\n".format('\";\"'.join(['pokemon','move','method','id']))
    idx = 1
    mod = True
    val = end[0] - init[0] + end[1] - init[1]
    for j in range(2):
        for i in range(init[j], end[j]):
            print('Fetching {}% --- {}/{}'.format(round(100 *i/val, 2), i, val))
            types = ['NULL', 'NULL']
            aux = pb.pokemon(i)
            for item in aux.types:
                types[item.slot-1] = item.type.name
            non_fetch = ['-totem', '-busted', 'rockruff-own-tempo']
            for item in non_fetch:
                mod = False if item in str(aux.name) else mod
            aux.name = 'mimkyu' if 'mimikyu-disguised' in aux.name else aux.name
            text += format(aux.name)
            for item in types:
                text += format(item)
            text += format(str(aux.height))
            text += format(str(aux.weight))
            text += format(cat_pokemon(aux.name))
            for item in aux.stats:
                text += format(item.base_stat)
            text += '{}\n'.format(i)
            for value in aux.moves:
                aux2 = pb.move(str(value.move.name))
                temp = [str(i), str(aux2.id)]
                values = set()
                for item_1 in value.version_group_details:
                    values.add(str(item_1.get('move_learn_method').get('name')))
                for item_1 in values:        
                    text2 += ';'.join(temp)
                    text2 += ';{};{}\n'.format(item_1, idx)
                    idx += 1
    write('pokemon2.csv', text)
    write('learnset2.csv', text2)

# pokemon()