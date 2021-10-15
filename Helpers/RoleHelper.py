import sqlite3

async def GetRoleName(RoleID):
  # Open connection to DB
  conn = sqlite3.connect('RaidPlanner.db')
  c = conn.cursor()

  try:
    c.execute("SELECT Name FROM Roles WHERE ID = (?)", (RoleID,))
    RoleName = c.fetchone()[0]
  except ValueError:
    conn.close()
  return RoleName

async def GetRoleID(RoleName):
  # Open connection to DB
  conn = sqlite3.connect('RaidPlanner.db')
  c = conn.cursor()

  try:
    c.execute("SELECT ID FROM Roles WHERE Name = (?)", (RoleName,))
    RoleID = c.fetchone()[0]
  except ValueError:
    conn.close()
  return RoleID
