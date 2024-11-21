import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json
from grpc_reflection.v1alpha import reflection

class ShowtimeServicer(showtime_pb2_grpc.ShowtimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def write(self, showtime):
        with open('{}/data/times.json'.format("."), 'w') as f:
            json.dump(showtime, f)

    def Home(self, request, context):
        print("Home")
        return showtime_pb2.ShowtimeHomeResponse(message="Bienvenue sur showtime")

    def GetAllSchedules(self, request, context):
        print("GetAllSchedules")
        if len(self.db) <= 0:
            return showtime_pb2.Schedule(date="", movies="")
        for schedule in self.db:
            yield showtime_pb2.Schedule(date=schedule["date"], movies=schedule["movies"])

    def GetSchedule(self, request, context):
        print("GetSchedule")
        if len(self.db) <= 0:
            return showtime_pb2.Schedule(date="", movies="")
        for schedule in self.db:
            if schedule["date"] == request.date:
                return showtime_pb2.Schedule(date=schedule["date"], movies=schedule["movies"])
        return showtime_pb2.Schedule(date="", movies="")

    def AddSchedule(self, request, context):
        # Vérifier si la date existe déjà
        for schedule in self.db:
            if schedule["date"] == request.date:
                # Ajouter les nouveaux films à la date existante
                for movie in request.movies:
                    schedule["movies"].append(movie)
                return showtime_pb2.Schedule(date=schedule["date"], movies=schedule["movies"])

        # Créer un nouvel horaire si la date n'existe pas
        new_schedule = {
            "date": request.date,
            "movies": list(request.movies)
        }

        self.db.append(new_schedule)
        self.write(self.db)
        return showtime_pb2.Schedule(date=new_schedule["date"], movies=new_schedule["movies"])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimeServicer_to_server(ShowtimeServicer(), server)

    SERVICE_NAMES = (
        showtime_pb2.DESCRIPTOR.services_by_name['Showtime'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port('[::]:3202')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()