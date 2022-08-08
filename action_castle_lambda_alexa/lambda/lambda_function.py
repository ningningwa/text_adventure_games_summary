#!/usr/bin/python
# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.

import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

from utils import *
from game_utils import *
from constants import *
from game_classes import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

game_state = None
END = False


class DirectionRequestHandler(AbstractRequestHandler):

    """Handler for Intent Direction."""

    def can_handle(self, handler_input):

        # type: (HandlerInput) -> bool

        if ask_utils.get_intent_name(handler_input) in [
            'north',
            'south',
            'east',
            'west',
            'up',
            'down',
            'in',
            'out',
            ]:
            return True
        else:
            return False

    def handle(self, handler_input):
        """ The user wants to go in some direction """

        # type: (HandlerInput) -> Response

        global game_state
        global END
        direction = ask_utils.get_intent_name(handler_input)
        speak_output = ''
        if direction in game_state.curr_location.connections:
            if game_state.curr_location.is_blocked(direction,
                    game_state):

                # check to see whether that direction is blocked.

                speak_output = \
                    game_state.curr_location.get_block_description(direction)
            else:

                # if it's not blocked, then move there

                game_state.curr_location = \
                    game_state.curr_location.connections[direction]

                # If moving to this location ends the game_state, only describe the location
                # and not the available items or actions.

                if game_state.curr_location.end_game:
                    speak_output = \
                        game_state.describe_current_location()
                else:
                    speak_output = game_state.describe()
        else:
            speak_output = "You can't go %s from here." \
                % direction.capitalize()

        END = game_state.curr_location.end_game
        print(END)
        print(game_state.curr_location.connections.keys())

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response

class EndRequestHandler(AbstractRequestHandler):

    """Handler for Intent Direction."""

    def can_handle(self, handler_input):

        # type: (HandlerInput) -> bool

        if ask_utils.get_intent_name(handler_input) in [
            'jump',
            'eatfish',
            'sitonthrone'
            ]:
            return True
        else:
            return False

    def handle(self, handler_input):
        """ The user wants to go in some direction """

        global game_state
        global END
        speak_output = ""
        if ask_utils.get_intent_name(handler_input)=="jump" and game_state.curr_location.name == "Top of the Tall Tree":
            END = True
            speak_output = "You cannot survive the fall. You are dead."
        if ask_utils.get_intent_name(handler_input)=="eatfish" and "fish" in game_state.inventory:
            END = True
            speak_output = "That's disgusting! It's raw! And definitely not sashimi-grade! But you've won this version of the game. THE END."
        if ask_utils.get_intent_name(handler_input)=="sitonthrone" and "crown worn" in game_state.inventory:
            END = True
            speak_output = "You win."
            
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response

class InventoryRequestHandler(AbstractRequestHandler):

    """Handler for Intent Inventory."""

    def can_handle(self, handler_input):

        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name('inventory')(handler_input)

    def handle(self, handler_input):
        """ The user wants to go in some direction """

        # type: (HandlerInput) -> Response

        global game_state
        global END
        speak_output = ''
        if len(game_state.inventory) == 0:
            speak_output = "You don't have anything."
        else:
            descriptions = []
            for item_name in game_state.inventory:
                item = game_state.inventory[item_name]
                descriptions.append(item.description)
            speak_output = 'You have: '
            speak_output += ', '.join(descriptions)

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class ExamineRequestHandler(AbstractRequestHandler):

    """Handler for Intent Inventory."""

    def can_handle(self, handler_input):

        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name('examine')(handler_input)

    def handle(self, handler_input):
        """ The user wants to go in some direction """

        # type: (HandlerInput) -> Response

        global game_state
        global END
        speak_output = ''
        command = ask_utils.request_util.get_slot_value(handler_input, 'item')
        matched_item = False

        # check whether any of the items at this location match the command

        for item_name in game_state.curr_location.items:
            if item_name == command:
                item = game_state.curr_location.items[item_name]
                if item.examine_text:
                    speak_output += item.examine_text + '\n'
                    matched_item = True
                break

        # check whether any of the items in the inventory match the command

        for item_name in game_state.inventory:
            if item_name == command:
                item = game_state.inventory[item_name]
                if item.examine_text:
                    speak_output += item.examine_text + '\n'
                    matched_item = True

        # fail

        if not matched_item:
            speak_output += "You don't see anything special.\n"

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class TakeRequestHandler(AbstractRequestHandler):

    """Handler for Intent Inventory."""

    def can_handle(self, handler_input):

        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name('take')(handler_input)

    def handle(self, handler_input):
        """ The user wants to go in some direction """

        # type: (HandlerInput) -> Response

        global game_state
        global END
        speak_output = ''
        command = ask_utils.request_util.get_slot_value(handler_input, 'item')
        print(command)
        matched_item = False
        for item_name in game_state.curr_location.items:
            if item_name == command:
                item = game_state.curr_location.items[item_name]
                if item.gettable:
                    game_state.add_to_inventory(item)
                    game_state.curr_location.remove_item(item)
                    speak_output += item.take_text + '\n'
                    END = item.end_game
                else:
                    speak_output += 'You cannot take the %s.' \
                        % item_name + '\n'
                matched_item = True
                break

        # check whether any of the items in the inventory match the command

        if not matched_item:
            for item_name in game_state.inventory:
                if item_name == command:
                    speak_output += 'You already have the %s.' \
                        % item_name + '\n'
                    matched_item = True

        # fail

        if not matched_item:
            speak_output += "You can't find it." + '\n'

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class DropRequestHandler(AbstractRequestHandler):

    """Handler for Intent Inventory."""

    def can_handle(self, handler_input):

        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name('drop')(handler_input)

    def handle(self, handler_input):
        """ The user wants to go in some direction """

        # type: (HandlerInput) -> Response

        global game_state
        global END
        speak_output = ''
        command = ask_utils.request_util.get_slot_value(handler_input, 'item')
        matched_item = False

        # check whether any of the items in the inventory match the command

        if not matched_item:
            for item_name in game_state.inventory:
                if item_name == command:
                    matched_item = True
                    item = game_state.inventory[item_name]
                    game_state.curr_location.add_item(item_name, item)
                    game_state.inventory.pop(item_name)
                    speak_output += 'You drop the %s.' % item_name \
                        + '\n'
                    break

        # fail

        if not matched_item:
            speak_output += "You don't have that.\n"

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class RedescribeRequestHandler(AbstractRequestHandler):

    """Handler for Intent Inventory."""

    def can_handle(self, handler_input):

        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name('redescribe')(handler_input)

    def handle(self, handler_input):
        """ The user wants to go in some direction """

        # type: (HandlerInput) -> Response

        global game_state
        speak_output = game_state.describe()

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class SpecialRequestHandler(AbstractRequestHandler):

    """Handler for Intent Inventory."""

    def can_handle(self, handler_input):

        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name('special')(handler_input)

    def handle(self, handler_input):
        """ The user wants to go in some direction """

        # type: (HandlerInput) -> Response

        global game_state
        global END
        speak_output = ''
        command = ask_utils.request_util.get_slot_value(handler_input,
                'specialCommand')

        for item in game_state.get_items_in_scope():
            special_commands = item.get_commands()
            for special_command in special_commands:
                if command == special_command.lower():
                    speak_output += item.do_action(special_command,
                            game_state)[0]
                    END = game_state.curr_location.end_game
                    return handler_input.response_builder.speak(speak_output).ask(speak_output).response
        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class LaunchRequestHandler(AbstractRequestHandler):

    """Handler for Skill Launch."""

    def can_handle(self, handler_input):

        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type('LaunchRequest')(handler_input)

    def handle(self, handler_input):

        # type: (HandlerInput) -> Response

        global game_state
        global END
        game_state = build_game()
        END = False
        speak_output = 'Welcome, to action castle! ' \
            + game_state.describe()

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class HelpIntentHandler(AbstractRequestHandler):

    """Handler for Help Intent."""

    def can_handle(self, handler_input):

        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name('AMAZON.HelpIntent'
                )(handler_input)

    def handle(self, handler_input):

        # type: (HandlerInput) -> Response

        speak_output = 'Add help instructions. '

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


class CancelOrStopIntentHandler(AbstractRequestHandler):

    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):

        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name('AMAZON.CancelIntent'
                )(handler_input) \
            or ask_utils.is_intent_name('AMAZON.StopIntent'
                )(handler_input)

    def handle(self, handler_input):

        # type: (HandlerInput) -> Response

        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
                True)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):

    """Single handler for Fallback Intent."""

    def can_handle(self, handler_input):

        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name('AMAZON.FallbackIntent'
                )(handler_input)

    def handle(self, handler_input):

        # type: (HandlerInput) -> Response

        logger.info('In FallbackIntentHandler')
        speech = game_state.describe()

        return handler_input.response_builder.speak(speech).response


class SessionEndedRequestHandler(AbstractRequestHandler):

    """Handler for Session End."""

    def can_handle(self, handler_input):

        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type('SessionEndedRequest'
                )(handler_input) or END == True

    def handle(self, handler_input):

        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.
        
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
                True)
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):

    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):

        # type: (HandlerInput, Exception) -> bool

        return True

    def handle(self, handler_input, exception):

        # type: (HandlerInput, Exception) -> Response

        logger.error(exception, exc_info=True)

        speak_output = \
            'Sorry, I had trouble doing what you asked. Please try again.'

        return handler_input.response_builder.speak(speak_output).ask(speak_output).response


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(DirectionRequestHandler())
sb.add_request_handler(EndRequestHandler())
sb.add_request_handler(InventoryRequestHandler())
sb.add_request_handler(ExamineRequestHandler())
sb.add_request_handler(TakeRequestHandler())
sb.add_request_handler(DropRequestHandler())
sb.add_request_handler(RedescribeRequestHandler())
sb.add_request_handler(SpecialRequestHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
