from collections import defaultdict
from game_utils import *


def check_preconditions(preconditions, game, print_failure_reasons=True):
    """Checks whether the player has met all of the specified preconditions"""
    all_conditions_met = True
    failure_reasons = ''
    for check in preconditions:
        if check == "inventory_contains":
            item = preconditions[check]
            if not game.is_in_inventory(item):
                all_conditions_met = False
                if print_failure_reasons:
                    failure_reasons = "You don't have the %s" % item.name
        if check == "in_location":
            location = preconditions[check]
            if not game.curr_location == location:
                all_conditions_met = False
                if print_failure_reasons:
                    failure_reasons = "You aren't in the correct location"
        if check == "location_has_item":
            item = preconditions[check]
            if not item.name in game.curr_location.items:
                all_conditions_met = False
                if print_failure_reasons:
                    failure_reasons = "The %s isn't in this location" % item.name
        if check == "location_does_not_have_item":
            item = preconditions[check]
            if item.name in game.curr_location.items:
                all_conditions_met = False
                if print_failure_reasons:
                    failure_reasons = "The %s is in this location" % item.name
        if check == "princess_flag":
            princess = preconditions[check]
            if princess.flag == False:
                all_conditions_met = False
                if print_failure_reasons:
                    failure_reasons = "You did not give rose to princess"
        # todo - add other types of preconditions
    return all_conditions_met, failure_reasons


def add_item_to_inventory(game, *args):
    """ Add a newly created Item and add it to your inventory."""
    (item, action_description, already_done_description) = args[0]
    if(not game.is_in_inventory(item)):
        game.add_to_inventory(item)
        return action_description
    else:
        return already_done_description


def describe_something(game, *args):
    """Describe some aspect of the Item"""
    (description) = args[0]
    return description


def destroy_item(game, *args):
    """Removes an Item from the game by setting its location is set to None."""
    (item, action_description, already_done_description) = args[0]
    if game.is_in_inventory(item):
        game.inventory.pop(item.name)
        return action_description
    elif item.name in game.curr_location.items:
        game.curr_location.remove_item(item)
        return action_description
    else:
        return already_done_description


def end_game(game, *args):
    """Ends the game."""
    end_message = args[0]
    return end_message


def perform_multiple_actions(game, *args):
    result=""
    for f, action in args[0]:
        result+=f(game, action)+"\n"
    return result


def change_flag(game, *args):
    (princess) = args[0]
    princess.flag = True
    return ""


def check_conditions(game, *args):
    (a, b, condition) = args[0]
    if check_preconditions(condition, game)[0]:
        f, action = b
        return f(game, action)
    f, action = a
    return f(game, action)


def create_item(game, *args):
    (item, action_description) = args[0]
    game.curr_location.add_item(item.name, item)
    return action_description


class Game:
    """The Game class represents the world.  Internally, we use a
    graph of Location objects and Item objects, which can be at a
    Location or in the player's inventory.  Each locations has a set of
    exits which are the directions that a player can move to get to an
    adjacent location. The player can move from one location to another
    location by typing a command like "Go North".
    """

    def __init__(self, start_at):
        # start_at is the location in the game where the player starts
        self.curr_location = start_at
        self.curr_location.has_been_visited = True
        # inventory is the set of objects that the player has collected/
        self.inventory = {}
        # Print the special commands associated with items in the game (helpful
        # for debugging and for novice players).
        self.print_commands = True

    def describe(self):
        """Describe the current game state by first describing the current 
           location, then listing any exits, and then describing any objects
           in the current location."""
        out = self.describe_current_location() + '. ' + self.describe_exits() + '. ' + self.describe_items()
        return out
    
    def describe_current_location(self):
        """Describe the current location by printing its description field."""
        return self.curr_location.description
    
    def describe_exits(self):
        """List the directions that the player can take to exit from the current
           location."""
        exits = []
        for exit in self.curr_location.connections.keys():
            exits.append(exit.capitalize())
        if len(exits) > 0:
            return "Exits: " + ', '.join(exits)
        return ""
      
    def describe_items(self):
        """Describe what objects are in the current location."""
        if len(self.curr_location.items) > 0:
            out = "You see: "
            for item_name in self.curr_location.items:
                item = self.curr_location.items[item_name]
                out += item.description
                if self.print_commands:
                    special_commands = item.get_commands()
                    for cmd in special_commands:
                        out += ' with special comand ' + cmd
                out += ' and '
            
            return out[:-5]
        return ""
    
    def add_to_inventory(self, item):
        """Add an item to the player's inventory."""
        self.inventory[item.name] = item
      
    def is_in_inventory(self,item):
        return item.name in self.inventory

    def get_items_in_scope(self):
        """Returns a list of items in the current location and in the inventory"""
        items_in_scope = []
        for item_name in self.curr_location.items:
            items_in_scope.append(self.curr_location.items[item_name])
        for item_name in self.inventory:
            items_in_scope.append(self.inventory[item_name])
        return items_in_scope


class Location:
    """Locations are the places in the game that a player can visit.
    Internally they are represented nodes in a graph.  Each location stores
    a description of the location, any items in the location, its connections
    to adjacent locations, and any blocks that prevent movement to an adjacent
    location.  The connections is a dictionary whose keys are directions and
    whose values are the location that is the result of traveling in that
    direction.  The travel_descriptions also has directions as keys, and its
    values are an optional short desciption of traveling to that location.
    """

    def __init__(self, name, description, end_game=False):
        # A short name for the location
        self.name = name
        # A description of the location
        self.description = description
        # True if entering this location should end the game
        self.end_game = end_game
        # Dictionary mapping from directions to other Location objects
        self.connections = {}
        # Dictionary mapping from directions to text description of the path there
        self.travel_descriptions = {}
        # Dictionary mapping from item name to Item objects present in this location
        self.items = {}
        # Dictionary mapping from direction to Block object in that direction
        self.blocks = {}
        # Flag that gets set to True once this location has been visited by player
        self.has_been_visited = False

    def add_connection(self, direction, connected_location, travel_description=""):
        """Add a connection from the current location to a connected location.
        Direction is a string that the player can use to get to the connected
        location.  If the direction is a cardinal direction, then we also
        automatically make a connection in the reverse direction."""
        self.connections[direction] = connected_location
        self.travel_descriptions[direction] = travel_description
        if direction == "north":
            connected_location.connections["south"] = self
            connected_location.travel_descriptions["south"] = ""
        if direction == "south":
            connected_location.connections["north"] = self
            connected_location.travel_descriptions["north"] = ""
        if direction == "east":
            connected_location.connections["west"] = self
            connected_location.travel_descriptions["west"] = ""
        if direction == "west":
            connected_location.connections["east"] = self
            connected_location.travel_descriptions["east"] = ""
        if direction == "up":
            connected_location.connections["down"] = self
            connected_location.travel_descriptions["down"] = ""
        if direction == "down":
            connected_location.connections["up"] = self
            connected_location.travel_descriptions["up"] = ""
        if direction == "in":
            connected_location.connections["out"] = self
            connected_location.travel_descriptions["out"] = ""
        if direction == "out":
            connected_location.connections["in"] = self
            connected_location.travel_descriptions["in"] = ""

    def add_item(self, name, item):
        """Put an item in this location."""
        self.items[name] = item

    def remove_item(self, item):
        """Remove an item from this location (for instance, if the player picks it
        up and puts it in their inventory)."""
        self.items.pop(item.name)

    def is_blocked(self, direction, game):
        """Check to if there is an obstacle in this direction."""
        if not direction in self.blocks:
            return False
        (block_description, preconditions) = self.blocks[direction]
        if check_preconditions(preconditions, game)[0]:
            # All the preconditions have been met.  You may pass.
            return False
        else:
            # There are still obstalces to overcome or puzzles to solve.
            return True

    def get_block_description(self, direction):
        """Check to if there is an obstacle in this direction."""
        if not direction in self.blocks:
            return ""
        else:
            (block_description, preconditions) = self.blocks[direction]
            return block_description

    def add_block(self, blocked_direction, block_description, preconditions):
        """Create an obstacle that prevents a player from moving in the blocked
        location until the preconditions are all met."""
        self.blocks[blocked_direction] = (block_description, preconditions)


class Item:
    """Items are objects that a player can get, or scenery that a player can
    examine."""

    def __init__(
        self,
        name,
        description,
        examine_text="",
        take_text="",
        start_at=None,
        gettable=True,
        end_game=False,
    ):
        # The name of the object
        self.name = name
        # The default description of the object.
        self.description = description
        # The detailed description of the player examines the object.
        self.examine_text = examine_text
        # Text that displays when player takes an object.
        self.take_text = take_text if take_text else ("You take the %s." % self.name)
        # Indicates whether a player can get the object and put it in their inventory.
        self.gettable = gettable
        # True if entering this location should end the game.
        self.end_game = end_game
        # The location in the Game where the object starts.
        if start_at:
            start_at.add_item(name, self)
        self.commands = {}
        self.flag = False

    def get_commands(self):
        """Returns a list of special commands associated with this object"""
        return self.commands.keys()

    def add_action(self, command_text, function, arguments, preconditions={}):
        """Add a special action associated with this item"""
        self.commands[command_text] = (function, arguments, preconditions)

    def do_action(self, command_text, game):
        """Perform a special action associated with this item"""
        end_game = False  # Switches to True if this action ends the game.
        preconditions_met = False
        arguments = ''
        if command_text in self.commands:
            function, arguments, preconditions = self.commands[command_text]
            preconditions_met, failure_reasons = check_preconditions(preconditions, game, True)
        if preconditions_met:
            speak_output = function(game, arguments)
            return speak_output, end_game
        else:
            return "Cannot perform the action %s" % command_text, end_game
