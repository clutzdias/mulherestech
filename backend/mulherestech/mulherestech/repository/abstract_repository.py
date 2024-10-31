import psycopg2
from psycopg2 import sql
from typing import List

class AbstractRepository:
    
  def __init__(self):
    self.connection = None
    self.cursor = None
    #self.db_connection_params = db_connection_params
  
  def set_connection(self):
    try:
      if self.connection:
        self.connection.close()
        
      self.connection = psycopg2.connect(**self.db_connection_params)
      self.cursor = self.connection.cursor()
    except Exception as e:
      raise RuntimeError(f'Falha ao conectar-se ao banco de dados: {e}')
    
  def begin(self):
    try:
      if self.connection is None:
        raise RuntimeError('Conexão não inicializada.')
      self.connection.autocommit = False
    except Exception as e:
      raise RuntimeError(f'Falha ao iniciar transação: {e}')
    
  def commit(self):
    try:
      if self.connection is None:
        raise RuntimeError('Conexão não inicializada.')
      self.connection.commit()
      self.connection.autocommit = True
    except Exception as e:
      raise RuntimeError(f'Falha ao commitar transação: {e}') 

  def rollback(self):
    try:
      if self.connection is None:
        raise RuntimeError('Conexão não inicializada.')
      self.connection.rollback()
      self.connection.autocommit = True
    except Exception as e:
      raise RuntimeError(f'Falha ao dar rollback na transação: {e}') 

  def __execute(self, sql: str, params: dict):
    from sqlparams import SQLParams
    if not isinstance(params, dict):
      params = params.__dict__

    try:
      sql2, params2 = SQLParams('named', 'format').format(sql, params)
      if self.connection is None:
        self.set_connection()
      cursor = self.cursor
      cursor.execute(sql2,params2)
      self.commit()
    except Exception as e:
      self.rollback()
      raise
      ##Colocar log de exceção

    return cursor
  
  def __executeMany(self, sql: str, params: List[dict]):
    from sqlparams import SQLParams

    if len(params) == 0:
      raise Exception('Sem dados para inserir')
    
    params_execucao = []

    sql2 = ''

    for i in range(len(params)):
      parametro = params[i]

      if not isinstance(parametro, dict):
        parametro = parametro.__dict__
      
      sql2,params2 = SQLParams('named', 'format').format(sql, parametro)

      params_execucao.append(tuple(params2))
    try:
      if self.connection is None:
        self.set_connection()
      cursor = self.connection.cursor()
      cursor.executemany(sql2, params_execucao)
      self.commit()
    except Exception as e:
      #Adicionar log de erro
      self.rollback()
      pass

    return cursor

  def execute(self, sql: str, params: dict):
    try:
      cursor = None
      cursor = self.__execute(sql, params)
    finally:
      if cursor != None:
        cursor.close()

  def executeMany(self, sql: str, params: List[dict]):
    cursor = self.__executeMany(sql, params)
    if cursor != None:
      cursor.close()

  def fetchAll(self, sql: str, params: dict) -> List[dict]:
    try:
      cursor = None
      try:
        cursor = self.__execute(sql, params)
        return cursor.fetchall()
      except Exception as e:
        raise
    finally:
      if cursor != None:
        cursor.close()

  def fetchOne(self, sql: str, params: dict) -> dict:
    try:
      cursor = None
      try:
        cursor = self.__execute(sql, params)
        if cursor is not None:
          dados = cursor.fetchall()
          if len(dados) > 0:
            return dados[0]  
      except Exception as e:
        raise
    finally:
      if cursor != None:
        cursor.close()

if __name__ == '__main__':
  pass

    
      

    