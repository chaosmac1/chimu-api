# Module Imports
import mariadb
import sys

from os import environ

dbPool: mariadb.ConnectionPool = None

def InitializeMySQL():
   print('MySQL: Initializing...')

   pool = None

   try:
      pool = mariadb.ConnectionPool(
         user      = environ.get('MYSQL_USERNAME'),
         password  = environ.get('MYSQL_PASSWORD'),
         host      = environ.get('MYSQL_HOSTNAME'),
         database  = environ.get('MYSQL_DATABASE'),
         port      = 3306,
         pool_name = 'chimu-api-v1',
      )

      print('MySQL: Test for connection')

      pool.get_connection()
      
      print('MySQL: Success')

   except mariadb.OperationalError as e:
      print(f'MySQL: Error opening an connection: {e}')
      print('Exiting...')
      exit(1)
      
   except mariadb.PoolError as e:
      print(f'MySQL: Error opening connection from pool: {e}')
      exit(1)
   
   global dbPool
   dbPool = pool

def GetBeatmaps(beatmapSetId: int):
   conn = GetDatabasePool().get_connection()
   cursor = conn.cursor()

   beatmaps = []

   cursor.execute('SELECT * FROM Beatmaps WHERE ParentSetId = ?', (set_id,))


   for bm in cursor:
      beatmaps.append({
         'BeatmapId'        : bm[0],
         'ParentSetId'      : bm[1],
         'DiffName'         : bm[2],
         'FileMD5'          : bm[3],
         'Mode'             : bm[4],
         'BPM'              : bm[5],
         'AR'               : bm[6],
         'OD'               : bm[7],
         'CS'               : bm[8],
         'HP'               : bm[9],
         'TotalLength'      : bm[10],
         'HitLength'        : bm[11],
         'Playcount'        : bm[12],
         'Passcount'        : bm[13],
         'MaxCombo'         : bm[14],
         'DifficultyRating' : bm[15],
         'OsuFile'          : bm[16],
         'DownloadPath'     : f'/d/{bm[1]}'
   })

   return beatmaps

def GetDatabasePool():
   return dbPool
