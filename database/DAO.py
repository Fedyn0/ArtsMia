from database.DB_connect import DBConnect
from model.arco import Arco
from model.artObject import ArtObject


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        res = []

        cursor = conn.cursor(dictionary=True)

        query = """ select *
                    from objects"""
        cursor.execute(query)

        for row in cursor:
            res.append(ArtObject(**row))
        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getEdgePeso(v1, v2):
        conn = DBConnect.get_connection()

        res = []

        cursor = conn.cursor(dictionary=True)

        query = """select eo.object_id as o1, eo2.object_id as o2, count(*) as peso 
                from exhibition_objects eo , exhibition_objects eo2 
                where eo.exhibition_id = eo2.exhibition_id 
                and eo.object_id < eo2.object_id 
                and eo.object_id = %s and eo2.object_id = %s"""
        cursor.execute(query, (v1.object_id, v2.object_id))

        for row in cursor:
            res.append(row["peso"])


        cursor.close()
        conn.close()

        if len(res) == 0:
            return None

        return res

    @staticmethod
    def getAllEdges(idMapAO):
        conn = DBConnect.get_connection()

        res = []

        cursor = conn.cursor(dictionary=True)

        query = """select eo.object_id as o1, eo2.object_id as o2, count(*) as peso 
                from exhibition_objects eo , exhibition_objects eo2 
                where eo.exhibition_id = eo2.exhibition_id 
                and eo.object_id < eo2.object_id 
                group by eo.object_id, eo2.object_id
                order by peso desc"""

        cursor.execute(query)

        for row in cursor:
            res.append(Arco(idMapAO[row["o1"]], idMapAO[row["o2"]], row["peso"]))


        cursor.close()
        conn.close()

        if len(res) == 0:
            return None

        return res
