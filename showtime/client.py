import grpc
import showtime_pb2_grpc
import showtime_pb2
from google.protobuf import empty_pb2 as googleEmpty


def get_home(stub):
    print(stub.Home(googleEmpty.Empty()))

# Renvoie tous les schedules 
def get_all_schedules(stub):
    schedules = stub.GetAllSchedules(googleEmpty.Empty())
    for schedule in schedules:
        print("Date : " + schedule.date + "\n Movies : ")
        for movie in schedule.movies:
            print(movie)
    print("\n")

# Renvoie un schedule en fonction de la date
def get_schedule(stub, date):
    schedule = stub.GetSchedule(date)
    print("Date : " + schedule.date + "\n Movies : ")
    for movie in schedule.movies:
        print(movie)
 

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3202') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)


        print("-------------- Home --------------")
        get_home(stub)
        print("-------------- GetAllSchedule --------------")
        get_all_schedules(stub)
        print("-------------- GetSchedule --------------")
        date = showtime_pb2.Date(date="20151203")
        get_schedule(stub, date)

    channel.close()

if __name__ == '__main__':
    run()
