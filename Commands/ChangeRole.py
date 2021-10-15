import re
import sqlite3
from Helpers import RoleHelper
from Helpers import DateTimeFormatHelper
from Helpers import OriginHelper
from Helpers import UserHelper
from Helpers import DMHelper
from Helpers import RaidIDHelper
from Helpers import MessageHelper

async def ChangeRole(message, bot, RoleName, UserID):
  try:
    RaidID = await RaidIDHelper.GetRaidIDFromMessage(message)
  except:
    await DMHelper.DMUserByID(bot, UserID, "Something went wrong obtaining run information")
    return

  # Get discord server ID
  Origin = await OriginHelper.GetOrigin(message)

  conn = sqlite3.connect('RaidPlanner.db')
  c = conn.cursor()

  # Check if the run exists and if the user is a member
  try:
    c.execute("SELECT RM.RoleID, RM.ID, R.ID, R.Name, R.Date FROM RaidMembers RM JOIN Raids R ON R.ID = RM.RaidID WHERE RM.Origin = (?) AND R.ID = (?) AND RM.UserID = (?)", (Origin, RaidID, UserID,))
    row = c.fetchone()

    OldRoleID = row[0]
    RaidMemberID = row[1]
    RaidID = row[2]
    RaidName = row[3]
    Date = row[4]
    LocalDate = await DateTimeFormatHelper.SqliteToLocalNoCheck(Date)
    OldRoleName = await RoleHelper.GetRoleName(OldRoleID)
    NewRoleID = await RoleHelper.GetRoleID(RoleName)
    DisplayName = await UserHelper.GetDisplayName(message, UserID, bot)
  except:
    await DMHelper.DMUserByID(bot, UserID, f"Run {RaidID} or role {RoleName} not found")
    conn.close()
    return

  if OldRoleID != NewRoleID:
    try:
      # Create an empty message variable first
      UpdatedMessage = None

      # Set column name to update for old role
      if OldRoleName == 'tank':
        OldRoleSignedUpColumn = 'NrOfTanksSignedUp'
      elif OldRoleName == 'dps':
        OldRoleSignedUpColumn = 'NrOfDpsSignedUp'
      elif OldRoleName == 'healer':
        OldRoleSignedUpColumn = 'NrOfHealersSignedUp'

      # Set column name to update for new role
      if RoleName == 'tank':
        NewRoleSignedUpColumn = 'NrOfTanksSignedUp'
      elif RoleName == 'dps':
        NewRoleSignedUpColumn = 'NrOfDpsSignedUp'
      elif RoleName == 'healer':
        NewRoleSignedUpColumn = 'NrOfHealersSignedUp'

      # Change role
      try:
        c.execute(f"UPDATE Raids set {OldRoleSignedUpColumn} = {OldRoleSignedUpColumn} - 1, {NewRoleSignedUpColumn} = {NewRoleSignedUpColumn} + 1 WHERE ID = (?) AND Origin = (?)", (RaidID, Origin,))
        c.execute("UPDATE RaidMembers set RoleID = (?) WHERE ID = (?) AND Origin = (?)", (NewRoleID, RaidMemberID, Origin,))
        await message.channel.send(f"{DisplayName} has changed role from {OldRoleName} to {RoleName} for {RaidName} on {LocalDate}")
        conn.commit()
        UpdatedMessage = await MessageHelper.UpdateRaidInfoMessage(message, bot, UserID, Origin)
      except:
        await DMHelper.DMUserByID(bot, UserID, "Something went wrong changing your role")
        conn.close()
        return

      try:
        if UpdatedMessage:
          await message.edit(content=UpdatedMessage)
          conn.close()
          return
        if not UpdatedMessage:
          await DMHelper.DMUserByID(bot, UserID, "Something went wrong changing your role, please make sure you're changing to a role that still has free slots")
          conn.close()
          return
      except:
        await DMHelper.DMUserByID(bot, UserID, "Something went wrong changing your role")
        conn.close()
        return

    except:
      await DMHelper.DMUserByID(bot, UserID, "Something went wrong changing your role")
      conn.close()
      return
  else:
    await DMHelper.DMUserByID(bot, UserID, "You cannot change to the same role you already signed up as")
    conn.close()
    return
  return
