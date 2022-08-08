#!/usr/bin/python
# -*- coding: utf-8 -*-
from game_classes import *


def build_game():

  # Locations

    cottage = Location('Cottage', 'You are standing in a small cottage.'
                       )
    garden_path = Location('Garden Path',
                           'You are standing on a lush garden path. There is a cottage here.'
                           )

  # cliff = Location("Cliff", "There is a steep cliff here. You fall off the cliff and lose the game. THE END.", end_game=True)

    fishing_pond = Location('Fishing Pond',
                            'You are at the edge of a small fishing pond.'
                            )
    winding_path = Location('Winding Path',
                            'You are walking along a winding path that leads south and east. There is a tall tree here.'
                            )
    top_of_the_tall_tree = Location('Top of the Tall Tree',
                                    'You are at the top of a tall tree. There is a stout deadbranch here. From your perch you can see the tower of Action Castle.'
                                    )
    drawbridge = Location('Drawbridge',
                          'You come to the drawbridge of Action Castle. There is a mean troll guarding the bridge.'
                          )
    courtyard = Location('Courtyard',
                         'You are in the courtyard of Action Castle. A castle guardstands watch to the east. Stairs lead up into the tower and down into darkness.'
                         )
    tower_stairs = Location('Tower Stairs',
                            'You climb the tower stairs until you come to a door.'
                            )
    tower = Location('Tower',
                     'You are in the tower. There is a princess here. Stairs lead down.'
                     )
    dungeon_stairs = Location('Dungeon Stairs',
                              'You are on the dungeon stairs. It\xe2\x80\x99s very dark here.'
                              )
    dungeon = Location('Dungeon',
                       'You are in the dungeon. There is a spooky ghost here. Stairs lead up.'
                       )
    great_feasting_hall = Location('Great Feasting Hall',
                                   'You stand inside the great feasting hall. There is a strange candle here. Exits are to the east and west.'
                                   )
    throne_room = Location('Throne Room',
                           'This is the throne room of Action Castle. There is an ornate gold throne here.'
                           )
    afterlife = Location('Afterlife', 'Your are dead. GAME OVER.',
                         end_game=True)

  # Connections

    cottage.add_connection('out', garden_path)

  # garden_path.add_connection("west", cliff)

    garden_path.add_connection('south', fishing_pond)
    garden_path.add_connection('north', winding_path)
    winding_path.add_connection('east', drawbridge)
    winding_path.add_connection('up', top_of_the_tall_tree)
    drawbridge.add_connection('east', courtyard)
    courtyard.add_connection('east', great_feasting_hall)
    courtyard.add_connection('up', tower_stairs)
    courtyard.add_connection('down', dungeon_stairs)
    tower_stairs.add_connection('in', tower)
    tower_stairs.add_connection('up', tower)
    dungeon_stairs.add_connection('down', dungeon)
    tower.add_connection('down', tower_stairs)
    dungeon.add_connection('up', dungeon_stairs)
    great_feasting_hall.add_connection('east', throne_room)
    top_of_the_tall_tree.add_connection('jump', afterlife,
            'You cannot survive the fall.')
    fishing_pond.add_connection('eat fish', afterlife,
                                "That's disgusting! It's raw! And definitely not sashimi-grade! But you've won this version of the game. THE END."
                                )

  # Items that you can pick up

    fishing_pole = Item('pole', 'a fishing pole',
                        'A SIMPLE FISHING POLE.', start_at=cottage)
    potion = Item('potion', 'a poisonous potion',
                  "IT'S BRIGHT GREEN AND STEAMING.",
                  take_text='As you near the potion, the fumes cause you to faint and lose the game. THE END.'
                  , end_game=True)
    rosebush = Item('rosebush', 'a rosebush',
                    'THE ROSEBUSH CONTAINS A SINGLE RED ROSE.  IT IS BEAUTIFUL.'
                    , start_at=garden_path)
    rose = Item('rose', 'a red rose', 'IT SMELLS GOOD.', start_at=None)
    fish = Item('fish', 'a dead fish', 'IT SMELLS TERRIBLE.')
    lamp = Item('lamp', 'an old lamp', 'IT IS CURRENTLY UNLIT.',
                start_at=cottage)
    lit_lamp = Item('lit lamp', 'an old lit lamp',
                    'IT IS CURRENTLY LIT.', start_at=None)
    branch = Item('branch', 'a dead branch',
                  'IT IS A DEAD BRANCH OF A TREE.',
                  start_at=top_of_the_tall_tree)
    key = Item('key', 'a hanged key', "IT HANGS FROM THE GUARD'S BELT."
               , start_at=None)
    candle = Item('candle', 'a strange candle',
                  'IT IS COVERED IN MYSTERIOUS RUNES.',
                  start_at=great_feasting_hall)
    lit_candle = Item('candle', 'a lit candle',
                      'IT GIVES OFF A STRANGE, ACRID SMOKE.')
    crown = Item('crown', 'a gold crown',
                 'YOU CAN PLACE IT ON YOUR HEAD.', start_at=None)
    crown_worn = Item('crown worn', 'a fantastic crown worn',
                      'You worn the crown, then you can go to the throne to be the winner'
                      , start_at=None)

  # Sceneary (not things that you can pick up)

    pond = Item('pond', 'a small fishing pond',
                'THERE ARE FISH IN THE POND.', start_at=fishing_pond,
                gettable=False)
    troll = Item('troll', 'a mean troll', 'THE TROLL BLOCKS YOUR PATH.'
                 , start_at=drawbridge, gettable=False)
    troll_in_eating = Item('troll eating fish', 'a troll eating fish',
                           'THE TROLL IS EATING. YOU CAN GO THIS WAY NOW.'
                           , gettable=False)
    guard = Item('guard', 'a castle guard',
                 'THE GUARD BLOCKS THE EASTERN EXIT.',
                 start_at=courtyard, gettable=False)
    unconscious_guard = Item('unconscious guard', 'an unconscious guard'
                             ,
                             'THE GUARD WAS HIT. NOW HE IS UNCONSCIOUS.'
                             )
    unconscious_troll = Item('unconscious troll', 'an unconscious troll'
                             ,
                             'THE TROLL WAS HIT. NOW HE IS UNCONSCIOUS.'
                             )
    princess = Item('princess', 'a beautiful, sad and lonely princess',
                    'NO KISSING OR TOUCHING, PLEASE.', start_at=tower,
                    gettable=False)
    ghost = Item('ghost', 'a scary ghost',
                 'IT HAS BONY, CLAW_LIKE FINGERS AND WEARS A GOLD CROWN.'
                 , start_at=dungeon, gettable=False)
    throne = Item('throne', 'a fantastic throne',
                  'ONLY WINNER CAN SIT THERE', start_at=throne_room,
                  gettable=False)
    tree = Item('top of the tree', 'a stout, dead branch',
                'YOU CAN GET THE DEAD BRANCH.',
                start_at=top_of_the_tall_tree, gettable=False)
    door = Item('door', 'an old door', 'YOU SHOULD UNLOCK IT.',
                start_at=tower_stairs, gettable=False)

  # Add special functions to your items

    rosebush.add_action('pick rose', add_item_to_inventory, (rose,
                        'You pick the lone rose from the rosebush.',
                        'You already picked the rose.'))
    rose.add_action('smell rose', describe_something, 'It smells sweet.'
                    )
    pond.add_action('catch fish', describe_something,
                    'You reach into the pond and try to catch a fish with your hands, but they are too fast.'
                    )
    pond.add_action('catch fish with pole', add_item_to_inventory,
                    (fish,
                    'You dip your hook into the pond and catch a fish.'
                    , "You weren't able to catch another fish."),
                    preconditions={'inventory_contains': fishing_pole})

    troll.add_action('give fish to troll', perform_multiple_actions,
                     [(destroy_item, (fish,
                     'You throw your fish to troll. The troll runs off to eat it.'
                     , 'You already tried that.')), (destroy_item,
                     (troll, 'The troll runs off.', '')), (create_item,
                     (troll_in_eating, 'The troll runs off to eat fish.'
                     ))], preconditions={'inventory_contains': fish,
                     'location_has_item': troll})

    guard.add_action('hit guard with branch', perform_multiple_actions,
                     [(destroy_item, (branch,
                     'You swing your branch against the guard. It shatters to pieces.'
                     , 'You already tried that.')), (destroy_item,
                     (guard, 'The guard slumps over, unconscious.', ''
                     )), (create_item, (unconscious_guard,
                     "The guard's unconscious body lies on the ground."
                     )), (create_item, (key,
                     'His key falls from his hand.'))],
                     preconditions={'inventory_contains': branch,
                     'location_has_item': guard})

    candle.add_action('light candle', perform_multiple_actions,
                      [(destroy_item, (candle, 'You lights your candle.'
                      , 'You already tried that.')),
                      (add_item_to_inventory, (lit_candle,
                      'light candle generated',
                      'You already tried that.'))],
                      preconditions={'inventory_contains': candle})

    lamp.add_action('light lamp', perform_multiple_actions,
                    [(destroy_item, (lamp, 'The lamp is lit now.',
                    'You already tried that.')),
                    (add_item_to_inventory, (lit_lamp,
                    'It is a lit lamp.', 'You already tried that.'))],
                    preconditions={'inventory_contains': lamp})

    throne.add_action('sit on throne', end_game,
                      'You sit on the throne. You are the winner.',
                      preconditions={'inventory_contains': crown_worn,
                      'location_has_item': throne})

    lit_candle.add_action('read runes', describe_something,
                          'The odd runes are part of an exorcism ritual used to dispel evil spirits.'
                          ,
                          preconditions={'inventory_contains': lit_candle})
    ghost.add_action('expel ghost', perform_multiple_actions,
                     [(destroy_item, (ghost,
                     'The strange candle gives off a strange, acrid smoke, causing the ghost to flee the dungeon.'
                     , 'You already tried that.')), (create_item,
                     (crown, 'The ghost leaves behind a gold crown'))],
                     preconditions={'inventory_contains': lit_candle,
                     'location_has_item': ghost})

    princess.add_action('give rose to princess',
                        perform_multiple_actions, [(destroy_item,
                        (rose, 'You gives the rose to princess.',
                        'You already tried that.')), (change_flag,
                        princess)],
                        preconditions={'inventory_contains': rose,
                        'location_has_item': princess})

    princess.add_action('talk to princess', describe_something,
                        'You can talk about the topic you are interested in with the princess.'
                        , preconditions={'location_has_item': princess,
                        'princess_flag': princess})
    princess.add_action('ask about ghost', describe_something,
                        'The guards whisper that the ghost of the king haunts the dungeons as a restless spirit!'
                        , preconditions={'location_has_item': princess,
                        'princess_flag': princess})
    princess.add_action('ask about crown', describe_something,
                        'My father\xe2\x80\x99s crown was lost after he died.'
                        , preconditions={'location_has_item': princess,
                        'princess_flag': princess})
    princess.add_action('ask about tower', describe_something,
                        'I cannot leave the tower until I\xe2\x80\x99m wed!'
                        , preconditions={'location_has_item': princess,
                        'princess_flag': princess})
    princess.add_action('ask about throne', describe_something,
                        'Only the rightful ruler of Action Castle may claim the throne!'
                        , preconditions={'location_has_item': princess,
                        'princess_flag': princess})
    princess.add_action('propose to princess', check_conditions,
                        [(describe_something,
                        'You\xe2\x80\x99re not royalty!'),
                        (perform_multiple_actions, [(destroy_item,
                        (crown, 'You will wear the crown.',
                        'You have already tried that.')), (create_item,
                        (crown_worn, 'You have worn the crown.')),
                        (add_item_to_inventory, (crown_worn,
                        'You have that now', 'You already had one.'
                        ))]), {'inventory_contains': crown,
                        'location_has_item': princess,
                        'princess_flag': princess}])
    door.add_action('unlock door', destroy_item, (door,
                    'The door is unlocked.', 'You already tried that.'
                    ), preconditions={'inventory_contains': key})

    drawbridge.add_block('east', 'The troll blocks your way',
                         preconditions={'location_does_not_have_item': troll})
    dungeon_stairs.add_block('down', "It's too dark to see.",
                             preconditions={'inventory_contains': lit_lamp})
    courtyard.add_block('east', 'The guard refuses to let you pass.',
                        preconditions={'location_does_not_have_item': guard})
    tower_stairs.add_block('up', 'The door is locked.',
                           preconditions={'location_does_not_have_item': door})

    return Game(cottage)
