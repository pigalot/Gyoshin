from Helpers import DMHelper
from discord_components import *

async def ListCommands(message, bot):
  # Grab the user ID before deleting the message that contains the command
  UserID = message.author.id
  
  # Generate message that lists all commands, split into 2 messages due to character limit
  await DMHelper.DMUserByID(bot, UserID, f"**All times provided to the but must be in UTC time for the bot to function properly:**\n**Commands:**\n**!addrun**, used to start a conversation with the bot that will guide you through the process to create a run\n**!adddefaulttemplates**, used to add some default templates for FFXIV\n**!addtemplate**, used to start a conversation with the bot that will guide you through the process to create a template\n**!commands**, lists all supported commands\n**!deletetemplate**, used to delete a template\n**!dismiss**, used to remove a member from the run example use: !dismiss 2 (this is the number you see after Run:) @UserName (you can just tag the user you want to dismiss, only the organizer of the run is allowed to dismiss members)\n**!myruns**, show upcoming runs you've signed up for up to a maximum of 5\n**!roles**, lists all available roles\n**!runs**, used to retrieve all runs planned on a specific date example use: !runs 01-08-2021\n**!templates**, lists all available templates\n**Buttons:**\n**Role (Tank/DPS/Healer) buttons**, if you're not part of a run clicking one of the role buttons will add you to that run on that role\nIf you're already part of the run and you click on the same role button as the role you've signed up with you'll be given the option to withdraw from the run\nIf you're already part of the run and you click on another role button then the role you've signed up with you'll be given the option to change your role for the run\n**Rally button**, you can use this button to tag all members that are signed up to this specific run (this can only be executed by players who are also signed up to this run up to a maximum amount of 3 times)\n**Reschedule button**, gives the organizer of the run the option to reschedule the run to another date\n**Cancel button**, gives the organizer of the run the option to cancel the run")
  return